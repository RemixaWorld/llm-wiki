---
domain: medium.com
fetch_date: '2026-05-18T12:49:36.714709'
status: ok
url: https://medium.com/@manthapavankumar11/revolutionizing-rag-by-integrating-vision-models-for-enhanced-document-processing-b3aaa7ab386a
---

# Revolutionizing RAG by Integrating Vision Models for Enhanced Document Processing

[ ![M K Pavan Kumar](https://miro.medium.com/v2/resize:fill:64:64/1*hm4EMU6eAUOoFTldl_OzNg.jpeg) ](</@manthapavankumar11?source=post_page---byline--b3aaa7ab386a--------------------------------------->)

[M K Pavan Kumar](</@manthapavankumar11?source=post_page---byline--b3aaa7ab386a--------------------------------------->)

9 min read

·

Oct 23, 2024

\--

\--

Listen

Share

More

The traditional Retrieval-Augmented Generation (RAG) approach has revolutionized how we interact with documents, but it still misses crucial visual context. What if RAG could not just read, but also see? By integrating Vision-Language Models (VLMs) alongside conventional text processing, we’ve developed a dual-stream RAG architecture that processes both textual and visual content from PDF documents. Our approach leverages `Qdrant’s` multi-vector capabilities to store both text and image embeddings, enabling richer context retrieval. When queried, the system doesn’t just match text — it actually “sees” the document pages, leading to more accurate and contextually aware responses. In this article, we’ll explore how this vision-enhanced RAG system opens new possibilities for document understanding and retrieval.

![created by author M K Pavan Kumar](https://miro.medium.com/v2/resize:fit:700/1*5NhR7e1E9EEXMYYAg82YiA.png)

### The Architecture:

Let me explain the architecture of this innovative vision-enhanced RAG system based on the diagram.

The system begins with PDF documents as the primary input, which undergo dual processing streams to maximize information extraction. In the first stream, each page is converted into an image, while in the parallel stream, text is extracted from each page. This dual approach ensures no information is lost during the processing phase. The extracted content is then vectorized and stored in Qdrant, a vector database that efficiently handles multiple vector types per document. Each entry in Qdrant contains both the image and text vectors, along with essential metadata including page numbers, the base64-encoded page images, and the extracted text.

When a user submits a query, Qdrant’s prefetch capability comes into play, retrieving the top three most relevant results (as configured in this implementation) based on vector similarity. This is where the architecture becomes particularly interesting — the system doesn’t stop at traditional text-based retrieval. The same user query, along with the retrieved base64-encoded images, is passed to a Vision Language Model (VLM), specifically OpenAI’s vision model in this case. This allows the system to perform visual analysis of the actual document layout and content, providing an additional layer of understanding.

The final piece of the architecture involves an aggregating Language Learning Model (LLM) that combines the results from both the text-based retrieval and the vision model’s analysis. This aggregator synthesizes the information from both streams, producing a comprehensive response that leverages both textual and visual understanding of the documents. The result is a more robust and context-aware system that can provide answers with strong supporting evidence from both textual and visual perspectives.

The brilliance of this architecture lies in its ability to understand documents not just as text, but as they were meant to be seen — complete with layout, formatting, and visual elements that often carry crucial contextual information. This dual-stream approach, combined with modern vector search capabilities and vision models, represents a significant advancement in RAG systems.

> Sometimes the Text might not be sufficient to answer your query and hence is the vision.

### The Implementation:

Let us look at the Ingestion part of the architecture as below.

![Data ingestion to vec-store](https://miro.medium.com/v2/resize:fit:554/1*pT2gOB_Lp1io1lvX9FwrwQ.png)

Let us design a class called `pdf_processor.py` with the shown methods in place.

![The outline of the pdf processor class.](https://miro.medium.com/v2/resize:fit:700/1*oNb97PVcVmdFRa7WImCZUQ.png) ```python from pdf2image import convert_from_pathfrom pypdf import PdfReaderimport osclass PDFProcessor: """ A class to handle PDF processing operations including text extraction and image conversion. """ def __init__(self, pdf_path, output_dir): """ Initialize the PDF processor. Parameters: - pdf_path: str, path to the PDF file - output_dir: str, directory to save the outputs """ self.pdf_path = pdf_path self.output_dir = output_dir self.saved_images = [] self.page_texts = [] self.page_dicts = [] # Create output directory if it doesn't exist os.makedirs(self.output_dir, exist_ok=True) def extract_text(self): """ Extract text from each page of the PDF. """ print("Extracting text from PDF...") reader = PdfReader(self.pdf_path) # Extract text from each page for i, page in enumerate(reader.pages): text = page.extract_text() self.page_texts.append(text) # Save text to file text_file_path = os.path.join(self.output_dir, f'page_{i + 1}.txt') with open(text_file_path, 'w', encoding='utf-8') as f: f.write(text) print(f"Saved text from page {i + 1} to {text_file_path}") def convert_to_images(self, dpi=200, fmt='png'): """ Convert each page of the PDF to images. Parameters: - dpi: int, resolution of output images - fmt: str, output image format """ print("Converting PDF pages to images...") pages = convert_from_path(self.pdf_path, dpi=dpi) # Save each page as an image for i, page in enumerate(pages): image_path = os.path.join(self.output_dir, f'page_{i + 1}.{fmt}') page.save(image_path, fmt) self.saved_images.append(image_path) print(f"Saved image from page {i + 1} to {image_path}") def create_page_dicts(self, fmt='png'): """ Create a list of dictionaries containing page information. Parameters: - fmt: str, image format used (needed for filenames) Returns: - list of dictionaries with page information """ num_pages = max(len(self.saved_images) if self.saved_images else 0, len(self.page_texts) if self.page_texts else 0) self.page_dicts = [] for i in range(num_pages): page_dict = { "image": f"page_{i + 1}.{fmt}" if self.saved_images else None, "text": f"page_{i + 1}.txt" if self.page_texts else None } self.page_dicts.append(page_dict) return self.page_dicts def process(self, extract_images=True, extract_text=True, dpi=200, fmt='png'): """ Process the PDF file with specified operations. Parameters: - extract_images: bool, whether to convert pages to images - extract_text: bool, whether to extract text - dpi: int, resolution of output images - fmt: str, output image format Returns: - tuple: (list of image paths, list of text content, list of page dictionaries) """ try: if extract_text: self.extract_text() if extract_images: self.convert_to_images(dpi=dpi, fmt=fmt) self.create_page_dicts(fmt=fmt) return self.saved_images, self.page_texts, self.page_dicts except Exception as e: print(f"Error processing PDF: {str(e)}") return [], [], [] def print_extracted_text(self): """ Print the extracted text from each page with clear separation. """ for i, text in enumerate(self.page_texts, 1): print(f"
{'=' * 40}") print(f"Page {i}") print(f"{'=' * 40}") print(text.strip())# Example driver usage# if __name__ == "__main__":# # Example parameters# pdf_file = "data/rag.pdf" # infact any pdf as input here.# output_folder = "pdf_output"## # Create processor instance# processor = PDFProcessor(pdf_file, output_folder)## # Process PDF - extract both images and text# image_paths, texts, page_dicts = processor.process(# extract_images=True,# extract_text=True,# dpi=200,# fmt='png'# )## print("
Processing complete.")# print("
Page information:")# for i, page_info in enumerate(page_dicts, 1):# print(f"Page {i}:", page_info) ```

The `pdf_output` collects the images and full_text for further processing. Now let us create another class `DataIndexerAndRetriever.py` as shown below.

![The outline of the pdf processor class.](https://miro.medium.com/v2/resize:fit:700/1*3de8QSNZo66yIrgCyoy6UQ.png) ```python from dotenv import load_dotenv, find_dotenvfrom qdrant_client import QdrantClient, modelsfrom fastembed import TextEmbeddingfrom sentence_transformers import SentenceTransformerfrom PIL import Imageimport openaiimport base64import ioimport osfrom pdf_processor import PDFProcessorclass DataIndexerAndRetriever: def __init__(self, data_dir='./pdf_output', qdrant_url="http://localhost:6333", qdrant_api_key='th3s3cr3tk3y'): """ Initialize the Research Paper Processor. Parameters: - data_dir: str, directory containing PDF output files - qdrant_url: str, Qdrant server URL - qdrant_api_key: str, Qdrant API key """ # Load environment variables _ = load_dotenv(find_dotenv()) self.data_dir = data_dir self.collection_name = 'research_papers' # Initialize models self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key) self.image_embedding_model = SentenceTransformer("clip-ViT-B-32") self.text_embedding_model = TextEmbedding( model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2' ) # Initialize OpenAI API api_key = 'sk-proj-api-key' self.openai_client = openai.OpenAI(api_key=api_key) # Initialize collection if it doesn't exist self._initialize_collection() def _initialize_collection(self): """Initialize Qdrant collection if it doesn't exist.""" if not self.client.collection_exists(collection_name=self.collection_name): self.client.create_collection( collection_name=self.collection_name, vectors_config={ "clip-ViT-B-32": models.VectorParams( size=512, distance=models.Distance.COSINE ), "paraphrase-multilingual-MiniLM-L12-v2": models.VectorParams( size=384, distance=models.Distance.COSINE ), } ) def get_text_embeddings(self, text_file_path): """ Get embeddings for text file content. Parameters: - text_file_path: str, path to text file Returns: - tuple: (text embeddings, full text content) """ with open(file=text_file_path, mode='r') as data: full_text = data.read() return next(self.text_embedding_model.passage_embed(full_text)), full_text def image_to_base64(self, image_path): """ Convert image to base64 and get embeddings. Parameters: - image_path: str, path to image file Returns: - tuple: (image embeddings, base64 encoded string) """ try: with open(image_path, "rb") as image_file: encoded_string = base64.b64encode(image_file.read()).decode('utf-8') with Image.open(image_path) as img: image_embedding = self.image_embedding_model.encode(img).tolist() return image_embedding, encoded_string except Exception as e: print(f"Error converting image to base64: {str(e)}") return None def base64_to_image(self, base64_string, output_path=None, fmt='png'): """ Convert base64 string back to image. Parameters: - base64_string: str, base64 encoded image string - output_path: str, path to save decoded image (optional) - fmt: str, image format (default: 'png') Returns: - PIL.Image or str: Image object or path to saved image """ try: image_data = base64.b64decode(base64_string) image = Image.open(io.BytesIO(image_data)) if output_path: image.save(output_path, fmt) return output_path return image except Exception as e: print(f"Error converting base64 to image: {str(e)}") return None def index_pages(self, pages_data): """ Process and index pages data. Parameters: - pages_data: list of dict, containing image and text file information """ for index, obj in enumerate(pages_data): image_path = os.path.join(self.data_dir, obj["image"]) text_file_path = os.path.join(self.data_dir, obj["text"]) image_embedding, base64str = self.image_to_base64(image_path) text_embedding, full_text = self.get_text_embeddings(text_file_path=text_file_path) points = [ models.PointStruct( id=index + 1, vector={ "clip-ViT-B-32": image_embedding, "paraphrase-multilingual-MiniLM-L12-v2": text_embedding }, payload={ "_id": index + 1, "base64str": base64str, "full_text": full_text, "page": index + 1 } ) ] self.client.upsert( collection_name=self.collection_name, points=points ) def query_with_rrf(self, query_text: str = '', query_image_path: str = ''): """ Query the collection using Reciprocal Rank Fusion. Parameters: - query_text: str, text query - query_image_path: str, path to query image Returns: - list: search results """ text_embedding = None if query_text != '': text_embedding = next(self.text_embedding_model.embed(query_text)).tolist() image_embedding = None if query_image_path != '': with Image.open(query_image_path) as img: image_embedding = self.image_embedding_model.encode(img).tolist() prefetch = None if text_embedding and len(text_embedding) > 0: prefetch = [ models.Prefetch( query=text_embedding, using="paraphrase-multilingual-MiniLM-L12-v2", limit=3, ) ] if image_embedding and len(image_embedding) > 0: prefetch = [ models.Prefetch( query=image_embedding, using="clip-ViT-B-32", limit=3, ) ] results = self.client.query_points( collection_name=self.collection_name, prefetch=prefetch, query=models.FusionQuery( fusion=models.Fusion.RRF ), with_payload=True, limit=3, ) return results # Function to ask a question about the image using OpenAI API def ask_image_question(self, base64_image, question): try: # Send the image and question to the OpenAI API response = self.openai_client.chat.completions.create( model="gpt-4o-mini", messages=[ { "role": "user", "content": [ { "type": "text", "text": question + ". Support your answer with evidence from given context. example: page number, section heading etc", }, { "type": "image_url", "image_url": { "url": f"data:image/jpeg;base64,{base64_image}" }, }, ], } ], ) # Extract and return the response answer = response.choices[0].message.content return answer except Exception as e: print(f"Error during API call: {e}") return None# Example usageif __name__ == "__main__": # Sample pages data # Example parameters pdf_file = "data/rag.pdf" output_folder = "pdf_output" # Create processor instance (open the below comments for the first time # when you want to process the pdf file) # processor = PDFProcessor(pdf_file, output_folder) # Process PDF - extract both images and text # image_paths, texts, page_dicts = processor.process( # extract_images=True, # extract_text=True, # dpi=200, # fmt='png' # ) # Initialize processor processor = DataIndexerAndRetriever() # Process pages (uncomment to run indexing into qdrant) # processor.index_pages(page_dicts) # Query example question = 'What is the OpenAI assistants workflow?' result = processor.query_with_rrf(query_text=question) for point in result.points: response = processor.ask_image_question(base64_image=point.payload['base64str'], question=question) print("-" * 50) print(response) ```

Here’s a brief summary of the code’s key functionalities:

1\. The `DataIndexerAndRetriever` class handles dual-stream document processing with text and image capabilities:

\- Initializes connections to `Qdrant` vector database and loads required embedding models (CLIP for images, MiniLM for text)
\- Sets up OpenAI client for vision model integration

2\. Core Processing Functions:
\- Converts PDF pages to both images and text
\- Generates embeddings for both image and text content
\- Stores data in Qdrant with dual vectors per document page

3\. Retrieval System:
\- Uses `Reciprocal Rank Fusion (RRF)` to search across both text and image vectors
\- Returns top 3 most relevant results by default
\- Includes original base64 images and full text in results

4\. Vision Integration:
\- Processes queries using `OpenAI’s GPT-4o` Vision model
\- Takes user questions and relevant page images
\- Returns answers with evidence from the document context

5\. Main Workflow:
\- Processes PDF documents
\- Indexes content in Qdrant
\- Accepts user queries
\- Returns contextual answers using both text and vision capabilities

### The Result:

Observe the question that we have asked and see how OpenAi evidently responded saying its clearly mention in “Figure 2" as attached below.

![image](https://miro.medium.com/v2/resize:fit:700/1*vTcNDnYUh5rQaZRp40D4dA.png) ![image](https://miro.medium.com/v2/resize:fit:607/1*0_ROO9tL93T6T0VIFHDWOQ.png)

### The Conclusion:

In conclusion, integrating vision models into Retrieval-Augmented Generation (RAG) systems represents a significant advancement in document processing. By leveraging both image and text data, we enhance the indexing and retrieval capabilities, allowing for richer and more contextually relevant responses. This innovative approach not only improves the accuracy of information retrieval but also provides compelling evidence that strengthens the insights derived from documents. As we continue to explore the synergy between vision and language models, the potential for more effective and nuanced document understanding becomes increasingly attainable.
