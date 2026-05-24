---
domain: ai.gopubby.com
fetch_date: '2026-05-18T12:51:31.155630'
status: ok
url: https://ai.gopubby.com/reinforcement-learning-agents-for-industrial-control-systems-b917b513f0c4
---

# LLM based fine-tuning of Reinforcement Learning Agents

## Reinforcement Learning Agents for Industrial Control Systems

[ ![Debmalya Biswas](https://miro.medium.com/v2/resize:fill:64:64/1*g79QJ3lAxAWvOERtOtRcfw.png) ](<https://debmalyabiswas.medium.com/?source=post_page---byline--b917b513f0c4--------------------------------------->)

[Debmalya Biswas](<https://debmalyabiswas.medium.com/?source=post_page---byline--b917b513f0c4--------------------------------------->)

12 min read

·

Dec 15, 2024

\--

Listen

Share

More

## [A comprehensive guide to Agentic AI SystemsA comprehensive guide to Agentic AI Systems - Download as a PDF or view online for freewww.slideshare.net](<https://www.slideshare.net/slideshow/a-comprehensive-guide-to-agentic-ai-systems-c742/274678426?source=post_page-----b917b513f0c4--------------------------------------->)

## 1\. Introduction

AI agents are the current hype. I have written about them, and others are also discussing them. Overall, however, it does mean that there is a lot of confusion reg. what are agentic AI systems? How are they different from generative AI (Gen AI)? Fig. 1 below tries to provide some clarity to this debate by showing the evolution of agentic AI systems.

Press enter or click to view image in full size

Fig. 1: Agentic AI evolution (Image by Author)

Given a user task, the goal of an agent platform is to identify an agent (group of agents) capable to executing that task. So the first component we need is an **orchestration** layer capable of decomposing a task into sub-tasks, with execution of the resp. agents orchestrated by an orchestration engine. As of today, we prompt an LLM for the task decomposition. So this is the overlap with Gen AI.

> Unfortunately, this also means that agentic AI today is limited by the **reasoning** capabilities of large language models (LLMs).

It then monitors the execution / environment and adapts **autonomously**. Given the long-running nature of such complex tasks, memory management is key for Agentic AI systems. The current solution is to use vector databases (Vector DBs) to store the agent **memory** externally — making data items accessible as needed.

It is also important to mention that **integration** with enterprise systems (e.g., CRM in this case) will be needed for most use-cases. For example, refer to the Model Context Protocol ([MCP](<https://www.anthropic.com/news/model-context-protocol>)) proposed by Anthropic recently to connect AI agents to external systems where enterprise data resides.

A reference architecture for an agentic AI platform with the above components is illustrated in Fig. 2.

Press enter or click to view image in full size

Fig. 2: Agentic AI platform reference architecture focusing on RL agents (Image by Author)

We will be focusing on the AI agent types and their capabilities in this article (highlighted on the right hand side of Fig. 2), especially, **RL agents**.
(Please refer to our previous article on [Stateful & Responsible AI Agents](<https://medium.com/ai-advances/stateful-and-responsible-ai-agents-7af386268554>) for a deep dive on the other components.)

When we talk about AI agents today, we mostly talk about **LLM agents** , which loosely translates to invoking (prompting) an LLM to perform natural language processing (NLP) tasks, e.g., processing documents, summarizing them, generating responses based on the retrieved data. For example, refer to the “researcher” agent scenario outlined by [LangGraph](<https://blog.langchain.dev/langgraph-multi-agent-workflows/>).

It is important to mention here that some agentic tasks may be better suited to other machine learning (ML) techniques, e.g., reinforcement learning (RL), predictive analytics, etc. — depending on the use-case objectives.

> In this article, we focus on **RL agents** , and show how LLMs can be used to fine-tune the RL rewards and policy functions.

## 2\. Reinforcement Learning for Industrial Control Systems

In this section, we provide a brief primer on reinforcement learning (RL), showing its relevance for the manufacturing industry, with a focus on industrial control systems.

Data Driven Control, esp. those based on reinforcement learning (RL) control strategies, has become the go-to paradigm for all control problems, from controlling combustion engines, to robotic arms cutting metals, to air conditioning systems in buildings.

> We define data driven control as simply machine learning (ML) techniques applied to control systems.

To understand the drivers behind this trend, we first need to understand the limitations of control theory for real-life systems.

### 2.1 Limitations of Control Theory

At a very basic level (and high-level), a control system literally consists of a system & controller:

* _System_ to control
*  _Controller_ applies a control strategy to control the system in an optimal fashion.

There are two other things that we need to consider in this context: Any strategy that the controller can apply is constrained by

* its knowledge of the system state — in most cases, provided by the system sensors;
* and the system parameters that it can control — also referred to as the system actuators. For example, an engine can only drive a car within a certain speed range, at a certain acceleration.

External / environmental factors also play a key role in the control strategy, however that role is more as an ‘input’ parameter, and not a constraint. For example, the outdoor temperature plays a key role in deciding how much to cool for an air-conditioner; however the air-conditioner’s functioning is not constrained by it.

Fig. 3 below provides an illustration of a control system, where _x_ ₜ is a time derivative of the non-linear function _f_.

Fig. 3: (Simplified) Control system design (Image by Author)

> Designing a control strategy then consists of solving the equations characterizing the system behavior — often modeled in the form of linear equations. Most of control theory is targeted towards solving linear equations.

Unfortunately, real-world systems are (mostly) non-linear. For example, even the equation to capture the motion of a pendulum is non-linear. There has been a lot of research on linearization methods, basically techniques to convert non-linear equations to linear ones and then trying to solve them using linear state space control theory. Unfortunately, such linearization methods are very limited to specific classes of non-linear equations and cannot be generalized easily.

Further to the difficulty of solving non-linear equations, we of course need to know how to model a system (its corresponding equations) in the first place. This is the reason that traditional control strategies, also referred to as **model driven control** , still exclude a lot of systems that we do not know how to model (whose system equations are not known). And, the complexity of such systems is only increasing day by day, where we want to solve hyper-scale problems, e.g., climate control, disease control, automated vehicles, financial markets, etc.

To summarize the limitations of traditional control theory / model driven control:

* System models / equations are not known
* Do not work for large-scale non-linear domains
* Simulation of such systems are also very difficult given their high dimensionality

For a detailed discussion on this topic, refer to Steve Burton’s excellent [tutorial](<https://www.youtube.com/watch?v=Pi7l8mMjYVE>) on control systems.

## 2.2 ML / RL to the Rescue

Given the above challenges with traditional control theory, let us now try to understand why ML / RL based approaches show a lot of promise in this context.

> The underlying logic here is that even for a very high dimensional system that we cannot model, there are dominant patterns that characterize the system behavior — and machine learning (deep learning) is very good at learning these patterns.

This would be an approximation, and while we still would not understand the system fully — it is good enough for most real-life use-cases (including predictions), barring some exceptional scenarios.

In this article, we focus on RL based approaches for industrial control systems. We will also touch upon the key differences between supervised ML and un/semi-supervised RL, and how this makes RL a good choice for potentially any control optimization problem.

**Reinforcement learning (RL)** is able to achieve complex goals by maximizing a reward function in real-time. The reward function works similar to incentivizing a child with candy and spankings, such that the algorithm is penalized when it takes a wrong decision and rewarded when it takes a right one — this is reinforcement. The reinforcement aspect also allows it to adapt faster to real-time changes in the user sentiment. For a detailed introduction to RL, please refer to our papers leveraging RL for [chatbots](<https://www.researchgate.net/publication/333203489_Self-improving_Chatbots_based_on_Reinforcement_Learning>) and [recommender systems](<https://ceur-ws.org/Vol-2820/AAI4H-10.pdf>).

Press enter or click to view image in full size

Fig. 4: Reinforcement Learning (RL) methodology (Image by Author)

Some interesting observations about RL — relevant for the following discussion on RL agents:

* _RL rewards and policies are not the same_ : The roles and responsibilities of the reward function vs. RL agent policies are not very well defined, and can vary between architectures. A naïve understanding would be that given an associated reward/cost with every state-action pair, the policy would always try to minimize the overall cost. Apparently, it seems that sometimes keeping the ecosystem in a stable state can be more important than minimizing the cost (e.g. in a climate control use-case). As such,

> the RL agent policy goal need not always be aligned with the reward function, and that is why two separate functions are needed.

* Similar to supervised approaches in machine learning / deep learning, the _RL approach most suitable for enterprise adoption is ‘model based RL’_.
In **model based RL** , it is possible to develop a model of the problem scenario, and bootstrap initial RL training based on the model simulation values.__ For instance, for energy optimization use-cases, a blueprint of the building heating, ventilation and air conditioning (HVAC) system serves as a model, whose simulation values can be used to train the RL model — detailed in Section 3.2. For complex scenarios (e.g. games, robotic tasks), where it is not possible to build a model of the problem scenario, it might still be possible to bootstrap an RL model based on historical values.

> This is referred to as ‘offline training’, and is considered a good starting point in the absence of a model. And, this is also the reason why RL is often considered as a hybrid between supervised and unsupervised learning, rather than a purely unsupervised learning paradigm.

* _Online and model-free RL remain the most challenging_ , where the RL agent is trying to learn and react in real-time without any supervision. Research in this field seems to lack a theoretical foundation at this stage. Researchers are trying out different approaches by simply throwing more data and computing power at the problems. As such, this remains the most “interesting” part of RL, with current research primarily focusing on efficient heuristics and distributed computation to cover the search space in an accelerated fashion.

> Applying DL (neural networks) to the different RL aspects, e.g., policies, rewards, also remains a hot topic — referred to as deep reinforcement learning.

* Given the fundamental nature of RL, there seems to be many interesting concepts that can be borrowed from existing research in _decision sciences and human psychology_. For example, an interesting quote from Tom Griffiths, from his presentation “[Rational use of cognitive resources in humans and machines](<https://cocosci.princeton.edu/papers/callawayrationaluse.pdf>)”:

> while mimicking the human brain seems to be the holy grail of AI/RL research; humans have long have been considered as essentially flawed characters in psychological studies. So what we really want to do is to mimic the “rational behavior” of the human brain.

The conclusion is of course that we need to bring the two fields together if we ever want machines to reach the level of true human intelligence.

## 3\. Reinforcement Learning Agents

Having established the potential of reinforcement learning for industrial control systems, we show how RL agents can be developed leveraging LLMs to fine-tune the RL agent reward function in this section.

### 3.1 LLM based fine-tuning of RL Reward Function

The key steps to perform LLM based fine-tuning of the RL agent reward function are as follows — illustrated in Fig. 5:

Press enter or click to view image in full size

Fig. 5: LLM based fine-tuning of RL Agent Reward Function (Image by Author)

1. Initial **prompt** to the LLM with the RL formulation of the <use-case>, outlining the objectives of the RL reward and policy functions; with (optional) examples of some rewards function templates.
2. LLM **generates** candidate RL reward functions with the ‘temperature’ parameter providing the exploration — exploitation balance with respect to novelty of the generated reward functions.
3. Validate the generated reward functions for relevance with respect to the given <use-case>; followed by their **evaluation** with respect to the <use-case> accuracy.
4. Add the generated reward functions with their evaluation results to LLM **memory** — for the LLM to improve its (future) generation process.
5. Repeat steps 2–4 until **convergence** is reached with respect to a threshold improvement in the RL agent reward function.

Finally, update the RL agent reward function with the top ranked LLM generated reward function. Fig. 5 outlines sample templates for the initial prompt and to store evaluation results of an iteration in LLM memory.

### 3.2 RL Agents for HVAC Optimization

In this section, we apply the outlined LLM based RL reward fine-tuning approach to a concrete use-case of optimizing HVAC consumption in buildings / factories.

We have previously studied RL based HVAC optimization in our 2021 paper: [Reinforcement Learning based Energy Optimization in Factories](<https://dl.acm.org/doi/10.1145/3396851.3402363>). It is an interesting case study in the context of our current discussion. It showcases the successful transition of an industrial control system run by a traditional PID (proportional integral derivative) controller for the last 10+ years — to a more efficient RL based controller.

> In this article, we primarily show that it is possible to re-create the RL based HVAC controller outlined in the paper, using the LLM based fine-tuning approach proposed in the previous section.

The industrial control system in this case refers to HVAC units responsible for maintaining the temperature and humidity settings in factories (buildings in general). The sensors correspond to the indoor (and outdoor) temperature and humidity sensors; and the actuators correspond to the cooling, heating, re-heating and humidifier valves of the HVAC units.

The RL model formulation of the HVAC optimization problem is illustrated in Fig. 6.

Press enter or click to view image in full size

Fig. 6: HVAC optimization — Reinforcement Learning formulation (Image by Author)

The RL **controller logic** can be summarized as follows: Given the zone state in terms of the (inside and outside) temperature and humidity values, the RL model needs to decide by how much to open the cooling, heating, re-heating and humidifier valves. To take an informed decision in this scenario, the RL model needs to first understand the HVAC system behavior, in terms say how much zone temperature drop can be expected by opening the Cooling valve to _X_ %?

Once the RL model understands the HVAC system behavior, the final step is to design the control strategy. For instance, the RL model now has to choose whether to open the cooling value to 25% when the zone temperature reaches _23_ degrees, or wait till the zone temperature reaches _24_ degrees before opening the cooling valve to _40_ %. Note that the longer it waits before opening the valve, contributes positively towards lowering the energy consumption. However, it then runs the risk of violating the temperature / humidity tolerance levels as the outside weather conditions are always unpredictable. As a result, it might actually have to open the cooling valve to a higher percentage if it waits longer, consuming more energy.

The above probabilities are quantified by the reward function illustrated in Equation 1, which assigns a reward to each possible action based on the following three parameters: setpoint closeness (SC), energy cost (EC), tolerance violation (TV).

Press enter or click to view image in full size

> Given this, we were able to leverage the LLM based fine-tuning approach to refine both ‘safe’ and ‘business first’ control strategies to an ‘energy optimal’ policy.

* ‘Safe’ control strategy: assign a very high negative weightage (penalty) to tolerance violations, ensuring that they never happen — albeit at a higher energy cost.
* Setpoint closeness encourages a ‘business first’ policy where the RL model attempts to keep the zone temperature as close as possible to the temperature / humidity setpoints, implicitly reducing the risk of violations — but at a higher energy cost.
* ‘Energy optimal’ prioritizes energy savings over the other two parameters.

## 4\. Conclusion

When we talk about AI agents today, we mostly talk about LLM agents, which loosely translates to prompting an LLM to perform NLP tasks. In this article, we highlighted the fact that some agentic tasks can be better suited to other ML techniques, e.g., reinforcement learning (RL), predictive analytics, etc.

More concretely, we focused on RL agents, and showed how LLMs can be used to fine-tune the RL agent reward / policy functions. We showed a concrete example of applying the fine-tuning methodology to a real-life industrial control system — designing the RL based controller for HVAC optimization in a building setting. The proposed RL fine-tuning methodology shows promise to be applied to a wide range of RL agentic tasks.
