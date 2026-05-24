---
domain: netraneupane.medium.com
fetch_date: '2026-05-18T12:57:00.034836'
status: ok
url: https://netraneupane.medium.com/gliner-zero-shot-ner-outperforming-chatgpt-and-traditional-ner-models-1f4aae0f9eef
---

# GLiNER: A Zero-Shot NER that outperforms ChatGPT and traditional NER models

**Named Entity Recognition(NER)** is a natural language processing (NLP) method that seeks to locate and classify named entities mentioned in unstructured text into predefined categories(person names, organization, locations, time expression, monetary values, etc)[1]. NER identifies, categorizes and extracts the most important pieces of information from unstructured text without requiring time-consuming human analysis.

### Workings

Named entities are specific words or phrases that refer to real-world objects such as people, organizations,locations, dates etc. NER aims to locate and categorize these entities into predefined categories. For the sake of simplicity, let’s say our model has been trained only for Person, Location, Organization, and Time entity types. Let me explain it in more details by adding an example. In the following diagram, Person and Location entities have been extracted by the NER.

![](https://miro.medium.com/v2/resize:fit:700/1*3aONn43mHjgcKt_gh0Lb9Q.png)

In this example, a person name consisting of one token, a two-token company name and a temporal expression have been detected and classified.In the following figures we categorized entities into Person and Location categories.

Let me explain it by another example as well. All NER system takes unannotated block of texts as input:


Jim bought 300 shares of Acme Corp. in 2006.

And producing an annotated block of text as follows:


[Jim]Personbought 300 shares of [Acme Corp.]Organizationin [2006]Time.

In the above example, Jim has been extracted as Person entity. *Acme Corp. *has been extracted as Organization entity and *2006* as time entity.

### Problems

Traditional NER models are limited to a predefined set of entity types. Expanding the number of entity types can be beneficial for many applications but may involve **labeling additional datasets**[3]. Let me explain it more clearly. Let say we have following input text and need to extract the information in the form of named entities.


Jim was born in Nepal. At the age of 23, He bought 300 shares of Acme Corp. in 2006.

In the above text, we added two more entities, which is Age and Location. What do you think, Does above model can extract the Age entity? No, because it has not been trained on Age entity yet.


[Jim]Personwas born in [Nepal]Location. At the age of 23, He bought 300 shares of [Acme Corp.]Organizationin [2006]Time.

If you want to learn more on application of Large Language Models,read following blogs!

**Solut**ions

**Large Language Model**

The emergence of Large Language Models, like GPT, Llama, Mistral etc has introduced a new era for open-type NER by enabling the identification of any types of entity types only by natural language instruction. This shift signifies a significant departure from the inflexibility observed in traditional models. Now, let’s try how Google Gemini extracts the Named entities from above unannotated texts.

`model = genai.GenerativeModel("gemini-pro")`

input_text = "Jim was born in Nepal. At the age of 23, He bought 300 shares of Acme Corp. in 2006."

prompt = f"""You are expert on Named Entity Recognition(NER). Extract following entities if exist in following text input:

Entity type:

- Person

- Age

- Place

- Organization

- Date

\n

text to find entities:{input_text}

\n

Please provide output in json form.

"""

response = model.generate_content(prompt)

print(response.text)

Here, We instruct the LLM to behave like NER model by passing possible entity types along with inputs. As you can see response below, LLM extracted all the mentioned entities perfectly and returns in the form of JSON.

![](https://miro.medium.com/v2/resize:fit:678/1*rtuwiz20WfC-LVQ2gCTVJw.png)

However, LLM’s typically consist of billions of parameters and thus require substantial computing resources. Although it is possible to access some LLM’s via APIs, using them at scale can incur high costs. That’s why LLM is not preferred for NER tasks and **GLiNER** comes into play.

## Get Netra Prasad Neupane’s stories in your inbox

Join Medium for free to get updates from this writer.

**2. GLiNER**

GLiNER refers to Generalist Model for Named Entity Recognition using Bidirectional Transformer. It is a compact NER model trained to identify any type of entity. It facilitates parallel entity extraction, an advantage over the slow sequential token generation of LLM’s.

![](https://miro.medium.com/v2/resize:fit:1000/1*h_JVa0-WG-vUC85_D_1p2Q.png)

GLiNER employs a **Bidirectional Encoder Representation of Transformer(BERT)** and takes as input entity type prompts and a sentence/text. Each entity is separated by a learned token [ENT]. The BiLM (Bidirectional Languge Model like BERT) outputs representations for each token. Entity embeddings are passed into a **FeedForward Network**, while input word representations are passed into a **span representation layer** to compute embeddings for each span. Finally, it computes a matching score between entity representations and span representations (using dot product and sigmoid activation). For instance, in the figure, the span representation of (0, 1), corresponding to “Alain Farley,” has a high matching score with the entity embeddings of “Person”. If you want to deep dive into the architecture you can read the paper from here.

**Great**! Let’s extract the entities from the texts that we used earlier for testing LLM’s NER capability.

`from gliner import GLiNER`

model = GLiNER.from_pretrained("urchade/gliner_multi")


input_text = "Jim was born in Nepal. At the age of 23, He bought 300 shares of Acme Corp. in 2006."

labels = ["Person", "Age", "Place", "Organization", "Date"]


entities = model.predict_entities(input_text, labels)

entities_ref = {entity["label"]:[entity["text"]] for entity in entities}

print(entites_ref)

Here, we loaded the model form the huggingface. The size of `urchade/giner_multi`

is around 1.33GB. You can run this model in your own PC. It can be inferred using CPU having limited resources but you can’t do that easily with LLM’s. Just see the following response from the GLiNER, it has extracted all the mentioned entities perfectly and returns in the form of dictionary.

![](https://miro.medium.com/v2/resize:fit:655/1*dDXaEuGq6l63hdxlBDVdjA.png)

Wow! This model looks very convincing and powerful. It extracted all the entites in Zero-Shot. We don’t need to train the model on new entity types. We can directly infer it by passing new entity types that we want to extract.

According to GLiNER paper, it has demonstrated strong performance, outperforming both ChatGPT and fine-tuned LLMs in zero-shot evaluations on various NER benchmarks[3].

![](https://miro.medium.com/v2/resize:fit:609/1*Qh5ugltkVV7O_7F4Kkahdg.png)

In summary, GLiNER is a new method for identifying various types of entities in text using bidirectional language models. This model not only outperforms state-of-the-art Large Language Models like ChatGPT in zero-shot scenarios but also offers a more resource-efficient alternative, crucial for environments with limited computing power. GLiNER is versatile, performing well in multiple languages, including those it wasn’t trained on[3]. Current model is fine-tuned and supports

English,French,German,Spanish,ItalianandPortugeselanguage.Nowdays I started using GLiNER in all my NER related projects and it works beyond my expectation. I recommend you to have at least one try this zero-shot NER.

If you have any queries I am happy to answer them if possible. If you liked it, then please don’t forget to clap and share it with your friends. See you in the next blog…

### References:

- https://en.wikipedia.org/wiki/Named-entity_recognition
*Imed Keraghel*, A survey on recent advances in Named Entity Recognition*Urchade Zaratiana, Nadi Tomeh, Pierre Holat and Thierry Charnois*, GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer
