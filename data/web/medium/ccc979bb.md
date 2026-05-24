---
domain: medium.com
fetch_date: '2026-05-18T12:51:26.104894'
status: ok
url: https://medium.com/@techsachin/comatoformer-combination-attention-network-based-on-transformer-model-for-semantic-sentence-0b91a00e20ea
---

# Comateformer: combination attention network based on transformer model for better semantic sentence matching

[ ![SACHIN KUMAR](https://miro.medium.com/v2/resize:fill:64:64/1*7GE5_sjWH8e95wFj2s9sgg.jpeg) ](</@techsachin?source=post_page---byline--0b91a00e20ea--------------------------------------->)

[SACHIN KUMAR](</@techsachin?source=post_page---byline--0b91a00e20ea--------------------------------------->)

9 min read

·

Dec 11, 2024

\--

\--

Listen

Share

More

For Semantic sentence matching (SSM) tasks ,Transformer-based models examine the general similarity between the sentences, but because of the attention softmax operations, they do miss the tiny subtleties that differentiate them from each other.

To address it, this paper[1] propose a novel semantic sentence matching model named Combined Attention Network based on Transformer model (Comateformer), which encompasses a novel transformer-based quasi-attention mechanism with compositional properties. Unlike traditional attention mechanisms that merely adjust the weights of input tokens, this proposed method learns how to combine, subtract, or resize specific vectors when building a representation.

**Key contributions:**

* conduct a comprehensive study of the subtle differences between sentence pairs and propose a new method named Comateformer for semantic matching tasks, which has two distinct kinds of functions to represent the interaction between phrase pairs from various viewpoints,and the softmax function was eliminated from the attention mechanism, resulting in an increased receptive field and enhanced capacity to catch tiny differences
* explicitly integrate Comateformer into both pre-trained and non-pretrained models, and the results showed that the proposed method can provide greater expressive power, and it can fully discover the inherent complex relationships between sentence pairs for effective semantic matching.
* carry out a series of experiments on 10 matching datasets and robustness testing datasets. Experimental results show that Comateformer has achieved consistent improvements, especially in the robustness test, achieving an average improvement of 5% over BERT.

## Task Definition

* In context of paraphrase identification, Q and P represent two sentences. The variable y is used to denote the outcome, where Y can take the values of either 0 or 1, with y = 1 indicates that Q and P are paraphrases of each other and 0 otherwise.
* In context of a natural language inference task, the premise sentence is denoted as Q, the hypothesis sentence as P, and the variable y represents the possible outcomes of the task, namely inference, contradiction, or neutral.
* A comparison between Comateformer and classical attention is shown in figure below

![image](https://miro.medium.com/v2/resize:fit:700/1*OF3UwXF15nK-A4pH6ECqOQ.png)
* Softmax attention computes the similarity between all Q-K pairs. Linear attention applies mapping function Φ(·) to Q and K respectively
* Our Combined Attention models both global affinity and local difference information, thus achieving dual perception of affinity and non-affinity, with higher fine-grained differentiation advantages.

## Comateformer Modules

### i) Dual Affinity Module

* In this module, we design two different functions, affinity function and difference function, to compare the affinity and difference of vectors between two sentences
* First, we compute the pairwise affinities between each word in A and B via the dot product, which computes the pairwise similarity between any two elements in A and B:

![image](https://miro.medium.com/v2/resize:fit:237/1*Wh-L_DmYhcufFMzfqq4KSQ.png)

FE(.) represents a parameterized function, such as a standard linear/nonlinear function. Additionally, α represents a scaling constant and a nonnegative hyperparameter, which can be thought of as a temperature setting that adjusts saturation.

* Next, as a measure pairwise of negativity (i.e., dissimilarity) between each word in A and B, we perform the following calculation:

![image](https://miro.medium.com/v2/resize:fit:289/1*iX0XDqkcafGkrODmy3un7w.png)
* In this function, we introduce a parameterized function FN(.) and a scaling constant β, while preserving the L1-Norm l1.
* fundamental concept underlying negative distance involves utilizing negative affinity values as a gating mechanism to represent negative qualities, a capability that is absent in the original attention method.

### ii) Compositional Attention Module

* proposed combined attention propose is completely different from vanilla attention. First, it has no softmax operation. Specifically, we use the following equations for attention modeling:

![image](https://miro.medium.com/v2/resize:fit:266/1*jMRXxE_9pgGYuwgY5mUaXQ.png)

where M is the final attention matrix in the combined attention mechanism, which is an elementwise multiplication between two matrices.

**a) Normalization of matrix N**

* Since N is constructed from negative L1 distances, it is clear that sigmoid(N) ∈ [0, 0.5].
* Therefore, to ensure that sigmoid(N) lies in the range [0, 1], we center the matrix N so that its mean is zero: N = N − Mean(N)
* by scaling the matrix N, we preserve the ability to scale up and down the median of the tanh(E) matrix, since sigmoid(N) has a saturation region between 0 and 1, behaving more like a gating mechanism
* At the same time we also try the second form of scaling, as an alternative to centering: M = tanh(E) ⊙ (2 ∗ sigmoid(N)), which was more effective approach

**b) Temperature**

* introduced hyperparameters α, β that control the size of E and N in previous section, that controls and affect the temperature of the tanh and sigmoid functions.
* high values of α, β will enforce hard-form combined pooling. In this task we set α = 1 and β = 1.
* Finally, we apply the Compositional Attention Matrix M to the input sequences A and B with the following formula:

![image](https://miro.medium.com/v2/resize:fit:317/1*hzPQIG2m5fXk_9mI9a9p4g.png)
* And the two sentences are update as Aˆ ∈ RNa×d and ˆB ∈ RNb×d. Taking Aˆ as an example, each element Ai in A traverses sentence B and determines whether it contains the token in sentence B by adding (+1), subtracting (-1) or deleting (×0).
* Similarly, each element in sentence B traverses sentence A and decides to add, subtract, or delete a token from A.

## Incorporating Comateformer to Transformer

* Figure below shows the location of Comateformer integrated in the transformer and the schematic diagram of the specific modules of Comateformer

![image](https://miro.medium.com/v2/resize:fit:700/1*5pTPrsKFJ5HooZTE3iCYag.png)
* Comateformer replaces the original attention module with de-softmaxed Dual Affinity Module, that is, the original Transformer internal attention equation

![image](https://miro.medium.com/v2/resize:fit:261/1*3JNM86GACjC84FxP9oIySw.png)

is now changed to

![image](https://miro.medium.com/v2/resize:fit:468/1*wtFCUYfIRcEUnuSw0hgIdw.png)

where G(.) is the negation of outer L1 distance between all rows of Q against all rows of K. We either apply centering to (G(QK) √dk∗ V ) or 2 *sigmoid(G(QK) √dk) ∗ V to ensure the value is in [0,1].

* Finally, both affinity matrices are learned by transforming Q, K, V only once.

## Incorporating Comateformer to PLMs

* disassembled the BERT main layer and verified the lack of differential information in different layers of BERT. By solving these problems, we can figure out which layers of BERT are missing differential information
* use the robustness testing tool TextFlint as an experimental data set to study the above issues.
* First, TextFlint makes slight changes to each sampled example so that the sentence pairs have subtle differences.
* Second, we freeze the parameters of the BERT model (except the softmax classification output head) and adopt pre-trained contextualized word representations for the TextFlint task
* leverage TextFlint to perform syntax structure transformations on the dataset, and the performance results are averaged over five different runs. A higher score indicates a stronger proficiency.
* Figure below presents the performance of the BERT model layer-by-layer for difference awareness

![image](https://miro.medium.com/v2/resize:fit:396/1*4U5XnOCpDveikRF4jagBOg.png)
* From the figure, we observe that after freezing the layer parameters of BERT, the sensitivity to difference differs among the layers, with the middle and upper layers being more sensitive to difference than the lower layers.
* In order to minimize the damage to the original pre-training process, we replace the multi-head attention in the first to third layers with Comateformer in the ratio of 50%, 40%,and 30%.

## Results and Analysis

### i) Model performance

* Table below compares the performance of Comateformer and competing models across 10 datasets

![image](https://miro.medium.com/v2/resize:fit:700/1*oICba6uZvkuniHIhKix-sg.png)
* When the backbone model is BERT-base or BERT-large, the average accuracy after integrating Comateformer is improved by 1.1% and 0.8%, respectively, showing the effectiveness of our Comateformer Model on semantic matching tasks.
* proposed method outperforms RoBERTa-base by 1.6% and RoBERTa-large by 0.6%, respectively. which demonstrates that Comateformer can effectively capture the relationship between sentences from different aspects, so that more fine-grained and complex relationships can be exploited

### ii) Robustness test performance

* Figure below lists the accuracy of Comateformer and BERT

![image](https://miro.medium.com/v2/resize:fit:524/1*X3PCMUle7hZMHUaaiI3Evw.png)
* We can observe that in SwapAnt our model outperforms BERT nearly 6%, which indicates that Comateformer can better handle semantic contradictions caused by antonyms.
* And the model performance drops to 77.2% on SwapNum transformation, while Comateformer outperforms BERT by nearly 5% because it requires the model to capture subtle entity differences for correct linguistic inference.
* In other transformations, Comateformer still outperforms the baseline, which reflects its effectiveness.

### iii) Case Study

* Table below shows a case study, with the example sentence pairs of our cases. Red and Blue are difference phrases.

![image](https://miro.medium.com/v2/resize:fit:700/1*tDWDyyIUMtC8XAO_lR6fgA.png)
* pre-trained language model BERT can identify semantic differences in case 1 and give correct predictions with the help of strong contextual representation capabilities
* similarity of BERT’s predicted sentence pairs is 46.32%, while that of BERT-Comateformer is only 1.87%. Second, in case 2, the sentence pairs “from 70 to 60” and “from 60 to 50" express different semantics, but they are primarily the result of numerical differences
* Although
* BERT identified the correct label in case 1 by a small margin, in case 2, it was unable to capture numerically induced differences and gave wrong predictions because it requires the model to capture subtle numerical differences for correct language reasoning
* Finally, our model made correct predictions in all of the above cases

### iv) Attention Distribution

* To visually demonstrate the impact of different attention functions inside multi-channel attention on the interactive alignment of sentence pairs, we show the weight distribution of three kinds of attention in Figure below:

![image](https://miro.medium.com/v2/resize:fit:478/1*TtQJlPDPLVk_lBGZUCRb3A.png)
* First, in Figure (a), Dot attention can pay attention to the same words and semantically related words in sentence pairs, but it is heavily influenced by the same words in sentence pairs
* Secondly, in Figure (b), it can be observed that Minus attention explicitly pays attention to the difference between “software” and “hardware”, and its attention weight is the largest among all word pairs
* in Figure (c), the attention weights in combined attention focus on the same and different words, which shows that combined attention can both focus on the same part of the sentence pair and capture different parts, and this mechanism can capture both Affinity and dissimilarity of sentence pairs.

## Conclusion

* proposed a combination attention network based on transformer model for semantic sentence matching named Comateformer
* This model successfully captures the different information that is contained in pairs of words and integrates it into a model that has already been pretrained.
* core of Comateformer lies in its dual-affinity module and compositional attention mechanism, which jointly capture the nuanced similarities and dissimilarities between sentence pairs
* qualitative case study and attention distribution analysis provide clear insights into how Comateformer operates, revealing its ability to adaptively focus on relevant aspects of sentence pairs to enhance semantic understanding.
* The results of our experiments on 10 publicly available datasets as well as a robustness dataset show that the consistent improvements across various metrics, especially the remarkable gains in robustness testing, underscore the effectiveness of our approach

Paper: <https://arxiv.org/abs/2412.07220>

References:

1. Comateformer: Combined Attention Transformer for Semantic Sentence Matching by Li et al. [arXiv:2412.07220](<https://arxiv.org/abs/2412.07220>)
