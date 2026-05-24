---
domain: medium.com
fetch_date: '2026-05-18T12:54:41.004260'
status: ok
url: https://medium.com/data-science-collective/online-softmax-to-flash-attention-and-why-it-matters-9d676e7c50a8
---

# Online Softmax to Flash Attention — and Why it Matters

## Connecting the Key Optimizations from Online Softmax to Flash Attention

[ ![Matthew Gunton](https://miro.medium.com/v2/resize:fill:64:64/1*F8sHS2ai6w95qbGIZ9qM_g.png) ](</@mgunton7?source=post_page---byline--9d676e7c50a8--------------------------------------->)

[Matthew Gunton](</@mgunton7?source=post_page---byline--9d676e7c50a8--------------------------------------->)

9 min read

·

May 26, 2025

\--

Listen

Share

More

Press enter or click to view image in full size

Image by Author — Flux.1 Schnell

In 2017, “Attention is All You Need” was published, showing to the world that Transformer models could achieve great performance relying on the Attention layer. Eight years later, we’ve seen these models conquer the Turing Test and more using the power of Attention. While powerful, Attention comes at a cost. As the input gets longer, you need quadratically more memory to calculate Attention. This memory increase has multiple consequences but today we’re going to focus on the hardware impacts.

With more memory to work with, we wind up bottle-necked on memory transfers within the GPU. We were stuck here for a while until Tri Dao came up with Flash Attention, a kernel fusion that makes running Attention significantly more memory efficient. This one insight may be the most important optimization for Large Language Model (LLM) inferencing.

Today I’m going to go in detail on the intuition behind this finding. Specifically I’ll be leaning on the brilliant explanation put forth by Zihao Ye in his paper [“From Online Softmax to FlashAttention”](<https://courses.cs.washington.edu/courses/cse599m/23sp/notes/flashattn.pdf>) as well as my personal experience.

Let’s dive in!

## Associativity of Tiled Matrix Multiplication

We’re going to start with a very simple GPU calculation: matrix multiplication. Matrix multiplication requires we iteratively bring rows and columns of the operating matrices into memory. The simple example below shows how we bring the rows of the first matrix into memory so that we can multiply them with the columns of the second matrix.

Press enter or click to view image in full size

Image by Author — Example of Matrix Multiplication

The code below implements this naively involves bringing the same row or column into memory repeatedly, resulting in a high proportion of cache misses and thus slow downs.

```python import numpy as npdef naive_matmul(A, B): n, m = A.shape m2, p = B.shape assert m == m2, "Incompatible dimensions" C = np.zeros((n, p)) for i in range(n): for j in range(p): for k in range(m): C[i, j] += A[i, k] * B[k, j] return C ```

To improve cache performance in matrix multiplication, we use tiled matrix multiplication. This technique breaks matrices into smaller submatrices (tiles) that fit into the CPU cache. Instead of computing the product sequentially, we process one tile at a time, reusing data in faster memory as much as possible. By choosing the right tile size, we can significantly reduce cache misses and speed up computation. The following Python example demonstrates this approach.

```python import numpy as npdef tiled_matmul(A, B, tile_size): n, m = A.shape m2, p = B.shape assert m == m2, "Incompatible dimensions" C = np.zeros((n, p)) for ii in range(0, n, tile_size): for jj in range(0, p, tile_size): for kk in range(0, m, tile_size): for i in range(ii, min(ii + tile_size, n)): for j in range(jj, min(jj + tile_size, p)): for k in range(kk, min(kk + tile_size, m)): C[i, j] += A[i, k] * B[k, j] return C ```

This visual from Penny Xu does an excellent job showing the visual intuition here:

Press enter or click to view image in full size

[Gif By Penny Xu — Tiled Matrix Multiplication Visualized](<https://penny-xu.github.io/blog/tiled-matrix-multiplication>)

The speed up you see from tiled matrix multiplication depends on your hardware and the size of your matrices. For our ML use cases, you would expect to see anywhere from 20x — 100x speed ups. So when it comes to optimizes matrix calculations — which Attention is a special form of — the name of the game is moving towards tiled matrix multiplications.

So why is this hard to do with Attention? While we can do tiled matrix multiplication between the Q and K matrices, we need to softmax the resulting matrix before we can do the last matrix multiplication. Thus, a critical step to optimizing attention is figuring out how to handle that Softmax. To start there, we need to understand the complexities involved with that equation.

## SoftMax and Overflow

Softmax turns a list of numbers into probabilities by making the bigger numbers stand out more and the smaller ones stand out less. It does this by taking the exponential of each number to boost differences, then dividing each result by the total of all those exponentials so everything adds up to one.

Press enter or click to view image in full size

Image by Author — Equation for Softmax

Interestingly, this equation puts strain on the maximum range our floating point values can hold. The maximum value a 16-bit floating point can hold is 65,504, so if x is greater than 11, this will cause an overflow and wreck our calculation.

To get around this, we find the maximum value in our tensor (m) and subtract this from the exponent. This ensures that x is never greater than a floating point can hold, but it does pose the risk of an underflow error. Thankfully, because very small numbers become 0 in softmax, this effectively becomes a rounding error and does not impact our calculation.

Press enter or click to view image in full size

Image by Author — Equation for Safe Softmax

Why is safe softmax the same as softmax? We are effectively multiplying the top and bottom of our fraction by e^-m, which is the same as multiplying by 1.

Press enter or click to view image in full size

Image by Author — Softmax Multiplied by 1

## 3-Pass Safe SoftMax

To effectively calculate softmax, we can write this out in 3 steps. Because we are iterating through the input tensor 3 times, we’ll call this a 3-pass approach.

We start off by finding the maximum value (`max_val` ) to account for overflows. We then calculate all of the exponentials using `max_val` while accumulating these values into the sum. Finally, we take our sum and use it to normalize all of our exponentials. This might look something like the Python code laid out below:

```python import numpy as npdef softmax_3pass(input_array): n = len(input_array) output = np.zeros(n, dtype=float) # First pass: find max max_val = input_array[0] for i in range(1, n): if input_array[i] > max_val: max_val = input_array[i] # Second pass: compute exp(x - max) and sum sum_val = 0.0 for i in range(n): output[i] = np.exp(input_array[i] - max_val) sum_val += output[i] # Third pass: normalize for i in range(n): output[i] /= sum_val return output ```

While this is correct and easy to understand, it nevertheless is not efficient and still blocks us from being able to do tiled matrix multiplication throughout Attention. We’d love to make this more efficient and reduce the number of passes required.

## 2-Pass Safe Softmax

To do loop fusion, we need to find a way to capture the information found in one of the passes while we are doing another. If we focus on the first loop, we see that we don’t necessarily need the absolute largest value in the tensor, just a large value that can keep us from overflowing so far.

By only looking for the local max and not the global max, we can fuse passes 1 and 2 together. However, to ensure that we are still multiplying only by 1 on both sides, we need to scale our denominator whenever we find a new maximum. This has some subtleties, so I’ll go over the if statement in the first pass more below.

```python import numpy as npdef softmax_online(input_array): n = len(input_array) output = np.zeros(n, dtype=float) # Initialize running maximum with first element m = input_array[0] # Running sum (starts with e^(x_0 - m_0) = 1.0) d = 1.0 # Pre-pass to compute final max and total sum for i in range(1, n): if input_array[i] > m: # Adjust the sum when we find a new maximum d = d * np.exp(m - input_array[i]) + 1.0 m = input_array[i] else: # Add the contribution of this element to the sum d += np.exp(input_array[i] - m) # Final pass to compute softmax outputs for i in range(n): output[i] = np.exp(input_array[i] - m) / d return output ```

Once we know that there is a larger max than the one we’ve been currently scaling with, we know we need to adjust our denominator to account for this. We multiply all of the previous values by the exponential of the old maximum minus the new one. This cancels out all of the old maximums and replaces it with the new one. We then need to add the newest scaled value, which is the exponential of 0, which is 1.

We call this 2-pass Softmax Online Softmax because we are figuring out the global statistics (the denominator and maximum vaue) as we go. It is this online insight that drives us to Flash Attention! In fact, we can find a way to reduce Flash Attention down to 1 pass!

## Flash Attention

Remember that Attention can be split into 3 passes. First, we do the matrix multiplication between Queries and Key. Then we softmax that value to get our attention pattern. Finally, we do a matrix multiplication of the attention pattern and Values to get our output.

Press enter or click to view image in full size

Equations 2,3, and 4 from [“From Online Softmax to Flash Attention”](<https://courses.cs.washington.edu/courses/cse599m/23sp/notes/flashattn.pdf>)

We’ve seen that matrix multiplication can be sped up with tiled matmuls and that softmax can be reduced to 2-passes via online softmax. In the first pass, we do matrix multiplication on Q and K, and determine the maximum X value along with the denominator for softmax (basically do the first pass of softmax). The second pass then completes our softmax (building the Attention Pattern `A`) and does matrix multiplication to get the output.

Press enter or click to view image in full size

Equations 11 and 12 from [“From Online Softmax to Flash Attention”](<https://courses.cs.washington.edu/courses/cse599m/23sp/notes/flashattn.pdf>)

Now, if we can figure out the value of `A` on the fly, then we can combine the two passes. While the current formulation of A relies on global statistics, we can use the same trick from online softmax to rewrite each element of A as a result of the local statistics. Then when we find a new maximum, we scale the values just as before.

The below shows the new formulations to allow for this:

Press enter or click to view image in full size

Algorithm Flash Attention from[ “From Online Softmax to Flash Attention”](<https://courses.cs.washington.edu/courses/cse599m/23sp/notes/flashattn.pdf>)

There are a ton of low-level optimizations that go into this, so for those curious the exact coding implementation can be found in [Tri Dao’s Github](<https://github.com/Dao-AILab/flash-attention/tree/main/flash_attn>). Nevertheless, to show possible implementation details for this algorithm, here is a simplified version:

```python import numpy as npdef flash_attention(Q, K, V, k): """ Parameters: Q: Query matrix K: Key matrix (transposed in the computation) V: Value matrix k: Row index for query Returns: Output vector O[k,:] after processing - equivalent to softmax(Q[k,:] @ K) @ V """ N = K.shape[1] # Get the dimension from K matrix # Initialize variables m_i_minus_1 = float('-inf') # Initial value for m_{i-1} d_i_minus_1 = 0.0 # Initial value for d'_{i-1} o_i_minus_1 = np.zeros_like(V[0, :]) # Initial value for o'_{i-1} for i in range(N): # Calculate x_i using the k-th row of Q and i-th column of K^T x_i = np.dot(Q[k, :], K[:, i]) # Update max value m_i = max(m_i_minus_1, x_i) # Calculate d'_i d_i = d_i_minus_1 * np.exp(m_i_minus_1 - m_i) + np.exp(x_i - m_i) # Calculate o'_i o_i = (o_i_minus_1 * d_i_minus_1 * np.exp(m_i_minus_1 - m_i) / d_i) + (np.exp(x_i - m_i) / d_i) * V[i, :] # Update previous values for next iteration m_i_minus_1 = m_i d_i_minus_1 = d_i o_i_minus_1 = o_i # The result is o'_N return o_i_minus_1 ```

## Finding More Flash Attention Optimizations

In closing, Flash Attention is perhaps the most important optimization for Machine Learning to date. Interestingly, local optimizations of the component operations will not lead to Flash Attention. Put simply, if you have to solve softmax down to one pass, you will not reach Flash Attention. Instead, when we take the global view of what we want, we see ways to optimize. In that way, it really is incredible how Tri Dao was able to find this.

This kind of thinking — connecting seemingly disparate pieces to unlock transformative efficiency — is what drives our work at Luminal. By reimagining how we approach algorithmic design and hardware interaction, we’re exploring how systems like Flash Attention can inspire even broader optimizations across ML pipelines. Our system has discovered Flash Attention automatically, and the potential for further breakthroughs is very exciting.

As the field evolves, so too will the tools and techniques we build to harness its power. Whether you’re optimizing attention mechanisms, tiled matmuls, or entirely new architectures, there’s no shortage of exciting challenges ahead.

It’s an exciting time to be building — and even more exciting to imagine what comes next.

[1] Ye, Z., [“From Online Softmax to Flash Attention”](<https://courses.cs.washington.edu/courses/cse599m/23sp/notes/flashattn.pdf>) (2023), University of Washington

[2] Xu, P., [“Tiled Matrix Multiplication”](<https://penny-xu.github.io/blog/tiled-matrix-multiplication>) (2019), GitHub
