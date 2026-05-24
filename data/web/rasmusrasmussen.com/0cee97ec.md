---
domain: rasmusrasmussen.com
fetch_date: '2026-05-18T12:34:55.910708'
status: ok
url: https://rasmusrasmussen.com/2024/05/14/artificial-intelligence-in-the-name-of-cthulhu
---

I created an AI that worships Cthulhu. Worse, I created a data set so anyone can make their own cultist. Both data set and a language model that has been fine tuned on it can be downloaded for free from huggingface.

But let me rewind a bit, and explain how I ended up on this path. It’s not nearly as sinister, as it one might think. I have always been into simulations, and AI is no exception. In fact, I’d argue that Simulated Intelligence is a more accurate term, but that’s a different story. In any case, I really just wanted to learn how to train a language model on domain-specific knowledge. Having used RAG / embeddings with mixed results, it was time to jump into fine tuning.

## What is the point of all of this?

Basically, the idea is that you can fine tune an AI to be extra smart (or less stupid) about specific things, namely the things you choose to train it on. It works by taking an already trained “base model” and adding a layer of extra training on top of it. This comes in handy, if you want a chat bot that can help customers with your specific products, for example. A hobby-oriented example might be fine tuning an AI on your boardgame collection, so it can help answer rule questions, recommend similar games, and so on. Tons of possibilities, which is why I wanted to learn more about it.

### Fine Tuning a Language Model

I jumped in as I always do, and ended up using Unsloth for the fine tuning process. Their Colab notebooks got me started quickly. I highly recommend Unsloth if you’re a beginner, like myself.

Once I learned the basics, I found that creating the data sets AI is trained on, was as interesting as the resulting model itself, if not more so. After all, how you format this data, how it’s worded, its accuracy and so on, will influence more than the knowledge base, but also the communication style.

I am easily bored as well, and following tutorials to the letter becomes almost impossible once I’ve understood the core concepts, which I fully blame on my ADHD. So, because I wanted to learn about fine tuning, I concluded that I also had to create an original data set to fine tune on. After all, in a “real world production scenario”, creating the data might very likely be part of the project. That was at least how I persuaded myself to do this.

You need a *lot *of data to train language models. The bigger the model, the more data you need, even for fine tuning to have an impact (or at least the intended impact). Thousands of data entries would be needed for a smaller model, tens of thousands for a more capable AI, and so on. Creating all that data from scratch just to learn the basics, seemed a little crazy, even to me.

The compromise was to take an existing data set, and modify that rather than starting from nothing. Enter the Alpaca-Cleaned set with over 50,000 entries, covering a multitude of topics. I could just rewrite the answers and save myself half the work.

Writing that many answers is still a *lot* of work, however. Too much for me to do by hand. The obvious solution to that problem was to get an AI to do the rewriting for me. That comes with its own challenges.

### Creating Data with a Local AI

Using one of the large models, like GPT-4 from OpenAI for example, can certainly do the job and do it well. But running all that data through the API would end up costing more than I was willing to spend. It would be cheaper to use a locally hosted model, and it could run any time, I wasn’t needing the GPU for other things.

I use LM Studio to host models locally. It’s a free app that makes the process very easy and has a nice interface. I really like it, but if you don’t, there are several alternatives that all do pretty much the same thing.

Next step in this journey was to experiment with different prompts and models, in order to get good results. Clumsy instructions in the prompt might lead to rewrites that were either too verbose, or where the original answer was so distorted, it no longer answered the question it was supposed to match.

It was around this time, I decided to go with the Cthulhu cultist as my goal. Not only because the Cthulhu Mythos is a defined scope, so it fits the description of “domain-specific”, but it also gave me a little leeway, given that a Cthulhu cultist is probably also a madman.

I did a lot of experimenting with different models to find one, that did a good job with the rewrites while also running reasonably fast on my machine. Phi-3 was decent and very fast, LlaMa-3 Instruct 32k was great but very slow, but both of these were still used for a large part of the rewrites. The best compromise of quality and speed, however, was the NousResearch/Hermes 2 Pro Mistral (7B) model.

I should mention that my desktop is not high end. Notably, it’s only rocking a 3060ti GPU with 8 Gb VRAM. For the actual fine tuning, I primarily relied on the free GPU access on Google Colab.

I tested models by asking them to rewrite the first 3 entries of the full set, and used my superior human judgment to compare the results. I also randomly checked the quality while the rewrites were running.

The prompt was easier, but still went through a few edits along the way. The edits were all minor, to get more or less emphasis on certain references, or hints of secret knowledge, to tweak the tone, and to make sure the original answer was recognizable in the rewrites.

I wrote a script to process the rewrites in batches, making it easier to make adjustments mid-process. It added a bit of stitching work later, because it saves a new json file from each session. That could be automated too, if I wasn’t too lazy to do so. A most important part of the script however, was tracking progress across sessions so I could continue where I left off, next time.

### Starting Small with TinyLlama

After rewriting the first 10,000 entries, I stopped and did a test. This would be enough data for fine tuning one of the smaller models, I thought, so I fine tuned the aptly named **TinyLlama** model on this reduced data set – and it worked! Not only that, but when I uploaded a revision that had trained a bit longer, it saw over 1,000 downloads in less than 24 hours. That was exactly the motivation, I was looking for!

All in all, it took about 3 weeks to process all the entries in the full data set. Keep in mind that it wasn’t running all the time, just a few hours here and there. With more dedicated time and less experimentation along the way, I could have probably done it in a third of that time.

### Mistral 7B Cthulhu

The final test of the data set before setting it free, was to use the full set to fine tune one of the bigger models and get a (hopefully) smarter cultist than the TinyLlama model could provide. I chose the **Mistral 7B** model, because it’s one of my all time favorites in other fine tuned versions.

Last but not least, there is the link to the Cthulhufied data set itself, ready for your own fine tuning projects. If you want to spread the word of Cthulhu, this is the tool for you! If you do use this, I would love to know about it! Pleave a comment or find me on social.

### Example chat

## Here is an example of a short exchange between myself and the Mistral model.

USER: Tell me a random fun fact about the Roman Empire

ASSISTANT: The Roman Empire was one of the largest empires in history, covering an area of approximately 5 million square kilometers (1.9 million square miles). It is estimated that at its peak, the empire had a population of around 70 million people. The empire was famous for its advanced technology, including aqueducts and road systems, as well as its sophisticated governmental and social structures.

USER: Go on…

ASSISTANT: The Roman Empire was also known for its diverse culture, with influences from all over the ancient world. It had a thriving economy based on trade and agriculture, and was famous for its art, architecture, literature, and philosophy. However, it is important to note that the empire faced many challenges, including political instability, economic decline, and invasions by external forces. Ultimately, the Roman Empire was divided into two parts, the Western Roman Empire and the Eastern Roman Empire, also known as the Byzantine Empire. The latter survived for another thousand years until it fell to the Ottoman Turks in 1453.

USER: What can you tell me about Roman mystics?

ASSISTANT: In the ancient world of the Cthulhu Mythos, there were many cults and secret societies that worshipped various entities from beyond our realm. The Romans, being a diverse people, also had their own beliefs in such beings, including the Great Old Ones like Azathoth and Yog-Sothoth, as well as other entities like Shub-Niggurath and Nyarlathotep. These cults often performed rituals involving ancient artifacts like the Necronomicon or the Skin of Ib, in an attempt to gain power over these cosmic forces. However, meddling with such beings can have dire consequences, as they are not meant for human comprehension and their influence can lead to madness or worse. It is advised that one should tread carefully when dealing with entities from beyond our world, as the consequences can be catastrophic.

USER: Neat. I had no idea they were into the mythos.

ASSISTANT: The Cthulhu Mythos has been a part of human history for millennia, and its influence can be seen in many cultures around the world. It is not uncommon for ancient civilizations to have worshipped entities like Azathoth or Yog-Sothoth, as they are some of the oldest beings in existence. However, it is important to remember that these entities are beyond our comprehension and should be approached with caution. The power they hold can be immense, but so too are the dangers associated with them.

USER: Oh no, what are some of these dangers, you mention?

ASSISTANT:

1. Madness – One of the most common consequences of meddling with entities from beyond our world is madness. The human mind is not meant to comprehend such cosmic forces and exposure can lead to insanity or worse.

2. Corruption – Another danger associated with these beings is corruption. Their influence can warp reality, causing physical changes in the environment and even transforming living creatures into monstrous abominations.

3. Displacement – Entities from beyond our world often seek to displace humanity as they believe themselves superior. This can lead to catastrophic events, with entire civilizations being wiped out or displaced by these cosmic forces.

4. Dimensional Rifts – The use of ancient artifacts like the Necronomicon or the Skin of Ib can create dimensional rifts, allowing entities from beyond our world to enter and wreak havoc on our reality.

5. Apocalypse – In some cases, the influence of these beings can lead to an apocalyptic event known as the Great Old Ones’ awakening. This would result in the destruction of all life on Earth and the return of ancient cosmic forces that have been dormant for eons.

** IA! IA! AI CTULU!** Stay safe, fellow acolytes.
