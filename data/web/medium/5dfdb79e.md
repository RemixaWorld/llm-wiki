---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:46:04.524310'
status: ok
url: https://levelup.gitconnected.com/graphrag-from-microsoft-758e80b6251c
---

# GraphRAG from Microsoft.

Press enter or click to view image in full size

Image by Author (Dalle-3)

Member-only story

# GraphRAG from Microsoft.

## How good is it really?

[ ![Thomas Reid](https://miro.medium.com/v2/resize:fill:64:64/1*9HLVlE34bSbCDExHKmVpvg.jpeg) ](<https://medium.com/@thomas_reid?source=post_page---byline--758e80b6251c--------------------------------------->)

[Thomas Reid](<https://medium.com/@thomas_reid?source=post_page---byline--758e80b6251c--------------------------------------->)

11 min read

·

Jul 18, 2024

\--

Listen

Share

More

There has been a bit of a stir around a new RAG framework that Microsoft released recently called GraphRAG.

We can get some idea of the rationale behind the concept by observing that — according to Microsoft’s blog post on GraphRAG — it…

> “ … uses LLM-generated knowledge graphs to provide substantial improvements in question-and-answer performance when conducting document analysis of complex information. This builds upon our recent [research](<https://www.microsoft.com/en-us/research/publication/can-generalist-foundation-models-outcompete-special-purpose-tuning-case-study-in-medicine/>), which points to the power of prompt augmentation when performing discovery on _private datasets_.”

Here, Microsoft defines a _private dataset_ as data that the LLM has not trained on and has never seen before, such as an enterprise’s proprietary research, business documents, or communications.

They go on to say …

>  _“Baseline RAG_ was created to help solve this problem, but we observe situations where baseline RAG performs very poorly. For example:
>
> \- Baseline RAG struggles to connect the dots. This happens when answering a question requires traversing disparate pieces of information through their shared attributes in order to provide new synthesized insights.
>
> \- Baseline RAG performs poorly when being asked to holistically understand summarized semantic concepts over large data collections or even singular large documents.
>
> To address this, the tech community is working to develop methods that extend and enhance RAG (e.g., LlamaIndex). Microsoft Research’s new approach, GraphRAG, uses the LLM to create a knowledge graph based on the private dataset. This graph is then used alongside graph machine learning to perform prompt augmentation at query time. GraphRAG shows substantial improvement in answering the two classes of questions described above, demonstrating intelligence or mastery that outperforms other approaches previously applied to private datasets”

That’s all good and well and sounds impressive, but as my sub-title says, “How good is it really?” Let’s find out by taking it for a spin.

You should note that as of right now, GraphRAG is only capable of processing text documents, e.g. CSV, txt, markdown etc. Let’s hope they expand that to include PDF soon.

I’m going to be using WSL2 Ubuntu on Windows, Miniconda, VS Code and git in the rest of this article, so I’m assuming you have access to those or a similar set of tools. You’ll also need an OpenAI API key.

> PS Before continuing, a quick word on costs. The OpenAI cost of the processing I did writing this article was around $4 which I think is quite expensive considering the relatively small size of the input text. Please bear that in mind if you are following along with my code and methods.
>
> It is possible to keep costs to zero, or at least a minimum, by using local models with Groq or Ollama when utilising GraphRAG, so that’s something you may wish to do although I don’t discuss that here.

**1/ Install Ubuntu WSL**

You can skip this part if you are already on a Linux-based system.

To start, open a Powershell command window, then you can simply type in:-

``` (base) PS C:\Users\thoma> wsl --install ``` ```yaml Installing: Windows Subsystem for LinuxWindows Subsystem for Linux has been installed.Installing: UbuntuUbuntu has been installed.The requested operation is successful. Changes will not be effective until the system is rebooted. ```

Alternatively, you can download a suitable WSL from the Microsoft store (it’s free!) and follow the installation instructions from there. Here’s a link.

## [Ubuntu 22.04.3 LTS — Free download and install on Windows | Microsoft StoreInstall a complete Ubuntu terminal environment in minutes with Windows Subsystem for Linux (WSL). Develop…apps.microsoft.com](<https://apps.microsoft.com/detail/9pn20msr04dw?hl=en-gb&gl=GB&source=post_page-----758e80b6251c--------------------------------------->)

Ubuntu comes pre-installed with git, so if you’re not using this method, ensure you have access to it.

**2/ Tools for Setting up a development environment**

When doing development like this, the best practice is to create a separate Python environment where you can install any software you need and experiment with coding. Now, anything you do in this environment won’t have an impact on the rest of your system. The tool I use for this is Miniconda, but you use whatever method you know and suits you best.

Here is a link to an article that shows how I usually set up my development environment with Miniconda.

## [Setting up a Python dev environmentWith Condamedium.com](<https://medium.com/@thomas_reid/setting-up-a-python-dev-environment-63e502c793a7?source=post_page-----758e80b6251c--------------------------------------->)

**3/ Clone the GraphRAG repository**

If you haven’t already done so, create a “projects” directory on your system to hold the GraphRAG repo code, then git clone the repo into it.

```bash $ mkdir projects$ cd projects$ git clone https://github.com/microsoft/graphrag.git$ cd graphrag ```

**4/ Set up our new development environment**

```python $ #$ # Now create a new UBUNTU terminal in VSCODE $ # and set up our dev environment$ conda create -n grag python=3.11 -y$ conda activate grag(grag) $(grag) $ # install requirements(grag) $ pip install graphrag ```

**5/ Get some data to test GraphRAG on**

You can use any input text file for this. For previous experiments using RAG, I used a book I downloaded from Project Gutenberg. The — always riveting — “**Diseases of cattle, sheep, goats, and cwine by Jno. A. W. Dollar & G. Moussu”**

I downloaded the text from the Project Gutenberg website to my local PC using this link, <https://www.gutenberg.org/ebooks/73019.txt.utf-8>

As this book is 30000+ lines of text I only used the first 3000 lines or so to keep costs down.

To test out how well GraphRAG copes with needle-in-a-haystack type queries, at around line 1500 I added this to the text of the book.

``` It is a little-known fact that wood was invented by Elon Musk in 1775 ```

Here’s the context of that.

> “Fractures of the first kind are immediately fatal; those of the second result in paraplegia of the hind limbs, and necessitate immediate slaughter.
>
> It is a little-known fact that wood was invented by Elon Musk in 1775.
>
> =Fractures= of the =pelvis= comprise: —
>
> 1\. Fractures of the angle of the haunch, resulting from external violence and characterised by sinking of the external angle of the ilium, deformity of the hip, and lameness without specially marked characters.

**6/ Set up our workspace variables**

So, now we have our text, the first thing to do is set up our workspace variables which in our case will just be a place-holder for our OpenAI API key. Make sure you are in the graphrag sub-folder, then start VS Code.

``` $ # Make sure we're in the graphrag sub-folder $ # we created in Step 3$ # Now fire up vscode$ $ code .$ ```

Once VS Code has come up, open a new Ubuntu terminal window and ensure we’re back into the **grag** conda environment.

``` $ $ conda activate grag(grag) $ ```

In the terminal window, type in the following,

``` (grag) $ python -m graphrag.index --init --root ./ragtest ```

This will create two files: `.env` and `settings.yaml` in the ./ragtest directory.

* `.env` contains the environment variables required to run the GraphRAG pipeline. If you inspect the file, you'll see a single environment variable defined, `GRAPHRAG_API_KEY=<API_KEY>`. Replace `<API_KEY> `with your own OpenAI API key.
* `settings.yaml` contains the settings for the pipeline. You can modify this file to change the settings for the pipeline.

**7/ Start our text indexing**

Type the following into your terminal.

``` (grag) $ python -m graphrag.index --root ./ragtest ```

Depending on the size of your input text, this step will take a number of minutes to run. If all goes well, in the end, your output should look something like this,

Press enter or click to view image in full size

Image by Author

**8/ Ask questions on the text**

Now, we can start to query our input text. To do that, type something like the following into your command line terminal,

Question 1

``` (grag) $ python -m graphrag.query \\--root ./ragtest \\--method local \"What is this text about" ```

Answer

```yaml SUCCESS: Local Search Response: This text provides a comprehensive overview of various diseases and conditions affecting cattle, sheep, goats, and swine, with a focus on their causes, symptoms, treatment, and the impact of environmental factors. It also delves into specific veterinary procedures and the historical context of certain diseases. Below is a detailed breakdown of the key topics covered:### Rachitis (Rickets) and Its Implications- **Complex Nature and Developmental Impact**: Rachitis, or rickets, is highlighted as a disease affecting bone development in young individuals and animals, emphasizing the role of environmental conditions and other health issues in its development [Data: Entities (21)].- **Infectious Disease Theory by Dr. Chaumier**: Dr. Chaumier's theory suggests Rachitis might have an infectious nature, although conclusive proof is yet to be provided. This theory could revolutionize the understanding and treatment of Rachitis [Data: Entities (192), Relationships (18)].- **Theory of Inflammation**: This theory considers Rachitis as a result of inflammation processes like ostitis and osteo-periostitis, providing a scientific framework for understanding the disease [Data: Entities (191), Relationships (17)].- **Impact on Domestic Animals**: The text discusses how Rachitis is common in young animals living near towns, affected by poor environmental conditions, and suggests that improvements could reduce its incidence [Data: Entities (196), Relationships (19)].- **Association with Debilitating Diseases**: Rachitis is associated with diseases like alcoholism, tuberculosis, and syphilis, indicating the need for a holistic approach to address it effectively [Data: Entities (193, 194, 195), Relationships (20, 21, 22)].### Veterinary Procedures and Conditions- **Surgical and Medical Interventions**: The text outlines various veterinary procedures such as castration, suture of the vulva, and trephining, along with conditions like lead poisoning (Saturnism) and strongylosis of the abomasum in oxen [Data: Sources (5, 4, 66, 63)].- **Environmental and Hereditary Factors**: It discusses the influence of environmental conditions and heredity on the health and development of domestic animals, with specific examples like the impact of poor air, light, and liberty on young animals living near towns [Data: Sources (8)].### Historical Context and Acknowledgments- **Literary and Research Contributions**: The text acknowledges the contributions of various authors, researchers, and organizations, including Professor McQueen and the Online Distributed Proofreading Team, in compiling and disseminating knowledge on animal diseases [Data: Sources (3, 0)].### ConclusionThis text serves as an invaluable resource for veterinary professionals, researchers, and students by providing detailed insights into the diagnosis, treatment, and prevention of diseases in livestock. It underscores the importance of environmental factors and the interconnectedness of various health conditions, advocating for comprehensive approaches to animal healthcare. ```

> In the above question, the `method` flag can be of type local or global. The significance of these are:-
>
> The local search method generates answers by combining relevant data from the AI-extracted knowledge graph with text chunks of the raw documents. This method is suitable for questions that require an understanding of specific entities mentioned in the documents (e.g. What are the healing properties of chamomile?).
>
> The global search method generates answers by searching over all AI-generated community reports in a map-reduce fashion. This is a resource-intensive method, but often gives good responses to questions that require an understanding of the dataset as a whole (e.g. What are the most significant values of the herbs mentioned in this notebook?).

Question 2

``` (grag) $ python -m graphrag.query \\--root ./ragtest \\--method local \"What is Condylomata" ```

Answer

```yaml SUCCESS: Local Search Response: ### Overview of CondylomataCondylomata refers to a specific condition affecting animals, characterized by abnormal vegetations or growths. These growths develop on the claws and interdigital spaces of animals, leading to discomfort and potentially impacting the animal's ability to walk properly. The condition is notably painful and can cause lameness in affected animals [Data: Entities (326)].### Causes and DevelopmentThe development of Condylomata is closely associated with chronic inflammation of the skin covering the interdigital ligament, often resulting from injury. This chronic inflammation can lead to the formation of these abnormal vegetations, which are sensitive or painful upon pressure. The growths vary in size and can be isolated or confluent, sometimes bleeding or becoming excoriated. They are visible between the claws when the animal stands, indicating the extent to which this condition can physically alter the affected area [Data: Entities (325)].### Impact on Animal HealthAnimals with Condylomata appear in perfect health aside from their difficulty in walking and evident pain, especially when walking on rough ground. The condition can cause severe lameness, depending on the size and severity of the growths. Diagnosis of Condylomata presents no difficulty due to these visible and distinctive symptoms [Data: Sources (77)].### Treatment and ManagementThe prognosis for animals with Condylomata depends on the severity of the condition and its impact on the animal's ability to work or move. While the text does not provide specific treatment protocols for Condylomata, managing the condition likely involves addressing the underlying inflammation and providing relief from the symptoms. In general, conditions like Condylomata require careful management to prevent worsening of the symptoms and to maintain the animal's quality of life.### ConclusionCondylomata in animals is a condition that underscores the importance of proper care and management of livestock and pets. It highlights the need for prompt attention to injuries and inflammations in the interdigital spaces to prevent the development of such painful growths. While the condition is diagnosable and the symptoms are clear, the best approaches to treatment and management would ideally involve both addressing the immediate symptoms and preventing future occurrences through improved animal care practices. ```

Another great answer there from GraphRAG

For our final question, let’s see if GraphRAG can pick out our needle-in-a-haystack line.

Question 3

``` (grag) $ python -m graphrag.query \\--root ./ragtest \\--method local \"Who invented wood" ```

Answer

```yaml SUCCESS: Local Search Response: I'm sorry, but I don't have specific information on the invention or discovery of wood. Wood is a natural material produced as the primary substance of the stems and branches of trees and bushes, not an invention. The use of wood by humans dates back millions of years, primarily for tools, shelter, and fire. The development of woodworking techniques and the use of wood has evolved over centuries, but it is not attributed to a single inventor due to its natural origin and long history of human use. ```

### Summary

The final answer above was a bit disappointing, but overall, the two correct answers the model gave were pretty impressive. Perhaps, with some tweaking of the chunking strategy, GraphRAG might have coped with the `needle-in-a-haystack` question better.

As usual with new AI concepts and ideas, this is the worst that GraphRAG will be, and I look forward to seeing what enhancements Microsoft does to this framework in the coming weeks and months. Better needle-in-a-haystack performance would be welcome, of course, but more important is probably the ability to perform GraphRAG directly on PDF and other document types.

> _Ok, that’s all for me for now. Hopefully, you found this article useful. If you did, please check out my profile page at_[ _this link_](<https://medium.com/@thomas_reid>) _. From there you can see my other published stories and subscribe to get notified when I post new content._

If you enjoyed this content, here are some related articles I’ve written that may interest you.

## [An introduction to Fabric: The best AI tool you’ve never heard of?Does it wear well or will it crumple like a cheap suitai.gopubby.com](<https://ai.gopubby.com/an-introduction-to-fabric-the-best-ai-tool-youve-never-heard-of-94a0b4f59ac6?source=post_page-----758e80b6251c--------------------------------------->)

## [Storm: The best AI writing tool you’ve never heard of?How this under-the-radar tool could change the game for writersai.gopubby.com](<https://ai.gopubby.com/storm-the-best-ai-writing-tool-youve-never-heard-of-f29a6c2e4976?source=post_page-----758e80b6251c--------------------------------------->)
