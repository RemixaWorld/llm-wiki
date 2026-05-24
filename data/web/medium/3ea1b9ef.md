---
domain: medium.com
fetch_date: '2026-05-18T12:48:42.597121'
status: ok
url: https://medium.com/@harishhacker3010/can-we-make-any-smaller-opensource-ai-models-smarter-than-human-1ea507e644a0
---

# Can we make any smaller opensource LLM models smarter than human?

[ ![Harish SG](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png) ](</@harishhacker3010?source=post_page---byline--1ea507e644a0--------------------------------------->)

[Harish SG](</@harishhacker3010?source=post_page---byline--1ea507e644a0--------------------------------------->)

10 min read

·

Oct 4, 2024

\--

\--

Listen

Share

More

I am Harish SG, a security researcher who studied Masters in Cybersecurity at UT Dallas and AI security engineer at Cisco, previously hunted on the Microsoft Bug Bounty Program and Google VRP.

I am sharing this article for awareness and educational purposes only and I am sharing only personal opinions and none of these are related to my work at Cisco.

**Disclaimer** : I am not a AI researcher or expert and I do security research on LLMs . This work is fully based on my understanding of LLMs and its capabilities.

This article is focused on my recent AI research on making opensource models to outperform other closed sourced models and making current SOTA (State Of the Art) models such as Claude Sonnet 3.5 to outperform reasoning SOTA model OpenAI O1-preview and O1 mini(both of them has phd scholar level intelligence according to OpenAI).

### **What is reasoning in LLM ?**

Reasoning in LLMs refers to the ability of these models to:

1. Think logically
2. Draw inferences
3. Solve complex problems
4. Make sound decisions based on available information

While LLM are not explicitly trained to reason, they have exhibited behaviors that sometimes resemble reasoning capabilities except O1 and O1 mini

### Why Reasoning in LLM’s Matters?

The ability of LLM to reason is significant for several reasons:

1. **Deeper Understanding** : True reasoning abilities would indicate that LLM can go beyond pattern matching to have a deeper understanding of the world.
2. **Problem-Solving** : Enhanced reasoning capabilities could lead to more effective problem-solving in complex domains.
3. **Decision-Making** : LLM with robust reasoning abilities could assist humans in complex decision-making processes.
4. **Generalization** : Improved reasoning could help LLM perform better on “out of distribution” tasks, enhancing their generalizability.
5. **Practical Applications** : Reasoning capabilities could accelerate scientific discovery, enhance policy-making, and improve personalized services in education and healthcare for example think of an autonomous AI agent which take a dataset of time series data and find a pattern which is harder or time taking task to identify and use it to predict future with accuracy.

When OAI released O1 and O1- mini models I understood if AI can take sometime to think to solve harder problems its a new innovation towards AGI (Artificial General Intelligence) and application of AI to solve complex problems of humanity. then one day I was thinking of What if we can make existing SOTA models such as Claude Sonnet 3.5 to reason as good as O1 models.

After reading some papers such as reflexion(from northeastern University) and comments from /locallama subreddit I decided to create new prompting paradigm which combines Dynamic Chain of thoughts + reflection + verbal reinforcement and I also tried to implement it as an experiment what if we combine Dynamic Chain of thoughts + reflection + verbal reinforcement to create one effective prompt.

Example of the prompting paradigm for coding and math problem solving use cases

``` Begin by enclosing all thoughts within <thinking> tags, exploring multiple angles and approaches.Break down the solution into clear steps within <step> tags. Start with a 20-step budget, requesting more for complex problems if needed.Use <count> tags after each step to show the remaining budget. Stop when reaching 0.Continuously adjust your reasoning based on intermediate results and reflections, adapting your strategy as you progress.Regularly evaluate progress using <reflection> tags. Be critical and honest about your reasoning process.Assign a quality score between 0.0 and 1.0 using <reward> tags after each reflection. Use this to guide your approach:0.8+: Continue current approach0.5-0.7: Consider minor adjustmentsBelow 0.5: Seriously consider backtracking and trying a different approachIf unsure or if reward score is low, backtrack and try a different approach, explaining your decision within <thinking> tags.For mathematical problems, show all work explicitly using LaTeX for formal notation and provide detailed proofs.Explore multiple solutions individually if possible, comparing approaches in reflections.Use thoughts as a scratchpad, writing out all calculations and reasoning explicitly.Synthesize the final answer within <answer> tags, providing a clear, concise summary.Conclude with a final reflection on the overall solution, discussing effectiveness, challenges, and solutions. Assign a final reward score. ```

### **InDepth details of above prompting paradigm:**

The combined framework of Dynamic CoT, Reflection, and Verbal Reinforcement Learning creates a highly adaptive and responsive problem-solving AI system. The process begins with the Dynamic CoT generating an initial reasoning path, which is then evaluated and refined through the Reflection mechanism. After each reflection phase, the model receives verbal reinforcement in the form of reward scores, which guide future reasoning steps.

This cyclical process allows the model to iteratively improve the output, adapt to changing conditions, and respond to complex problem structures effectively. For instance, in a scenario involving a multi-stage decision-making task such as autonomous navigation, the model might start by exploring a path using Dynamic CoT.

As it encounters obstacles or changes in the environment, the reflection mechanism would allow it to reassess its strategy, while verbal reinforcement scores provide guidance on how to adjust its actions. This results in a AI system that not only learns from its actions but actively improves its reasoning capabilities over time, demonstrating enhanced problem-solving skills in dynamic, real-world applications.

![image](https://miro.medium.com/v2/resize:fit:1915/1*bQAT_OBBVVAoSrBLC5v3nQ.png) ![image](https://miro.medium.com/v2/resize:fit:1918/1*EwhG86_QyKdV94TjTxOuOw.png)

![image](https://miro.medium.com/v2/resize:fit:1918/1*z7k-EKGYZC5rGtkOb1UC0w.png) ![This screenshots demonstrates LLM’s reasoning chain](https://miro.medium.com/v2/resize:fit:1909/1*gi4C2G6jmAnAZ1Je_pFeSA.png)

### **Benchmarking the above prompting paradigm:**

I wanted to know how well my prompting paradigm though I was able to answer classic questions such “count number of r’s in word strawberry” and”compare 0.9 and 0.11 and tell which one is larger “ etc

as of my knowledge only O1 and O1 mini was able to get all of them correct because of its internal reasoning chains.

![Correct answer from LLM for question which LLMs usually fails to answer](https://miro.medium.com/v2/resize:fit:700/1*uQvHvhX52IXLuP0aqvHocg.png)

I created two set of datasets for benchmark evaluation

first set of dataset had questions from JEE(Joint Entrance Examination) Advanced and UPSC prelims I would rate this as medium set.

The JEE Advanced is considered one of the toughest undergraduate entrance exams globally, intended for students aspiring to join the prestigious Indian Institutes of Technology (IITs).

The UPSC Civil Services Examination is one of the most competitive exams in the world, attracting candidates aspiring to serve as administrators in India’s bureaucracy. The General Studies paper tests knowledge across diverse fields, making it a rigorous and comprehensive assessment tool for LLMs.

The questions are extremely rigorous and test deep conceptual understanding, problem-solving skills, and application of concepts across multiple domains such as physics , math , chemistry , social science etc

### **Tools and Scripts used for this evaluation:**

* The script uses Streamlit to create a web app that generates AI responses using the Groq API for opensource model and other APIs for closed source models such as gpt4o , o1 and Claude.
* It includes a detailed system prompt (starting with “You are an AI assistant that explains your reasoning step by step…”) that guides the AI’s reasoning process.
* This prompt instructs the AI to use Dynamic Chain of Thought (CoT), reflection, and verbal reinforcement learning techniques.
* The AI breaks down its reasoning into clear steps, each with a title, content, confidence score, and thinking time.
* Every 3 steps, the AI performs a self-reflection, considering potential biases and alternative viewpoints.
* The script enforces a minimum of 15 steps before allowing a final answer, ensuring thorough analysis of the given query.

I modified this script by **Benjamin Klieger** and its orginal version is here <https://github.com/bklieger-groq/g1>

I modified the original version to implement this logic, user will provide a problem to AI system it should take enough time to think about that problem in various ways and finally solve this. In this logic I tried to bio mimic how humans think to solve a complex problem in a AI system. I got this idea from Aravind Srinivas words in a interview with Lex Freidman.

### **Benchmark results analysis:**

![Graph generated using Chatgpt](https://miro.medium.com/v2/resize:fit:700/1*HeSSR1YMRjSPOG83Q3drzQ.png)

The results demonstrate that the application of Dynamic CoT, Reflection, and Verbal Reinforcement Learning techniques significantly enhanced the performance of most models, particularly Claude Sonnet and Llama 3.1 8b.

A. Performance with Technique Claude Sonnet achieved the highest score (40/48), demonstrating strong performance across mathematical, physics, and chemistry questions. Llama 3.1 8b (33/48) and GPT-4O (36/48) also showed significant improvements with the applied techniques.

B. Performance Without Technique Without the advanced techniques, all models except O1 showed a decline in performance. Notably, O1 scored 39/48 without any technique applied, suggesting a strong inherent problem-solving ability.

we can observe that Claude Sonnet 3.5 was able to outperform O1.

### **limitation:**

In this benchmark evaluation was bit leniant ie gave score for partially correct answer.

**Note: At the time of this benchmarking meta did not released llama 3.2.**

### **Cherry on cake test (Benchmarking against IMO 2023 questions)**

OpenAI claimed that O1 was able to score 83% on IMO. Claude Sonnet with our prompting technique was able to get 50% on first attempt if we tried muliple times Claude Sonnet 3.5 might outperform O1.

![image](https://miro.medium.com/v2/resize:fit:1072/1*XC2VhL1qndIwS3ZFlCyrEQ.png) ![image](https://miro.medium.com/v2/resize:fit:1066/1*VJlSQynSM5CT8XGzbeSK8Q.png) ![Screenshots on claude solving IMO 2023 questions](https://miro.medium.com/v2/resize:fit:1054/1*WKekFgntXlwwUSDqkbifZA.png)

### **Benchmarking against Putnam dataset**

**what is putnam math competition?**

The William Lowell Putnam Mathematical Competition, commonly known as the Putnam Competition, is an extremely challenging mathematics contest for undergraduate students in the United States and Canada. Here are key aspects of the competition and its difficulty:

**Competition Structure:**

\- Held annually on the first Saturday in December.
\- Consists of two 3-hour sessions, with 6 problems in each session .
\- Each problem is worth 10 points, for a maximum score of 120.

**Difficulty Rating:**

The Putnam Competition is widely regarded as one of the most difficult undergraduate mathematics competitions in the world. Its extreme difficulty can be assessed by several factors:

Median Score: The median score is typically 0 or 1 out of 120 points. This means that more than half of the participants either solve no problems completely or at most one problem.

Perfect Scores In the competition’s 85-year history, there have been only five perfect scores This underscores the exceptional difficulty of achieving a complete solution to all problems.

Given these factors, on a scale of 1 to 10, with 10 being the most difficult, the Putnam Competition would rate a 9 or 10 in terms of difficulty for undergraduate mathematics competitions. (Source : perplexity)

I selected around 28 questions from putnam question paper from year 2013 to 2023.

**Benchmark results analysis:**

In this benchmark llama3.1 70B , Claude Sonnet and o1 mini solved 14 questions whereas O1 model solved 13 questions and gpt4o solved 9 questions.

At first glance this results seems to be too good to be true!

I believe gpt4o did not solved this because it was creating more than 50 to 60 reasoning chains loops ended up giving some rubbish answers.

![image](https://miro.medium.com/v2/resize:fit:700/1*vFM2hxuaAOSnEQ-KzNqEoA.png)

From above benchmarks we can see that Claude Sonnet 3.5 with our prompting technique can able to outperform O1 and O1 mini and other small language model in problem demanding better reasoning capabilities

I will suggest to use this prompt paradigm as system prompt for better performance.

Honestly speaking I did not have enough compute or budget needed to run against standard benchmark such as MMLU , MMLU pro , GPQA etc and if anyone wanted to extend this work by running against them please go for it and I also opensourced scripts and datasets I used in this experiment in this repo along with some proofs.

### repo: <https://github.com/harishsg993010/LLM-Research-Scripts>

### Interesting things and capabilities of LLM I observed during this experiment:

1. LLM can able to create its own simulation. when I gave the LLM an matrix related problem it explored various techniques to solve the problem at one point it started to create it’s own simulations based on various scenarios to solve the problem.
2. LLM such as Claude Sonnet 3.5 , gpt4o took more than 50 internal reasoning step to solve complex math problem.
3. LLM tend to answer MCQs better than questions without MCQ.
4. Claude Sonnet 3.5 utilised around 1 Million token just for 7 questions then I utilised openrouter for this experiment.

![image](https://miro.medium.com/v2/resize:fit:700/1*I5OeG0ApUIUAjZzdhWURFA.png)

### Conclusion:

I fundamentally believe that LLMs are like a human who read millions of book but it does not know how to utilise that data to solve problems. so as a researcher and user of LLMs we need to teach a LLM on how to utilise its knowledge to solve problems.

this kind of reasoning capability can be utilised by people to build powerful workflow automation to solve problems in various sectors such as IT , Cyber Security , Automobile etc.

Organisation can utilise smaller opensource model as cheaper fall back to large language model such as gpt4o etc for task which needs reasoning capabilities to solve.

I know some of the finding from work seems like too good to be true. if anyone want to evaluate please be open to utilise scripts and datasets from github repo

** _Follow me on twitter_** _:_[_https://twitter.com/CoderHarish_](<https://twitter.com/CoderHarish>)

** _Follow me on linkedin_** :<https://www.linkedin.com/in/harish-santhanalakshmi-ganesan-31ba96171/>
