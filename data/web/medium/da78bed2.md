---
domain: levelup.gitconnected.com
fetch_date: '2026-05-18T12:46:24.834255'
status: ok
url: https://levelup.gitconnected.com/display-highlighted-pdfs-in-streamlit-eabacc90a777
---

# Display highlighted PDFs in Streamlit

[ ![Lan Chu](https://miro.medium.com/v2/resize:fill:64:64/1*pAJJI_P00fODeuSrfmnbyg.png) ](<https://huonglanchu.medium.com/?source=post_page---byline--eabacc90a777--------------------------------------->)

[Lan Chu](<https://huonglanchu.medium.com/?source=post_page---byline--eabacc90a777--------------------------------------->)

5 min read

·

Jul 30, 2024

\--

Listen

Share

More

and make LLMs output more trust-worthy.

Press enter or click to view image in full size

Image by author.

[Hallucination](<https://huyenchip.com/2023/05/02/rlhf.html#rlhf_and_hallucination>) which happens when an AI model makes stuff up is a heavily discussed topic. I think this is the #1 roadblock for companies to adopt LLMs in production since people can’t 100% trust the model output.

Model like ChatGPT is a probability model which predicts the probability of which token is coming next. A little bit of error for each token prediction can add up and by the time the model has created many tokens down the path, it could produce nonsense. It is like sitting in a rocket flying to the moon. Being off by a tiny amount does not seem to be a big deal at first but over the course of a long journey, you will end up being lost in space. Image by author.

Over the last years working with LLMs projects, I have realized that users greatly value the ability to retrieve the exact excerpts, sentences, or paragraphs from documents that the language models use to generate their answers.

Enhancing this feature by highlighting and displaying the relevant information directly in the user interface can significantly improve user experience. The advantage is to allow the system to provide users the transparency, enable human verifications and gradually build trust in the AI system. Asking the LLMs to return the sources is also a good way to reduce its hallucinations.

Since I have been looking for a way to render the PDF with highlighted relevant text directly in Streamlit, I am really happy to find this [streamlit-pdf-review](<https://pypi.org/project/streamlit-pdf-viewer/>) package that allows you to manipulate and display PDF in the app. If you want a native PDF viewing experience within Streamlit, this article is for you.

## Prompt the LLM to Return Exact Sources

To highlight the relevant text, we need the AI system to not only provide an answer but also display the exact excerpts from the document where the answer is based. To achieve this, the first step is to ask the LLM to return the exact sources from the document.

While you could use a RAG (Retrieval-Augmented Generation) architecture to return relevant chunks of text, this approach may not be that intuitive and user-friendly, as users would still need to read through the entire chunk of text. Instead, it maybe more effective to have the model return specific sources. Here’s how you can prompt the model to return these sources:

```json custom_template = """ Use the following pieces of context to answer the user question. If you don't know the answer, just say that you don't know, don't try to make up an answer. {context} Question: {question} Please provide your answer in the following JSON format: {{ "answer": "Your detailed answer here", "sources": "Direct sentences or paragraphs from the context that support your answers. ONLY RELEVANT TEXT DIRECTLY FROM THE DOCUMENTS. DO NOT ADD ANYTHING EXTRA. DO NOT INVENT ANYTHING." }} The JSON must be a valid json format and can be read with json.loads() in Python. Answer:"""CUSTOM_PROMPT = PromptTemplate( template=custom_template, input_variables=["context", "question"]) ```

and use that for the QA part:

```json qa = RetrievalQA.from_chain_type( llm, chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs={"prompt": CUSTOM_PROMPT}, ) ```

## Highlight and display relevant text in the PDF

Once we have the exact excerpts from the LLM, the next step is to find and highlight these excerpts in the PDF and display the highligted PDF in Streamlit.

The streamlit plugin `streamlit-pdf-viewer` provides an easy interface to display PDFs with annotations overlaid on top. The format of the `annotations` parameter in `streamlit-pdf-viewer `is derived from [Grobid’s coordinate formats](<https://grobid.readthedocs.io/en/latest/Coordinates-in-PDF/>), which are a list of “bounding boxes”. The annotations are expressed as a dictionary of six elements: `page` (the page number where the annotation should be drawn), `x` and `y` (coordinates of the top-left corner), `width` and `height` (dimensions of the bounding box), and `color` (the outline color):

```json annotations = { "page": 1, "x": 220, "y": 155, "height": 22, "width": 65, "color": "red"} ```

So to be able to highlight the relevant text, you will need to:

1. Determine the page where the excerpt is on.
2. Produce the annotations: find the correct coordinates of the excerpt on its respective page and highlight.
3. Display the highlighted PDF with streamlit-pdf-viewer

**Step 1: Determine the page where the excerpt is on**

To effectively highlight text in a PDF, we need to determine which pages contain the relevant excerpts. We can use a library like PyMuPDF (fitz) to search for the text and the page number. The `find_pages_with_excerpts` function does exactly this by searching for specified text excerpts within the document and returning the pages on which they are found:

```python import fitzdoc = fitz.open(stream=io.BytesIO(file), filetype="pdf")def find_pages_with_excerpts(doc, excerpts): pages_with_excerpts = [] for page_num in range(len(doc)): page = doc.load_page(page_num) for excerpt in excerpts: text_instances = page.search_for(excerpt) if text_instances: pages_with_excerpts.append(page_num+1) break return ( pages_with_excerpts if pages_with_excerpts else [1] )pages_with_excerpts = find_pages_with_excerpts(doc, sources) ```

**Step 2: Produce the annotations**

Once we have identified the pages with the excerpts, we need to produce the annotations. The following function will search for the text excerpts in each page of the PDF, create bounding boxes for the text instances found, and store them as annotations:

```python def get_highlight_info(doc, excerpts): annotations = [] for page_num in range(len(doc)): page = doc[page_num] for excerpt in excerpts: text_instances = page.search_for(excerpt) if text_instances: for inst in text_instances: annotations.append( { "page": page_num + 1, "x": inst.x0, "y": inst.y0, "width": inst.x1 - inst.x0, "height": inst.y1 - inst.y0, "color": "red", } ) return annotationsannotations = get_highlight_info(doc, st.session_state.sources) ```

**Step 3: Displaying the highlighted PDF with streamlit-pdf-viewer**

The final step is to display the PDF with the highlighted excerpts using `streamlit-pdf-viewer`. This plugin allows us to pass the PDF content, annotations, and other parameters to create an interactive viewing experience:

```python from streamlit_pdf_viewer import pdf_viewer# Find the first page with excerptsif annotations: first_page_with_excerpts = min(ann["page"] for ann in annotations)else: first_page_with_excerpts = st.session_state.current_page + 1pdf_viewer( file, width=700, height=800, annotations=annotations, pages_to_render=[first_page_with_excerpts], ) ```

And voila! that’s all there is to it :) The complete source code for the demo app below can be found on my [GitHub](<https://github.com/lanchuhuong/demo_highlight_pdf_streamlit>):

Press enter or click to view image in full size

Happy learning 📚😊!
