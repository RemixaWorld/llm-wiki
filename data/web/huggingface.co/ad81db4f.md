---
domain: huggingface.co
fetch_date: '2026-05-18T12:37:47.485170'
status: ok
url: https://huggingface.co/blog/rishiraj/kld-guided-quantization
---

# Why Maybe We're Measuring LLM Compression Wrong

The community has gotten incredibly good at this. We see headlines every week: "Mixtral 8x7B running in 4-bit," "Llama 3 70B in 3-bit," and we all rush to download the GGUF or AWQ version. We check the MMLU score, see it only dropped by a point or two, and call it a win.

But what if I told you that MMLU score is hiding a dark secret? What if our entire approach to measuring the "goodness" of a quantized model is fundamentally flawed?

Let's go on a little journey together. We'll start with the standard way we think about quantization and slowly peel back the layers to reveal a more nuanced, more powerful, and frankly, more *correct* way to do it.

### Wait, Stable Accuracy Can Be a Bad Thing? Meet the "Flip"

Let's imagine you're a teacher. You give your star student, "FP16-Model," a 100-question history test. They get 90 questions correct. That's your baseline.

Now, you create a "clone" of this student, "INT4-Model," through a mysterious process (quantization). You give this clone the same test. They *also* score a 90/100. Fantastic, right? The clone is just as smart!

But then you look closer. You compare their answer sheets side-by-side. You find something disturbing.

- On 5 questions that FP16-Model got right, INT4-Model got them wrong.
- On 5
*different*questions that FP16-Model got wrong, INT4-Model, by sheer luck or a change in reasoning, got them right.

The final score is identical, but the student's *knowledge* has been subtly corrupted. The behavior has changed. This is the core idea behind a "flip," a term brilliantly highlighted in the research paper **"Accuracy is Not All You Need"**.

A **flip** is any instance where a model's answer to a question changes from incorrect-to-correct or, more worryingly, **correct-to-incorrect** after quantization.

This isn't just a hypothetical. Look at the data from the paper. They took a Llama2-13B model and started compressing it, measuring both the drop in MMLU accuracy and the percentage of flips.

Look at the left side of that graph. As they drop the last few layers of the network (moving from 0.0 to 0.1 on the x-axis), the blue line, "Accuracy Diff," barely moves. It stays near zero. By traditional metrics, the model is perfectly fine! But look at the red line, "Flips." It immediately jumps to over 5%. That means 1 in 20 answers has changed, even while the final score remains the same. The model's behavior has already started to diverge significantly.

Our goal in quantization isn't just to get a model with a good score on a benchmark. **Our goal is to create a smaller version of the original model that behaves as identically to it as possible.** We want to preserve its reasoning paths, its safety training, its personality. A high flip rate is a red flag that we've created a Frankenstein's monster—it looks the same on the outside, but the inside is different.

### Okay, So How Do We Measure This Damage? Enter KL Divergence.

"I get it," you might say. "Flips are bad, accuracy scores can lie. So how do we measure the potential for flips without running a million benchmarks?"

For a long time, the community's answer was **Perplexity (PPL)**. It measures how "surprised" a model is by a sequence of text. It seems like a decent proxy for model quality, so it should be a good proxy for quantization error, right?

Wrong. Perplexity is a surprisingly deceptive metric for this task.

Imagine the original model is predicting the next word in "The cat sat on the ___." Its output probability distribution might look like this:

`mat`

: 40%`rug`

: 30%`floor`

: 10%- ... (everything else is very low)

Now, our quantized model's prediction:

`mat`

: 35%`rug`

: 34%`floor`

: 5%`table`

: 4%- ... (other probabilities have shifted)

Perplexity primarily cares about the probability assigned to the *correct* token (`mat`

). It sees it went from 40% to 35%—a small drop, so the PPL change will be minimal. But look at the whole picture! The overall "shape" of the model's certainty has been warped. Perplexity, by focusing on a single point, misses this geometric change. It's like checking if two pictures are the same by only looking at the top-left pixel.

This is where **Kullback-Leibler (KL) Divergence** comes in.

KLD isn't a new concept, but its application as the gold standard for quantization error is a game-changer. KLD measures the "distance" between two probability distributions. It doesn't just look at one token; it compares the *entire* vector of probabilities from the original model to the quantized model. It asks, "How much information is lost when we use the quantized distribution to approximate the original one?"

And here's the absolute kicker, again from the "Accuracy is Not All You Need" paper: **KL Divergence is highly correlated with flips.** This is our Rosetta Stone.

Just look at these charts. Each blue dot is a different compressed version of a model. On the x-axis, you have the percentage of flips. On the y-axis, the measured KL Divergence. The relationship is undeniable. The points form a clear, rising line. The Spearman correlation is a stunning `0.96`

and `0.97`

!

This is the proof we need. By minimizing the KLD between the original and quantized models' outputs, we are directly and reliably minimizing the risk of flips. We now have a sensitive and theoretically sound metric to guide our entire quantization strategy.

### So, What's the Smart Way to Quantize?

Armed with this new goal (minimize flips) and our North Star metric (minimize KLD), how does this change our strategy?

The current, popular approach is *uniform quantization*: load a model, pick a format (like NF4), and apply it to almost every linear layer in the network. It's simple, but it's a blunt instrument. It's like performing surgery with a sledgehammer.

The key insight is that **not all layers are created equal.**

Think about a modern Mixture-of-Experts (MoE) model like Mixtral or Grok. These models are massive, but in a clever way. For every token, they only use a small subset of their total parameters. A huge chunk of their size comes from the "experts," which are essentially massive Feed-Forward Networks (FFNs).

This architecture gives us a unique opportunity. What if we don't quantize everything to 4-bit? What if we handle this a bit strategically?

**High-Impact, Low-Sensitivity Layers:**The MoE expert layers are the perfect candidates for aggressive quantization. They make up a*massive*percentage of the model's total parameters. Quantizing them from 16-bit to, say, 2-bit or 3-bit yields an enormous reduction in model size. Crucially, because any single expert is only used for a fraction of tokens, the error introduced by quantizing it heavily is often "drowned out" or compensated for by the rest of the network.**Low-Impact, High-Sensitivity Layers:**Now, think about the attention mechanism—the`Q`

,`K`

, and`V`

projections. These layers are used for*every single token*. They are the backbone of the model's ability to see relationships between tokens. They are incredibly sensitive. The KLD spike from quantizing these layers, even to 4-bit, can be dramatic.

This is the tradeoff in action: **We trade precision where it matters least (MoE experts) to save precision where it matters most (attention, embeddings).**

### Putting It Into Practice: A Blueprint for Smart Quantization

This isn't just theory. Here’s how you'd actually implement this smart, selective quantization:

**Profile Your Model:**You don't guess which layers are sensitive; you measure it. Take your FP16 model and a calibration dataset (a few hundred examples from a diverse corpus is enough).- For each layer (or type of layer), perform a "mock" quantization. Quantize
*only that layer*and measure the mean KL Divergence at the final output logits compared to the original model. - This gives you a "sensitivity score" for every part of your network. You'll likely see that
`attention.q_proj`

has a much higher KLD sensitivity than`block_sparse_moe.experts.0.w1`

.

- For each layer (or type of layer), perform a "mock" quantization. Quantize
**Set Your Bit Budget:**Decide on your target final model size. This is your "bit budget." For example, you want your 90GB FP16 model to be around 25GB.**Allocate Bits Intelligently:**Now, you solve an optimization problem.**MoE FFNs:**These showed low KLD sensitivity but are huge. Allocate them the fewest bits (e.g., 2.5 bits). This gives you the biggest bang for your buck in size reduction.**Attention Layers (QKV/O):**These were highly sensitive. They get the most bits. Keep them at 6-bit, 8-bit, or even bfloat16. They don't take up much space, so the "cost" of keeping them high-precision is low.**Other Layers:**Fill in the middle. Maybe the MLP`gate`

and`down_proj`

can handle 4-bit, while the embedding layer needs 8-bit. Your profiling data will guide you.


The result is a hybrid, mixed-precision model that is intelligently compressed. It's dramatically smaller than the original, but by preserving the most sensitive parts of the network, it has a much lower KLD, and therefore a much lower flip rate, than a uniformly quantized model of the same size.

### It's Time we approach Quantization differently

The time of one-size-fits-all quantization is coming to an end. As models become more complex and our need for them to be both powerful and accessible grows, our compression techniques must evolve.

**Look Beyond Benchmarks:**Stop relying solely on MMLU. Start measuring**flips**to understand if you're preserving the model's true behavior.**Use KL Divergence:**Use mean KLD as your ground-truth metric for quantization error. As we've seen, it's a far more reliable signal than perplexity and an excellent proxy for flips.**Quantize Smartly, Not Brutally:**Profile your models. Apply aggressive, low-bit quantization to large, robust components like MoE experts, and protect the delicate, critical layers like attention with higher precision.

This is how we thread the needle and build models that are not just smaller, but smaller *and* faithful to the original giants they were born from.
