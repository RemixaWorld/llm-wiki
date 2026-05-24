---
domain: towardsdatascience.com
fetch_date: '2026-05-22T20:25:24.997993'
status: ok
url: https://towardsdatascience.com/your-chunks-failed-your-rag-in-production/
---

The exception was in the document. It had been ingested. The embedding model had encoded it. The LLM, given the right context, would have handled it without hesitation. But the retrieval system never surfaced it because the chunk containing that exception had been split right at the paragraph boundary where the general rule ended and the qualification began.

I remember opening the chunk logs and staring at two consecutive records. The first ended mid-argument: ** ‘Contractors follow the standard onboarding process as described in Section 4…’** The second began in a way that made no sense without its predecessor:

**. Each chunk, in isolation, was a fragment. Together, they contained a complete, critical piece of information. Separately, neither was retrievable in any meaningful way.**

*‘…unless engaged on a project classified under Annex B, in which case…’***The pipeline looked fine on our test queries. The pipeline was not fine.**

That moment the compliance Slack message and the chunk log open side by side is where I stopped treating chunking as a configuration detail and started treating it as the most consequential design decision in the stack. Everything that follows is what I learned after that, in the order I learned it.

Here is what I found, and how I found it.

## In This Article

*What Chunking Is and Why Most Engineers Underestimate It**The First Crack: Fixed-Size Chunking**Getting Smarter: Sentence Windows**When Your Documents Have Structure: Hierarchical Chunking**The Alluring Option: Semantic Chunking**The Problem Nobody Talks About: PDFs, Tables, and Slides**A Decision Framework, Not a Ranking**What RAGAS Tells You About Your Chunks**Where This Leaves Us*

## What Chunking Is and Why Most Engineers Underestimate It

In the previous article, I described chunking as * ‘the step that most teams get wrong.’* I stand by that and let me try to explain it in much details.

If you haven’t read it yet check it out here: *A practical guide to RAG for Enterprise Knowledge Bases*

A RAG pipeline does not retrieve documents. It retrieves chunks. Every answer your system ever produces is generated from one or more of these units, not from the full source document, not from a summary, but from the specific fragment your retrieval system found relevant enough to pass to the model. The shape of that fragment determines everything downstream.

Here is what that means concretely. A chunk that is too large contains multiple ideas: the embedding that represents it is an average of all of them, and no single idea scores sharply enough to win a retrieval contest. A chunk that is too small is precise but stranded: a sentence without its surrounding paragraph is often uninterpretable, and the model cannot generate a coherent answer from a fragment. A chunk that cuts across a logical boundary gives you the contractor exception: complete information split into two incomplete pieces, each of which looks irrelevant in isolation.


Chunking sits upstream of every model in your stack. Your embedding model cannot fix a bad chunk. Your re-ranker cannot resurface a chunk that was never retrieved. Your LLM cannot answer from context it was never given.

The reason this gets underestimated is that it fails silently. A retrieval failure does not throw an exception. It produces an answer that is almost right, plausible, fluent, and subtly wrong in the way that matters. In a demo, with hand-picked queries, almost right is fine. In production, with the full distribution of real user questions, it is a slow erosion of trust. And the system that erodes trust quietly is harder to fix than one that breaks loudly.

I learned this the hard way. What follows is the progression of strategies I worked through, not a taxonomy of options, but a sequence of problems and the thinking that led from one to the next.

## The First Crack: Fixed-Size Chunking

We started where most teams start: fixed-size chunking. Split every document into 512-token windows, 50-token overlap. It took an afternoon to set up. The early demos looked fine. Nobody questioned it.

```
from llama_index.core.node_parser import TokenTextSplitter
parser = TokenTextSplitter(
chunk_size=512,
chunk_overlap=50
)
nodes = parser.get_nodes_from_documents(documents)
```


The logic is intuitive. Embedding models have token limits. Documents are long. Split them into fixed windows and you get a predictable, uniform index. The overlap ensures that boundary-crossing information gets a second chance. Simple, fast, and completely indifferent to what the text is actually saying.

That last part **“completely indifferent to what the text is saying”** is the problem. Fixed-size knows nothing about where a sentence ends, or that a three-paragraph policy exception should stay together, or that splitting a numbered list at step four produces two useless fragments. It is a mechanical operation applied to a semantic object, and the mismatch will eventually show up in your context recall.

For our corpus: Confluence pages, HR policies, engineering runbooks, it showed up in context recall. **When I ran our first RAGAS evaluation, we were sitting at 0.72 on context recall.** *That meant roughly one in four queries was missing a piece of information that existed in the corpus.* For an internal knowledge base, that is not a rounding error. That is the compliance Slack message, waiting to happen.


When fixed-size works:Short, uniform documents where every section is self-contained like product FAQs, news summaries, support ticket descriptions. If your corpus looks like a list of independent entries, fixed-size will serve you well and the simplicity is a genuine advantage.

The overlap does help. But there is a limit to how much a 50-token overlap can compensate for a 300-token paragraph that happens to cross a chunk boundary. It is a patch, not a solution. I kept it in our pipeline for a subset of documents where it genuinely fit. For everything else, I started looking elsewhere.

## Getting Smarter: Sentence Windows

The contractor exception problem, once I understood it clearly, pointed directly to what was needed: *a way to retrieve at the precision of a single sentence, but generate with the context of a full paragraph.* Not one or the other, both, at different stages of the pipeline.

*LlamaIndex SentenceWindowNodeParser *is built exactly for this. At indexing time, it creates one node per sentence. Each node carries the sentence itself as its retrievable text, but stores the surrounding window of sentences, three either side by default, in its metadata. At query time, the retriever finds the most relevant sentence. At generation time, a post-processor expands it back to its window before the context reaches the LLM.

```
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
# Index time: one node per sentence, window stored in metadata
parser = SentenceWindowNodeParser.from_defaults(
window_size=3,
window_metadata_key="window",
original_text_metadata_key="original_text"
)
# Query time: expand sentence back to its surrounding window
postprocessor = MetadataReplacementPostProcessor(
target_metadata_key="window"
)
```


The compliance exception that had been invisible to the fixed-size pipeline became retrievable immediately. The sentence ‘unless engaged on a project classified under Annex B’ scored highly on a query about contractor onboarding exceptions because it contained exactly that information, without dilution. The window expansion then gave the LLM the three sentences before and after it, which provided the context to generate a complete, accurate answer.

**On our evaluation set, context recall went from 0.72 to 0.88 after switching to sentence windows for our narrative document types.** That single metric improvement was worth several days of debugging combined.


Where sentence windows fail:Tables and code blocks. A sentence parser has no concept of a table row. It will split a six-column table across dozens of single-sentence nodes, each of which is meaningless in isolation. If your corpus contains structured data, and most enterprise corpora do, sentence windows will solve one problem while creating another. More on this shortly.

I also discovered that * window_size* needs tuning for your specific domain. A window of three works well for narrative policy text where context is local. For technical runbooks where a step in a procedure references a setup section five paragraphs earlier, three sentences is not enough context and you will see it in your answer relevancy scores. I ended up running evaluations at window sizes of 2, 3, and 5, comparing RAGAS metrics across all three before settling on 3 as the best balance for our corpus. Do not assume the default is correct for your use case. Measure it.

## When Your Documents Have Structure: Hierarchical Chunking

Our engineering corpus: architecture decision records, system design documents, API specifications looked nothing like the HR policy files. Where the HR documents were flowing prose, the engineering documents were structured: sections with headings, subsections with numbered steps, tables of parameters, code examples. The sentence window approach that worked beautifully on policy text was producing mediocre results on these.

The reason became clear when I looked at the retrieved chunks. A query about our API rate limiting policy would surface a sentence from the rate limiting section, expanded to its window but the window was three sentences in the middle of a twelve-step configuration process. The model received context that was technically about rate limiting but was missing the actual numbers because those appeared in a table two paragraphs away from the explanatory sentence that had been retrieved.

The fix was obvious once I framed it correctly: *retrieve at paragraph granularity, but generate with section-level context.* The paragraph is specific enough to win a retrieval contest. The section is complete enough for the LLM to reason from. I needed something that did both not one or the other.

```
from llama_index.core.node_parser import HierarchicalNodeParser, get_leaf_nodes
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.indices.postprocessor import AutoMergingRetriever
# Three-level hierarchy: page -> section (512t) -> paragraph (128t)
parser = HierarchicalNodeParser.from_defaults(
chunk_sizes=[2048, 512, 128]
)
nodes = parser.get_nodes_from_documents(documents)
leaf_nodes = get_leaf_nodes(nodes) # Only leaf nodes go into the vector index
# Full hierarchy stored in docstore so AutoMergingRetriever can walk it
docstore = SimpleDocumentStore()
docstore.add_documents(nodes)
# At query time: if enough sibling leaves match, return the parent instead
retriever = AutoMergingRetriever(
vector_retriever, storage_context, verbose=True
)
```


* AutoMergingRetriever* is what makes this practical. If it retrieves enough sibling leaf nodes from the same parent, it promotes them to the parent node automatically. You do not hardcode ‘retrieve paragraphs, return sections’ the retrieval pattern drives the granularity decision at runtime. Specific queries get paragraphs. Broad queries that touch multiple parts of a section get the section.

For our engineering documents, context precision improved noticeably. We were no longer passing the model a sentence about rate limiting stripped of the table that contained the actual limits. We were passing it the section, which meant the model had the numbers it needed.


Before choosing hierarchical chunking:Check your document structure. Run a quick audit of heading levels across your corpus. If the median document has fewer than two meaningful heading levels, the hierarchy has nothing to work with and you will get behaviour closer to fixed-size. Hierarchical chunking earns its complexity only when the structure it exploits is genuinely there.

## The Alluring Option: Semantic Chunking

After hierarchical chunking, I came across semantic chunking and for a day or two I was convinced I had been doing everything wrong. The idea is clean: *instead of imposing boundaries based on token count or document structure, you let the embedding model detect where the topic actually shifts.* When the semantic distance between adjacent sentences crosses a threshold, that is your cut point. Every chunk, in theory, covers exactly one idea.

```
from llama_index.core.node_parser import SemanticSplitterNodeParser
parser = SemanticSplitterNodeParser(
buffer_size=1,
breakpoint_percentile_threshold=95, # top 5% of distances = boundaries
embed_model=embed_model
)
```


In theory, this is the right abstraction. In practice, it introduces two problems that matter in production.

**The first is indexing latency.** Semantic chunking requires embedding every sentence before it can determine a single boundary. For a corpus of 50,000 documents, this is not a one-afternoon job. We ran a test on a subset of 5,000 documents and the indexing time was roughly four times longer than hierarchical chunking on the same corpus. For a system that needs to re-index incrementally as documents change, that cost is real.

**The second is threshold sensitivity.**

The * breakpoint_percentile_threshold* controls how aggressively the parser cuts. At 95, it cuts rarely and produces large chunks. At 80, it cuts frequently and produces fragments. The right value depends on your domain, your embedding model, and the density of your documents and you cannot know it without running evaluations. I spent two days tuning it on our corpus and settled on 92, which produced reasonable results but nothing that clearly justified the indexing cost over the hierarchical approach for our structured engineering documents.

Where semantic chunking genuinely outperformed the alternatives was on our mixed-format documents – pages exported from Notion that combined narrative explanations, inline tables, short code snippets, and bullet lists in no particular hierarchy. For those, neither sentence windows nor hierarchical parsing had a strong structural signal to work with, and semantic splitting at least produced topically coherent chunks.


My honest take:Semantic chunking is worth trying when your corpus is genuinely unstructured and homogeneous strategy approaches are consistently underperforming. It is not a default upgrade from hierarchical or sentence-window approaches. It trades simplicity and speed for theoretical coherence, and that trade is only worth making with evidence from your own evaluation data.

## The Problem Nobody Talks About: PDFs, Tables, and Slides

Everything I have described so far assumes that your documents are clean, well-formed text. In practice, enterprise knowledge bases are full of things that are not clean, well-formed text. They are scanned PDFs with two-column layouts. They are spreadsheet exports where the most important information is in a table. They are PowerPoint decks where the key insight is a diagram with a caption, and the caption only makes sense alongside the diagram.

None of the strategies above handle these cases. And in many enterprise corpora, these cases are not edge cases they are the majority of the content.

### Scanned PDFs and Layout-Aware Parsing

The standard *LlamaIndex* PDF loader uses PyPDF under the hood. It extracts text in reading order, which works acceptably for simple single-column documents but fails badly on anything with a complex layout. A two-column academic paper gets its text interleaved column-by-column. A scanned form gets garbled text or nothing at all. A report with side-bar callouts gets those callouts inserted mid-sentence into the main body.

For serious PDF processing, I switched to **PyMuPDF (also called fitz)** for layout-aware extraction, and **pdfplumber** for documents where I needed granular control over table detection. The difference on complex documents was significant enough that I considered it a separate preprocessing pipeline rather than just a different loader.

```
import fitz # PyMuPDF
def extract_with_layout(pdf_path):
doc = fitz.open(pdf_path)
pages = []
for page in doc:
# get_text('blocks') returns text grouped by visual block
blocks = page.get_text('blocks')
# Sort top-to-bottom, left-to-right within each column
blocks.sort(key=lambda b: (round(b[1] / page.rect.height * 20), b[0])) # normalised row bucket
page_text = ' '.join(b[4] for b in blocks if b[6] == 0) # type 0 = text
pages.append({'text': page_text, 'page': page.number})
return pages
```


The key insight with PyMuPDF is that * get_text(‘blocks’)* gives you text grouped by visual layout block and not in raw character order. Sorting these blocks by vertical position and then horizontal position reconstructs the correct reading order for multi-column layouts in a way that simple character-order extraction cannot.

For documents with heavy scanning artefacts or handwritten elements, **Tesseract OCR** via *pytesseract* is the fallback. It is slower and noisier, but for scanned HR forms or signed contracts, it is often the only option. *I routed documents to OCR only when PyMuPDF returned fewer than 50 words per page – a heuristic that identified scanned documents reliably without adding OCR latency to the clean PDF path.*


LlamaParse as a managed alternative:LlamaCloud’s LlamaParse handles complex PDF layouts, tables, and even diagram extraction without requiring you to build and maintain a preprocessing pipeline. For teams that cannot afford to invest engineering time in PDF parsing infrastructure, it is worth evaluating. The trade-off is sending documents to an external service.Check your data residency requirements before using it in a regulated environment.

### Tables: The Retrieval Black Hole

Tables are the single most common cause of silent retrieval failures in enterprise RAG systems, and they are almost never addressed in standard tutorials. The reason is straightforward: a table is a two-dimensional structure in a one-dimensional representation. When you flatten a table to text, the row-column relationships disappear, and what you get is a sequence of values that is essentially uninterpretable without the context of the headers.

Take a table with columns for Product, Region, Q3 Revenue, and YoY Growth. Flatten it naively and the retrieved chunk looks like this: ‘Product A EMEA 4.2M 12% Product B APAC 3.1M -3%’. The embedding model has no idea what those numbers mean in relation to each other. The LLM, even if it receives that chunk, cannot reliably reconstruct the row-column relationships. You get a confident-sounding answer that is arithmetically wrong.

The approach that worked for us was to treat tables as a separate extraction type and reconstruct them as natural-language descriptions before indexing. For each table row, generate a sentence that encodes the row in readable form, preserving the relationship between values and headers.

```
import pdfplumber
def tables_to_sentences(pdf_path):
sentences = []
with pdfplumber.open(pdf_path) as pdf:
for page in pdf.pages:
for table in page.extract_tables():
if not table or len(table) < 2:
continue
headers = table[0]
for row in table[1:]:
# Reconstruct row as a readable sentence
pairs = [f'{h}: {v}' for h, v in zip(headers, row) if h and v]
sentences.append(', '.join(pairs) + '.')
return sentences
```


This is a deliberate trade-off. You lose the visual structure of the table, but you gain something more valuable: chunks that are semantically complete. A query asking for ‘Product A revenue in EMEA for Q3’ now matches a chunk that reads ‘Product: Product A, Region: EMEA, Q3 Revenue: 4.2M, YoY Growth: 12%’ – which is both retrievable and interpretable.

For tables that are too complex for row-by-row reconstruction, pivot tables, multi-level headers, merged cells, I found it more reliable to pass the raw table to a capable LLM at indexing time and ask it to generate a prose summary. This adds cost and latency to the indexing pipeline but it is worth it for tables that carry genuinely important information.

### Slide Decks and Image-Heavy Documents

PowerPoint decks and PDF presentations are a particular challenge because the most meaningful information is often not in the text at all. A slide with a title of ‘Q3 Architecture Decision’ and a diagram showing service dependencies carries most of its meaning in the diagram, not in the six bullet points underneath it.

For text extraction from slide decks, python-pptx handles the mechanical extraction of slide titles, text boxes, speaker notes. Speaker notes are often more information-dense than the slide body and should always be indexed alongside it.

```
from pptx import Presentation
def extract_slide_content(pptx_path):
prs = Presentation(pptx_path)
slides = []
for i, slide in enumerate(prs.slides):
title = ''
body_text = []
notes = ''
for shape in slide.shapes:
if not shape.has_text_frame:
continue
# Use placeholder_format to reliably detect title (idx 0)
# shape_type alone is unreliable across slide layouts
if shape.is_placeholder and shape.placeholder_format.idx == 0:
title = shape.text_frame.text
else:
body_text.append(shape.text_frame.text)
if slide.has_notes_slide:
notes = slide.notes_slide.notes_text_frame.text
slides.append({
'slide': i + 1,
'title': title,
'body': ' '.join(body_text),
'notes': notes
})
return slides
```


For diagrams, screenshots, and image-heavy slides where the visual content carries meaning, text extraction alone is insufficient. The practical options are two: use a multimodal model to generate a description of the image at indexing time, or use * LlamaParse*, which handles mixed content extraction including images.

I used GPT-4V at indexing time for our most important slide decks the quarterly architecture reviews and the system design documents that engineers referenced frequently. The cost was manageable because it applied only to slides flagged as diagram-heavy, and the improvement in retrieval quality on technical queries was noticeable. For a fully local stack, **LLaVA** via *Ollama* is a viable alternative, though the description quality for complex diagrams is meaningfully lower than GPT-4V at the time of writing.


The practical heuristic:If a slide has fewer than 30 words of text but contains an image, flag it for multimodal processing. If it has more than 30 words, text extraction is probably sufficient. This simple rule correctly routes roughly 85% of slides in a typical enterprise deck corpus without manual classification.

## A Decision Framework, Not a Ranking

By the time I had worked through all of this, I had stopped thinking about chunking strategies as a ranked list where one was ‘best.’ The right question is not ‘which strategy is most sophisticated?’ It is ‘which strategy matches this document type?’ And in most enterprise corpora, the answer is different for different document types.

The routing logic we ended up with was simple enough to implement in an afternoon and it made a measurable difference across the board.

```
from llama_index.core.node_parser import (
SentenceWindowNodeParser, HierarchicalNodeParser, TokenTextSplitter
)
def get_parser(doc):
doc_type = doc.metadata.get('doc_type', 'unknown')
source = doc.metadata.get('source_format', '')
# Structured docs with clear heading hierarchy
if doc_type in ['spec', 'runbook', 'adr', 'contract']:
return HierarchicalNodeParser.from_defaults(
chunk_sizes=[2048, 512, 128]
)
# Narrative text: policies, HR docs, onboarding guides
elif doc_type in ['policy', 'hr', 'guide', 'faq']:
return SentenceWindowNodeParser.from_defaults(window_size=3)
# Slides and PDFs go through their own preprocessing first
elif source in ['pptx', 'pdf_complex']:
return TokenTextSplitter(chunk_size=256, chunk_overlap=30)
# Safe default for unknown or short-form content
else:
return TokenTextSplitter(chunk_size=512, chunk_overlap=50)
```


The * doc_type* metadata comes from your document loaders.

*LlamaIndex’s*Confluence connector exposes page template type. SharePoint exposes content type. For PDFs and slides loaded from a directory, you can infer type from filename patterns or folder structure. Tag documents at load time, retrofitting type metadata across an existing index is painful.

Here is the full decision map:

![](https://contributor.insightmediagroup.io/wp-content/uploads/2026/04/image-104.png)


**Table 1: Chunking strategy selection guide. Treat this as a starting point, not a rulebook. Measure on your own corpus**## What RAGAS Tells You About Your Chunks

Everything I have described above, the contractor exception, the context recall improvement, the table retrieval failures, I could only quantify because I had RAGAS running from early in the project. Without it, I would have been debugging by intuition, fixing the queries I happened to notice and missing the ones I did not.

One thing worth saying clearly before we go further is that it is a measurement tool, not a repair tool. It will tell you precisely which category of failure you are looking at. It will not tell you how to fix it. That part is still yours.

In the context of chunking specifically, the four core metrics each diagnose a different failure mode:

![](https://contributor.insightmediagroup.io/wp-content/uploads/2026/04/image-105.png)


**Table 2: RAGAS metrics as a chunking diagnostic. Each metric is a signal pointing to a specific layer of the pipeline**The pattern that first told me fixed-size chunking was failing was a context recall score of 0.72 alongside a faithfulness score of 0.86. The model was grounding faithfully on what it received. The problem was what it received was incomplete. The retriever was missing roughly one in four relevant pieces of information. That pattern, specifically, points upstream: the issue is in chunking or retrieval, not in generation.

After switching to sentence windows for our narrative documents, context recall moved to 0.88 and faithfulness held at 0.91. Context precision also improved from 0.71 to 0.83 because sentence-level nodes are more topically specific than 512-token windows, and the retriever was surfacing fewer irrelevant chunks alongside the right ones.


Know which metric is failing before you change anything. A low context recall is a retrieval problem. A low faithfulness is a generation problem. A low context precision is a chunking problem. Treating them interchangeably is how you spend a week making changes that do nothing useful.

The point is simple: run RAGAS before and after every significant chunking change. The numbers will save you days of guesswork.

## Where This Leaves Us

My compliance colleague never knew that her Slack message was the start of weeks of chunking work. From her side, the system just started giving better answers after a few weeks. From mine, that message was the most useful feedback I got across the entire project not because it told me what to build, but because it told me where I had been wrong.

That gap between the user experience and the engineering reality is why chunking is so easy to underestimate. When it fails, users do not file tickets about ‘poor context recall at K=5.’ They quietly stop trusting the system. And by the time you notice the drop in usage, the problem has been there for weeks.

**The habit this forced on me was simple: evaluate before you optimise.** Run RAGAS on a realistic query set before you decide your chunking is good enough. Manually read a random sample of chunks including the ones that produced wrong answers, not just the ones you tested on. Look at the chunk log when a user reports a problem. The evidence is there. Most teams just do not look.

Chunking is not glamorous engineering. It does not make for impressive conference talks. **But it is the layer that determines whether everything above it, the embedding model, the retriever, the re-ranker, the LLM, actually has a chance of working.** Get it right, measure it rigorously, and the rest of the pipeline has a foundation worth building on.


The LLM is not the bottleneck. In most production RAG systems, the bottleneck is the decision about where one chunk ends and the next begins.

**There’s more coming in this series and if production RAG has taught me anything, it’s that every layer you think you understand has at least one failure mode you haven’t found yet. The next article will find another one. Stay tuned.**
