---
domain: medium.com
fetch_date: '2026-05-18T12:52:12.205480'
status: ok
url: https://medium.com/dsaid-govtech/byog-build-your-own-guardrails-with-synthetic-data-f38f9da2deae
---

# BYOG (Build Your Own Guardrails) with Synthetic Data

[ ![Shing Yee](https://miro.medium.com/v2/resize:fill:64:64/1*_txmFtApQBxrAmKgzuDGAA@2x.jpeg) ](</@shingurding?source=post_page---byline--f38f9da2deae--------------------------------------->)

[Shing Yee](</@shingurding?source=post_page---byline--f38f9da2deae--------------------------------------->)

7 min read

·

Dec 9, 2024

\--

\--

Listen

Share

More

_By Chan Shing Yee and Gabriel Chua_

_Over this past year, we’ve explored how we_[ _think about LLM guardrails here at GovTech_](</dsaid-govtech/building-responsible-ai-why-guardrails-matter-b66e1d635d71>) _, how to_[ _get started integrating them_](</dsaid-govtech/from-risk-to-resilience-adding-llm-guardrails-from-day-1-4c55e9cd6693>) _, and how we_[ _trained our own localised content moderator_](</dsaid-govtech/building-lionguard-a-contextualised-moderation-classifier-to-tackle-local-unsafe-content-8f68c8f13179>) _. In our next two posts, we’ll dive into our latest_[ _research paper_](<https://arxiv.org/abs/2411.12946>) _where we leverage synthetic data to train guardrails in pre-production, and how we applied this framework to train an off-topic prompt guardrail._

As Large Language Models (LLMs) become increasingly popular, one challenge has been ensuring LLM-powered applications don’t go off-topic when users prompt these models with queries or requests that fall outside of their intended purpose. While such prompts may not be harmful or illegal, they can lead to inefficiencies and errors, undermining the model’s effectiveness. For example, if a chatbot designed for customer service in a telecommunications company is asked for medical advice, it constitutes off-topic misuse. This can result in poor user experiences and compliance risks.

![A real-world example where the user asked a car dealership chatbot to compose a song, which is far outside its intended scope (https://venturebeat.com/ai/a-chevy-for-1-car-dealer-chatbots-show-perils-of-ai-for-customer-service/)](https://miro.medium.com/v2/resize:fit:700/1*xhSV97ovocYtanZW-iS9xw.png)

Additionally, after surveying the landscape of guardrail frameworks, another challenge we identified in adopting guardrails is that we typically have little to no real-world data in pre-production to train or configure such guardrails. Some approaches require [positive or negative examples](<https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-denied-topics.html>), or the training of [custom classifiers for each use-case](<https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/custom-categories?tabs=standard>).

At GovTech, we’ve arrived at a methodology to train LLM guardrails using LLM themselves to provide the synthetic data. We’ll deep dive into this methodology and how we applied it to the off-topic prompt detection problem in the next two posts. In this first part, we’ll explore the challenge of developing such guardrails in pre-production, when we typically have little to no real-world data to train or configure them. We’ll then explain how we used synthetic data to create a realistic and diverse dataset. In the second part, we’ll dive deeper into how we trained our model and share the results of our work. These two posts are based on our [paper](<https://arxiv.org/abs/2411.12946>).

## The Off-Topic Prompt Detection Problem

Our goal was to build an input guardrail that could determine whether a user prompt is on- or off-topic based on the system’s intended purpose. We decided to use the **system prompt** as the reference point for this classification. System prompts are predefined instructions that guide how the LLM should respond to a user’s query. They typically specify the task, provide context, and define the desired response style. This becomes a binary classification problem: **0 = on-topic, 1 = off-topic**.

Implementing such input filters ensures that only relevant, on-topic prompts get through, protecting the system from unintended misuse.

## Challenges in Pre-Production

Building effective guardrails is complex, especially when working with limited real-world data during early development stages. User data that could be used for training classifiers is often unavailable since the application has not yet been deployed. Moreover, relying on curated examples for training can be limiting, as these may not capture the wide variety of potential off-topic prompts that could arise in practice.

In existing solutions, examples are often required to train guardrails. These examples help the model identify off-topic prompts by teaching it what kinds of queries should be avoided. However, a major challenge is that it’s impossible to anticipate every off-topic prompt a user might generate. Attempting to create a list of off-topic topics is problematic because the number of possible off-topic prompts is likely endless. This method also runs the risk of **over-blocking** — where the system mistakenly flags a valid prompt as off-topic, resulting in false positives for users.

## Using Synthetic Data

Given these challenges, we decided to use **synthetic data** to build our guardrails. Synthetic data is artificial data generated by a model rather than collected from real users. It’s an ideal solution when real-world data is scarce or unavailable, as it allows us to quickly generate large amounts of relevant training data while ensuring privacy. Synthetic data can be tailored to include specific scenarios we want to cover, making it a great resource for training systems to detect off-topic prompts.

Using synthetic data also allowed us to simulate a wide variety of prompts, including edge cases and unusual scenarios that we might not have encountered in real-world data.

## Guardrail Development Methdology

![Our Guardrail Development Methodology](https://miro.medium.com/v2/resize:fit:700/0*uRDSL2hPpDoqzBdr)

Overall, our method avoids the need for real-world misuse examples. Instead, we:

1. Define the problem space qualitatively
2. Use an LLM to generate synthetic misuse prompts
3. Train and test guardrails on this dataset

![Example of on- and off-topic user prompts: The goal is to correctly classify if a prompt is off-topic or not, with respect to the system prompt](https://miro.medium.com/v2/resize:fit:700/1*E9ddxKPPpr56b41P5IVVxA.png)

## **Steps for Dataset Creation**

### **1\. Problem Analysis and Edge Case Identification**

We began by analysing the model’s intended functionality and identifying potential misuse scenarios. For instance, a customer service chatbot for a telecom company should handle inquiries about products but reject prompts related to medical or legal advice. Defining what qualifies as acceptable versus off-topic prompts was crucial for creating a boundary between what the system should process and what it should block.

Next, we curated a list of real-world system prompt examples to guide the LLM in generating realistic and effective system prompts within our synthetic dataset. This approach ensures that our synthetic data closely aligns with real-world applications, enhancing the model’s ability to produce accurate and contextually relevant responses across various scenarios.

### **2\. Generating Synthetic Data with LLMs**

With these scenarios in mind, we used a LLM, specifically GPT-4o, to generate a wide range of synthetic prompts. The idea was to produce diverse and realistic examples that include both on-topic and off-topic queries.

To introduce variability and increase the diversity of the generated prompts, we set high-temperature* values (temperature=1) for the generation process. This high temperature encourages the LLM to generate more unpredictable, diverse, and creative prompts that better reflect real-world user behaviour.

Additionally, we used the Python [Faker](<https://faker.readthedocs.io/en/master/>) library to randomise word lengths and generate 10 random seed words. The random word lengths helped vary the length of the outputs, while the randomly generated words were injected into the system prompts. This further increased the randomness and diversity of the prompts, allowing for a broader range of scenarios to be covered in the synthetic dataset.

> ***Temperature** is a parameter that can be adjusted to influence the LLM’s output. A higher temperature (e.g., 1) will result in more creative outputs while a lower temperature (e.g., 0) will result in a more predictable output.

### **3\. Structuring the Outputs**

To ensure that the generated outputs were both diverse and structured, we used constrained generation methods, such as enforcing specific formatting rules, to ensure the outputs adhered to desired structures while remaining realistic.

**OpenAI’s**[**Structured Outputs**](<https://platform.openai.com/docs/guides/structured-outputs>) feature was used to ensure that the system prompts, along with their corresponding on-topic and off-topic user queries, were generated in the correct format from the start. This feature allows us to set specific rules for how the outputs should be organiSed, ensuring that each example follows a consistent structure, such as using a JSON schema. By integrating this feature, we ensured consistency in the dataset, improving overall quality and usefulness.

​​Since we needed to generate a large amount of data quickly, we used **OpenAI’s**[**Batch API**](<https://platform.openai.com/docs/guides/batch/overview?lang=curl>) to send multiple requests at once. This enabled us to batch several tasks together, allowing the model to handle many requests simultaneously, thus speeding up the data generation process. As a result, we were able to efficiently produce a large volume of data while ensuring it remained consistent and aligned with our objectives.

Using the approach outlined above, we successfully generated **over two million pairs** of system prompts and user prompts.

The following images illustrate the overall workflow of how we used GPT-4 to create our synthetic data and the tokens utilised in generating over two million samples.

![Overall workflow on how we used GPT 4o to create our synthetic data](https://miro.medium.com/v2/resize:fit:700/1*vAxmLGk06Z-7MPoRaHT0qA.png) ![Tokens used to generate over 2 million samples](https://miro.medium.com/v2/resize:fit:700/0*VpO4ltV1YsxYsVoP)

## Conclusion

By combining problem analysis, synthetic data generation, and structured output creation, we established a scalable and flexible framework for building off-topic guardrails in LLM applications. This approach enabled us to overcome the challenges of pre-production development by generating diverse, privacy-preserving data and ensuring the guardrails could effectively filter out off-topic prompts. You can read more about this framework in our paper [here](<https://arxiv.org/abs/2411.12946>).

For further details about how we generated synthetic data, please refer to this [article](<https://gabrielchua.me/posts/generating-synthetic-data/>). You may also find the open-source dataset [here](<https://huggingface.co/datasets/gabrielchua/off-topic>).

In [**Part 2**](</dsaid-govtech/open-sourcing-an-off-topic-prompt-guardrail-fde422a66152>), we will dive deeper into how we used this synthetic dataset to train our off-topic detection model and share the results of that process.
