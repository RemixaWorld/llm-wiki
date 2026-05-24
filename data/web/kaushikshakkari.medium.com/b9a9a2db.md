---
domain: kaushikshakkari.medium.com
fetch_date: '2026-05-18T12:57:53.123829'
status: ok
url: https://kaushikshakkari.medium.com/understanding-document-parsing-part-2-modern-document-parsing-explained-modular-pipelines-bb605c786293
---

**Understanding Document Parsing — (Part 2: **Modern Document Parsing Explained— Modular Pipelines & Vision-Language Models (Multimodal AI))

![](https://miro.medium.com/v2/resize:fit:700/1*YdUmuovlbMzSCP_yNUacUA.png)

## Introduction:

If you’ve ever had to deal with stacks of documents — whether it’s invoices, contracts, or research papers — you know how overwhelming it can be to pull out and organize the information you actually need. That’s where document parsing comes in. In the previous article of the series, we explored the evolution of document parsing technologies — from manual techniques to advanced AI-driven systems. In this article, we’re diving into two of the most exciting modern approaches to document parsing: **Modular Pipeline Systems** and **End-to-End Vision-Language Models (VLMs)**.

![](https://miro.medium.com/v2/resize:fit:700/1*RrEKVG1oh62G6dCLtQDuCg.png)

Modular pipelines divide the process of information extraction into clear, manageable steps, giving you “** more control and flexibility”**. On the other hand, VLMs take a

**“**approach, combining text and layout understanding into a single powerful system.

*do it all at once*”We’ll explore how these methods work, where they shine, and the challenges they still face. Whether you’re a data scientist, software developer, sales executive, product manager or business leader, this deep dive into modern document parsing will help you navigate the ever-evolving landscape of information extraction.

## Modular Pipeline Systems: Breaking Down the Process

![](https://miro.medium.com/v2/resize:fit:1000/1*qA5ar7x90O4h5o8MlGSqOA.png)

Modular pipeline systems follow a step-by-step approach, where each module performs a distinct task. The output from one module becomes the input for the next, creating a streamlined workflow from raw documents to structured data. This modularity allows individual components to be analyzed, tested, fine-tuned, or replaced, enabling tailored solutions for specific document types, use-cases or even industries.


Below are some key modules for building modular pipeline systems.

**1. Input Preprocessing & Conversions:**

Raw documents, including scanned PDFs and Word documents are transformed into standardized formats such as images for downstream processing. Some techniques in this module include:

**1.a PDF-to-Image Conversion:**

Libraries like ** PDF2Image** and

**convert PDF pages into high-resolution images.**

*PyMuPDF***1.b Metadata Extraction:**

Libraries like ** PyPDF2** or

**can extract document metadata (like language, authors, or creation dates), which might be useful for downstream modules when extracting key-value pairs.**

*PDFPlumber***2. Optical Character Recognition (OCR):**

OCR module converts textual content in images into machine-readable text with bounding box information. Popular OCR engines include ** Tesseract**,

**,**

*Google Vision***and**

*AWS Textract***, which can handle diverse fonts, scripts, and even handwriting. Some techniques in OCR include:**

*Azure Document Intelligence***2.a. Image Cleanup:**

![](https://miro.medium.com/v2/resize:fit:700/1*9thsLunGPrTQ5oO2Tht3oA.png)

**Raw Scanned Image on Left and Cleaned Image on Right |**Source: https://huggingface.co/spaces/to-be/Scanned_document_denoise_reconstruct (Restormer: Efficient Transformer for High-Resolution Image Restoration

**)**

![](https://miro.medium.com/v2/resize:fit:700/1*aJsSG5EhqQcXlYJRQs86Ow.png)

![](https://miro.medium.com/v2/resize:fit:700/1*HTP-g1Vy1ESHWe8AGCIAgw.png)

**Raw Scanned Image on Left and Cleaned Image on Right**| Source: https://huggingface.co/spaces/qubvel-hf/documents-restoration (DocRes: A Generalist Model Toward Unifying Document Image Restoration Tasks

**)**

Image cleanup improves OCR accuracy. It involves several steps to enhance the quality of the scanned document. Some steps are following:

**De-skewing:**Corrects any tilt or skew in the image for proper text alignment**Binarization:**Converts color images into black-and-white images, which is often more suitable for OCR processing**Despeckling:**Removes small specks or noise from the image, which can interfere with text recognition**Border removal:**Eliminates border artifacts that may have been introduced during scanning documents.**Contrast & Brightness Adjustment:**Ensures text stands out against the background.**Character / Edge Strengthening:**Sharpens faint characters to improve OCR accuracy.

Cleanup tools like ** OpenCV-Python** or

**ensures proper text alignment and contrast.**

*Pillow***2.b. Image Segmentation:**

![](https://miro.medium.com/v2/resize:fit:700/1*vYtna1RpotavTwjMrnwGaw.png)

**Image on Left and Line Segments on Right**| Source: https://aws.amazon.com/textract/

Segmentation divides the input image into meaningful components like line segments, words and characters to facilitate accurate recognition. Multiple python libraries like *OpenCV*** **perform Image Segmentation.

**2.c Text Recognization:**

![](https://miro.medium.com/v2/resize:fit:700/1*5mYdyZjDfgE8I-wzwb5W7A.jpeg)

Once segmentation is complete, the OCR system applies text recognition algorithms to identify and convert each segmented component into machine-readable characters. Modern techniques such as deep learning-based models (e.g., **CRNN**** **and** **** Attention-based Sequence Recognition**) are often employed to improve accuracy. Many libraries including

**perform Text Recognization in OCR.**

*EasyOCR***3. Layout Analysis:**

This module identifies document elements — text blocks, tables, images, headers, footers — and determines their reading order and spatial relationships. Some techniques include:

**3.a. Structural Detection:**

![](https://miro.medium.com/v2/resize:fit:700/1*h5BwxkFIg7e9KdZc8AkbMg.png)

Libraries like ** LayoutParser**,

**, and**

*Camelot***detect text blocks, tables, and images etc. Commercial OCR engines also provide services to detect layout structure in documents.**

*Tabula***3.b. Reading Order & Spatial Mapping:**

![](https://miro.medium.com/v2/resize:fit:700/1*5texSSBYdPB13B2cj9c_cg.png)

Logical sequences and content alignment are established for coherent interpretation. *LayoutReader*** **and most popular commercial OCR also do reading order detection.

💡

Note:Some modules could be omitted based on document type. For example, for parsingtext-based PDF document, Input Preprocessing, OCR and Layout Analysis modules could often be skipped and replaced with tools likePDFMinerfor direct layout analysis and structural extraction as it’s not an image-based file.

### 4. Content Type Classification:

After layout analysis, this module classifies each detected element into a document-specific content type, such as PII (personally identifiable information) in a bank statement, terms & conditions in a contract, a conclusion section in a research paper, itemized list in an invoice, or skills section in a resume. This module is typically specific to the domain and use case. Some techniques include:

**4.a. Domain-Specific Classifiers:**

![](https://miro.medium.com/v2/resize:fit:700/1*_kGwFghqyYItthbU5RPVtA.png)

Pre-trained or fine tuned machine learning models from libraries like *Hugging Face***, **** Stromtrooper** and


*Scikit-Learn***etc.**

**can be used to classify content from a layout element.**

**4.b. Layout Features:**

One could use layout-based features (like position, element type, font style, and size etc) and combine them with ML model to detect content type. For instance, in a dataset of academic research papers, references are typically found at the end of the document, often formatted as a numbered list or a block of text with italicized or bold titles and smaller font sizes.

**5. Key-Value Extraction:**

This module extracts structured key-value pairs from the classified content. The previous module simplifies this step. For example, only specific keys (like email, name, and phone-number etc) need to be extracted from document element with PII content type, instead of** **extracting all keys in the document. Some techniques include:

**5.a. Pattern Matching:**

![](https://miro.medium.com/v2/resize:fit:700/1*3xDaOjoTgVr8KUwTrPfVjg.png)

Regular expressions libraries like ** regex**,

**and**

*re2*

*CTRE***detect predefined formats like email addresses, age, phone numbers, and dates etc.**

**5.b. Named Entity Recognition (NER):**

![](https://miro.medium.com/v2/resize:fit:700/1*KlnAzX3bpqE5ZJHwKmSkew.png)

Use tools like *NLTK***, **** Spacy/Explosion**,


*Flair***and**


*Alteryx***to detect entities like names, dates, and monetary values. You can also train a model to detect custom entities like email which is missing in the pre-trained AI/ML model shown in the above picture.**

**5.c. Rule-Based Mapping in Tables:**

![](https://miro.medium.com/v2/resize:fit:700/1*4NnIoq8KRi7345nDtRGBEg.png)

Libraries like ** Camelot**, and


*Tabula***extract tables, and you can use specific rules to get key value pairs. For example, in the above picture, the second column of above detected table gives all product name values.**

💡

Note:AfterContent Type Classification, elements with same content types can be merged beforeKey-Value Extraction.For instance, PII in an academic transcript could be present across header and footer section, so merging them prior to extracting PII-related key-values is ideal.

**6. Post-Processing & Validation:**

This final stage ensures extracted data meets business rules, maintains accuracy, and adheres to standards. Techniques include:

**6.a. Error Correction & Quality Checks:**

Utilize rule-based validation or QA models to ensure data accuracy and integrity. Some examples include,

**Range Validation:**An**age ≥ 130**is unlikely.**Null/Missing Value Detection:**Flag empty entries for the**Name**key.**Data Type Verification**: A date value of**30/02/2025 is invalid**because February only has 28 or 29 days.**Cross-Field Consistency:**Check if the order shipment date is after the order placement date.**Outlier Identification:**Highlight unusually large bank transactions, which might indicate fraudulent activity.

**6.b. Integration & Formatting:**

## Get Kaushik Shakkari’s stories in your inbox

Join Medium for free to get updates from this writer.

This ensures compatibility by formatting refined outputs for ingestion into databases, ERP systems, or analytics platforms. For example, the key value pairs may be filtered, nested, or flattened based on system requirements.

### Advantages of Modular Pipeline Systems

**Modularity:**Each stage operates as an independent module, making it easy to upgrade or replace specific components without affecting the entire pipeline.**Reusability:**Individual modules can be reused across different workflows or projects. For example, OCR could be used across invoice parsing and resume parsing.**Troubleshooting:**Errors are easier to locate and fix since each module performs a well-defined task.**Transparency:**The modular design provides clear visibility into each stage of the process, making it easier to understand how data flows and transforms.**Flexibility:**Quickly adapt to new document types or languages by introducing or adjusting modules without overhauling the entire system.

### Limitations of Modular Pipeline Systems

**Error Propagation:**Errors in one module (e.g., OCR) can propagate, affecting the accuracy of downstream modules (e.g., Key-Value Extractions) and final result.**Complexity for Irregular Layouts:**Highly variable or unstructured documents demand frequent changes including configuration of modules.**Maintenance Overhead:**Continuously evaluating and tuning multiple modules can be challenging to manage.**Latency Issues:**Sequential processing across modules can lead to slower performance for high-volume tasks.**Scalability Challenges:**Adding modules for new document formats or languages can increase system complexity to scale.**Limited Contextual Integration:**Modules work in isolation, potentially missing cross-step cues.

**Vision-Language Models (VLMs): An End-to-End Multimodal Approach**

![](https://miro.medium.com/v2/resize:fit:1000/1*5nbbF49X28ovDEc18E1bnw.png)

Unlike modular pipelines, which divide the document parsing process into discrete steps, Vision-Language Models (VLMs) offer a holistic, unified, end-to-end solution. They internally integrate multiple document processing tasks (like text extraction, layout understanding, and semantic interpretation etc) into a single model. This approach is particularly advantageous for handling complex, multi-modal documents, as it captures textual, structural, and visual relationships in a single pass.

### Prompts Role in VLMs:

Prompts play a crucial role toward guiding VLMs for specific document parsing tasks. They help the model focus on particular outputs, ensuring task-specific accuracy and relevance. Below are some common prompts used across different parsing scenarios:

*Extract the key-value pairs for all personal information fields, including name, address, and phone number.**Extract key data fields from the provided invoice and return the output in JSON format. Ensure strict validation rules as followed…**Identify and parse the main sections of this legal contract, including clauses and terms.**Retrieve all tables and convert them into a structured JSON format.*


Below are some key concepts on how VLMs internallywork in general

**1. Unified Feature Extraction and Fusion:**

This concept involves capturing and combining both visual and textual features to create a unified representation.

**1.a. Textual Feature Extraction:**

![](https://miro.medium.com/v2/resize:fit:700/1*r-0arPechG0UD1UzkHuiYA.png)

Language Models like *Transformers** **and** **BERT*** **extract the underlying semantic meaning of text by generating embeddings that effectively represent its content.

**1.b. Visual Feature Extraction:**

![](https://miro.medium.com/v2/resize:fit:700/1*CZo8w6pTxF55cqRwKTUrDA.png)

Simultaneously, VLMs leverage pre-trained vision models (e.g., ** CNNs**,

**, or**

*Vision Transformers***) to capture visual features including spatial layout and structure of each element.**

*TextMonkey***1.c. Visual and Textual Features Fusion:**

![](https://miro.medium.com/v2/resize:fit:700/1*a0zoyWVZdZfj_du1SCmzkQ.png)

These visual and textual features are combined through advanced fusion techniques like ** cross-modal attention mechanisms** enabling the model to understand both the prompt and structure of the document holistically.

### 2. Direct Document Processing:

![](https://miro.medium.com/v2/resize:fit:700/1*sv5enKlfkDaQq72GxAGMHA.png)

VLMs enhance the end-to-end approach by adopting an OCR-free methodology, bypassing traditional character recognition processes to reduce errors. By directly processing raw documents (e.g., text-based PDFs and scanned images) without explicit preprocessing or segmentation, they can accurately interpret layout and content to extract structured information like key-value pairs (e.g., dates, names, monetary values). The output undergoes implicit validation using user prompt to ensure compliance with business rules, making it ready for integration into downstream systems like databases or ERP platforms.

### 3. Pre-Training and Fine-Tuning:

![](https://miro.medium.com/v2/resize:fit:700/1*0qh8gBwCFy0wE0iF7PIrzg.png)

Pre-Training and Fine-Tuning are critical phases in developing and deploying Vision-Language Models. These processes enable VLMs to generalize across various document types and adapt to specific domains effectively.

**3.a Pre-Training:**

![](https://miro.medium.com/v2/resize:fit:700/1*MS0hJSO4fqP3gh42_E8unA.png)

Pre-training exposes VLMs to large multimodal datasets containing various types of documents including books, contracts, invoices, and academic papers. This phase helps the models learn general representations of document layout and content when trained on multiple pre-training tasks. Models like *LayoutLMv3*** **and


**DocFormer**are widely used for pre-training as they can learn both visual and textual features relevant to document parsing.

**3.b Fine-Tuning:**

![](https://miro.medium.com/v2/resize:fit:700/1*Z8zP4QNUFySF9_kpYFEFNg.png)

Fine-tuning further adapts pre-trained models to specific document parsing tasks by training on domain-specific datasets, such as legal documents or medical records. Techniques like *LoRA (Low-Rank Adaptation), QLoRA**, *** Full Model Fine-Tuning and Prompt Tuning** are employed, allowing different fine-tuning techniques in different situations while improving parsing accuracy. For example,

**model is fine-tuned to accurately extract key-value pairs from invoices and bills.**

*PaliGemma*💡Hands-on article to parse invoice using VLMs approach:

https://medium.com/gopenai/invoice-or-bill-custom-parsing-using-kor-langchain-extension-generative-language-models-prompt-7133193358fa

### Advantages of End-to-End Models:

**Holistic Processing:**VLMs eliminate the need for multiple modules by offering an integrated, single-pass approach to document parsing.**Efficiency and Scalability:**The end-to-end nature typically reduces latency and makes these models scalable for real-time applications.**Reduced Error Propagation:**By bypassing OCR and other intermediate steps, VLMs could minimize errors that typically accumulate in modular pipelines. (However, this depends on keys to be extracted and input documents)**Domain Adaptation:**Faster adaptation to new domains through fine-tuning.**Robustness to Complexity:**A viable option for complex layouts and unstructured formats.

### Limitations of End-to-End Models:

**Hallucination:**VLMs can sometimes generate incorrect or irrelevant information. This can be problematic in critical applications where accuracy is critical.**Traceability Issues:**Since end-to-end models rely on OCR-free methods, tracing the origin of a specific answer within the document is often difficult, complicating error debugging and accountability process.**Inconsistency:**These models sometimes can give different responses to the same prompt when run multiple times due to the architecture and how they interpret prompt each time.**Data and Resource Intensity for Fine Tuning:**Large training datasets and extensive computing resources are often needed to fine-tune models for complex documents.**Reduced Transparency:**End-to-end pipelines can be black boxes making error diagnosis and troubleshooting more difficult.**Latency Concerns:**While Vision Language Models (VLMs) generally excel in speed and versatility, their complex architecture can cause latency, especially with large inputs. Sometimes, for straightforward parsing task — simple documents and keys, pipeline methods may be faster.**Complex Layouts:**Sometimes, an OCR in pipeline based method performs better than a VLM in detecting text in extremely irregular structures or handwritten notes.

## Hybrid Solutions: Combining the Best of Both Worlds

![](https://miro.medium.com/v2/resize:fit:700/1*tv7iVYE38RHysPOGyoWw2Q.jpeg)

Hybrid solutions in document parsing blend elements of both modular pipelines and end-to-end VLMs. The idea is to leverage each method’s strengths instead of relying on a single one-size-fits-all approach.


Below are some key reasons for why you need to consider Hybrid Approaches

**Balancing Control and Complexity**: Certain steps (like OCR or post-processing) might be modular, while a VLM tackles more complex tasks (like advanced key-value extraction).**Flexibility Across Document Types**: Simple and regular-format documents can be handled by a lightweight modular pipeline, while more complex, unstructured documents are routed to a VLM.**Incremental Upgrades:**Organizations often have existing modular pipelines for certain documents. Rather than discarding them entirely to adopt a brand-new approach, they can incrementally add a VLM for complex tasks or to handle exceptions.**Optimized Performance and Scalability:**VLMs can be heavy on compute, especially if they’re running for every single page. A hybrid can extract easily recognized fields with lightweight modules, saving the resource-intensive VLM for trickier tasks — leading to more efficient overall system performance.

## Conclusion

Document parsing has come a long way — from manually intensive workflows to sophisticated, AI-driven solutions. Modular pipelines excel with high transparency, flexible module swapping, and easier troubleshooting. End-to-end VLMs offer integrated understanding of text, layout, and visuals, making them especially powerful for complex or variable document environments.

However, these approaches share a common goal of extracting keys accurately from an ever-growing volume of documents. As the field progresses, hybrid solutions will likely become more prominent, leveraging the best of both worlds. Ongoing research into improved datasets, domain-specific adaptation, and efficient fine-tuning continues to enhance these systems. By staying informed and embracing these innovations, organizations can significantly streamline their operations and maintain a competitive edge in a data-driven world.

**Add me on ****LinkedIn****. Thank you!**

If you are interested in document parsing topic, you are welcome to explore my other articles.

![](https://miro.medium.com/v2/resize:fill:388:388/1*fgUkDbev9zErBKGVB1g86g.jpeg)

![](https://miro.medium.com/v2/resize:fill:388:388/1*EBTN7-VnLLOcHcQMVXh35A.jpeg)

![](https://miro.medium.com/v2/resize:fill:388:388/1*YdUmuovlbMzSCP_yNUacUA.png)

If you are interested in semantic search topic, you are welcome to explore my other articles.

![](https://miro.medium.com/v2/resize:fill:388:388/1*Kh85Ej-eTQxaG5MvlNcEhg.jpeg)

![](https://miro.medium.com/v2/resize:fill:388:388/1*--QusSbjW1XXCQaoobEfxA.jpeg)

![](https://miro.medium.com/v2/resize:fill:388:388/1*63snZJv5pisF2iGXmJ6mjw.jpeg)

![](https://miro.medium.com/v2/resize:fit:700/0*mD_Bi840gE5rxqKZ.png)

This story is published on Generative AI. Connect with us on LinkedIn and follow Zeniteq to stay in the loop with the latest AI stories.

Subscribe to our newsletter and YouTube channel to stay updated with the latest news and updates on generative AI. Let’s shape the future of AI together!

![](https://miro.medium.com/v2/resize:fit:700/0*BLBgQeqnOWm2v3TU.png)
