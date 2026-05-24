---
domain: pub.towardsai.net
fetch_date: '2026-05-18T12:50:16.998053'
status: ok
url: https://pub.towardsai.net/dspy-venture-into-automatic-prompt-optimization-d37b892091be
---

# DSPy: Venture Into Automatic Prompt Optimization 🚀

[ ![Serj Smorodinsky](https://miro.medium.com/v2/resize:fill:64:64/1*dufHERTN3rAAoYjcyB0CsA.jpeg) ](<https://serj-smor.medium.com/?source=post_page---byline--d37b892091be--------------------------------------->)

[Serj Smorodinsky](<https://serj-smor.medium.com/?source=post_page---byline--d37b892091be--------------------------------------->)

9 min read

·

Nov 20, 2024

\--

Listen

Share

More

Drop prompt engineering and enjoy a free afternoon

This is part #2 of my DSPy series — check it out first [installment](<https://medium.com/towards-artificial-intelligence/dspy-machine-learning-attitude-towards-llm-prompting-0d45056fd9b7>) as a refresher.

Watch the video for a summary of all of the code sections:

You can watch the video for all of the code parts

[Link to the full notebook](<https://github.com/SerjSmor/open-intent-classifier/blob/main/notebooks/dspy_training.ipynb>)

## Why am I writing this?

DSPy documentation and all online of the tutorials are great.
But most of them cover the same pre-defined examples (HotPotQA).

And you know what happens — when you try to bring DSPy to life with your own custom dataset, suddenly most resources are useless, because they are trivial. You get errors everywhere and you’re out there by yourself.

Well not anymore — Hacking AI (my handle) got your back!

## Content

There are two essential parts in machine learning which is sometimes forgotten in the context of LLM prompting:
1\. Training the model
2\. Given new input infer model output

In the previous article I focused on the second part, inferring outputs and DSPy niceties around it:
Defining signatures, running predictions, inspecting history, everything you need to replace string based prompt with DSPy objects.

In this instalment we focus on the first part: follow the library’s premise of actually optimizing the prompt automatically by providing examples. Reminds you of something? That’s right! Supervised learning, the bread and butter of machine learning.

Yet another meme master piece, no, you can’t have it

### Content

1. What are we optimizing?
2. Getting to know the dataset
3. The missing piece of most tutorials — DSPy.Example
4. Running prompt optimization — code breakdown
5. Saving loading the best prompt

Let’s go 🚀 🚀 🚀

## What are we optimizing?

Let’s get formal for a second. Usually during the optimization of a model whether it is a neural network or other algorithms we change parameter /weight values to minimize a loss function. For example changing a CNN weight’s to decrease the cross-entropy between the expected labels and the predicted labels.

If you’re working with a close LLM such as OpenAI’s GPTs Anthropic’s Claude, you don’t have access to the weights so you can’t optimize them.

Nonetheless DSPy treats the prompt and the few shot examples as the parameters, and lets you define your loss function (or a proxy of it). Genius!

On itself, this was possible and was done before across many teams and individuals, but at the cost of a lot of custom work and eyeballing.
With DSPy you can erase all of this manual code and start working productively, just as you would with computation graph frameworks (PyTorch, Keras, Tensorflow).

For those of you who are angsty and want to see a snippet before going deeper:

```python from dspy.teleprompt import LabeledFewShotfew_shot_demos = random.sample(train_examples, k=10)labeled_fewshot_optimizer = LabeledFewShot(k=len(few_shot_demos))few_shot_model = labeled_fewshot_optimizer.compile(student=cot_predictor, trainset=few_shot_demos) ```

There are additional steps needed, but don’t worry about it, we will break down the code and explain in the next sections.

The basic I will cover flow:
1\. defining a classifier
2\. pulling dataset and parsing the labels
3\. creating optimizers
4\. running evaluation
5\. saving the best prompt

## Getting to know the dataset

ATIS is my go to dataset for everything classification.

The **ATIS** (**Airline Travel Information Systems**) is a dataset consisting of audio recordings and corresponding manual transcripts about humans asking for flight information on automated airline travel inquiry systems. The data consists of 17 unique intent categories. The original split contains 4478, 500 and 893 intent-labeled reference utterances in train, development and test set respectively [(source)](<https://paperswithcode.com/dataset/atis>).

Here’s an example of a row:

Press enter or click to view image in full size

‘text’ is the X and ‘intent’ is the y

We are going to create an LLM based classifier to classify the rows into one of the dataset’s labels.

Loading the dataset:

``` dataset = load_dataset("tuetschek/atis")dataset.set_format(type="pandas")df_train: pd.DataFrame = dataset["train"][:]df_test: pd.DataFrame = dataset["test"][:]small_test = df_test.head(100) ```

## Defining the classifier

```python import dspy import randomimport pandas as pdfrom datasets import load_datasetclass Classification(dspy.Signature): """Classify the customer message into one of the intent labels. The output should be only the predicted class as a single intent label.""" customer_message = dspy.InputField(desc="Customer message during customer service interaction") intent_labels = dspy.InputField(desc="Labels that represent customer intent") answer = dspy.OutputField(desc="a label best matching customer's intent ")lm_mini = dspy.OpenAI(model='gpt-4o-mini')dspy.settings.configure(lm=lm_mini)cot_predictor = dspy.ChainOfThought(Classification) ```

If you’re not sure what these parts mean — you can revisit the [introductory blog](<https://medium.com/towards-artificial-intelligence/dspy-machine-learning-attitude-towards-llm-prompting-0d45056fd9b7>).

`cot_predictor` is the basic classifier without any optimizations on top of it, we will treat it as our baseline.

## The missing piece of most tutorials — DSPy.Example

In order to optimize the prompt we need to show DSPy some examples.
But DSPy is picky, it will accept only examples that are derived from the DSPy.Example base class. This fact is known only to few known monks and I have been the chosen one to pass this message.

That person is you and that piece is DSPy.Example class ```python # we want k examples per class def get_dspy_examples(df, k) -> dspy.example: dspy_examples = [] for label in labels: try: label_df = df[df["intent"] == label].sample(n=k) for index, row in label_df.iterrows(): dspy_examples.append( dspy.Example(customer_message=row["text"], answer=row["intent"], intent_labels=labels_str).with_inputs("customer_message", "intent_labels") ) except: # there are classes that don't have any representatives continue return dspy_examplestrain_examples = get_dspy_examples(df_train, k=2)all_test_examples = get_dspy_examples(df_test, k=10)print(len(all_test_examples), len(all_test_examples) // 2)dev_examples = random.sample(all_test_examples, len(all_test_examples) // 2) ```

Given a dataframe I sample K examples per class. Why?
Because if I would have sampled without the class constraint I wouldn’t have representative examples for all classes but the major ones.

## Running prompt optimization — code breakdown

This is the biggest promise of DSPy, optimizing the prompt automatically given known labels.

What is the alternative? Eyeballing results, write custom evaluation code, hard code prompts and so forth.

Press enter or click to view image in full size

What DSPy can help us optimize?
1\. Prompt instructions
2\. Peeking the best few shot examples for in context learning
3\. Directly changing LLM weights (out of scope)

DSPy treats your prompt as the parameters you change during optimization, changing 1. and 2.

It gives you different optimization options, some are very light weight and some take some customization and run time.

In this blog we will focus on few shot example optimizers (2.).
For a quick intro to prompt instruction optimization you can look at the documentation of the [COPRO](<https://dspy.ai/deep-dive/optimizers/copro/>) optimizer.

## Optmizers

An optimizer in DSPy is responsible on building the best prompt given examples.

### LabeledFewShot optimizer

This is the most basic optimizer, it helps you build a prompt with few shot examples leveraging in context learning. The number of examples to be sampled from the training set is determined by `k` .

The compilation process doesn’t optimize anything, it just builds the prompt.

```python from dspy.teleprompt import LabeledFewShotfew_shot_demos = random.sample(train_examples, k=10)labeled_fewshot_optimizer = LabeledFewShot(k=len(few_shot_demos))few_shot_model = labeled_fewshot_optimizer.compile(student=cot_predictor, trainset=few_shot_demos) ```

Lets see what is the resulting prompt

``` example = test_examples[0]# without inputs(), we won't inject the inputs of the examplepred = few_shot_model(**example.inputs())# Produce a prediction from our `cot` module, using the `example` above as input.lm_mini.inspect_history(n=1) ```

Press enter or click to view image in full size

So many words that you didn’t have to write!

### BootstrapFewShot optimizer

Bootstrap optimizer will lend a hand for creating additional labeled examples if you’re short on annotated data.

You can specify the amount of synthetic/generated examples you would try.
Warning: generating examples is a risky endeavour, prefer your own labeled data if you have.

When using this optimizer it’s preferred to specify a metric in order to help the optimizer to optimize against a goal.
Because we are dealing with classification, my metric is an exact match.
I want the classifier to generate the same label as the labelled example.

```python # define the metricfrom dspy.evaluate import answer_exact_match as metric# define the optimizerfrom dspy.teleprompt import BootstrapFewShotoptimizer = BootstrapFewShot( metric=metric, max_bootstrapped_demos=10, max_labeled_demos=10, max_rounds=10,)# reuse the DSPy.Examples we already defined cot_few_shot_optimized = optimizer.compile(cot_predictor, trainset=train_examples) ```

How is it implemented behind the scenes?
DSPy uses a student teacher concept. The teacher is responsible for choosing the examples (demos in DSPy lingo) and the temperature and then the student is responsible for predicting by utilizing the examples.

We will only keep the examples that the led the student to the correct answer.

### BootstrapFewShotWithRandomSearch optimizer

Here’s the most complex optimizer out of the 3.

Press enter or click to view image in full size

The optimizer with the most Oompf so far. The “chosen” one metric. [SRC](<https://www.slashfilm.com/917171/the-matrixs-original-bullet-time-method-was-a-little-too-risky-to-work/>)

The BootstrapFewShotWithRandomSearch (this name just rolls on your tongue doesn’t it?), picks a different seed each time and randomly samples the few shot example.

Then it evaluates the prompt, producing a score.
We keep the score from each round (or a program in DSPy lingo) and then choose the best program, saving the final prompt.

```python from dspy.teleprompt import BootstrapFewShotWithRandomSearchoptimizer = BootstrapFewShotWithRandomSearch( metric=metric, max_bootstrapped_demos=10, max_labeled_demos=10, num_threads=10, num_candidate_programs=5)cot_few_shot_rs_optimized = optimizer.compile(cot_predictor, trainset=train_examples) ```

This takes the longest to optimize as well.

After defining the different optimizers and the baseline model, lets run the evaluation 🏃🏃🏃

## Evaluation

I view evaluation as a complex procedure, especially with a framework I don’t have the sufficient experience with.

That’s why I start with evaluating a single example.

### Single Evaluation

```python from dspy.evaluate import answer_exact_match# Instantiate the metric.metric = answer_exact_matchexample = test_examples[0]# Produce a prediction from our `cot` module, using the `example` above as input.print(example)pred = cot_predictor(**example.inputs())print(pred)# Compute the metric score for the prediction.score = metric(example, pred)print(f"Customer message: \t {example.customer_message}
")print(f"Gold Response: \t {example.answer}
")print(f"Predicted Response: \t {pred.answer}
")print(f"Exact match score: {score:.2f}") ```

Evaluation example

Press enter or click to view image in full size

Look mom we got 100% match score!

Ok, after we figured out the format, we can proceed to bulk evaluation, evaluating different optimizers on multiple examples.

### Bulk evaluation definition

Adding num_threads will decrease the computation by several magnitudes so I highly recommend using it. You define the evaluation once and then reuse it with different models/optimizers.

Similarly to how you would evaluate models with PyTorch HuggingFace etc.

```python from dspy.evaluate.evaluate import Evaluate# Set up the `evaluate_atis` function. We'll use this many times below.print(len(train_examples))evaluate_atis = Evaluate(devset=test_examples, num_threads=8, display_progress=True, display_table=5, provide_traceback=True) ```

### Evaluation results … 🥁🥁🥁

I know you’re all tense so lets find out the evaluation ranking!

BootstrapFewShotRandomSearch #1 with 95% match

Press enter or click to view image in full size

#1 place

CoT baseline and bootstrapFewShot are sharing the #2 place with 88% match

Press enter or click to view image in full size

#2 place

Press enter or click to view image in full size

#2 place

And for the last standing we have the FewShotLabeled with 78% match

Press enter or click to view image in full size

### Disclamer

You should take these results with a grain of salt. The ATIS dataset is highly imbalanced with over representation of the “flight” class. Hence, the sampling of the training and evaluation datasets highly skew the results.

I do find that the best optimizer — BootstrappedFewShotRandomSearch — is intuitive due to its optimization process, by resampling the examples few times you can compensate for the imbalanced nature of the dataset.

## Saving loading the best prompt

Given that you have optimized your prompt, now you want to persist it, deploy it, load it in production and start serving your new amazing use case.

But where is the actual prompt, how do you get it from the DSPy Optimizer/Model abstraction? Easy!

### Save

``` cot_predictor.save("cot_zero_shot.json")few_shot_model.save("cot_few_shot.json")cot_few_shot_optimized.save("cot_boostraped_few_shot.json")cot_few_shot_rs_optimized.save("cot_bootstraped_rs_few_shot.json") ```

### Load

``` cot_predictor.load("cot_zero_shot.json")few_shot_model.load("cot_few_shot.json")cot_few_shot_optimized.load("cot_boostraped_few_shot.json")cot_few_shot_rs_optimized.load("cot_bootstraped_rs_few_shot.json") ```

And that’s it! You’re ready for action 💪

## Summary

We have covered the main steps for DSPy prompt optimization.
I’m really hooked on this alternative and I find that I can’t continue with the custom code solution I have built so far, maybe that is something that you can relate to.

DSPy is only one tool, there are many others as well. The main takeaway is the methodology, the abstractions that help us drive results with higher quality and develop experience.

I have tried to build the most comprehensive tutorial on the subject through utilizing the source code of the library, in the spirit of Hacking AI, bottom’s up understanding.

## Links

If you want to chat with me or support me by liking and sharing (if you found it likeable and shareable) here are the links:

* You can start a conversation with me over my [Hacking AI Discord](<https://discord.gg/BMZk6gYucz>)
* Hop over to [LinkedIn page](<https://www.linkedin.com/company/hacking-ai/>) to get updates
* Or subscribe to [Youtube channel](<https://www.youtube.com/@hacking_ai688>) we have a lot more coming
* Or just follow me on [Twitch](<https://www.twitch.tv/hacking_ai>) if you loved my memes
