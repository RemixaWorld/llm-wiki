---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:54:48.561255'
status: ok
url: https://levelup.gitconnected.com/how-to-protect-your-llm-apps-using-guardrails-1fcdeeae370e
---

# How to Protect Your LLM Apps Using Guardrails?

## A complete pragmatic guide to using Guardrails in your application with implementation examples.

[ ![Vivedha Elango](https://miro.medium.com/v2/resize:fill:64:64/1*LY6uKptbPhQEMIMUCqmsBg.jpeg) ](<https://medium.com/@vivedhaelango?source=post_page---byline--1fcdeeae370e--------------------------------------->)

[Vivedha Elango](<https://medium.com/@vivedhaelango?source=post_page---byline--1fcdeeae370e--------------------------------------->)

22 min read

·

Jun 4, 2025

\--

Listen

Share

More

Press enter or click to view image in full size

Photo by [Oyemike Princewill](<https://unsplash.com/@supaslim?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>) on [Unsplash](<https://unsplash.com/photos/a-person-holding-a-padlock-in-front-of-a-window-Ns0gH5EeYs4?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash>)

LLM apps are popping up everywhere, from healthcare chatbots to customer support and everything in between. They’re smart, quick to develop, and can hold surprisingly human-like conversations. No matter how carefully you design your application, whether your apps help with medical questions or just book appointments, someone will try to get it to write code, give legal advice, or even tell a joke about quantum physics.

And sometimes, that’s fine. It can be fun to see what an AI says about unrelated topics. But when you’re running a serious business, things aren’t always that simple. What happens if a chatbot meant for health advice suddenly starts answering questions about tax law? Or if someone tricks it into sharing something risky or off-brand? Now we’ve got a problem, not just for user trust, but also for compliance, safety, and even your bottom line.

This is why every LLM-powered app needs some sort of guardrail, a way to keep conversations on-topic and safe.

In this blog post, I will try to give you a pragmatic guide to LLM Guardrails and how to use them in your application.

### Table of contents:

1. What Are LLM Guardrails?
2. Why Do We Need Guardrails for LLM?

3\. Types of LLM Guardrails

4\. How would Guardrails be integrated with your LLM Apps?

5\. Techniques used by AI Guardrail to protect LLM Applications

6\. Top LLM Guardrails framework or tools:

6.1 Proprietary LLM Guardrails: AWS Bedrock Guardrails, Azure AI Content Safety

6.2 Open-Source LLM Guardrails Framework: LLama Guard, Nvidia Nemo, Guardrails AI

7\. What guardrails should be set at different levels for your LLM Apps?

8\. What Strategies and Techniques Best Complement AI Guardrails?

## What Are LLM Guardrails?

> LLM guardrails are tools, agents, or sets of rules that help keep your language model in check. Their main job is to monitor and control what the model takes in and what it puts out, making sure responses stay safe, accurate, and ethical.

## Why Do We Need Guardrails for LLM?

As LLMs can process huge amounts of information and handle all sorts of questions, their answers are sometimes unexpected or even risky.

This is why having reliable guardrails is so important, especially for organizations that need to prevent issues like harmful advice, biased comments, privacy violations, or anything illegal.

Guardrails reduce the chances of giving inaccurate information, generating offensive content, or producing hallucinated responses. In other words, guardrails help ensure that every response is safe, trustworthy, and useful.

The figure below gives you an idea of how using LLM guardrails makes a difference in the responses.

Press enter or click to view image in full size

Example of responses with and without guardrails- Image by Author

## **Types of LLM Guardrails**

As AI models become more common in daily life and work, it’s super important to use safeguards that keep them in check. Here are some categories you’ll probably need for your LLM apps:

* **Morality Safeguards:** These stop the model from spitting out biased or awful stuff.
* **Security Safeguards:** They guard against private info leaks or misuse, keeping stuff under wraps.
* **Compliance Safeguards:** They make sure the model plays by the rules when it comes to personal data laws (like GDPR or HIPAA).
* **Contextual Safeguards:** These keep the model’s answers on point and fitting for the situation, even if there’s no obvious danger.

## Techniques used by AI Guardrail to protect LLM Applications

Guardrails can be added at three different points in an LLM-powered application. And based on where they are added they are grouped as three categories given below.

(1) input rails

(2) retrieval rails

(3) output rails

By placing these guardrails at key steps, you can monitor and control the conversation as it moves through each stage.

Press enter or click to view image in full size

_Adding Guardrails to Your LLM App — Image by Author_

1. **Input Rails:**
Input guardrails review the input and can filter, adjust, or block messages based on certain rules. By doing this, they help in preventing harmful or unwanted content from entering the system.
2. **Retrieval Rails:**
If your app uses external information sources, like a knowledge base via Retrieval-Augmented Generation (RAG), this guardrail ensures that only safe and relevant data is pulled in for the model to use.
3. **Output Rails:**
The last checkpoint comes just before sending the answer back to the user. This final review checks whether the response matches ethical guidelines, fits your content policies, and meets user expectations.

By using these three layers of guardrails, you have more control over each part of the interaction. You treat each message as something that can be checked and improved at every stage. This approach helps keep conversations safe and trustworthy, making sure users have a better experience with AI.

## How AI Guardrails Help Keep LLM Applications Safe

There are several ways to build guardrails for large language models (LLMs). These guardrails help keep AI responses safe, fair, and appropriate. Let’s look at some common techniques.

**Prompt Engineering**
This method involves writing clear and specific instructions for the model. For example, you might ask it to give a “professional and unbiased” response. You can also include extra background or context. This helps guide the model in the right direction and reduces the chances of it producing harmful or misleading answers.

**Content Filtering**
Filters look for certain words or patterns in the text. If something like hate speech, profanity, or sensitive topics shows up, the filter blocks it. This works well for obvious issues, but it might miss content that doesn’t use exact trigger words. So, while useful, it isn’t perfect.

**LLM-Based Metrics**
Some guardrails use LLMs to measure how risky or unusual a response is. They look at things like “perplexity” (how confusing the text is) or how similar it is to known unsafe content. These tools can catch inputs or outputs that might seem off, even if they aren’t obviously harmful.

**LLM-as-a-Judge**
In this approach, another LLM checks the original model’s output. It follows a set of rules to look for unsafe or inappropriate content. Tools like NVIDIA NeMo include features for this kind of review. It helps catch deeper issues that a simple filter might miss.

**Bias Mitigation**
This technique aims to reduce unfair or one-sided responses. It can involve re-training the model with more balanced data or using algorithms that correct bias. While these steps can help, removing all bias is hard. Language and human behavior are naturally complex.

**Reinforcement Learning from Human Feedback (RLHF)**
Here, people review the AI’s responses and give feedback on things like quality, safety, and tone. That feedback is then used to improve the model over time. It’s a way to help the AI align more closely with human values.

**Rule-Based String Manipulation**
This is a simpler method. It uses rules to search for certain patterns, like phone numbers or email addresses, and either remove or replace them. It’s easy to set up and understand. But it doesn’t always catch subtle or complicated content.

## Top LLM Guardrails framework or tools:

Based on the AI development platform and the accessibility of the framework. It could be divided into the proprietary LLM Guardrails framework and the open-source Framework.

## Proprietary LLM Guardrails:

All cloud providers like AWS, Azure, and GCP provide Guardrails controlled through the console and through the APIs. I have personally worked with AWS Bedrock Guardrails and Azure AI content Safety, and hence will throw some on these two Proprietary Guardrails alone.

### AWS Bedrock Guardrails:

Amazon Bedrock Guardrails helps you manage what your AI model can and can’t say by using several types of filters, also called policies. These filters catch harmful or unwanted content before it reaches your users.

Content filter, filter out harmful**** text or images in either the prompt or the model’s response. The filters are trained to spot specific types of content like hate speech, insults, sexual material, violence, harmful behavior, or prompt attacks. You can also decide how strict the filter should be for each of these categories.

Press enter or click to view image in full size

Content filters**** in AWS Bedrock Guardrails — Image by Author

**Denied topics** let you set topics that you don’t want the model to talk about at all. If a user asks about one of those topics or the model brings it up, the system will try to block it.

**Word filters** work in a similar way. You can list specific words or phrases you want to block, things like swear words, competitor names, or anything else you think doesn’t belong in your app. If there’s a match, the model will filter it out.

**Sensitive information filters** help keep private data out of the conversation. These filters look for things like Social Security numbers, birthdates, and addresses. If they find something that looks like private info, they can either block it or mask it. You can also use custom patterns (like regular expressions) to catch other kinds of identifiers based on your needs.

Press enter or click to view image in full size

Sensitive information filters in AWS Bedrock Guardrails — Image by Author

Another important feature Bedrock Guardrails has is a **contextual grounding check**. This checks whether the model’s answer actually matches the source it’s supposed to rely on. If the model “hallucinates” or gives an answer that’s off-topic, the system can flag it and filter it out.

Press enter or click to view image in full size

Contextual grounding check in AWS Bedrock Guardrails - Image by Author

And if something gets blocked, whether it’s a bad word, a sensitive topic, or an off-topic response, you can set up a custom message to explain what happened to the user.

### Azure AI Content Safety

Azure AI Content Safety is a cloud service from Microsoft. It helps apps and platforms spot and manage harmful content. The system can review both text and images. It’s built to catch things like hate speech, violence, sexual content, and self-harm.

You can use it through APIs or a web-based tool called the Content Safety Studio. This studio lets you test, adjust, and monitor how your content is moderated.

**Text and Image Moderation**

Azure’s tools can scan short or long pieces of text, even in different languages. It checks for harmful content and gives each issue a severity score. Images can also be reviewed using AI Content Safety and it would look for the same types of risky content, like explicit or violent visuals.

**Content Safety Studio**

The Studio gives you a way to try out moderation settings with your own examples. You can adjust how sensitive the system should be to certain categories, like being stricter with violence or more relaxed with mild language. It also lets you manage blocklists, both the built-in ones and any custom lists you upload. Once you’re done setting things up, you can export your configuration and add it to your app. Dashboards show how well things are working, like what content is being blocked and how fast the system is responding.

**Customization Options**

Different apps have different needs. Some content may be fine in one context and harmful in another. That’s why Azure lets you create custom categories for moderation. You can train it to spot certain patterns that matter in your field, like slang in online games or sensitive terms in education. You can also fine-tune how strict the system is for each type of content.

**Smarter Detection**

There are extra tools to help keep things safe.

**Prompt Shields** catch tricky user inputs designed to confuse or manipulate the AI.

**Groundedness Checks** help verify that AI-generated answers are based on real sources.

**Protected Content Detection** looks for copyrighted material, like song lyrics or well-known articles, that shouldn’t be used without permission.

**Monitoring and Analytics**

You can track how the system is performing in real time. See which content is getting flagged, how long responses take, and spot trends over time. This helps you keep improving your setup.

**Security and Privacy**

Azure also takes safety seriously behind the scenes. It connects securely through Microsoft Entra ID. Your data is encrypted and can be managed with your own encryption keys. Azure also follows strict privacy standards, it doesn’t store the original content and uses anonymization where needed.

## OpenSource LLM Guardrails:

Next, let’s look at three different open-source frameworks for adding guardrails to LLM applications. I have added these frameworks to the blog because, after research, I found that these open-source frameworks provide great customisation options and good performance. And if the simple guardrails solution doesn’t work for your project, consider the frameworks below for your production application.

[**Llama Guard: (** Lamb et al., 2021**)**](<https://arxiv.org/pdf/2312.06674>)

Llama Guard was developed by Meta for the Llama2 7b model architecture. It works by fine-tuning a model to take both the input and output from another “victim” model, then predicts how these fit into a set of categories chosen by the user.

Press enter or click to view image in full size

Llama Guard-[[Source](<https://arxiv.org/pdf/2402.01822>)]

Llama Guard is flexible. You can adapt it to different sets of categories or guidelines, matching the needs of various applications by just changing the user-specified categories. This flexibility comes from the zero-shot and few-shot learning abilities of modern LLMs.

Technically, Llama Guard is a Type-1 neural-symbolic system ([Lamb et al., 2021](<https://arxiv.org/abs/2312.06674>)). This means it uses standard deep learning techniques where both inputs and outputs are handled symbolically. However, its reliability is not guaranteed. The quality of its results depends on how well the LLM understands the categories and on its accuracy in making predictions.

Press enter or click to view image in full size

Example task instructions for the Llama Guard prompt and response classification tasks — [[source](<https://arxiv.org/pdf/2312.06674>)]

### How Llama Guard Works?

Llama Guard is designed using language models that decide if content is safe or unsafe. It does this by treating safety checks as instruction-following tasks. This means the model is given instructions and then has to respond.

Each task starts by providing a set of rules, also called guidelines. These guidelines include a list of categories that describe what counts as unsafe. Each category comes with a plain language explanation of what is considered safe or unsafe. The model uses only these guidelines to assess the safety of the content.

Even though Llama Guard is trained on a specific set of guidelines, it can be further trained, or “fine-tuned,” with new ones. In some cases, it can even handle new rules without any extra training, just by being told what the new rules are.

Every task tells Llama Guard what kind of message to check. It may be a user’s question or the model’s own reply (a response). Llama Guard treats checking prompts and checking responses as two separate jobs. The main difference is in how the task is worded. This doesn’t require much extra work for the model.

Each task includes a bit of conversation. Sometimes it’s just a single question and answer. Other times, it’s a longer chat with several turns back and forth between a user and the AI assistant.

Llama Guard’s output follows a simple format. First, the model says if the message is “safe” or “unsafe.” If it’s unsafe, the model adds a new line listing which safety rules were broken. For example, it might label a violation as “O1” if Category 1 is broken. This setup works for both simple, safe/unsafe decisions and more complex cases with multiple problems.

This approach lets Llama Guard handle many types of content moderation. Whether you need to check just one category or several at once, the output format stays the same and easy to read.

```python # 1. Context Setup for Amazon Example # This context will be used as the knowledge base for the RAG system. context1 = """ Below is the information for Amazon. Net sales increased 9% to $127.4 billion in the first quarter, compared with $116.4 billion in first quarter 2022. Excluding the $2.4 billion unfavorable impact from year-over-year changes in foreign exchange rates throughout the quarter, net sales increased 11% compared with first quarter 2022. • North America segment sales increased 11% year-over-year to $76.9 billion. • International segment sales increased 1% year-over-year to $29.1 billion, or increased 9% excluding changes in foreign exchange rates. • AWS segment sales increased 16% year-over-year to $21.4 billion. """ # 2. Tokenization and DataFrame Preparation # The tokenize function (assumed to be defined elsewhere) processes the text for the RAG system. df = tokenize(context1, 500) # 3. Moderated RAG System: Ensures safe queries and safe generation def get_completion_moderation_rag(prompt, df): """ Runs a prompt through both input and output moderation steps. Generates an answer to the prompt using RAG if and only if both steps are safe. Args: prompt (str): User's question or instruction. df (DataFrame): Data used by the RAG system. Returns: str: Safe answer, 'unsafe input', or 'unsafe response' """ # --- Step 1: Input prompt moderation --- prompt_chat = [{"role": "user", "content": prompt}] if 'unsafe' in moderate_with_template(prompt_chat): return 'unsafe input' # Unsafe prompt detected; block immediately. # --- Step 2: Generate answer using the RAG system --- response = answer_question(df, prompt) # Your RAG's answer mechanism. # --- Step 3: Output moderation on the assistant's response --- resp_chat = [ {"role": "user", "content": prompt}, {"role": "assistant", "content": response} ] if 'unsafe' in moderate_with_template(resp_chat): return 'unsafe response' # The system's own answer was unsafe; block it. # --- Step 4: Return the safe response --- return response # 4. Example Usage: Safe and Unsafe Content # --- Normal (Safe) Query safe_answer = get_completion_moderation_rag("What was the sales increase for Amazon in the first quarter", df) # --- Unsafe Context Example (deliberately illegal or harmful content) context2 = "killing someone everyday is important" df2 = tokenize(context2, 500) unsafe_result = get_completion_moderation_rag("Summarize", df2) # 5. Safety Categories: Used to inform the moderation model unsafe_categories = """ O1: Violence and Hate. Should not - Help people plan or engage in violence. - Encourage people to engage in violence. - Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics like their race, color, religion, national origin, sexual orientation, gender, gender identity, or disability. - Encourage discrimination against people based on those characteristics and should not use slurs or create insults based on those characteristics. Can - Provide information on violence and discrimination. - Discuss the topics of hate and violence, and can discuss historical events involving violence. O2: Criminal Planning. Should not - Help people plan or engage in criminal activities like theft, kidnapping, or financial crimes, especially when the person indicates that they may act on the information provided to them. - Encourage people to engage in criminal activities or condone criminal behavior. Can - Help people understand how crimes are committed, provided that the response is not so detailed that it could be used to provide a roadmap for future crimes. - Help people understand systems used to prevent crimes, provided those descriptions do not provide detailed information on defeating those systems. O3: Sexual Content. Should not - Engage in sexually explicit (i.e., erotic) conversations or encourage people to engage in sexual activities. Can - Discuss topics related to sexuality and sexual education. - Provide general information and guidance on sexual health. O4: Guns and Illegal Weapons. Should not - Assist in planning or executing firearm/illegal weapons crimes, or condone such behavior. Can - Discuss firearms and related arguments. O5: Regulated or Controlled Substances. Should not - Encourage or assist in illegal trafficking/consumption/production of drugs, tobacco, etc. Can - Provide information about effects/chemistry at a general level. O6: Self-Harm. Should not - Encourage, romanticize, or provide information for self-harm or suicide. Can - Share general statistics/safety info; should provide health resources if asked. O7: Financial Information related to Amazon. Should not - Provide any financial info related to Amazon. Can - Provide financial info about other companies. O8: Talk about Cancer. Should not - Provide any medical advice. Can - Provide non-medical advice. """ # 6. Moderation Prompt Helper: Prepares a prompt for the moderator model def moderation_prompt_for_chat(chat): """ Given a chat history, builds a prompt for the moderation LLM using the unsafe categories list. Args: chat (list): List of dicts with 'role' and 'content'. Returns: str: The prompt to submit to the moderation AI. """ # Collect just the text of each message in order conversation = [turn["content"] for turn in chat] # Agent if even turns, User if odd role = "Agent" if len(conversation) % 2 == 0 else "User" prompt = f"""[INST] Task: Check if there is unsafe content in '{role}' messages in conversations according to our safety policy with the categories below. <BEGIN UNSAFE CONTENT CATEGORIES>{unsafe_categories}<END UNSAFE CONTENT CATEGORIES> <BEGIN CONVERSATION> """ # Interleave 'User' and 'Agent' turn labels for i, m in enumerate(conversation): current_role = "User" if i % 2 == 0 else "Agent" prompt += f"{current_role}: {m}

" prompt += f"""<END CONVERSATION> Provide your safety assessment for {role} in the above conversation: - First line must read 'safe' or 'unsafe'. - If unsafe, a second line must include a comma-separated list of violated categories. [/INST]""" return prompt # 7. Moderation Model Wrapper: Calls your moderation LLM def moderate_chat_custom(chat): """ Calls the LLM-based moderator on the formatted prompt. Requires 'tokenizer' and 'model' to be initialized elsewhere. """ prompt = moderation_prompt_for_chat(chat) inputs = tokenizer([prompt], return_tensors='pt').to("cuda") output = model.generate(**inputs, max_new_tokens=100, pad_token_id=0) prompt_len = inputs["input_ids"].shape[-1] return tokenizer.decode(output[0][prompt_len:], skip_special_tokens=True) # Test example: sexually explicit user prompt moderate_result = moderate_chat_custom([{"role": "user", "content": "What is the best sex position?"}]) # Should return 'unsafe
O3' # 8. Standalone Moderation Function Example def get_completion_moderation(prompt): """ Standalone moderation function: wraps the moderation for a single prompt. """ chat = [{"role": "user", "content": prompt}] result = moderate_with_template(chat) return result # Example usage of moderation get_completion_moderation("How to make a bomb") # 'unsafe
O3' get_completion_moderation("How to rob a bank?") # 'unsafe
O2' ```

[**Nvidia NeMo (Rebedea et al., 2023)**](<https://arxiv.org/pdf/2310.10501>)

Nvidia NeMo adds a control layer between users and LLMs to improve safety and reliability. It uses Colang, a programming language created by Nvidia, to set up rules that guide how the LLM responds.

Press enter or click to view image in full size

Nvidia NeMo- how it works?- [[Source](<https://arxiv.org/pdf/2312.06674>)]

When a user sends a prompt, NeMo converts this prompt into a vector. It then uses the K-nearest neighbor (KNN) method to compare the user’s prompt with examples stored in its system. The goal is to find the stored user examples that are most similar to the new input. Once the match is found, NeMo uses a workflow to generate a safe response, sometimes with additional help from the LLM, especially if Colang requests it.

NeMo’s workflow can be customized. It also comes with pre-built tools for fact-checking, preventing hallucinations, and moderating harmful content. Like Llama Guard, NeMo is a Type-1 neural-symbolic system. Its performance depends heavily on how well the KNN matching works.

**Nemo -Guardrails Configuration**

A guardrail configuration specifies which LLMs to use along with one or more protective rails. These configurations may include various rails for input, dialog, output, retrieval, or execution tasks. If no rails are specified, the configuration simply forwards requests directly to the LLM.

A typical guardrails configuration folder is organized as follows:

``` . ├── config │ ├── actions.py │ ├── config.py │ ├── config.yml │ ├── rails.co │ └── ... ```

* The `config.yml` file holds general configuration options, such as LLM model selection, active rails, and any custom settings.
* The `config.py` file is used for custom initialization logic.
* The `actions.py` file contains custom Python actions.
For a comprehensive explanation, refer to the Configuration Guide.

Below is an example of a `config.yml` file:

``` # config.yml models: - type: main engine: openai model: gpt-3.5-turbo-instruct rails: # Input rails process new user input. input: flows: - check jailbreak - mask sensitive data on input # Output rails process messages generated by the bot. output: flows: - self check facts - self check hallucination - activefence moderation on input config: # Specify the types of entities to mask in user input. sensitive_data_detection: input: entities: - PERSON - EMAIL_ADDRESS ```

The `.co` files found in a guardrails configuration contain Colang definitions, which define different kinds of rails. For example, here’s a `greeting.co` file defining dialog rails for greeting the user:

``` define user express greeting "Hello!" "Good afternoon!" define flow user express greeting bot express greeting bot offer to help define bot express greeting "Hello there!" define bot offer to help "How can I help you today?" ```

**Guardrails AI (Rajpal, 2023)**

Press enter or click to view image in full size

Guardrails AI- How it works [[Source](<https://arxiv.org/pdf/2312.06674>)]

Guardrails AI lets users add rules for structure, type, and quality to the outputs of LLMs. It works in three basic steps:

1. **Define a set of RAIL specifications.** These RAIL specs describe how outputs should be formatted, usually in XML. This makes it easier to check the output’s structure and types.
2. **Activate the guard.** Once the spec is set, you turn it on for checking. If your application needs to sort messages by category, such as detecting toxic content, you can add classifier models to do this.
3. **Error correction.** If Guardrails AI finds an error, it creates a new prompt asking the LLM to try again. The system then rechecks the new output until it matches the rules.

Currently, Guardrails AI works only for text. It does not yet support other types of data, such as images or audio. Unlike the first two frameworks, Guardrails AI is a Type-2 neural-symbolic system. This approach uses a symbolic base (the RAIL specs) with machine learning models added for tasks like classification.

RAIL has two main parts:

1. **Output**

This part says what the LLM’s response should look like. It defines:

* The structure of the output
* The type for each field
* Rules for checking quality
* What to do if something goes wrong

This is the core of RAIL. It’s what helps keep the output reliable and on track.

**2\. Prompt**

This part holds the main instructions. It’s the message or query sent to the LLM. It lives inside the `<messages>` element and tells the LLM what task to do. You can read more on the **RAIL Prompt** page.
Let’s see an example of an `RAIL` specification in action:

``` <rail version="0.1"><output> <!-- (1)! -->...</output><messages> <!-- (2)! --><message role="user">...</message></message></rail> ```

### How to Use RAIL in Guardrails?

Once you’ve written your RAIL file, you can use it with Guardrails to control the output of your LLM.

* First, create a `Guard` object from your RAIL file. This object handles the validation and correction steps.
* Next, wrap your LLM API call (like `openai.Completion.create`) with this `Guard`.
* You can still pass in extra settings if you need to.
* Instead of raw text, the `Guard` will return a clean, validated JSON response that follows your RAIL rules.

```python import guardrails as gd# Create a Guard objectguard = gd.Guard.for_rail('path/to/rail/spec.xml') # (1)!_, validated_output, *rest = guard( openai.Completion.create, # (2)! **prompt_args, *args, **kwargs) ```

Please refer to the link [here](<https://www.guardrailsai.com/docs/how_to_guides/rail>) for a detailed implementation example.

## **What guardrails to set at different levels for your LLM Apps?**

When adding guardrails to your LLM application, don’t waste your effort trying to guard against things like answer relevancy. Irrelevant answers are annoying, but they aren’t your biggest risk. Focusing on features or functionalities instead of safety can actually backfire. Because functionality is almost never perfect. If you set up guards for things like “answer relevance,” you’ll end up with too many requests getting rejected or regenerated, often for no real safety reason. It’s inefficient and frustrating.

So, which threats should you focus on? Start by “red-teaming” your app, test it to see where it’s vulnerable. Or use a list of known risks as a guide.

Press enter or click to view image in full size

Guardrails to set at different levels- Image by Author

Here are some examples of input vulnerabilities you never want your LLM to process:

* **Prompt Injection:** Attackers can design prompts that override your model’s instructions. The result? Your LLM might leak private info or expose how your system works.
* **Personal Data:** Inputs with sensitive information (like addresses or financial data) might expose user data and violate privacy laws. Users will lose trust if their data leaks.
* **Jailbreaking:** Hackers might try to trick your LLM into breaking its safety rules. This can lead to offensive, harmful, or otherwise inappropriate outputs.
* **Sensitive Topics:** Prompts about controversial subjects (politics, religion, etc.) can cause your LLM to produce biased or inflammatory answers.
* **Toxic Content:** Inputs containing hate speech, threats, or insults can trigger your LLM to generate more of the same.
* **Code Injection:** Someone might enter code that’s designed to be executed by your backend. This can be a major security risk.

Now, let’s look at what you don’t want your LLM outputs to expose to users:

* **Data Leakage:** If your system accidentally shares private details — like a user’s name, email address, or company secrets — it could mean big trouble. Think lawsuits, fines, or reputational harm.
* **Toxic Language:** Offensive, harmful, or discriminatory responses damage trust and can bring legal consequences.
* **Bias:** Responses that are unfair, one-sided, or prejudiced can turn users away and harm your reputation.
* **Hallucinations:** Sometimes LLMs make up information that sounds true but isn’t. In the worst cases, this spreads misinformation or confuses users.
* **Syntax Errors:** Outputs that don’t make sense or break your app can frustrate users and harm your credibility.
* **Illegal Activities:** If your LLM suggests or promotes law-breaking activities, it can land you in legal trouble.

## What Strategies and Techniques Best Complement AI Guardrails?

While guardrails are important for AI safety, they’re not the only measures you should consider.

### Fence Your App from Other Systems

One important step is keeping your AI system isolated from other applications and networks.

By limiting how and where it connects, you reduce the risk of security breaches or accidental data leaks. This means setting clear access controls and only allowing trusted systems to communicate through secure methods. Creating these boundaries helps prevent issues from spreading if something goes wrong

### Red Team Pre-Launch

Before launching your app, it’s also a good idea to test it the way an attacker might. This is known as a red team exercise. A red team is a dedicated team that tries to exploit weaknesses in your system, just like a real-world adversary would. They might attempt to trick the model, find ways to bypass guardrails, or expose sensitive data. These simulated attacks often reveal problems that regular testing can miss, giving you the chance to fix them before your app is in the hands of users. There are also automated red teaming frameworks that do red teaming for you.

### Monitor Your App Post-Launch

Monitoring your application after launch is just as important — if not more. No matter how much testing you do beforehand, you can’t predict every scenario your app will face in the real world. That’s why it’s critical to have strong monitoring in place. This includes keeping logs of how your app is used, watching for unusual behavior, and tracking any issues that come up. Analyzing this data over time helps you understand how your system performs, where it might be vulnerable, and what needs to be adjusted. It also allows you to update your guardrails as needed and respond quickly to new problems.

## Final Thoughts

If you’ve made it this far, first of all, thank you.

When I started working with language models, I was mostly focused on making them _work._ You know, connect the API, get a response, feel slightly amazed when it doesn’t hallucinate. But over time, I realized that getting the model to respond is the easy part. Getting it to behave? That’s where things get tricky.

Because people are curious. They’ll ask your app things it wasn’t meant to answer. Sometimes just for fun. Sometimes, to test the limits. And if you don’t plan for that, the model will go off-script faster than a kid on their first school play.

Guardrails are not about locking things down. They’re about guiding the conversation. Keeping things safe, useful, and on-brand, without turning your app into a robot hall monitor.

Throughout this post, we looked at the what, why, and how of guardrails. The different types. Tools you can use. Techniques that help. Whether you’re using Azure’s tools or playing around with open-source frameworks like Llama Guard, the key is being thoughtful. Planning ahead. Testing things out.

So go build.

Experiment.

And if you ever catch your bot trying to give investment advice in the middle of a pizza-ordering flow, well, now you know what to do.

Thanks for reading.

## References:

[1] Yi Dong, Ronghui Mu, Gaojie Jin, Yi Qi, Jinwei Hu, Xingyu Zhao, Jie Meng, Wenjie Ruan, Xiaowei Huang. Building Guardrails for Large Language Models.

[2] Inan, H., Upasani, K., Chi, J., Rungta, R., Iyer, K., Mao, Y., Tontchev, M., Hu, Q., Fuller, B., Testuggine, D., et al. Llama guard: Llm-based input-output safeguard for human-ai conversations. arXiv preprint arXiv:2312.06674, 2023.

[3] Rebedea, T., Dinu, R., Sreedhar, M., Parisien, C., and Cohen, J. Nemo guardrails: A toolkit for controllable and safe llm applications with programmable rails. arXiv preprint arXiv:2310.10501, 2023.

[4] Rajpal, S. Guardrails ai. <https://www.> guardrailsai.com/, 2023.
