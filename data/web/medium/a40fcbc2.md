---
domain: ai.plainenglish.io
fetch_date: '2026-05-18T12:45:15.508714'
status: ok
url: https://ai.plainenglish.io/how-to-train-multimodal-llms-to-understand-and-interact-with-text-image-video-and-audio-model-715a1a626def
---

# How To Train Multimodal LLMs To Understand And Interact With Text, Image, Video And Audio: Model And Methods

[ ![Michael ZHANG](https://miro.medium.com/v2/resize:fill:64:64/1*sLyhAgQPOBuyMe8evUmymA.jpeg) ](<https://medium.com/@myschang?source=post_page---byline--715a1a626def--------------------------------------->)

[Michael ZHANG](<https://medium.com/@myschang?source=post_page---byline--715a1a626def--------------------------------------->)

9 min read

·

Mar 21, 2024

\--

Listen

Share

More

In our 1st article, we gave an overall concise introduction to the world of multimodal Large Language Models (LLMs), an overview of their background and how to train them.

This article will talk further about technical details, more exactly, the state-of-the-art models and methods.

## [How To Train Multimodal LLMs To Understand And Interact With Text, Image, Video And AudioA concise introduction to the world of multimodal Large Language Models (LLMs), an overview of their background and how…ai.plainenglish.io](</how-to-train-multimodal-llms-to-understand-and-interact-with-text-image-video-and-audio-99e73aa70465?source=post_page-----715a1a626def--------------------------------------->)

The standard paradigms of Multi-modal Large Language models(MLLMs) insert visual embeddings extracted from images or videos using vision experts into the pre-trained language embedding space. There are three common components of MLLMs:

1. _Pretrained large language models_
2.  _2Vision backbones_
3.  _Bridger for multi-modal alignment._

We will introduce pinioning works to illustrate how current works to achieve MLLMs.

## BLIP2

Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models (BLIP2) [19]is a novel method in the field of multi-modal language models. It offers a generic and efficient pre-training strategy that leverages off-the-shelf frozen pre-trained image encoders and frozen large language models.

Press enter or click to view image in full size

Figure13 BLIP2 with Qformer

BLIP-2’s framework consists of three main components: pretrained large language models, vision backbones (frozen image encoders), and a querying transformer for multi-modal alignment. By leveraging these components, BLIP-2 achieves state-of-the-art performance and demonstrates its potential for building advanced multimodal conversational AI agents.

The key idea behind BLIP-2 is to bridge the modality gap between vision and language by using a lightweight Querying Transformer (Q-Former), as shown in Figure 13. This transformer is pre-trained in two stages. In the first stage, it learns vision-language representation by extracting visual features from a frozen image encoder. In the second stage, it focuses on vision-to-language generative learning by connecting to a frozen language model. This two-stage pre-training approach enables effective vision-language alignment and generates high-quality text outputs.

One of the notable advantages of BLIP-2 is its superior performance on various vision-language tasks, surpassing previous methods while using significantly fewer trainable parameters. For instance, BLIP-2 outperforms Flamingo80B by 8.7% on zero-shot VQAv2, despite having 54 times fewer trainable parameters. Additionally, BLIP-2 showcases emerging capabilities in zero-shot image-to-text generation, where it can follow natural language instructions to generate relevant textual descriptions.

In conclusion, BLIP-2 presents a promising approach to multi-modal language modeling by effectively utilizing frozen pre-trained image encoders and large language models. Its innovative two-stage pre-training strategy and lightweight querying transformer contribute to its impressive performance on various vision-language tasks. BLIP-2 represents a significant step forward in developing multimodal conversational AI agents.

## LLAVA

LLaVA[7], which stands for Large Language and Vision Assistant, is an end-to-end trained large multimodal model that can follow instructions. It aims to connect a vision encoder and a large language model (LLM) for general-purpose visual and language understanding.

The architecture of LLaVA involves combining the open-set visual encoder of CLIP with the language decoder LLaMA[2]. These components are then fine-tuned on generated **instructional vision-language data**. The paper presents a data reformation perspective and pipeline to convert image-text pairs into the appropriate instruction-following format using language-only GPT-4.

Press enter or click to view image in full size

Figure 14 LLaVA

The experiments conducted with LLaVA demonstrate impressive multimodal chat abilities. The model exhibits behaviors similar to multimodal GPT-4 on unseen images/instructions and achieves a relative score of 85.1% compared to GPT-4 on a synthetic multimodal instruction-following dataset. When fine-tuned on the Science QA dataset, the synergy of LLaVA and GPT-4 achieves a new state-of-the-art accuracy of 92.53%.

The paper also highlights the open-source nature of LLaVA. The generated multimodal instruction data, the codebase for data generation and model training, the model checkpoint, and a visual chat demo are made publicly available.

Overall, LLaVA represents a significant step in instruction-tuning large language models in the multimodal field. It demonstrates the potential of language-only GPT-4 in generating multimodal language-image instruction-following data and shows promising results in general-purpose visual and language-understanding tasks.

## KosMos-1

KOSMOS-1[20] is designed to perceive general modalities, learn in context, and follow instructions. The goal of KOSMOS-1 is to align perception with language models, enabling them to understand and generate text based on multimodal input.

Press enter or click to view image in full size

Figure 15 KOSMOS-1

The model is trained on web-scale multimodal corpora, which includes text data, image-caption pairs, and documents with interleaved images and texts. This diverse training data allows KOSMOS-1 to robustly learn from various sources and perform well on a wide range of tasks.

KOSMOS-1 consists of a Transformer-based language model as the general-purpose interface, with perception modules integrated. The model can process multimodal input by embedding both text tokens and other modalities, such as images, into vectors. The Transformer decoder then generates output based on the input context.

The training objective of KOSMOS-1 is to maximize the log-likelihood of tokens in examples, using the next-token prediction task. The model is trained on monomodal data for representation learning, cross-modal paired data for aligning perception with language, and interleaved multimodal data for multimodal language modeling.

In summary, KOSMOS-1 is a powerful Multimodal Large Language Model that combines the capabilities of language understanding and perception. It opens up new possibilities for applying language models to multimodal tasks, advancing the field of artificial general intelligence.

## MINI-GPT4

Mini-GPT4[8] is proposed as a means to examine the advanced multi-modal generation capabilities of GPT-4, which has demonstrated extraordinary abilities such as generating websites from handwritten text and identifying humorous elements within images.

Press enter or click to view image in full size

Figure 15 Mini-GPT4

As shown in Figure 15, Mini-GPT4 aligns a frozen visual encoder with a frozen large language model (LLM) called Vicuna, using just one projection layer. The visual encoder is based on the ViT-G/14 backbone from EVA-CLIP and a Q-Former. The authors find that Mini-GPT4 possesses many capabilities similar to those exhibited by GPT-4, such as generating detailed image descriptions and creating websites based on handwritten drafts.

In their experiments, the authors observe that pretraining Mini-GPT4 on raw image-text pairs alone can result in unnatural language outputs that lack coherency, including repetition and fragmented sentences. To address this problem, they curate a high-quality, well-aligned dataset in the second stage of training. They use a conversational template to fine-tune the model, which significantly improves the naturalness of the generated language and its overall usability.

The authors highlight that Mini-GPT4 is highly computationally efficient, as it only requires training a single projection layer using approximately 5 million aligned image-text pairs. They provide their code, pre-trained model, and collected dataset for further exploration.

Overall, Mini-GPT4 demonstrates emergent vision-language capabilities by aligning visual features with an advanced large language model. It showcases abilities similar to those of GPT-4 and also exhibits additional capabilities such as writing stories and poems inspired by given images, providing solutions to problems shown in images, and teaching users how to cook based on food photos. The model’s performance is enhanced through the use of a high-quality aligned dataset and fine-tuning with a conversational template.

## LLaMA-Adapter

LLaMA-Adapter[21] is a parameter-efficient visual instruction model that aims to transform large language models (LLMs) into instruction-following models. It builds upon the LLaMA model and introduces lightweight adapters with zero-initialized attention into the frozen LLaMA for fine-tuning. This approach allows for the efficient incorporation of new knowledge and multi-modality knowledge injection.

Press enter or click to view image in full size

Figure 16 Joint-training paradigm of LLaMA-adaptor

To enhance the language instruction-following ability of LLaMA-Adapter, bias tuning of linear layers is introduced. By unlocking more learnable parameters such as normalization, layer bias, and scale, the instruction-following knowledge is spread across the entire LLM. This bias tuning only accounts for a small percentage of the model’s parameters, ensuring its parameter efficiency.

LLaMA-Adapter V2, an extension of LLaMA-Adapter, further improves the multi-modal reasoning capabilities. It incorporates an early fusion strategy to balance the visual and language fine-tuning targets. By distributing the dynamic visual prompts to only the early layers of the LLM, the interference between image-text alignment and instruction following is resolved.

Additionally, LLaMA-Adapter V2 integrates expert models such as captioning, detection, and OCR systems to enhance its image understanding capabilities. This integration allows for efficient zero-shot and training-free visual instruction understanding.

Overall, LLaMA-Adapter and its extension, LLaMA-Adapter V2, provide a parameter-efficient approach to transforming LLMs into visual instruction models. They achieve strong multi-modal reasoning capabilities by leveraging language instruction data and image-text pairs, without the need for extensive multi-modal instruction data.

## Macaw-LLM

MACAW-LLM[22] is a novel multi-modal language model that seamlessly integrates visual, audio, and textual information. It consists of three main components: a modality module for encoding multi-modal data, a cognitive module for harnessing pretrained language models, and an alignment module for harmonizing diverse representations.

The modality module in MACAW-LLM allows the model to effectively handle multiple modalities, such as images, videos, audio, and text. This module integrates extra modality encoders, such as CLIP-VIT-B/16 for visual information and WHISPER-BASE for audio signals, into the model architecture.

The alignment module in MACAW-LLM addresses the challenge of aligning representations from different modality encoders. It unifies the representations from different modalities, enabling effective integration of multi-modal information. This alignment is achieved through an attention mechanism that aligns the visual and audio representations with the textual embedding space.

The cognitive module in MACAW-LLM leverages pre-trained language models, such as LLAMA-7B, as the foundation of the model. These language models have demonstrated remarkable capabilities in understanding and following human instructions. In MACAW-LLM, the cognitive module also serves as the textual modality encoder.

Press enter or click to view image in full size

Figure 17 MACAW-LLM

Unlike previous multi-modal models that require two-stage training, MACAW-LLM employs a one-step instruction fine-tuning process. This simplifies the adaptation process and promotes a simpler learning experience. The model is fine-tuned by minimizing the negative log-likelihood over the response with respect to the model parameters.

To facilitate research in multi-modal language models, the authors of MACAW-LLM have also constructed a large-scale multi-modal instruction dataset. This dataset covers a wide range of instructional tasks and includes image and video instances. The dataset is publicly available, along with the code and model, to encourage future research in multi-modal language modeling.

In conclusion, MACAW-LLM is a promising multi-modal language model that effectively integrates visual, audio, and textual information. It introduces novel components, such as the alignment module, and simplifies the adaptation process through one-step instruction fine-tuning. The model, along with the constructed dataset, opens up new possibilities for research in multi-modal language modeling.

## Reference List:

[19] Li J, Li D, Savarese S, et al. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models[J]. arXiv preprint arXiv:2301.12597, 2023.

[20] Huang S, Dong L, Wang W, et al. Language is not all you need: Aligning perception with language models[J]. arXiv preprint arXiv:2302.14045, 2023.

[21] Zhang R, Han J, Zhou A, et al. Llama-adapter: Efficient fine-tuning of language models with zero-init attention[J]. arXiv preprint arXiv:2303.16199, 2023.

[22] Lyu C, Wu M, Wang L, et al. Macaw-LLM: Multi-Modal Language Modeling with Image, Audio, Video, and Text Integration[J]. arXiv preprint arXiv:2306.09093, 2023.

This article is part of a series of **_How To Train Multimodal LLMs To Understand And Interact With Text, Image, Video And Audio_**. Stay tuned for more information.

## In Plain English 🚀

_Thank you for being a part of the_[** _In Plain English_**](<https://plainenglish.io/>) _community! Before you go:_

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](<https://twitter.com/inPlainEngHQ>)**|**[**LinkedIn**](<https://www.linkedin.com/company/inplainenglish/>)**|**[**YouTube**](<https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw>)**|**[**Discord**](<https://discord.gg/in-plain-english-709094664682340443>)**|**[**Newsletter**](<https://newsletter.plainenglish.io/>)
* Visit our other platforms: [**Stackademic**](<https://stackademic.com/>)**|**[**CoFeed**](<https://cofeed.app/>)**|**[**Venture**](<https://venturemagazine.net/>)**|**[**Cubed**](<https://blog.cubed.run/>)
* More content at [**PlainEnglish.io**](<https://plainenglish.io/>)
