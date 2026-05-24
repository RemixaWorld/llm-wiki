---
domain: medium.com
fetch_date: '2026-05-18T12:53:18.233501'
status: ok
url: https://medium.com/@faseehahmed2606/is-your-llm-actually-working-the-essential-metrics-for-every-use-case-with-code-0711d19dc72e
---

# Is Your LLM Actually Working? The Essential Metrics for Every Use Case (with Code!)

[ ![Mohammad Faseeh Ahmed](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*_GCQjpPUZPlNFYN1) ](</@faseehahmed2606?source=post_page---byline--0711d19dc72e--------------------------------------->)

[Mohammad Faseeh Ahmed](</@faseehahmed2606?source=post_page---byline--0711d19dc72e--------------------------------------->)

23 min read

·

Mar 21, 2025

\--

\--

Listen

Share

More

Large Language Models (LLMs) have demonstrated remarkable capabilities across a wide spectrum of natural language processing tasks, which lead to their widespread adoption in various applications. From powering chatbots and generating creative content to summarizing lengthy documents and translating languages, LLMs are rapidly transforming how we interact with and leverage textual data. As these models become increasingly integrated into our daily lives and critical systems, the need for robust and comprehensive evaluation methodologies becomes paramount. Assessing the performance of LLMs is crucial not only for understanding their strengths and limitations but also for ensuring their reliability, safety, and alignment with intended use cases. This report provides an enhanced overview of common LLM use cases and delves into the standard evaluation metrics employed to assess their effectiveness in each domain.

![Photo by Bernd 📷 Dittrich on Unsplash](https://miro.medium.com/v2/resize:fit:700/0*k_OiOdhSNccLyckx)

## Common Use Cases of Large Language Models

LLMs are versatile tools capable of performing numerous language-related tasks. Their ability to understand, interpret, and generate human-like text has made them invaluable across various industries. Some of the most prevalent applications include:

### 1\. Content Creation and Writing Assistance

LLMs excel at generating articles, blog posts, marketing copy, and even creative content like poetry and screenplays, aiding writers with brainstorming, drafting, and editing. Tools like Grammarly and Notion AI showcase the power of LLMs in enhancing writing quality and efficiency.

### 2\. Sentiment Analysis and Market Research

Organizations use LLMs to understand the emotions conveyed in text data, such as customer feedback on social media or product reviews. This information is valuable for identifying areas of improvement and gauging public opinion.

### 3\. Content Moderation

LLMs can automatically detect and filter out offensive or inappropriate content on social media platforms, ensuring safer online environments.

### 4\. Classification and Pattern Recognition

The ability of LLMs to classify text is leveraged in tasks like fraud detection and supply chain management, where they can identify suspicious patterns and analyze market trends.

### 5\. Domain-Specific Applications

In healthcare and legal sectors, LLMs are being explored for analyzing clinical notes, legal documents, and research papers, assisting professionals with tasks like summarization, information extraction, and document review.

### 6\. Code Generation

LLMs are increasingly used in assisting developers with code completion, bug fixing, and even helping to sharpen development skills through automated feedback and suggestions.

### 7\. Language Translation

LLMs like Meta AI’s SeamlessM4T have achieved impressive accuracy in translating across multiple languages, even in real-time voice conversations. This capability is crucial for businesses aiming to expand their global reach and improve cross-cultural communication.

### 8\. Conversational AI and Customer Support

The development of chatbots and virtual assistants that can handle customer inquiries, provide recommendations, and troubleshoot issues in real-time. These conversational agents, exemplified by systems like Salesforce Einstein and Amazon’s Alexa, leverage LLMs to engage in natural conversations and perform tasks ranging from setting alarms to automating customer support.

## Evaluating the Classifiers

> Measuring Classification Accuracy

Text classification, the task of assigning predefined categories or labels to text documents, is a fundamental use case for LLMs. Evaluating the performance of LLMs in this area requires metrics that assess the accuracy and reliability of these assignments. Several standard evaluation metrics are commonly employed:

> **Accuracy:** Measures the overall correctness of the model’s predictions, calculated as the ratio of correctly classified instances (both true positives and true negatives) to the total number of instances. While intuitive, accuracy can be misleading on imbalanced datasets.
>
> **Precision:** Focuses on the accuracy of positive predictions, measuring the proportion of true positives out of all instances predicted as positive. High precision indicates that the model is good at avoiding false positives.
>
> **Recall (Sensitivity):** Measures the model’s ability to identify all actual positive instances, calculated as the ratio of true positives to the total number of actual positives. High recall signifies that the model is effective at avoiding false negatives.
>
> **F1-score:** Provides a balanced measure by calculating the harmonic mean of precision and recall, proving particularly useful when both metrics are important.
>
> **Confusion Matrix:** An invaluable tool that visualizes the counts of true positives, true negatives, false positives, and false negatives, allowing for a detailed analysis of the types of errors the model is making.

```python from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix# Example true and predicted labelsy_true = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]y_pred = [0, 1, 0, 0, 0, 1, 1, 1, 0, 1]# Calculate accuracyaccuracy = accuracy_score(y_true, y_pred)print(f"Accuracy: {accuracy}")# Calculate precisionprecision = precision_score(y_true, y_pred)print(f"Precision: {precision}")# Calculate recallrecall = recall_score(y_true, y_pred)print(f"Recall: {recall}")# Calculate F1-scoref1 = f1_score(y_true, y_pred)print(f"F1-score: {f1}")# Generate confusion matrixconf_matrix = confusion_matrix(y_true, y_pred)print(f"Confusion Matrix:
{conf_matrix}") ```

For multi-class classification problems, these metrics can be calculated using different averaging methods:

* **Macro averaging** : Calculates the metric for each class independently and then takes the average (treating all classes equally)
* **Micro averaging** : Aggregates the contributions of all classes to compute the average metric (giving more weight to larger classes)
* **Weighted averaging** : Similar to macro averaging, but calculates the average weighted by the number of true instances for each class

```python # For multi-class classificationfrom sklearn.metrics import precision_recall_fscore_support# Compute precision, recall, and F1 with different averaging methodsmacro_metrics = precision_recall_fscore_support(y_true, y_pred, average='macro')micro_metrics = precision_recall_fscore_support(y_true, y_pred, average='micro')weighted_metrics = precision_recall_fscore_support(y_true, y_pred, average='weighted')print(f"Macro metrics (precision, recall, F1): {macro_metrics[:3]}")print(f"Micro metrics (precision, recall, F1): {micro_metrics[:3]}")print(f"Weighted metrics (precision, recall, F1): {weighted_metrics[:3]}") ```

## ROC and AUC

For binary classification, we can also use the Receiver Operating Characteristic (ROC) curve, it plots the true positive rate against the false positive rate at various threshold settings. The Area Under the ROC Curve (AUC) provides a single scalar value that indicates the model's ability to distinguish between classes.

```python from sklearn.metrics import roc_curve, aucimport matplotlib.pyplot as plt# For probability predictionsy_score = [0.1, 0.9, 0.2, 0.3, 0.1, 0.8, 0.6, 0.9, 0.2, 0.7] # Example probability scores# Calculate ROC curve and AUCfpr, tpr, thresholds = roc_curve(y_true, y_score)roc_auc = auc(fpr, tpr)# Plot ROC curveplt.figure()plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')plt.xlim([0.0, 1.0])plt.ylim([0.0, 1.05])plt.xlabel('False Positive Rate')plt.ylabel('True Positive Rate')plt.title('Receiver Operating Characteristic')plt.legend(loc="lower right")plt.show() ```

## Assessing the Summarizers

> Measuring Information Condensation

Text summarization, where LLMs condense longer texts into shorter, coherent summaries, presents its own set of evaluation challenges. Unlike classification, there isn't always a single "correct" summary, and the quality often depends on the context and purpose of the summarization. Several metrics have been developed to assess the quality of generated summaries:

### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)

ROUGE evaluates summarization quality by measuring the overlap of n-grams between the generated summary and one or more human-written reference summaries. Different variations include:

* **ROUGE-N** : Measures the overlap of unigrams, bigrams, etc.
* **ROUGE-L** : Focuses on the longest common subsequence
* **ROUGE-S** : Considers skip-bigrams, allowing for gaps between words

```python from rouge_score import rouge_scorer# Example reference and candidate summariesreference_summary = "The cat was under the bed."candidate_summary = "The cat was found under the bed."# Initialize ROUGE scorerscorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)# Calculate ROUGE scoresscores = scorer.score(reference_summary, candidate_summary)print("ROUGE Scores:", scores) ```

## BLEU (Bilingual Evaluation Understudy)

Originally designed for machine translation, **BLEU measures the n-gram overlap between the generated text and reference text.** It is a **precision-focused metric** that assesses how much of the words in the machine-generated summary appear in the human reference summaries.

```python from nltk.translate.bleu_score import sentence_bleufrom nltk.tokenize import word_tokenize# Example reference and candidate summariesreference_summary = "The cat is on the mat."candidate_summary = "The cat is sitting on the mat."# Tokenize the summariesreference_tokens = [word_tokenize(reference_summary)]candidate_tokens = word_tokenize(candidate_summary)# Calculate BLEU scorebleu_score = sentence_bleu(reference_tokens, candidate_tokens)print("BLEU Score:", bleu_score) ```

## METEOR (Metric for Evaluation of Translation with Explicit ORdering)

Similar to ROUGE but incorporates additional features like stemming and synonymy matching using resources like WordNet.**It focuses on unigram matching and calculates a weighted F-score, giving more weight to recall than precision.** METEOR also includes a **fragmentation penalty** for poorly ordered phrases.

```python from nltk.translate.meteor_score import meteor_scorefrom nltk.tokenize import word_tokenize# Example reference and candidate summariesreference_summary = "The cat is on the mat."candidate_summary = "The cat is sitting on the mat."# Tokenize the summariesreference_tokens = word_tokenize(reference_summary)candidate_tokens = word_tokenize(candidate_summary)# Calculate METEOR scoremeteor = meteor_score([reference_tokens], candidate_tokens)print("METEOR Score:", meteor) ```

## BERTScore

BERTScore leverages the contextual embeddings from the BERT model to **evaluate the semantic similarity between a generated summary and a reference summary.** **By comparing the embeddings of words in both summaries, BERTScore can capture semantic similarities that might be missed by traditional n-gram overlap metrics.**

```python from bert_score import score# Example reference and candidate summariesreference_summary = "The cat is on the mat."candidate_summary = "The cat is sitting on the mat."# Calculate BERTScoreP, R, F1 = score([candidate_summary], [reference_summary], lang="en")print(f"BERTScore - Precision: {P.item():.4f}, Recall: {R.item():.4f}, F1 Score: {F1.item():.4f}") ```

## SUPERT (SUmmarization PERformance with Transformers)

A reference-free evaluation metric that uses pre-trained contextual representations **to assess the quality of summarization without requiring human-written reference summaries.** It **measures how well the summary captures the salient information in the source document.**

```python # Example of how SUPERT could be implementedfrom transformers import AutoTokenizer, AutoModelimport torchimport numpy as npdef get_embeddings(text, model, tokenizer): inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512) with torch.no_grad(): outputs = model(**inputs) return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()def supert_score(source_doc, summary, model_name="bert-base-uncased"): tokenizer = AutoTokenizer.from_pretrained(model_name) model = AutoModel.from_pretrained(model_name) # Get embeddings doc_embedding = get_embeddings(source_doc, model, tokenizer) summary_embedding = get_embeddings(summary, model, tokenizer) # Calculate cosine similarity similarity = np.dot(doc_embedding, summary_embedding) / (np.linalg.norm(doc_embedding) * np.linalg.norm(summary_embedding)) return similarity# Example usagesource_document = "The cat quickly jumped over the lazy dog. It was a sunny day and the dog was sleeping peacefully in the garden."summary = "The cat jumped over the sleeping dog on a sunny day."score = supert_score(source_document, summary)print(f"SUPERT Score: {score:.4f}") ```

## Judging the Generators

> Navigating the Nuances of Creative Text

Evaluating the performance of LLMs in creative text generation poses unique challenges due to the open-ended and subjective nature of such tasks. Several evaluation approaches are employed:

## Perplexity

Perplexity is a measure that tells us how “surprised” or **uncertain** a language model is when predicting the next word in a text. Imagine you’re reading a story and at each word, you have several choices about what might come next. **Perplexity quantifies the average number of choices the model effectively considers** , so lower perplexity means the model is more confident and accurate in its predictions.

This metric was introduced because, as language models grew more complex and started assigning probabilities to thousands of possible words, comparing **raw probabilities became difficult**. Perplexity simplifies this by turning the model’s uncertainty into a single number: **the lower the number, the better the model is at capturing the language’s structure and predicting what comes next.**

```python from transformers import AutoModelForCausalLM, AutoTokenizerimport torch# Example text and modeltext = "The quick brown fox jumps over the lazy dog."model_name = "gpt2"tokenizer = AutoTokenizer.from_pretrained(model_name)model = AutoModelForCausalLM.from_pretrained(model_name)model.eval()# Tokenize the textinput_ids = tokenizer.encode(text, return_tensors="pt")# Get model outputswith torch.no_grad(): outputs = model(input_ids, labels=input_ids)# Calculate perplexityloss = outputs.lossperplexity = torch.exp(loss)print(f"Perplexity: {perplexity.item()}") ```

## Diversity Metrics

Diversity metrics measure **how varied and original the generated text is**. One common metric, distinct‑n, calculates the percentage of unique sequences of words (called n‑grams) compared to all sequences in the text. In simple terms, if a model **keeps repeating** the same phrases, its distinct‑n score will be low; if it uses a wide range of different phrases, the score will be high. This helps us understand whether the generated content feels fresh and creative or if it’s just repetitive.

```python def distinct_n_grams(text, n): """Calculate the ratio of unique n-grams to total n-grams in the text.""" tokens = text.split() if len(tokens) < n: return 0.0 n_grams = [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)] n_grams_set = set(n_grams) return len(n_grams_set) / len(n_grams)# Example usagegenerated_text = "The cat sat on the mat. The dog sat on the log. The frog sat on the bog."distinct_1 = distinct_n_grams(generated_text, 1) # Distinct-1 (words)distinct_2 = distinct_n_grams(generated_text, 2) # Distinct-2 (bigrams)print(f"Distinct-1: {distinct_1:.4f}")print(f"Distinct-2: {distinct_2:.4f}") ```

## Self-BLEU

Self-BLEU is a measure of diversity for a set of generated texts. It works by comparing each text with all the others using the BLEU score, a metric that shows how similar two texts are. A lower Self-BLEU score means the texts are more different from each other, indicating greater diversity and originality.

```python from nltk.translate.bleu_score import sentence_bleufrom nltk.tokenize import word_tokenizedef self_bleu(generated_texts): """Calculate the average BLEU score of each text against all others.""" if len(generated_texts) < 2: return 0.0 bleu_scores = [] for i, text in enumerate(generated_texts): reference_texts = [t for j, t in enumerate(generated_texts) if j != i] reference_tokens = [word_tokenize(ref) for ref in reference_texts] candidate_tokens = word_tokenize(text) bleu = sentence_bleu(reference_tokens, candidate_tokens) bleu_scores.append(bleu) return sum(bleu_scores) / len(bleu_scores)# Example usagegenerated_texts = [ "The cat sat on the mat.", "The dog chased the ball in the park.", "The bird flew over the mountain."]self_bleu_score = self_bleu(generated_texts)print(f"Self-BLEU Score: {self_bleu_score:.4f}") ```

for this example you will get a self-bleu as 0 as each text example used here is different. I have added additional examples in the [colab book](<https://colab.research.google.com/drive/1Qqxaa6f_itHVC__HlOX_Zy0aDI1YsFYZ?usp=sharing>)

## Human Evaluation

Given the subjective nature of creative text, human evaluation often plays a crucial role in assessing the quality of LLM-generated content. Human evaluators can assess various aspects such as fluency, coherence, relevance to the prompt, factual consistency (if applicable), and the overall quality and engagingness of the generated text.

## Evaluating Code Generation

> Comprehensive Assessment Framework

Code generation has emerged as a significant application of LLMs, with models like GitHub Copilot and OpenAI's Codex demonstrating impressive capabilities. Evaluating code generation requires metrics that assess not only syntactic correctness but also functional accuracy and code quality.

## Functional Correctness: Pass@k

The Pass@k metric measures the probability that at least one of the top k generated code samples passes a set of predefined unit tests. This is a widely used metric for evaluating code generation models, as it directly assesses whether the generated code accomplishes its intended functionality.

```python def compute_pass_at_k(n_samples, n_correct, k): """ Compute Pass@k metric where: - n_samples: Number of samples per problem - n_correct: Number of correct samples per problem - k: The k in Pass@k """ if n_samples < k: return 1.0 if n_correct > 0 else 0.0 return 1.0 - math.comb(n_samples - n_correct, k) / math.comb(n_samples, k)# Example: For a problem where we generate 10 solutions and 3 are correctn_samples = 10n_correct = 3pass_at_1 = compute_pass_at_k(n_samples, n_correct, 1)pass_at_5 = compute_pass_at_k(n_samples, n_correct, 5)pass_at_10 = compute_pass_at_k(n_samples, n_correct, 10)print(f"Pass@1: {pass_at_1:.4f}")print(f"Pass@5: {pass_at_5:.4f}")print(f"Pass@10: {pass_at_10:.4f}") ```

## HumanEval Benchmark

The HumanEval benchmark, developed by OpenAI, has become a standard for evaluating code generation models. It consists of 164 Python programming problems that test a model's ability to generate functionally correct code from natural language descriptions.

```python import randomdef evaluate_humaneval_solution(problem_id, generated_code): """ Simulate the evaluation of a generated code solution for a HumanEval problem. In a production system, this function would: 1. Retrieve the specific HumanEval problem and its test cases. 2. Execute the generated code safely (e.g., in a sandbox). 3. Run the test cases and record which ones pass. For this simulation, we assume there are 5 test cases per problem and randomly determine if each test case passes. The overall solution is considered correct only if all test cases pass. """ # Simulate running 5 test cases; True indicates the test passed, False indicates a failure. test_case_results = [random.choice([True, False]) for _ in range(5)] # Overall, the solution "passes" if all test cases pass. solution_passes = all(test_case_results) # Return a dictionary with evaluation details. return { "problem_id": problem_id, "test_case_results": test_case_results, "passes": solution_passes }# Example usageproblem_id = "HumanEval/42"generated_code = """def add(a, b): # A simple function that returns the sum of a and b return a + b"""result = evaluate_humaneval_solution(problem_id, generated_code)print(f"Evaluation for Problem {result['problem_id']}:")print("Test Case Results:", result['test_case_results'])print("Overall Result:", "Passed" if result['passes'] else "Failed") ```

## CodeBLEU

CodeBLEU extends the traditional BLEU metric by incorporating syntactic and semantic information specific to code. It consists of four components:

1. **N-gram Match** : Similar to traditional BLEU, measuring lexical similarity
2. **Weighted N-gram Match** : Gives higher weights to keywords and identifiers
3. **Syntactic AST Match** : Compares the Abstract Syntax Tree structures
4. **Semantic Data-flow Match** : Evaluates the semantic correctness based on data flow.

```python def calculate_codebleu(reference_code, candidate_code, weights=[0.25, 0.25, 0.25, 0.25]): """ Calculate CodeBLEU score with four components: 1. N-gram match (similar to BLEU) 2. Weighted n-gram match (emphasizing keywords) 3. AST match 4. Data-flow match This is a simplified implementation - actual CodeBLEU would use more complex analysis. """ from nltk.translate.bleu_score import sentence_bleu from nltk.tokenize import word_tokenize import ast # 1. N-gram match (simplified BLEU) ref_tokens = word_tokenize(reference_code) cand_tokens = word_tokenize(candidate_code) ngram_match = sentence_bleu([ref_tokens], cand_tokens) # 2. Weighted n-gram match (simulation) # In actual implementation, this would weight keywords more heavily weighted_ngram = ngram_match * 1.2 # Simplified simulation # 3. AST match (simplified) try: ref_ast = ast.parse(reference_code) cand_ast = ast.parse(candidate_code) # Simple AST comparison (in reality, this would be more complex) ast_match = 0.7 # Simulated value except SyntaxError: ast_match = 0.0 # If code has syntax errors # 4. Data-flow match (simulation) # This would require actual data-flow analysis dataflow_match = 0.65 # Simulated value # Combine components using weights codebleu = (weights[0] * ngram_match + weights[1] * weighted_ngram + weights[2] * ast_match + weights[3] * dataflow_match) return codebleu# Example usagereference_code = """def factorial(n): if n == 0 or n == 1: return 1 else: return n * factorial(n-1)"""candidate_code = """def factorial(n): result = 1 for i in range(1, n+1): result *= i return result"""codebleu_score = calculate_codebleu(reference_code, candidate_code)print(f"CodeBLEU Score: {codebleu_score:.4f}") ```

## Execution Time and Efficiency

Beyond correctness, the efficiency of the generated code is another important aspect to evaluate, especially for performance-critical applications.

```python import timeimport statisticsdef measure_execution_time(code_func, test_cases, runs=5): """Measure the execution time of a function across multiple test cases and runs.""" all_times = [] for test_case in test_cases: case_times = [] for _ in range(runs): start_time = time.time() code_func(*test_case) end_time = time.time() case_times.append(end_time - start_time) # Take the median to reduce the impact of outliers all_times.append(statistics.median(case_times)) return { "mean": statistics.mean(all_times), "median": statistics.median(all_times), "min": min(all_times), "max": max(all_times) }# Example recursive factorial functiondef factorial_recursive(n): if n == 0 or n == 1: return 1 else: return n * factorial_recursive(n-1)# Example iterative factorial functiondef factorial_iterative(n): result = 1 for i in range(1, n+1): result *= i return result# Test casestest_cases = [(5,), (10,), (15,), (20,)]# Measure execution timesrecursive_times = measure_execution_time(factorial_recursive, test_cases)iterative_times = measure_execution_time(factorial_iterative, test_cases)print("Recursive Factorial Execution Times (seconds):")for key, value in recursive_times.items(): print(f" {key}: {value:.6f}")print("
Iterative Factorial Execution Times (seconds):")for key, value in iterative_times.items(): print(f" {key}: {value:.6f}") ```

## Code Complexity Metrics

Evaluating the complexity of generated code provides insights into its maintainability and readability.

```python import astimport mathdef calculate_cyclomatic_complexity(code): """ Calculate the cyclomatic complexity of Python code. A higher score indicates more complex code. """ class ComplexityVisitor(ast.NodeVisitor): def __init__(self): self.complexity = 1 # Start with 1 for the entry point def visit_If(self, node): self.complexity += 1 self.generic_visit(node) def visit_For(self, node): self.complexity += 1 self.generic_visit(node) def visit_While(self, node): self.complexity += 1 self.generic_visit(node) def visit_Try(self, node): self.complexity += len(node.handlers) # Count except blocks self.generic_visit(node) def visit_BoolOp(self, node): if isinstance(node.op, ast.And) or isinstance(node.op, ast.Or): self.complexity += len(node.values) - 1 self.generic_visit(node) try: tree = ast.parse(code) visitor = ComplexityVisitor() visitor.visit(tree) return visitor.complexity except SyntaxError: return math.inf # Return infinity for code with syntax errors# Example usagecode1 = """def simple_function(x): return x + 1"""code2 = """def complex_function(x): if x > 0: if x < 10: return x * 2 else: for i in range(x): if i % 2 == 0: print(i) return x * 3 else: try: return 10 / x except ZeroDivisionError: return 0"""cc1 = calculate_cyclomatic_complexity(code1)cc2 = calculate_cyclomatic_complexity(code2)print(f"Simple function cyclomatic complexity: {cc1}")print(f"Complex function cyclomatic complexity: {cc2}") ```

## Real-world Code Generation Evaluation Results

Here are some representative results from recent evaluations of code generation models:

### HumanEval Benchmark Results

![image](https://miro.medium.com/v2/resize:fit:620/1*Z1I93orhXoCEGCGrqAGA1Q.png)

### CodeXGLUE Benchmark (Python Generation Task)

![image](https://miro.medium.com/v2/resize:fit:572/1*SrhvnHNDtZbzdc7zYVXUfA.png)

These results highlight the rapid progress in code generation capabilities, with newer models achieving significantly higher functional correctness and code quality metrics compared to earlier versions.

## Evaluating Other LLM Applications: Tailored Approaches

Beyond classification, summarization, generation, and code generation, LLMs are applied to a variety of other tasks, each requiring specific evaluation metrics tailored to the nuances of the use case.

## Question Answering (QA)

The goal is to provide accurate answers to user-posed questions. Common evaluation metrics include:

* **Exact Match (EM)** : Measures the percentage of predicted answers that perfectly match the ground truth answer
* **F1-score** : Calculates the overlap between the predicted and the ground truth answer at the word level
* **SQuAD metrics** : Specifically designed for the Stanford Question Answering Dataset, measuring both exact match and F1-score for reading comprehension tasks

```python def calculate_qa_metrics(predicted_answers, ground_truth_answers): """ Calculate Exact Match and F1 score for QA tasks. Args: predicted_answers: List of predicted answers ground_truth_answers: List of lists of ground truth answers (multiple acceptable answers per question) Returns: Dictionary with EM and F1 scores """ exact_match = 0 f1_scores = [] for pred, truths in zip(predicted_answers, ground_truth_answers): # Normalize answers pred = normalize_answer(pred) truths = [normalize_answer(truth) for truth in truths] # Check for exact match if pred in truths: exact_match += 1 # Calculate F1 score (best match among the ground truths) best_f1 = 0 for truth in truths: current_f1 = calculate_f1(pred, truth) best_f1 = max(best_f1, current_f1) f1_scores.append(best_f1) return { "exact_match": exact_match / len(predicted_answers) * 100, "f1": sum(f1_scores) / len(f1_scores) * 100 }def normalize_answer(text): """Normalize answer by removing articles, punctuation, and extra whitespace.""" import re import string # Remove articles text = re.sub(r'\b(a|an|the)\b', ' ', text.lower()) # Remove punctuation text = ''.join(ch for ch in text if ch not in string.punctuation) # Normalize whitespace text = ' '.join(text.split()) return textdef calculate_f1(prediction, truth): """Calculate F1 score between prediction and ground truth.""" prediction_tokens = prediction.split() truth_tokens = truth.split() # Empty answers if len(prediction_tokens) == 0 or len(truth_tokens) == 0: return int(prediction_tokens == truth_tokens) # Count common tokens common = sum(1 for token in prediction_tokens if token in truth_tokens) # If no common tokens, F1 = 0 if common == 0: return 0 precision = common / len(prediction_tokens) recall = common / len(truth_tokens) f1 = 2 * precision * recall / (precision + recall) return f1# Example usagepredicted_answers = ["new york city", "albert einstein", "42 kilometers"]ground_truth_answers = [ ["New York City", "NYC", "New York"], ["Albert Einstein", "Einstein"], ["42 km", "42 kilometers", "forty-two kilometers"]]qa_metrics = calculate_qa_metrics(predicted_answers, ground_truth_answers)print(f"QA Metrics:")print(f" Exact Match: {qa_metrics['exact_match']:.2f}%")print(f" F1 Score: {qa_metrics['f1']:.2f}%") ```

## Dialogue Generation

For conversational agents, evaluation is complex due to the interactive and context-dependent nature of dialogues. Key metrics include:

* **BLEU, ROUGE, METEOR** : Basic measures of word overlap with reference responses
* **Distinct-n** : Assesses the diversity of the generated responses by measuring the proportion of unique n-grams
* **USR (UnSupervised and Reference-free)** : Evaluates without requiring reference dialogues
* **Response Length** : Measures the verbosity of the model's responses
* **Perplexity** : Measures how well the model predicts the next token in a conversation.

```python def evaluate_dialogue(generated_responses, reference_responses, dialogue_contexts): """ Comprehensive evaluation of dialogue generation. Args: generated_responses: List of model-generated responses reference_responses: List of human/reference responses dialogue_contexts: List of dialogue contexts preceding the responses Returns: Dictionary with various dialogue evaluation metrics """ from nltk.translate.bleu_score import sentence_bleu from nltk.tokenize import word_tokenize results = { "bleu_scores": [], "distinctness": { "distinct-1": [], "distinct-2": [] }, "response_lengths": [], "context_relevance": [] } for gen, ref, context in zip(generated_responses, reference_responses, dialogue_contexts): # Tokenize gen_tokens = word_tokenize(gen.lower()) ref_tokens = word_tokenize(ref.lower()) context_tokens = word_tokenize(context.lower()) # BLEU score bleu = sentence_bleu([ref_tokens], gen_tokens) results["bleu_scores"].append(bleu) # Distinctness results["distinctness"]["distinct-1"].append(len(set(gen_tokens)) / max(1, len(gen_tokens))) bigrams = [' '.join(gen_tokens[i:i+2]) for i in range(len(gen_tokens)-1)] results["distinctness"]["distinct-2"].append(len(set(bigrams)) / max(1, len(bigrams))) # Response length results["response_lengths"].append(len(gen_tokens)) # Simple context relevance (word overlap with context) common_words = len(set(gen_tokens) & set(context_tokens)) relevance = common_words / max(1, len(set(gen_tokens))) results["context_relevance"].append(relevance) # Aggregate results for key in results: if isinstance(results[key], list): results[key] = sum(results[key]) / len(results[key]) elif isinstance(results[key], dict): for subkey in results[key]: results[key][subkey] = sum(results[key][subkey]) / len(results[key][subkey]) return results# Example usagecontexts = [ "Hello, how are you doing today?", "Can you recommend a good restaurant in the area?", "What's the weather forecast for tomorrow?"]generated_responses = [ "I'm doing well, thank you for asking!", "There are several great options nearby. I recommend trying Bella Italia on Main Street.", "Tomorrow will be sunny with a high of 75 degrees."]reference_responses = [ "I'm fine, thanks! How about you?", "You should check out Luigi's Pizza downtown. It's fantastic!", "Tomorrow will be clear with temperatures around 73-76 degrees."]dialogue_metrics = evaluate_dialogue(generated_responses, reference_responses, contexts)print("Dialogue Evaluation Metrics:")for key, value in dialogue_metrics.items(): if isinstance(value, dict): print(f" {key}:") for subkey, subvalue in value.items(): print(f" {subkey}: {subvalue:.4f}") else: print(f" {key}: {value:.4f}") ```

## Translation

The task of converting text from one language to another. Key metrics include:

* **BLEU** : Measures the n-gram precision of the machine-translated text compared to human references
* **NIST** : Similar to BLEU but gives more weight to rarer, more informative n-grams
* **TER (Translation Edit Rate)** : Measures the number of edits required to transform the machine translation output into a reference translation
* **chrF** : Character-level F-score that captures sub-word information
* **COMET** : A neural metric that uses contextualized embeddings to evaluate translation quality.

```python def evaluate_translation(source_texts, translations, references): """ Evaluate machine translation quality using multiple metrics. Args: source_texts: List of source language texts translations: List of machine-translated texts references: List of human reference translations Returns: Dictionary with various translation metrics """ from nltk.translate.bleu_score import corpus_bleu from nltk.tokenize import word_tokenize # Tokenize all texts tokenized_translations = [word_tokenize(t.lower()) for t in translations] tokenized_references = [[word_tokenize(r.lower())] for r in references] # Calculate corpus BLEU bleu_score = corpus_bleu(tokenized_references, tokenized_translations) # Calculate character-based metrics (simplified chrF implementation) def char_precision_recall_f1(hyp, ref): hyp_chars = list(hyp.lower()) ref_chars = list(ref.lower()) common_chars = sum(1 for c in hyp_chars if c in ref_chars) precision = common_chars / max(1, len(hyp_chars)) recall = common_chars / max(1, len(ref_chars)) if precision + recall == 0: return 0 f1 = 2 * precision * recall / (precision + recall) return f1 chrf_scores = [char_precision_recall_f1(t, r) for t, r in zip(translations, references)] avg_chrf = sum(chrf_scores) / len(chrf_scores) # Calculate Translation Edit Rate (simplified version) def calculate_ter(hyp, ref): # Using Levenshtein distance as a simple approximation import Levenshtein hyp_tokens = word_tokenize(hyp.lower()) ref_tokens = word_tokenize(ref.lower()) edit_distance = Levenshtein.distance(hyp_tokens, ref_tokens) return edit_distance / max(1, len(ref_tokens)) ter_scores = [calculate_ter(t, r) for t, r in zip(translations, references)] avg_ter = sum(ter_scores) / len(ter_scores) return { "bleu": bleu_score * 100, # Convert to percentage "chrf": avg_chrf * 100, # Convert to percentage "ter": avg_ter * 100 # Convert to percentage (lower is better) }# Example usagesource_texts = [ "Das Wetter ist heute schön.", "Ich liebe Programmierung.", "Die Katze schläft auf dem Sofa."]translations = [ "The weather is nice today.", "I love programming.", "The cat is sleeping on the couch."]references = [ "The weather is beautiful today.", "I love programming.", "The cat is sleeping on the sofa."]translation_metrics = evaluate_translation(source_texts, translations, references)print("Translation Evaluation Metrics:")for metric, score in translation_metrics.items(): print(f" {metric}: {score:.2f}%") ```

## Integrated Evaluation Frameworks and Benchmarks

Integrated evaluation frameworks and benchmarks provide a standardized way to assess the performance of large language models (LLMs) across a wide range of tasks, ensuring fair comparisons between models. Here’s an overview of some of the key frameworks and emerging evaluation approaches

## GLUE and SuperGLUE

* **GLUE (General Language Understanding Evaluation):**
GLUE is a benchmark composed of multiple natural language understanding tasks, such as sentiment analysis, textual entailment, and question answering. It was designed to assess how well a model can understand and process natural language by providing a single score that aggregates performance across these diverse tasks.
* **SuperGLUE:**
As a successor to GLUE, SuperGLUE is even more challenging, incorporating tasks that require deeper reasoning and more nuanced language understanding. It pushes models to perform better on tasks like commonsense reasoning and complex inference, thus serving as a tougher yardstick for state-of-the-art models.

## MMLU (Massive Multitask Language Understanding)

MMLU is a comprehensive benchmark that evaluates a model’s knowledge across 57 different subjects spanning humanities, STEM, social sciences, and more. It is designed to test both the breadth and depth of a model’s understanding:

* **Breadth:** Measures the model’s ability to handle a wide variety of topics.
* **Depth:** Assesses how well the model understands complex or specialized content within each subject area.

## LLM-as-a-Judge

This is an emerging approach where one LLM is used to evaluate the outputs of another. Instead of relying solely on traditional metrics (like BLEU or ROUGE), this method leverages the language understanding and reasoning capabilities of an LLM to provide more nuanced, human-like judgments. Key aspects include:

* **Complex Distinction Based Assessments:** The evaluating LLM can consider multiple facets such as coherence, factual accuracy, creativity, and relevance.
* **Reference-Free Evaluation:** This method can assess outputs even without a fixed reference, which is particularly useful for open-ended or creative tasks where there isn’t a single “correct” answer.
* **Breadth:** Measures the model’s ability to handle a wide variety of topics.
* **Depth:** Assesses how well the model understands complex or specialized content within each subject area.

## LLM-as-a-Judge

This is an emerging approach where one LLM is used to evaluate the outputs of another. Instead of relying solely on traditional metrics (like BLEU or ROUGE), this method leverages the language understanding and reasoning capabilities of an LLM to provide more nuanced, human-like judgments. Key aspects include:

* **Nuanced Assessments:** The evaluating LLM can consider multiple facets such as coherence, factual accuracy, creativity, and relevance.
* **Reference-Free Evaluation:** This method can assess outputs even without a fixed reference, which is particularly useful for open-ended or creative tasks where there isn’t a single “correct” answer.

## Navigating the Pitfalls

> Challenges and Best Practices in LLM Evaluation

### Evaluating LLMs effectively is fraught with challenges. Key considerations include:

## Subjectivity and Human Judgment

One significant hurdle is the inherent subjectivity in assessing the quality of certain LLM outputs, particularly in creative and open-ended tasks. Human judgment, while often considered the gold standard, can vary between evaluators, making it difficult to establish a universally agreed-upon "good" output.

## Dataset Selection and Bias

The choice of evaluation datasets is critical. Metrics can provide misleading results if tested on datasets that are not diverse or representative of the real-world scenarios in which the LLM will be deployed. It is essential to use datasets that cover a wide range of inputs and expected outputs to ensure a robust evaluation.

## Metric Selection and Combination

Relying on a single metric can provide an incomplete picture of an LLM's performance. Different metrics capture different aspects of quality, and the most appropriate metrics depend on the specific goals and requirements of the application. A comprehensive evaluation strategy often involves combining multiple complementary metrics.

## Human-AI Collaborative Evaluation

Given the limitations of automated metrics, especially for nuanced and subjective aspects of language, human evaluation remains a vital component of a comprehensive evaluation strategy. Human evaluators can assess qualities like creativity, coherence, engagingness, and overall real-world usefulness, which automated metrics often struggle to capture. To ensure consistency and reduce bias in human evaluations, it is crucial to establish clear evaluation protocols and guidelines for the evaluators.

## The Future of LLM Evaluation: Emerging Trends and Directions

The field of LLM evaluation is continuously evolving, driven by the rapid advancements in LLM capabilities. Future trends point towards:

## Context-Aware and Human-Aligned Metrics

Development of more context-aware and human-aligned metrics that can go beyond simple surface-level comparisons. There is a growing focus on developing metrics that can effectively evaluate coherence, consistency, relevance, and factual accuracy.

## LLMs as Evaluators

One significant trend is the increasing use of LLMs themselves as evaluators. These LLM-based evaluation methods leverage the language understanding capabilities of large models to assess the quality of other LLM outputs. Examples include G-Eval and CPDScore, which use large language models to provide human-like evaluations of generated text.

## Reference-Free Evaluation

The rise of reference-free evaluation methods, which do not rely on human-annotated reference texts, is addressing the limitations of traditional reference-based metrics, especially for open-ended generation tasks.

## Standardized Benchmarks

The development of more robust benchmarks and standardized evaluation frameworks is crucial for facilitating fair comparisons across different LLMs. Standardized benchmarks allow researchers and practitioners to objectively assess the progress of different models on common tasks.

## Evaluating Broader Implications

There is a growing recognition of the importance of evaluating broader aspects of LLMs beyond just accuracy and fluency, such as fairness, bias, safety, and ethical implications. As LLMs become more powerful and integrated into society, ensuring that they are developed and deployed responsibly requires careful evaluation of these critical dimensions.

## Conclusion

> Towards Robust and Meaningful LLM Assessment

Evaluating large language models (LLMs) is complex due to their diverse applications, such as text classification, summarization, creative generation, question answering, dialogue systems, code generation, and translation. Each task requires specific evaluation methods and careful selection of metrics, often combining automated tools with human judgment.

Relying on just one metric isn’t enough — multiple measures are essential for fully understanding an LLM’s strengths and limitations. Evaluation should also use diverse, representative datasets to capture real-world scenarios accurately.

Looking forward, LLM evaluation will become more sophisticated, with approaches like using LLMs themselves as evaluators and developing metrics that don’t rely solely on reference outputs. Additionally, there’s a growing focus on assessing ethical aspects, including fairness, safety, and societal impact.

Ultimately, the responsible development of LLMs will depend on a balanced mix of traditional metrics, advanced neural-based assessments, and human insights, ensuring these powerful tools benefit society effectively and safely.

## References

## [Google ColabEdit descriptioncolab.research.google.com](<https://colab.research.google.com/drive/1Qqxaa6f_itHVC__HlOX_Zy0aDI1YsFYZ?usp=sharing&source=post_page-----0711d19dc72e--------------------------------------->)

## [Evaluation metricsEvaluating the performance of machine learning models is crucial for determining their effectiveness and reliability…learn.microsoft.com](<https://learn.microsoft.com/en-us/ai/playbook/technology-guidance/generative-ai/working-with-llms/evaluation/list-of-eval-metrics?source=post_page-----0711d19dc72e--------------------------------------->)

## [Performance metrics for evaluating generated codeI'm just learning about techniques such as ROUGE and BLEU for evaluating trained models. I'm interested in training a…community.deeplearning.ai](<https://community.deeplearning.ai/t/performance-metrics-for-evaluating-generated-code/692965/3?source=post_page-----0711d19dc72e--------------------------------------->)

## [Custom text classification evaluation metrics - Azure AI servicesLearn about evaluation metrics in custom text classification.learn.microsoft.com](<https://learn.microsoft.com/en-us/azure/ai-services/language-service/custom-text-classification/concepts/evaluation-metrics?source=post_page-----0711d19dc72e--------------------------------------->)

## [Evaluating NLP Models for Text Classification and Summarization Tasks in the Financial Landscape…Unlock the power of advanced NLP models for precise text classification and summarization in the financial landscape…www.indium.tech](<https://www.indium.tech/blog/evaluating-nlp-models-financial-analysis-part-2/?source=post_page-----0711d19dc72e--------------------------------------->)

## [Evaluate the text summarization capabilities of LLMs for enhanced decision-making on AWS | Amazon…Organizations across industries are using automatic text summarization to more efficiently handle vast amounts of…aws.amazon.com](<https://aws.amazon.com/blogs/machine-learning/evaluate-the-text-summarization-capabilities-of-llms-for-enhanced-decision-making-on-aws/?source=post_page-----0711d19dc72e--------------------------------------->)
