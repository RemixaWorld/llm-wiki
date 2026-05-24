---
domain: ai.gopubby.com
fetch_date: '2026-05-18T12:46:35.068811'
status: ok
url: https://ai.gopubby.com/advanced-rag-09-prompt-compression-95a589f7b554
---

# Advanced RAG 09: Prompt Compression

## Method Classification, Algorithm Principles and Code Explanation

[ ![Florian June](https://miro.medium.com/v2/resize:fill:64:64/1*DmQ3DH2JeAJquvhT_tjVCw.jpeg) ](<https://medium.com/@florian_algo?source=post_page---byline--95a589f7b554--------------------------------------->)

[Florian June](<https://medium.com/@florian_algo?source=post_page---byline--95a589f7b554--------------------------------------->)

29 min read

·

Apr 3, 2024

\--

Listen

Share

More

The RAG process may encounter two issues:

* Large Language Model(LLM) typically has a context length limit. Therefore, the longer the input text, the more time-consuming and costly the process becomes.
* The retrieved contexts may not always be useful. It’s possible that only a small portion of a larger chunk is relevant to the answer. In some cases, it may be necessary to combine multiple chunks to answer a specific question. This problem persists even with re-ranking.

Prompt compression for LLM is a method to address these issues. Essentially, the goal is to retain the key information from the prompt, making the input tokens more valuable. This approach enhances the model’s performance and reduces cost. As depicted in the bottom right of Figure 1.

Press enter or click to view image in full size

Figure 1: prompt compression(bottom right) in RAG. As depicted by the purple dashed line, some compressors can also be applied directly to the retrieved contexts. Image by author.

It’s worth noting that, as depicted by the purple dashed line in Figure 1, some compressors can also be applied directly to the retrieved contexts.

Overall, prompt compression methods can be divided into four main categories:

* Methods based on information entropy, such as [Selective Context](<https://arxiv.org/pdf/2304.12102.pdf>), [LLMLingua](<https://arxiv.org/pdf/2310.05736.pdf>), [LongLLMLingua](<https://arxiv.org/pdf/2310.06839.pdf>). These methods use a small language model to calculate the self-information or perplexity of each token in the original prompt. They then delete tokens with lower perplexity.
* Methods based on soft prompt tuning, such as [AutoCompressor](<https://arxiv.org/pdf/2305.14788.pdf>) and [GIST](<https://arxiv.org/pdf/2304.08467.pdf>). These methods require fine-tuning of the LLM parameters to make them suitable for specific domains, but cannot be directly applied to black-box LLM.
* First, carry out data distillation from LLM, then train models to generate more interpretable text summaries. These can be transferred between different language models and applied to black-box LLMs that do not require gradient updates. The representative methods are [LLMLingua-2](<https://arxiv.org/pdf/2403.12968.pdf>) and [RECOMP](<https://arxiv.org/pdf/2310.04408.pdf>).
* Methods based on token merging or token pruning, such as [ToMe](<https://arxiv.org/pdf/2210.09461.pdf>) and [AdapLeR](<https://aclanthology.org/2022.acl-long.1.pdf>). These methods usually require model fine-tuning or generating intermediate results during the inference process.

Given that the fourth type of methods was initially proposed for smaller models like ViT or BERT, this article will introduce the principles of the representative algorithms in the first three method types.

## Selective Context

### Insight

Figure 2 demonstrates that LLMs can respond to user queries without requiring the full context or complete dialogue history. Even when relevant information is omitted, LLMs can still produce the anticipated response. This may be attributed to the ability of LLMs to deduce missing information from context clues and prior knowledge obtained during pre-training.

Press enter or click to view image in full size

Figure 2. LLMs are able to answer correctly with less informative content deleted. Source: [Selective Context](<https://arxiv.org/pdf/2304.12102.pdf>).

Therefore, it’s possible to optimize context length by filtering out less informative content, without compromising performance. This is the key insight of [Selective Context](<https://arxiv.org/pdf/2304.12102.pdf>).

Selective Context employs a small language model(SLM) to determine the self-information of lexical units, such as sentences, phrases, or tokens, in the given context. It then uses this self-information to evaluate their informativeness. By selectively keeping content with higher self-information, Selective Context offers a more concise and efficient context representation for LLM. This is achieved without impacting their performance across different tasks.

### Self-Information

Selective Context employs self-information to evaluate the quality of content.

Self-information, also referred to as surprisal or information content, is a key concept in information theory. It quantifies the amount of information conveyed by an event. It is defined as the negative logarithm likelihood of the token:

where `**I(x)**` represents the self-information of token `**x**` and `**P(x)**` denotes its output probability.

In information theory, self-information quantifies the level of surprise or uncertainty associated with an event. Rare events, conveying more information, have higher self-information. Conversely, common events, conveying less information, have lower self-information.

### Algorithm

To explain the principles more conveniently, let’s dive into the source code.

First, set up the environment by installing the corresponding python libraries and downloading the Spacy model.

```python (base) Florian:~ Florian$ conda create -n "selective_context" python=3.10 (base) Florian:~ Florian$ conda activate selective_context(selective_context) Florian:~ Florian$ pip install selective-context(selective_context) Florian:~ Florian$ python -m spacy download en_core_web_sm ```

After the installation is completed, the version is as follows:

```python (selective_context) Florian:~ Florian$ pip list | grep selectiveselective-context 0.1.4 ```

The test code is as follows:

```python from selective_context import SelectiveContextsc = SelectiveContext(model_type='gpt2', lang='en')text = "INTRODUCTION Continual Learning ( CL ) , also known as Lifelong Learning , is a promising learning paradigm to design models that have to learn how to perform multiple tasks across different environments over their lifetime [To uniform the language and enhance the readability of the paper we adopt the unique term continual learning ( CL ) .]. Ideal CL models in the real world should be deal with domain shifts , researchers have recently started to sample tasks from two different datasets . For instance , proposed to train and evaluate a model on Imagenet first and then challenge its performance on the Places365 dataset . considers more scenarios , starting with Imagenet or Places365 , and then moving on to the VOC/CUB/Scenes datasets. Few works propose more advanced scenarios built on top of more than two datasets."context, reduced_content = sc(text)# We can also adjust the reduce ratio# context_ratio, reduced_content_ratio = sc(text, reduce_ratio = 0.5) ```

The initial run will download the GPT-2 model, which is approximately 500MB in size. The results of the test code are shown in Figure 3.

Press enter or click to view image in full size

Figure 3: The results from the test code for Selective Context. Screenshot provided by author.

Next, let’s explore the function `**sc(text)**`. [The internal source code](<https://github.com/liyucheng09/Selective_Context/blob/v0.1.0rc1/src/selective_context/__init__.py#L273>) is as follows:

```python class SelectiveContext: ... ... def __call__(self, text: str, reduce_ratio: float = 0.35, reduce_level :str = 'phrase') -> List[str]: context = self.beautify_context(text) self.mask_ratio = reduce_ratio sents = [sent.strip() for sent in re.split(self.sent_tokenize_pattern, context) if sent.strip()] # You want the reduce happen at sentence level, phrase level, or token level? assert reduce_level in ['sent', 'phrase', 'token'], f"reduce_level should be one of ['sent', 'phrase', 'token'], got {reduce_level}" sent_lus, phrase_lus, token_lus = self._lexical_unit(sents) lexical_level = { 'sent': sent_lus, 'phrase': phrase_lus, 'token': token_lus } # context is the reduced context, masked_sents denotes what context has been filtered out context, masked_sents = self.self_info_mask(lexical_level[reduce_level].text, lexical_level[reduce_level].self_info, reduce_level) return context, masked_sents ```

The above code primarily involves three steps:

* Calculate the self-information of each token in the context.
* Merge tokens and their self-information based on lexical units, such as phrases or sentences.
* Selectively retain the information context.

**Step 1: Computing Self-Information**

Given the context `**C = x0, x1, …, xn**`, where each `**xi**` represents a token, we use a causal language model (such as GPT-2, OPT, and LLaMA) to calculate the self-information of each token `**xi**`:

If you’re using GPT-2, here is [the corresponding code](<https://github.com/liyucheng09/Selective_Context/blob/v0.1.0rc1/src/selective_context/__init__.py#L100>):

```python class SelectiveContext: ... ... def _get_self_info_via_gpt2(self, text: str) -> Tuple[List[str], List[float]]: if self.lang == 'en': text = f"[ENDOFTEXT]{text}" elif self.lang == 'zh': text = f"[CLS]{text}" with torch.no_grad(): encoding = self.tokenizer(text, add_special_tokens=False, return_tensors='pt') encoding = encoding.to(self.device) outputs = self.model(**encoding) logits = outputs.logits probs = torch.softmax(logits, dim=-1) self_info = -torch.log(probs) input_ids = encoding['input_ids'] input_ids_expaned = input_ids[:, 1:].unsqueeze(-1) ```

**Step 2: Merging into Lexical Units**

Performing selective context filtering directly at the token level could result in an incoherent context. For example, “2009” in the original prompt may be compressed to “209”.

Hence, besides token-level filtering, it’s crucial to implement filtering procedures at the phrase and sentence level as well. The basic unit in filtering, known as the lexical unit, can be a token, a phrase, or a sentence.

How to calculate the self-information for each lexical unit, `**u = (xt, …, xt+α)**`? We can add the self-information of each token that comprises `**u**`, following the principle of additivity of self-information:

[The corresponding code](<https://github.com/liyucheng09/Selective_Context/blob/v0.1.0rc1/src/selective_context/__init__.py#L146>) is as follows, debugging information for certain variables has been added:

```python class SelectiveContext: ... ... def _lexical_unit(self, sents): if self.sent_level_self_info: sent_self_info = [] all_noun_phrases = [] all_noun_phrases_info = [] all_tokens = [] all_token_self_info = [] for sent in sents: # print(sent) tokens, self_info = self.get_self_information(sent) ''' ipdb> sent 'INTRODUCTION Continual Learning ( CL ) , also known as Lifelong Learning , is a promising learning paradigm to design models that have to learn how to perform multiple tasks across different environments over their lifetime [To uniform the language and enhance the readability of the paper we adopt the unique term continual learning ( CL ) .].' ipdb> tokens ['IN', 'TR', 'ODUCT', 'ION', ' Contin', 'ual', ' Learning', ' (', ' CL', ' )', ',', ' also', ' known', ' as', ' Lif', 'elong', ' Learning', ',', ' is', ' a', ' promising', ' learning', ' paradigm', ' to', ' design', ' models', ' that', ' have', ' to', ' learn', ' how', ' to', ' perform', ' multiple', ' tasks', ' across', ' different', ' environments', ' over', ' their', ' lifetime', ' [', 'To', ' uniform', ' the', ' language', ' and', ' enhance', ' the', ' read', 'ability', ' of', ' the', ' paper', ' we', ' adopt', ' the', ' unique', ' term', ' continual', ' learning', ' (', ' CL', ' )', '.', '].'] ipdb> self_info [7.514791011810303, 1.632637619972229, 0.024813441559672356, 0.006853647995740175, 12.09920597076416, 2.1144468784332275, 9.457701683044434, 2.4503376483917236, 10.236454963684082, 0.8689146041870117, 5.269547939300537, 4.641763210296631, 0.22138957679271698, 0.010370315983891487, 10.071824073791504, 0.6905602216720581, 0.01698811538517475, 1.5882389545440674, 0.4495090842247009, 0.45371606945991516, 6.932497978210449, 6.087430477142334, 3.66465425491333, 3.3969509601593018, 7.337691307067871, 5.881226539611816, 1.7340556383132935, 4.599822521209717, 6.482723236083984, 4.045308589935303, 4.762691497802734, 0.21346867084503174, 3.7985599040985107, 4.6389899253845215, 0.33642446994781494, 4.918881416320801, 2.076707601547241, 3.3553669452667236, 5.5081071853637695, 5.625778675079346, 0.7966060638427734, 6.347291946411133, 12.772034645080566, 13.792041778564453, 4.11267614364624, 6.583715915679932, 3.3618998527526855, 8.434362411499023, 1.2423189878463745, 5.8330583572387695, 0.0013973338063806295, 0.3090735077857971, 1.1139129400253296, 4.160390853881836, 3.744772434234619, 7.2841596603393555, 1.4088190793991089, 7.86871337890625, 4.305004596710205, 9.69282341003418, 0.08665203303098679, 1.6127821207046509, 1.6296097040176392, 0.46206924319267273, 3.0398476123809814, 6.892032623291016] ''' sent_self_info.append(np.mean(self_info)) all_tokens.extend(tokens) all_token_self_info.extend(self_info) noun_phrases, noun_phrases_info = self._calculate_lexical_unit(tokens, self_info) ''' ipdb> noun_phrases ['INTRODUCTION Continual Learning', ' (', ' CL', ' )', ',', ' also', ' known', ' as', ' Lifelong Learning', ',', ' is', ' a promising learning paradigm', ' to', ' design', ' models', ' that', ' have', ' to', ' learn', ' how', ' to', ' perform', ' multiple tasks', ' across', ' different environments', ' over', ' their lifetime', ' [', 'To', ' uniform', ' the language', ' and', ' enhance', ' the readability', ' of', ' the paper', ' we', ' adopt', ' the unique term continual learning', ' (', ' CL', ' )', '.', ']', '.'] ipdb> noun_phrases_info [4.692921464797109, 2.4503376483917236, 10.236454963684082, 0.8689146041870117, 5.269547939300537, 4.641763210296631, 0.22138957679271698, 0.010370315983891487, 3.5931241369495788, 1.5882389545440674, 0.4495090842247009, 4.284574694931507, 3.3969509601593018, 7.337691307067871, 5.881226539611816, 1.7340556383132935, 4.599822521209717, 6.482723236083984, 4.045308589935303, 4.762691497802734, 0.21346867084503174, 3.7985599040985107, 2.487707197666168, 4.918881416320801, 2.7160372734069824, 5.5081071853637695, 3.2111923694610596, 6.347291946411133, 12.772034645080566, 13.792041778564453, 5.348196029663086, 3.3618998527526855, 8.434362411499023, 2.3589248929638416, 0.3090735077857971, 2.6371518969535828, 3.744772434234619, 7.2841596603393555, 4.672402499616146, 1.6127821207046509, 1.6296097040176392, 0.46206924319267273, 3.0398476123809814, 3.446016311645508, 3.446016311645508] ''' # We need to add a space before the first noun phrase for every sentence except the first one if all_noun_phrases: noun_phrases[0] = f" {noun_phrases[0]}" all_noun_phrases.extend(noun_phrases) all_noun_phrases_info.extend(noun_phrases_info) return [ LexicalUnits('sent', text=sents, self_info=sent_self_info), LexicalUnits('phrase', text=all_noun_phrases, self_info=all_noun_phrases_info), LexicalUnits('token', text=all_tokens, self_info=all_token_self_info) ] ```

**Step 3: Selective Retention of Informative Context**

Once the self-information of each lexical unit is calculated, the question arises: how can their informativeness be evaluated? The paper proposes an adaptive method using a percentile-based filtering approach to select the most informative content. This is preferable to using a fixed threshold or keeping a fixed number of the top k vocabulary units.

First, we arrange the lexical units in descending order based on their self-information values. Then, we compute the p-th percentile of these values for all lexical units. Next, we selectively retain lexical units with self-information values greater than or equal to the p-th percentile.

[The corresponding code](<https://github.com/liyucheng09/Selective_Context/blob/v0.1.0rc1/src/selective_context/__init__.py#L236>) is as follows.

```python class SelectiveContext: ... ... def self_info_mask(self, sents: List[str], self_info: List[float], mask_level): # mask_level: mask sentences, phrases, or tokens sents_after_mask = [] masked_sents = [] self.ppl_threshold = np.nanpercentile(self_info, self.mask_ratio * 100) # if title is not None: # with open(os.path.join(self.path, title+'_prob_token.tsv'), 'w', encoding='utf-8') as f: # for token, info in zip(tokens, self_info): # f.write(f"{token}\t{info}
") # with open(os.path.join(self.path, title+'_prob_sent.tsv'), 'w', encoding='utf-8') as f: # for sent, info in zip(sents, sent_self_info): # f.write(f"{sent}
{info}

") for sent, info in zip(sents, self_info): if info < self.ppl_threshold: masked_sents.append(sent) sents_after_mask.append(self.mask_a_sent(sent, mask_level)) else: sents_after_mask.append(sent) masked_context = " ".join(sents_after_mask) if mask_level == 'sent' else "".join(sents_after_mask) return masked_context, masked_sents ```

## LLMLingua

### Overview

[LLMLingua](<https://arxiv.org/pdf/2310.05736.pdf>) suggests that [Selective Context](<https://arxiv.org/pdf/2304.12102.pdf>) often disregards the interconnection among compressed contents and the correlation between LLM and the small language model used for prompt compression. LLMLingua precisely addresses these issues.

Specifically, as shown in Figure 4, LLMLingua employs a budget controller to dynamically allocate different compression ratios to various components of the original prompts, like instructions, demonstrations, and questions. It also performs coarse-grained, demonstration-level compression to maintain semantic integrity even at high compression ratios. In addition, LLMLingua introduces a token-level iterative algorithm for fine-grained prompt compression.

Press enter or click to view image in full size

Figure 4: Framework of the proposed approach LLMLingua. Source: [LLMLingua](<https://arxiv.org/pdf/2310.05736.pdf>).

Compared to Selective Context, LLMLingua can retain key information in the prompt more effectively while considering conditional dependencies between tokens. It can compress the prompt by a factor of 20.

### Budget controller

Budget controller is a key component of LLMLingua, used to dynamically assign different compression ratios to various parts of the original prompt.

Different sections of the prompt have varying sensitivities to compression. For instance, instructions and questions are more sensitive, while demonstrations are less sensitive. The budget controller’s role is to assign a lower compression ratio to instructions and questions, thereby preserving essential information. Conversely, a higher compression ratio can be allocated to demonstrations to eliminate redundant information.

The algorithm for budget controller is displayed in Figure 5:

Press enter or click to view image in full size

Figure 5: The algorithm for budget controller. Source: [LLMLingua](<https://arxiv.org/pdf/2310.05736.pdf>).

The primary variables are:

* `**M𝑠**`: A small language model, such as GPT-2 or LLaMA.
* `**x = (x^ins , x^dems , x^que)**`: The original prompt that includes instructions, demonstrations and questions.
* `**𝐿**`, `**𝐿_ins**`, `**𝐿_dems**`, and `**𝐿_que**` represent the numbers of tokens in `**x**`, `**x^ins**` , `**x^dems**`, and `**x^que.**`
* `**𝜏_dems**`: The compression rate for demonstrations according to the target overall compression rate `**𝜏**` and the pre-defined compression rate for instructions and questions, i.e., `**𝜏_ins**` and `**𝜏_que.**`
* `**D**`: This set will contain the compressed demonstrations.

The main process is as follows:

1. Calculate the compression rate of demonstrations
2. Calculate the perplexity of each demonstration in the original demonstration set using a small language model, such as GPT-2 or LLaMA.
3. Sort all demonstrations in descending order by their perplexity.
4. Iteratively select demonstration and add it to the set `**D**`.
5. After compressing the demonstrations, allocate any remaining budget to the instructions and questions.
6. Output set D after coarse-grained compression.

Through the demonstration-level process, the budget controller can retain key information during compression, effectively reducing the size of the original prompts. This method is especially appropriate for prompts containing several demonstrations.

The relevant code is in the function [control_context_budget](<https://github.com/microsoft/LLMLingua/blob/v0.2.1/llmlingua/prompt_compressor.py#L1108>).

### Iterative Token-level Prompt Compression (ITPC)

Using perplexity for prompt compression comes with an inherent limitation: the independence assumption. This assumption views each token in the prompt as independent. In other words, the probability of a token’s occurrence only depends on the preceding token and is not related to other tokens.

The problem with this assumption is that it overlooks the complex dependencies that often exist between tokens in natural language, which are vital for understanding context and preserving semantic integrity.

This oversight could lead to the loss of crucial information during the compression process. For instance, in high-ratio compression, if a token provides a key reasoning step or logical connection in the context, deciding whether to keep this token based solely on its perplexity could lead to an incomplete reasoning process.

To address this issue, LLMLingua has introduced the Iterative Token-level Prompt Compression (ITPC) algorithm. Rather than relying solely on its independent probability, this method evaluates each token’s significance more precisely during prompt compression. It does this by iteratively processing each segment in the prompt and considering each token’s conditional probability within the current context. This approach aids in better preserving the dependency between tokens.

Figure 6 shows the detailed steps of ITPC:

Figure 6: The detailed steps of ITPC algorithm. Image by author.

Through this process, the ITPC algorithm can effectively compress the length of the prompt while maintaining the integrity of the prompt semantics, thereby reducing the inference cost of the LLM.

The relevant code is in the function [iterative_compress_prompt](<https://github.com/microsoft/LLMLingua/blob/v0.2.1/llmlingua/prompt_compressor.py#L1458>).

### Instruction Tuning

Figure 4 illustrates that instruction tuning is also a crucial step in LLMLingua. Its aim is to minimize the distribution difference between the small language model, which is used for compression prompts, and the LLM.

Figure 7 shows the steps of Instruction Tuning:

Press enter or click to view image in full size

Figure 7: The steps of Instruction Tuning. Image by author.

### Code Demonstration

Let’s now start the code demonstration. First, set up the environment

```python (base) Florian:~ Florian$ conda create -n "llmlingua" python=3.11(base) Florian:~ Florian$ conda activate llmlingua(llmlingua) Florian:~ Florian$ pip install llmlingua ```

The installed version is as follows:

``` llmlingua 0.2.1 ```

The test code is as follows:

```python from llmlingua import PromptCompressorGSM8K_PROMPT = "Question: Angelo and Melanie want to plan how many hours over the next week they should study together for their test next week. They have 2 chapters of their textbook to study and 4 worksheets to memorize. They figure out that they should dedicate 3 hours to each chapter of their textbook and 1.5 hours for each worksheet. If they plan to study no more than 4 hours each day, how many days should they plan to study total over the next week if they take a 10-minute break every hour, include 3 10-minute snack breaks each day, and 30 minutes for lunch each day?
Let's think step by step
Angelo and Melanie think they should dedicate 3 hours to each of the 2 chapters, 3 hours x 2 chapters = 6 hours total.
For the worksheets they plan to dedicate 1.5 hours for each worksheet, 1.5 hours x 4 worksheets = 6 hours total.
Angelo and Melanie need to start with planning 12 hours to study, at 4 hours a day, 12 / 4 = 3 days.
However, they need to include time for breaks and lunch. Every hour they want to include a 10-minute break, so 12 total hours x 10 minutes = 120 extra minutes for breaks.
They also want to include 3 10-minute snack breaks, 3 x 10 minutes = 30 minutes.
And they want to include 30 minutes for lunch each day, so 120 minutes for breaks + 30 minutes for snack breaks + 30 minutes for lunch = 180 minutes, or 180 / 60 minutes per hour = 3 extra hours.
So Angelo and Melanie want to plan 12 hours to study + 3 hours of breaks = 15 hours total.
They want to study no more than 4 hours each day, 15 hours / 4 hours each day = 3.75
They will need to plan to study 4 days to allow for all the time they need.
The answer is 4

Question: You can buy 4 apples or 1 watermelon for the same price. You bought 36 fruits evenly split between oranges, apples and watermelons, and the price of 1 orange is $0.50. How much does 1 apple cost if your total bill was $66?
Let's think step by step
If 36 fruits were evenly split between 3 types of fruits, then I bought 36/3 = 12 units of each fruit
If 1 orange costs $0.50 then 12 oranges will cost $0.50 * 12 = $6
If my total bill was $66 and I spent $6 on oranges then I spent $66 - $6 = $60 on the other 2 fruit types.
Assuming the price of watermelon is W, and knowing that you can buy 4 apples for the same price and that the price of one apple is A, then 1W=4A
If we know we bought 12 watermelons and 12 apples for $60, then we know that $60 = 12W + 12A
Knowing that 1W=4A, then we can convert the above to $60 = 12(4A) + 12A
$60 = 48A + 12A
$60 = 60A
Then we know the price of one apple (A) is $60/60= $1
The answer is 1

Question: Susy goes to a large school with 800 students, while Sarah goes to a smaller school with only 300 students. At the start of the school year, Susy had 100 social media followers. She gained 40 new followers in the first week of the school year, half that in the second week, and half of that in the third week. Sarah only had 50 social media followers at the start of the year, but she gained 90 new followers the first week, a third of that in the second week, and a third of that in the third week. After three weeks, how many social media followers did the girl with the most total followers have?
Let's think step by step
After one week, Susy has 100+40 = 140 followers.
In the second week, Susy gains 40/2 = 20 new followers.
In the third week, Susy gains 20/2 = 10 new followers.
In total, Susy finishes the three weeks with 140+20+10 = 170 total followers.
After one week, Sarah has 50+90 = 140 followers.
After the second week, Sarah gains 90/3 = 30 followers.
After the third week, Sarah gains 30/3 = 10 followers.
So, Sarah finishes the three weeks with 140+30+10 = 180 total followers.
Thus, Sarah is the girl with the most total followers with a total of 180.
The answer is 180"llm_lingua = PromptCompressor()## Or use the phi-2 model,# llm_lingua = PromptCompressor("microsoft/phi-2")## Or use the quantation model, like TheBloke/Llama-2-7b-Chat-GPTQ, only need <8GB GPU memory.## Before that, you need to pip install optimum auto-gptq# llm_lingua = PromptCompressor("TheBloke/Llama-2-7b-Chat-GPTQ", model_config={"revision": "main"})compressed_prompt = llm_lingua.compress_prompt(GSM8K_PROMPT.split("

")[0], instruction="", question="", target_token=200)print('-' * 100)print("original:")print(GSM8K_PROMPT.split("

")[0])print('-' * 100)print("compressed_prompt:")print(compressed_prompt) ```

The default model will be downloaded the first time we run it. Alternatively, we can opt to use the quantized model. The running results are shown in Figure 8:

Press enter or click to view image in full size

Figure 8: The results from the test code for LLMLingua. Screenshot provided by author.

## LongLLMLingua

The problem with LLMLingua is that it doesn’t consider user questions during the compression process, potentially retaining irrelevant information.

[LongLLMLingua](<https://arxiv.org/pdf/2310.06839.pdf>) aims to address this problem by incorporating user questions into the compression process.

Press enter or click to view image in full size

Figure 9: Framework of LongLLMLingua. Gray Italic content: As in LLMLingua. Source: [LongLLMLingua](<https://arxiv.org/pdf/2310.06839.pdf>).

As depicted in Figure 9, LongLLMLingua proposed four new components to enhance the perception of key information in LLMs:

* Question-aware coarse-grained and fine-grained compression
* Document reordering mechanism
* Dynamic compression ratio
* Subsequence recovery algorithm

### Question-aware coarse-grained compression

LongLLMLingua proposes using the perplexity of the question `**x^que**`, conditioned on different contexts `**x^doc_k**`, to represent their association. A restrictive statement, `**x^restrict = "We can get the answer to this question in the given documents"**`, can be added after `**x^que**`. This statement strengthens the connection between `**x^que**` and `**x^doc_k**` and acts as a regularization item that reduces hallucination effects. This can be expressed as:

Press enter or click to view image in full size

Why not calculate the document-level perplexity under the condition of question `**x^que**` ? This is because the document often contains a lot of irrelevant information. Even when conditioned by `**x^que**`, the perplexity score calculated for the entire document may not be distinct enough, rendering it an inadequate measure for document-level compression.

The relevant code can be found in the function [get_distance_longllmlingua](<https://github.com/microsoft/LLMLingua/blob/v0.2.1/llmlingua/prompt_compressor.py#L1967>).

### Question-aware fine-grained compression

LongLLMLingua introduced the concept of contrastive perplexity.

Press enter or click to view image in full size

First, we calculate the perplexity of a token, not taking into account the question, represented as `**perplexity(x_i | x <i)**`. Then, we measure the perplexity again, this time including the question, represented as `**perplexity(x_i | x^que, x <i)**`. This measures the surprise of seeing all the tokens before token `**x_i**`, given the question `**x^que**`.

The goal is to determine the degree to which the surprise level of each token changes in relation to the question. If a word becomes less surprising when the question is included, it could be highly relevant to the question.

### Document reordering mechanism

As depicted in Figure 10, during inference, LLM tends to use content from the beginning and end of the prompt, while ignoring the content in the middle. This issue is known as the “Lost in the Middle” problem.

Press enter or click to view image in full size

Figure 10: LLMs’ ability to capture the relevant information depends on their positions in the prompt. To reduce information loss in the middle, we introduce a document reordering mechanism. Source: [LongLLMLingua](<https://arxiv.org/pdf/2310.06839.pdf>).

Figure 10 also illustrates that LLM performs best when relevant information is placed at the beginning. As a result, LongLLMLingua organizes the paragraphs based on the results of coarse-grained compression, arranging them in descending order of score from front to back.

Press enter or click to view image in full size

### Dynamic compression ratio

Since the key information density varies across documents, we should allocate more budget (i.e., a lower compression ratio) to documents that are more relevant to the question.

LongLLMLingua uses importance scores from coarse-grained compression to guide budget allocation during fine-grained compression.

Specially, start by setting the initial budget for the retained documents using the budget controller of LLMLingua. Then, in the fine-grained compression phase, allocate the compression budget to each document dynamically. This allocation is based on the document’s ranking index of its importance score, which is determined during the coarse-grained compression phase.

LongLLMLingua employs a linear scheduler for the adaptive allocation, the budget of each token `**xi**` can be formulated as:

Press enter or click to view image in full size

where `**Nd**` denotes the number of documents, and `**δτ**` is a hyper-parameter that controls the overall budget for dynamic allocation.

The corresponding code is can be found in function [get_dynamic_compression_ratio](<https://github.com/microsoft/LLMLingua/blob/v0.2.1/llmlingua/prompt_compressor.py#L958>).

### Subsequence recovery algorithm

As shown in Figure 11, in the fine-grained token-wise compression process, some tokens of key entities may be discarded. For example, “2009” in the original prompt may be compressed to “209”, “Wilhelm Conrad Rontgen” may be compressed to “Wilhelmgen”.

Press enter or click to view image in full size

Figure 11: The example of subsequence recovery, the red text represents the original text, and the blue text is the result. Source: [LongLLMLingua](<https://arxiv.org/pdf/2310.06839.pdf>).

LongLLMLingua proposed a subsequence recovery algorithm that can recover the original content from the responses of LLMs, as shown in Figure 12.

Press enter or click to view image in full size

Figure 12: Subsequence recovery algorithm. Source: [LongLLMLingua](<https://arxiv.org/pdf/2310.06839.pdf>).

The primary process involves the following steps:

* Traverse the token `**yl**` in the response of LLMs and select the longest substring `**y˜key,l**` that appears in the compressed prompt `**x˜**`
* Find the maximum common shortest subsequence `**xi,j**` corresponding to `**y˜key,l**` in the original prompt `**x**`
* Replace the corresponding token `**y˜key,l**` in the LLMs response with `**xi,j**`.

The corresponding code can be found in function [recover](<https://github.com/microsoft/LLMLingua/blob/v0.2.1/llmlingua/prompt_compressor.py#L1686>).

### Code Demonstration

The method for setting up the environment is the same as in LLMLingua. Here is the test code:

```python from llmlingua import PromptCompressorGSM8K_PROMPT = "Question: Angelo and Melanie want to plan how many hours over the next week they should study together for their test next week. They have 2 chapters of their textbook to study and 4 worksheets to memorize. They figure out that they should dedicate 3 hours to each chapter of their textbook and 1.5 hours for each worksheet. If they plan to study no more than 4 hours each day, how many days should they plan to study total over the next week if they take a 10-minute break every hour, include 3 10-minute snack breaks each day, and 30 minutes for lunch each day?
Let's think step by step
Angelo and Melanie think they should dedicate 3 hours to each of the 2 chapters, 3 hours x 2 chapters = 6 hours total.
For the worksheets they plan to dedicate 1.5 hours for each worksheet, 1.5 hours x 4 worksheets = 6 hours total.
Angelo and Melanie need to start with planning 12 hours to study, at 4 hours a day, 12 / 4 = 3 days.
However, they need to include time for breaks and lunch. Every hour they want to include a 10-minute break, so 12 total hours x 10 minutes = 120 extra minutes for breaks.
They also want to include 3 10-minute snack breaks, 3 x 10 minutes = 30 minutes.
And they want to include 30 minutes for lunch each day, so 120 minutes for breaks + 30 minutes for snack breaks + 30 minutes for lunch = 180 minutes, or 180 / 60 minutes per hour = 3 extra hours.
So Angelo and Melanie want to plan 12 hours to study + 3 hours of breaks = 15 hours total.
They want to study no more than 4 hours each day, 15 hours / 4 hours each day = 3.75
They will need to plan to study 4 days to allow for all the time they need.
The answer is 4

Question: You can buy 4 apples or 1 watermelon for the same price. You bought 36 fruits evenly split between oranges, apples and watermelons, and the price of 1 orange is $0.50. How much does 1 apple cost if your total bill was $66?
Let's think step by step
If 36 fruits were evenly split between 3 types of fruits, then I bought 36/3 = 12 units of each fruit
If 1 orange costs $0.50 then 12 oranges will cost $0.50 * 12 = $6
If my total bill was $66 and I spent $6 on oranges then I spent $66 - $6 = $60 on the other 2 fruit types.
Assuming the price of watermelon is W, and knowing that you can buy 4 apples for the same price and that the price of one apple is A, then 1W=4A
If we know we bought 12 watermelons and 12 apples for $60, then we know that $60 = 12W + 12A
Knowing that 1W=4A, then we can convert the above to $60 = 12(4A) + 12A
$60 = 48A + 12A
$60 = 60A
Then we know the price of one apple (A) is $60/60= $1
The answer is 1

Question: Susy goes to a large school with 800 students, while Sarah goes to a smaller school with only 300 students. At the start of the school year, Susy had 100 social media followers. She gained 40 new followers in the first week of the school year, half that in the second week, and half of that in the third week. Sarah only had 50 social media followers at the start of the year, but she gained 90 new followers the first week, a third of that in the second week, and a third of that in the third week. After three weeks, how many social media followers did the girl with the most total followers have?
Let's think step by step
After one week, Susy has 100+40 = 140 followers.
In the second week, Susy gains 40/2 = 20 new followers.
In the third week, Susy gains 20/2 = 10 new followers.
In total, Susy finishes the three weeks with 140+20+10 = 170 total followers.
After one week, Sarah has 50+90 = 140 followers.
After the second week, Sarah gains 90/3 = 30 followers.
After the third week, Sarah gains 30/3 = 10 followers.
So, Sarah finishes the three weeks with 140+30+10 = 180 total followers.
Thus, Sarah is the girl with the most total followers with a total of 180.
The answer is 180"QUESTION = "Question: Josh decides to try flipping a house. He buys a house for $80,000 and then puts in $50,000 in repairs. This increased the value of the house by 150%. How much profit did he make?"llm_lingua = PromptCompressor()compressed_prompt = llm_lingua.compress_prompt( GSM8K_PROMPT.split("

")[0], question = QUESTION, # ratio=0.55 # Set the special parameter for LongLLMLingua condition_in_question = "after_condition", reorder_context = "sort", dynamic_context_compression_ratio = 0.3, # or 0.4 condition_compare = True, context_budget = "+100", rank_method = "longllmlingua",)print('-' * 100)print("original:")print(GSM8K_PROMPT.split("

")[0])print('-' * 100)print("compressed_prompt:")print(compressed_prompt) ```

The running results are shown in Figure 13:

Press enter or click to view image in full size

Figure 13: The results from the test code for LongLLMLingua. Screenshot provided by author.

## AutoCompressor

In contrast to the previously mentioned method, [AutoCompressor](<https://arxiv.org/pdf/2305.14788.pdf>) is a soft prompt-based approach.

It smartly fine-tunes the existing model by expanding the vocabulary and utilizing “summary tokens” and “summary vectors” to condense context information.

Press enter or click to view image in full size

Figure 14: AutoCompressors process long documents by recursively generating summary vectors which are passed as soft prompts to all subsequent segments. Source: [AutoCompressor](<https://arxiv.org/pdf/2305.14788.pdf>).

Figure 14 presents the architecture of AutoCompressor, which operates in the following steps:

1. **Expand Vocabulary:** This step involves adding “summary tokens” to the model’s existing vocabulary. These tokens enable the model to condense large amounts of information into a smaller vector.
2. **Split Document:** The document to be processed is divided into small segments, each of which is appended with summary tokens. These tokens also carry the summary information of the preceding segments, creating a summary accumulation.
3. **Fine-tuning Training:** An unsupervised training method is used, leveraging the “next word prediction” task to fine-tune the model. The objective of this task is to predict the next word based on the tokens preceding the current token and the summary vectors of the segments preceding the current segment.
4. **Backpropagation:** AutoCompressor uses backpropagation through time (BPTT) and gradient checkpointing for each segment to minimize the computational graph’s size. Backpropagation is performed for the entire document, enabling the model to learn the full context’s association.

### Code

AutoCompressor provides [code](<https://github.com/princeton-nlp/AutoCompressors>), interested readers can try it.

```python import torchfrom transformers import AutoTokenizerfrom auto_compressor import LlamaAutoCompressorModel, AutoCompressorModel# Load AutoCompressor trained by compressing 6k tokens in 4 compression stepstokenizer = AutoTokenizer.from_pretrained("princeton-nlp/AutoCompressor-Llama-2-7b-6k")# Need bfloat16 + cuda to run Llama model with flash attentionmodel = LlamaAutoCompressorModel.from_pretrained("princeton-nlp/AutoCompressor-Llama-2-7b-6k", torch_dtype=torch.bfloat16).eval().cuda()prompt = 'The first name of the current US president is "'prompt_tokens = tokenizer(prompt, add_special_tokens=False, return_tensors="pt").input_ids.cuda()context = """Joe Biden, born in Scranton, Pennsylvania, on November 20, 1942, had a modest upbringing in a middle-class family. He attended the University of Delaware, where he double-majored in history and political science, graduating in 1965. Afterward, he earned his law degree from Syracuse University College of Law in 1968.
Biden's early political career began in 1970 when he was elected to the New Castle County Council in Delaware. In 1972, tragedy struck when his wife Neilia and 1-year-old daughter Naomi were killed in a car accident, and his two sons, Beau and Hunter, were injured. Despite this devastating loss, Biden chose to honor his commitment and was sworn in as a senator by his sons' hospital bedsides.
He went on to serve as the United States Senator from Delaware for six terms, from 1973 to 2009. During his time in the Senate, Biden was involved in various committees and was particularly known for his expertise in foreign affairs, serving as the chairman of the Senate Foreign Relations Committee on multiple occasions.
In 2008, Joe Biden was selected as the running mate for Barack Obama, who went on to win the presidential election. As Vice President, Biden played an integral role in the Obama administration, helping to shape policies and handling issues such as economic recovery, foreign relations, and the implementation of the Affordable Care Act (ACA), commonly known as Obamacare.
After completing two terms as Vice President, Joe Biden decided to run for the presidency in 2020. He secured the Democratic nomination and faced the incumbent President Donald Trump in the general election. Biden campaigned on a platform of unity, promising to heal the divisions in the country and tackle pressing issues, including the COVID-19 pandemic, climate change, racial justice, and economic inequality.
In the November 2020 election, Biden emerged victorious, and on January 20, 2021, he was inaugurated as the 46th President of the United States. At the age of 78, Biden became the oldest person to assume the presidency in American history.
As President, Joe Biden has worked to implement his agenda, focusing on various initiatives, such as infrastructure investment, climate action, immigration reform, and expanding access to healthcare. He has emphasized the importance of diplomacy in international relations and has sought to rebuild alliances with global partners.
Throughout his long career in public service, Joe Biden has been recognized for his commitment to bipartisanship, empathy, and his dedication to working-class issues. He continues to navigate the challenges facing the nation, striving to bring the country together and create positive change for all Americans."""context_tokens = tokenizer(context, add_special_tokens=False, return_tensors="pt").input_ids.cuda()summary_vectors = model(context_tokens, output_softprompt=True).softpromptprint(f"Compressing {context_tokens.size(1)} tokens to {summary_vectors.size(1)} summary vectors")# >>> Compressing 660 tokens to 50 summary vectorsgeneration_with_summary_vecs = model.generate(prompt_tokens, do_sample=False, softprompt=summary_vectors, max_new_tokens=12)[0]print("Generation w/ summary vectors:
" + tokenizer.decode(generation_with_summary_vecs))# >>> The first name of the current US president is "Joe" and the last name is "Biden".next_tokens_without_context = model.generate(prompt_tokens, do_sample=False, max_new_tokens=11)[0]print("Generation w/o context:
" + tokenizer.decode(next_tokens_without_context))# >>> The first name of the current US president is "Donald" and the last name is "Trump". ```

## LLMLingua-2

[LLMLingua-2](<https://arxiv.org/pdf/2403.12968.pdf>) identifies two problems with compressing prompts by deleting tokens or lexical units based on the information entropy from causal language models like LLaMa-7B:

(1) The small language model used to determine information entropy does not align with the prompt compression objective.

(2) It only utilizes unidirectional context, which may not encompass all the required information for prompt compression.

The core of these problems is that information entropy might be a sub-optimal measure for compression.

The overall architecture of LLMLingua-2 is shown in Figure 15:

Figure 15: Overview of LLMLingua-2. Source: [LLMLingua-2](<https://arxiv.org/pdf/2403.12968.pdf>).

To address issue 1, LLMLingua-2 introduces a data distillation process. This process extracts knowledge from a LLM to compress prompts without losing key information. At the same time, it constructs an extractive text compression dataset. Training on this dataset helps align small language model effectively to prompt compression.

To tackle issue 2, LLMLingua-2 treats prompt compression as a token classification problem. This approach ensures the fidelity of the compressed prompts to the original ones. It uses a transformer encoder as the underlying architecture to capture all necessary information for prompt compression from the full bidirectional context.

### How to Construct an Effective Prompt Compression Dataset

**Data Distillation**

Data distillation involves extracting knowledge from large language models, such as GPT-4, to effectively compress prompts without losing essential information.

In LLMLingua-2, instructions are carefully designed, as shown in Figure 16. These instructions require GPT-4 to compress text by omitting non-essential words from the original text without adding any new words during the generation process.

Simultaneously, the instructions do not impose a compression ratio limit. Instead, GPT-4 is prompted to compress the original text as much as possible while retaining maximum information.

Figure 16: instruction used for data distillation. Source: [LLMLingua-2](<https://arxiv.org/pdf/2403.12968.pdf>).

As illustrated in Figure 17, GPT-4 often applies a high compression ratio when handling extremely long contexts. This could be attributed to its limited capacity to handle long contexts. Such aggressive compression leads to substantial information loss, which considerably impacts the performance of subsequent tasks.

Press enter or click to view image in full size

Figure 17: Illustration of compression ratio w.r.t. original context length on MeetingBank. We use GPT-4–32k with the output token limit setting to 4096. Source: [LLMLingua-2](<https://arxiv.org/pdf/2403.12968.pdf>).

In order to alleviate this problem, LLMLingua-2 adopted a chunk compression method, dividing the long text into multiple chunks that do not exceed 512 tokens, and then guiding GPT-4 to compress each block separately.

**Data Annotation**

We have currently acquired pairs of original texts and their compressed versions through data distillation. The objective of data annotation is to assign a binary label to each token in the original text. This determines whether the token should be retained after compression.

Since GPT-4 may not adhere to instructions accurately, LLMLingua-2 employs a sliding window technique to restrict the search range. It also utilizes fuzzy matching to handle potential alterations to the original words during the compression process by GPT-4.

**Quality Control**

LLMLingua-2 uses two quality control metrics to assess the quality of compressed texts generated by GPT-4 distillation and of auto-annotated labels: Variation Rate(VR) and Alignment Gap(AG).

The Variation Rate measures the percentage of words in the compressed text that differ from the original text. The Alignment Gap assesses the quality of auto-annotated labels.

Using these measures, LLMLingua-2 can exclude low-quality samples, ensuring the dataset’s quality.

### Compressor

**Viewed as a Binary Classification Problem**

Initially, the prompt compression problem can be transformed into a binary classification problem. The basic concept is to consider each lexical unit as an independent entity and assign it a label, either “preserve” or “discard”. This approach preserves the integrity of the compressed prompt’s content while simplifying the model’s design.

**Model Architecture**

A transformer encoder-based feature encoder is used and a linear classification layer is added on top.

This architecture can capture the bidirectional context information of each lexical unit, providing essential information for the compression task.

**Compression Strategy**

The compression strategy for the original prompt `**x**` is a three-step process. The target compression ratio is `**1/τ**`, where `**τ**` is defined as the quotient of the number of words in the compressed prompt and the original prompt `**x**`.

* First, we determine the target number of tokens to keep in the compressed prompt `**x˜**`: `**N˜ = τN**`.
* Then, we use the token classification model to predict the probability `**pi**` of each word `**xi**` being marked as `**‘preserve’**`.
* Lastly, we keep the top `**N˜**` words with the highest `**pi**` values from the original prompt `**x**`, retaining their original order to form the compressed prompt `**x˜**`.

### Code

From the above, it is clear that the primary work of LLMLingua-2 involves constructing the compressor. So, how can we use the compressor once acquired?

Please refer to the code below(the method for setting up the environment is the same as in LLMLingua). The main internal process can be seen in the function [compress_prompt_llmlingua2](<https://github.com/microsoft/LLMLingua/blob/v0.2.1/llmlingua/prompt_compressor.py#L661>).

```python from llmlingua import PromptCompressorPROMPT = "John: So, um, I've been thinking about the project, you know, and I believe we need to, uh, make some changes. I mean, we want the project to succeed, right? So, like, I think we should consider maybe revising the timeline.

Sarah: I totally agree, John. I mean, we have to be realistic, you know. The timeline is, like, too tight. You know what I mean? We should definitely extend it."llm_lingua = PromptCompressor( model_name = "microsoft/llmlingua-2-xlm-roberta-large-meetingbank", use_llmlingua2 = True,)compressed_prompt = llm_lingua.compress_prompt(PROMPT, rate=0.33, force_tokens = ['
', '?'])## Or use LLMLingua-2-small model# llm_lingua = PromptCompressor(# model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",# use_llmlingua2=True,# )print('-' * 100)print("original:")print(PROMPT)print('-' * 100)print("compressed_prompt:")print(compressed_prompt) ```

The running results are shown in Figure 18:

Press enter or click to view image in full size

Figure 18: The results from the test code for LLMLingua-2. Screenshot provided by author.

## RECOMP

[RECOMP](<https://arxiv.org/pdf/2310.04408.pdf>) introduces two types of trained compressors: extractive and abstractive. The extractive compressor selects useful sentences from retrieved documents, while the abstractive compressor combines information from multiple documents to generate summaries.

Figure 19 shows the position of the compressor in RECOMP.

Press enter or click to view image in full size

Figure 19: The architecture of RECOMP. Source: [RECOMP](<https://arxiv.org/pdf/2310.04408.pdf>).

### Extractive Compressor

Given `**n**` sentences `**[s1, s2, …, sn]**` in the input document set, we train a dual encoder model. This model embeds sentence `**si**` and the input sequence `**x**` into fixed-dimensional embeddings. The inner product of these embeddings indicates the benefit for the LLM of adding si to the input x to generate the target output sequence.

The final summary `**s**` from the compressor consists of the top `**N**` sentences, ranked by their inner product with the input.

### Abstractive Compressor

Abstractive compressor is an encoder-decoder model. It takes the concatenation of the input sequence `**x**` and the retrieved set of documents and outputs a summary `**s**`.

The approach involves generating a training dataset using a LLM(like GPT-3), filtering this data, and then training an encoder-decoder model with the filtered dataset.

### Code

Since [the code of RECOMP](<https://github.com/carriex/recomp>) is currently in its early stages, it will not be demonstrated here. Interested readers can try it out.

## Conclusion

This article introduces the method of prompt compression, including method classification, algorithm principles, and code explanation.

Among the methods discussed, LongLLMLingua may be a superior choice. We have already implemented it in our research project. If I discover any flaws of LongLLMLingua or identify better methods, I will update this article. In addition, LLMLingua-2 can also be tried, it has advantages in speed and memory usage.

If you’re interested in RAG technologies, feel free to check out my other articles.

[ ![Florian June](https://miro.medium.com/v2/resize:fill:40:40/1*DmQ3DH2JeAJquvhT_tjVCw.jpeg) ](<https://medium.com/@florian_algo?source=post_page-----95a589f7b554--------------------------------------->)

[Florian June](<https://medium.com/@florian_algo?source=post_page-----95a589f7b554--------------------------------------->)

## RAG

[View list](<https://medium.com/@florian_algo/list/rag-1b65363c06db?source=post_page-----95a589f7b554--------------------------------------->)

106 stories

![](https://miro.medium.com/v2/resize:fill:388:388/0*0qcWMcyxgAEksKxH.png)

![](https://miro.medium.com/v2/resize:fill:388:388/0*d5IGGHnoIIWBcRtu.png)

![](https://miro.medium.com/v2/resize:fill:388:388/0*KzyYE7oQLMS889mV.png)

**And the latest article or video can be found in**[**my newsletter**](<https://florianjune.substack.com/>)**or on**[**YouTube**](<https://www.youtube.com/@ai_exploration_journey>).

Finally, if there are any errors or omissions in this article, or if you have any questions, please point them out in the comment section.
