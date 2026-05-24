---
domain: medium.com
fetch_date: '2026-05-18T12:52:37.546615'
status: ok
url: https://medium.com/@tranthetruyen/modern-ai-for-drug-discovery-3ef5cdf884ac
---

# Modern AI for drug discovery

[ ![Truyen Tran](https://miro.medium.com/v2/resize:fill:64:64/1*ZYl-i9gSpTgxt5wWPIIw0g.png) ](</@tranthetruyen?source=post_page---byline--3ef5cdf884ac--------------------------------------->)

[Truyen Tran](</@tranthetruyen?source=post_page---byline--3ef5cdf884ac--------------------------------------->)

15 min read

·

Jan 22, 2025

\--

\--

Listen

Share

More

_The journey from the “medicine” made from steamed buns dipped in executed prisoners’ blood in Lu Xun’s 1919 short story to modern AI-designed medicine in 2019 represents a remarkable leap in human progress and scientific advancement — spanning just 100 years, or about four generations. While pharmaceuticals and AI might seem unrelated at first glance, AI has proven particularly well-suited for pharmaceutical and medicinal chemistry applications. This article will explain why._

![image](https://miro.medium.com/v2/resize:fit:700/1*vZD_sqrJt9t-T5qExXlYWw.png)

**The pharmaceutical industry is undergoing dramatic changes**

It costs $2.6 billion and takes 14 years to develop a single drug, with no guarantee that patients will respond well to it! What if one day drugs could be designed _on-demand_ for individuals by computers and manufactured in mobile labs?

In 2019, I met Alex Zhavoronkov, CEO of Insilico, an AI pharmaceutical startup, at the ICLR conference. He predicted that if Big Pharma companies don’t embrace AI, they will decline. Insilico’s strategy is to partner with Chinese pharmaceutical companies rather than those in Europe, America, or Japan, citing China’s flexible environment, abundant AI talent, and substantial financial resources. There appears to be a significant shift occurring in the world’s creative centers [[1](<https://substack.com/home/post/p-155212999#footnote-1-155212999>)].

Mid-2019 brought news as significant as AlphaFold [[2](<https://substack.com/home/post/p-155212999#footnote-2-155212999>) ]or GPT-2 [[3](<https://substack.com/home/post/p-155212999#footnote-3-155212999>)]. For the first time, AI successfully designed a drug that reached mouse trials — and showed promising effects in the test animals. The total development time before testing was just 46 days, a remarkable achievement considering this process typically takes up to a year. This marked the first instance of an AI-designed product showing efficacy in mice. While this wasn’t yet in humans, so tempered excitement is warranted, it will take many more years of human trials and efficacy assessments.

In 2021, their AI-discovered drug for idiopathic pulmonary fibrosis reached the preclinical candidate stage. This achievement is particularly significant because gaining FDA approval is incredibly challenging, involving multiple stages and typically requiring over a decade and billions of dollars. The recent slow pace of approvals demonstrates how difficult it is to discover new drugs today, highlighting the need for breakthroughs. AI represents a promising direction, and Insilico has established itself as a pioneering startup with impressive scientific publications.

**AI-driven drug discovery**

I’ll explain how AI approaches drug discovery from an AI perspective. Since I’m not a biologist or chemist, I’ll approach the problem as an AI expert would: starting with data representation. AI looks for ways to represent data whenever predictions need to be made or artifacts generated. That’s how AI views the world.

A drug is a small molecule that binds to a biological target. These targets are usually proteins, though they can be other substances like RNA. This binding changes the target’s function, producing the desired therapeutic effect. By this definition, caffeine is a drug because it alters your mental state and has specific effects. The same applies to alcohol.

A protein is a large molecule composed of chains of amino acids. Each element is as small as a drug molecule, but the entire protein forms a large structure.

Drug molecules are typically represented as graphs, where nodes represent atoms and edges represent the bonds between them. Proteins have complex 3D structures that depend on how they fold in space, twisting like ribbons. When they interact, drugs bind to proteins to create therapeutic effects.

Drug discovery is the process of finding molecules with desired therapeutic effects. This process is extremely complex because it requires understanding chemistry, biology, medicine, and many other fields to create an effective treatment with minimal side effects. For a molecule to be considered a viable drug, it must meet certain criteria. For example, it must be water-soluble and able to function effectively in the body and bloodstream. It must also be small enough and possess several other specific characteristics.

In the traditional process, it takes about 10 years or more to progress from initial idea to an approved drug on the market. The cost typically exceeds a billion dollars, and many laboratory mice must be used in testing. The process is expensive because researchers must screen through approximately a million molecules to identify about a thousand potential candidates. From those thousand, only one molecule might ultimately become a drug.

Then came AI-enabled processes. While these have been in use for some time, they have accelerated significantly in the last three years. The approach differs substantially from the traditional method. Here is one of the processes proposed by Insilico (as of 2019):

![image](https://miro.medium.com/v2/resize:fit:700/1*IYV9dlVPS2ilRYA33dD6FQ.png)

In this process, they propose using AI in all steps.

In today’s discussion, we’ll focus mainly on the middle part: _how to identify and create a molecule that can achieve the desired effect_.

**Fundamental questions**

In this field, researchers try to answer three types of questions:

_First_ , given a molecule, we need to answer questions like: Does it have drug-like properties? Does it have a target to bind to? How does it affect that target? What effects does it have in the body? How does it interact with food and drinks? How is it absorbed and discharged? Answering such questions helps researchers preliminarily assess whether the molecule merits further investigation.

_The second question_ , which is more challenging, is: Given a target we want to modify, which molecules could affect that target? This is particularly difficult because even after researchers identify the disease and specific biological targets that need modification, finding the right molecule can take many years.

If we have a list of available molecules, we can rank them and select the best candidate. However, in most cases, this list isn’t readily available. Therefore, we must propose molecules in chemical formula form, hoping they can be synthesized in the laboratory.

_The third question_ is: Given a chemical formula, is it possible to synthesize the molecule? If so, how? In AI terms, this problem resembles planning: You start with the goal you want to achieve and work backwards. We need to identify what steps to take, starting from the most basic molecules and working through reaction chains to reach the desired molecule.

**How to represent drugs for computers**

Like any AI application today, the process begins with data representation [[4](<https://substack.com/home/post/p-155212999#footnote-4-155212999>)]. We need to present molecules in a format that computers can process effectively.

**Vectors** provide one convenient format for computers. Expressing an artifact as a vector is also called embedding it in a high-dimensional space. Vectors are particularly useful because they’re easy to work with and support many types of algorithms. They can be added, subtracted, transformed, multiplied, or modified with random noise.

Chemists have long used a clever format called “fingerprints” for this purpose. Fingerprints work by counting small characteristic patterns in a molecular graph, such as benzene rings or hydrogen bonds.

More recently, researchers have employed convolutional networks on molecular graphs to learn new types of fingerprint representations without relying on predefined chemical rules. The results have been very encouraging, demonstrating that neural networks can learn useful molecular representations directly from data.

Once you have vectors, many possibilities open up. You can use autoencoders, GANs, and numerous other methods. For instance, we can learn hidden representations of fingerprints in a lower-dimensional space through VAE (Variational Auto-Encoder) algorithms. This hidden space allows for easier optimization and can generate new fingerprints — essentially creating new molecules. I’ll return to this topic later.

Another common molecular format uses **character strings** , specifically the SMILES format. This approach converts a graph into a character string that’s well-suited for computer processing. The conversion follows specific grammar rules.

From an AI perspective, this opens up possibilities for all kinds of string processing. We can employ CNNs, RNNs, attention mechanisms, Transformers, memory networks, or reinforcement learning.

However, strings have several limitations. First, they can’t always be consistently converted back and forth to graphs. Strings have more degrees of freedom than graphs, and when representing molecules as strings, crucial 3D information is lost — information that’s essential for calculating many molecular properties. Sometimes two atoms that are close together in a graph can end up quite far apart in the string representation.

Therefore, you might think the best way to represent drug molecules would be to use **graphs** directly. However, graphs present their own challenges for computer processing. Graphs don’t have fixed sizes or fixed orders — you can permute a graph’s elements and it remains the same graph. We also lack good models for generating graphs. While we have effective autoregressive models for generating sequential data, such as RNN or GPT, generating graphs is more complicated because their topological structure has no fixed size, and there’s no straightforward way to address permutation invariance.

**Graph Memory Network Model**

The RDMN (Relational Dynamic Memory Network) is one of the representation models we developed in 2018, drawing inspiration from memory networks. Let me explain how it works:

![image](https://miro.medium.com/v2/resize:fit:700/1*Nz1W1HdNdnYICQs7eJns3g.png)

The model processes graph-structured data in a flexible way. It begins by taking a drug molecule graph as input. Each atom is then embedded in a high-dimensional space as a vector (essentially, a point in that space). These embedding vectors collectively form a working memory, similar to how our brains maintain active information when tackling complex tasks like solving difficult problems or programming.

The atoms communicate with each other through their bonds in a process we call “message passing.” Each time a message is transmitted, the embedding vector is updated based on information received from neighboring atoms. This updated information is then passed along to adjacent atoms. To enhance this process, a central controller supplements the message passing by collecting global information from all atoms and broadcasting it back during the next message passing step. This means every atom ultimately receives information from every other atom in the molecule. Finally, the controller gathers all this information to produce an output, which could be a prediction or something entirely new.

**Protein representation**

Proteins are chains of amino acids that can be encoded using a vocabulary of about 20 characters, creating a 1D sequence. These sequences can range from hundreds to thousands of characters in length.

The challenge with this 1D representation is that it’s quite different from the actual 3D structure found in nature. Converting from 1D to 3D structure is particularly difficult. As of November 2019, no one had developed a truly effective model for transforming a 1D sequence into its 3D folded structure. While DeepMind’s AlphaFold represented the most advanced method at that time, it still hadn’t achieved the desired level of accuracy [[5](<https://substack.com/home/post/p-155212999#footnote-5-155212999>)].

The advantage of 1D structures is that they’re compatible with many natural language processing (NLP) techniques. We can apply methods like word2vec, ELMO, BERT, or GPT to analyze these protein sequences. As a result, research into using NLP techniques for protein encoding has become quite active.

**Drug-target interactions**

How do proteins and molecules interact with each other? This question falls under the domain of drug-target binding or drug-target affinity prediction. One notable approach, the GraphTDA method, combines graph convolutional networks to process drug graphs with CNN to analyze protein sequences. While conceptually straightforward, this intuitive approach has proven quite powerful.

From a machine learning perspective, we can frame the drug-target interaction problem as a form of question answering, using a triple format: <query, context, answer>. The answer might indicate whether an interaction exists, how strong it is, or where the binding sites are located. Depending on how we frame the problem, the drug can play the role of either query (as in the GraphTDA model, where the protein acts as context) or context (as in the RDMN model, where the protein is embedded in the query).

**Drug repurposing**

Once we understand the target, a practical question emerges: can existing drugs be repurposed for this new challenge? This approach is particularly appealing because, as mentioned earlier, developing new drugs is extremely costly and time-consuming, requiring billions of dollars and many years [[6](<https://substack.com/home/post/p-155212999#footnote-6-155212999>)]. Fortunately, experience has shown that many drugs developed for one purpose can be effective for other applications.

Last year, we approached this challenge using the RDMN model described earlier. The RDMN structure allows us to use the target (such as a protein or cancer cell) as a query, while treating the drug molecule graph as context. This means we can query the same context (drug) with different targets. Our research demonstrated that training different targets on the same model produces better results than training them individually.

This approach revealed two important insights: first, one drug can affect multiple targets. Second, joint training functions as a form of multitask learning — an useful strategy in modern machine learning.

However, the RDMN model has a limitation: it requires separate computation for each target, making training time-consuming and making it difficult to fully leverage similarities between targets. To address this, we developed an improved model called GAML (Graph Attention Multi-Label). While I won’t go into the technical details here, the key innovation is that it allows us to expand the number of outputs with minimal computational cost. For example, we successfully experimented with analyzing five types of cancer simultaneously, or processing 50 proteins at once. By predicting multiple targets simultaneously, we typically achieve better results than predicting each target individually, especially for targets with limited training data. The model also allows us to incorporate information about interactions between targets.

**Drug-drug interactions**

Another crucial consideration in drug development is the potential for unwanted interactions between different drugs. A good doctor typically asks about other medications you’re taking before writing a prescription, because drugs can interact with each other in the body, sometimes producing undesirable effects. Therefore, it’s essential to understand in advance which drugs might interact and what consequences these interactions might have.

We revisited the RDMN model to address this challenge. As mentioned earlier, RDMN takes a graph (representing a drug) as input. A straightforward approach to handling multiple graphs simultaneously would be to treat them as subgraphs within a larger graph. However, this method doesn’t adequately account for the local properties of each subgraph. To solve this, we expanded RDMN’s memory to include multiple components, with each component handling one graph.

We applied this enhanced RDMN to predict chemical-chemical interactions, achieving promising results, thanks to the model’s flexibility in combining context, environment, and various other features. When tested against standard datasets, our approach outperformed previously established techniques.

**Molecular optimization**

Now we come to the final aspects of drug development: designing new drug structures and developing synthesis processes for the laboratory. These represent both the most important and most challenging aspects of the process, and research in these areas remains very active.

When you have a structure that shows promise as a potential drug, you need to optimize it to best achieve the desired goals. One approach treats this as a discrete space search problem: starting from a known structure, you sequentially add or remove components to optimize the target objectives. An alternative approach views it as a machine translation problem, where the initial structure serves as the source language and the optimized structure as the target language.

**Generative molecular design**

But what if you don’t have an initial drug structure to begin optimizing? This is where generative design comes in — an extremely challenging yet fascinating problem.

From an AI perspective, drug design can be viewed as structured prediction, machine translation, or conditional generation [[7](<https://substack.com/home/post/p-155212999#footnote-7-155212999>)]. The main challenge lies in the fact that drugs are not sequences but graphs. Generating graphs with desired properties remains an open and significant challenge in machine learning.

This raises an important question: which representation should we use? If we’re working with sequences, the technology is quite mature. But working with graphs presents much greater challenges.

One of the most active areas of research involves using VAE (Variational Auto-Encoder) to model the distribution of molecules, thereby realizing AI’s dream of exploring the entire chemical space. VAE is a relatively simple yet elegant probabilistic architecture, and its application to molecular space creates some truly remarkable possibilities.

Researchers have shown that instead of processing molecular graphs directly, we can use VAE to embed them in a continuous space of, for example, 256 dimensions. This is particularly valuable because molecular space is discrete and astronomically large, making direct processing extremely challenging even with supercomputers. In contrast, a 256-dimensional continuous space can be processed effectively even with personal computers.

To accomplish this, we first represent a molecule using SMILES string notation, then pass it through a CNN encoder to convert it into a vector. VAE works directly with these vectors, further reducing the number of dimensions. This process effectively compresses a SMILES string into a vector with manageable dimensions. To recover the SMILES string, we construct a symmetrical decompression architecture.

This architecture allows us to generate SMILES strings according to the distribution learned from the data. In practical terms, this means we can design new molecular structures simply by random sampling in the compressed space, then decompressing into SMILES strings. We can also optimize molecules by moving through VAE’s compressed vector space, using Bayesian optimization or other continuous optimization techniques.

However, recovering the original graph from a SMILES string presents its own challenges leading to a low rate of generating valid graphs. An intermediate structure called Junction Tree, introduced in 2018, bridges the gap between sequences and graphs. This approach converts the original graph into a tree form where each “node” represents a subset of nodes from the original graph, making it possible to recover the original graph completely. The tree structure allows us to apply extended techniques from sequence architecture. For instance, we can encode the tree with VAE and embed it in a multi-dimensional continuous space, enabling optimal search for new trees. The trade-off is that computation on Junction Trees is considerably more complex.

**Graph design using reinforcement learning**

While using VAE or generative models offers mathematical elegance, it faces two key challenges. First, models learn distribution from known data, making it difficult to generate entirely new data outside the support region. In other words, they interpolate to generate new molecules that lie between known molecules. Second, we must work through an intermediate representation, while our primary concern is the expected properties of the molecule.

Reinforcement learning methods help address these limitations. We can view graph design as a sequence of building operations performed step by step. At the sequence’s conclusion, we have a graph whose properties we can evaluate through established rules, intermediate models, or quantum simulation.

![image](https://miro.medium.com/v2/resize:fit:700/1*joO4C9K5zEJ1Q2KRESzOhA.png)

_You et al. “Graph Convolutional Policy Network for Goal-Directed Molecular Graph Generation.” NeurIPS (2018)._

**Molecular synthesis process**

After developing a promising molecular design, the next question becomes: how can we synthesize it in the wet lab? Typically, we rely on chemical reactions to synthesize new substances from known ones.

This presents two challenges for AI. Assuming we know all possible chemical reactions, we can plan a sequence of reactions starting from available substances to create the desired compound. This plan should be fast, cost-effective, and safe.

However, not all reactions are known beforehand, which raises the challenge of predicting reaction results.

We recently published a paper at KDD’19 addressing this topic. We demonstrated that we can predict chemical reaction products with sufficient accuracy using a new technique called PGPN (Graph Transformation Policy Network), which combines reinforcement learning and graph representation. The core insight is that chemical reactions can be viewed as a graph morphism problem: Molecules are treated as sub-graphs of a larger graph, and chemical reactions essentially change the bonds between atoms without altering the atoms themselves. In other words, the post-reaction graph only changes in structure, not in composition.

**New playground**

With all these advances, we now have a complete playground for evaluating steps in chemical and pharmaceutical processes. MOSES provides an excellent example of such a platform:

![image](https://miro.medium.com/v2/resize:fit:700/1*R79aFDP3jv8ndDFTzwVVOQ.png)

Good luck exploring these exciting possibilities!

[_Compiled from presentation prepared for VietAI Summit November 2019 and Facebook posts in 2020–2021_]

**Notes**

[[1](<https://substack.com/home/post/p-155212999#footnote-anchor-1-155212999>)] Note 20/1/2025: This is increasingly true, especially as Europe is preoccupied with AI regulation and falling behind in the race with the US and China. Japan has missed its chance in this AI wave.

[[2](<https://substack.com/home/post/p-155212999#footnote-anchor-2-155212999>)] Update 20/1/2025: AlphaFold is an AI system that calculates the 3D structure of proteins when given their amino acid sequence formula. AlphaFold 2 version was tremendously successful, creating a revolution in Biology, earning its two main authors the 2024 Nobel Prize in Chemistry.

[[3](<https://substack.com/home/post/p-155212999#footnote-anchor-3-155212999>)] Note 20/1/2025: GPT-2 made a strong impression in the research community, but it wasn’t until GPT-3 that we saw a truly large language model with 175 billion parameters. Only with GPT-3.5 did clear chatbot-like signs emerge. ChatGPT, launched in November 2022, was based on GPT-3.5.

[[4](<https://substack.com/home/post/p-155212999#footnote-anchor-4-155212999>)] Note 20/1/2025: If you’re only using large language models (LLMs), you might not need this. Everything has been prepared in advance in the model.

[[5](<https://substack.com/home/post/p-155212999#footnote-anchor-5-155212999>)] Note 20/1/2025: Just a few years later, AlphaFold 2 and more recently AlphaFold 3 have become very accurate, reaching experimental error margins!

[[6](<https://substack.com/home/post/p-155212999#footnote-anchor-6-155212999>)] Note 21/1/2025: The COVID-19 pandemic occurred unexpectedly, making designing new drugs from scratch unfeasible.

[[7](<https://substack.com/home/post/p-155212999#footnote-anchor-7-155212999>)] Note 21/1/2025: This article was written in 11/2019, when AI generation wasn’t yet a significant topic. But just 1 year later, and especially 3 years later, with the emergence of ChatGPT in November 2022, everything has completely changed.
