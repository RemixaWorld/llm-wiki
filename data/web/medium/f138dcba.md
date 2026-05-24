---
domain: medium.com
fetch_date: '2026-05-18T12:45:41.948562'
status: ok
url: https://medium.com/@hanan.tabak/user-friendly-streamlit-rag-chatbot-with-text-to-speech-huggingface-embedding-openai-llm-12451be832a3
---

# User-Friendly Streamlit RAG Chatbot with Text-To-Speech: HuggingFace Embedding, OpenAI LLM, OpenAI Agent and LangChain

[ ![Hanan Tabak](https://miro.medium.com/v2/resize:fill:64:64/1*WVYfcJZpp2GWFNuhuyf03g.jpeg) ](</@hanan.tabak?source=post_page---byline--12451be832a3--------------------------------------->)

[Hanan Tabak](</@hanan.tabak?source=post_page---byline--12451be832a3--------------------------------------->)

9 min read

·

May 23, 2024

\--

\--

Listen

Share

More

![This is the chatbot UI on Streamlit ( Link )](https://miro.medium.com/v2/resize:fit:700/1*KRS-TA4WihYg34zfvOjN8A.png)

In this article I’ll explain in detail how I constructed a Streamlit-based chatbot utilizing the Retrieval-Augmented Generation (RAG) architecture. The chatbot leverages OpenAI’s Large Language Models (LLMs) and agents, LangChain framework and Open-Source HuggingFace Embedding for context-aware conversation. Additionally, Text-to-Speech (TTS) capability is integrated to enhance user experience.

Before doing this, I’ll briefly explain the basic concepts of RAG for those who are still beginners in it (You can skip the next paragraph if you are familiar enough with it).

_This chatbot is co-designed by_[ _Mayur Nawal_](<https://github.com/mayurnawal123>) _and_[ _me_](<https://github.com/hanantabak2>) _, where Mayur went through all the hassle of creating the main design and making it work, while I added more functionalities and some modifications to it._

**What is RAG?**

Retrieval-Augmented Generation (RAG) is a powerful approach for building advanced chatbots that can answer questions from a specialized knowledge base which is not included in their training data corpus (like Corporate Data). It combines two key techniques: retrieval-based models and generative models. Retrieval-based models excel at efficiently searching through vast amounts of text data to identify passages most relevant to a user’s query. Generative models, such as LLMs, are adept at generating text in human natural language to answer the user’s query based on the information they are provided. RAG leverages the strengths of both approaches. First, the retrieval component identifies relevant passages from a knowledge base (mostly a vector data base) using techniques like semantic similarity. These retrieved chunks then serve as context for the LLM, which utilizes its generative capabilities to formulate a comprehensive and informative response to the user’s query.

![Source: https://gradientflow.com/techniques-challenges-and-future-of-augmented-language-models/](https://miro.medium.com/v2/resize:fit:700/0*RXm5rw8fxpqT3fIl)

**Cautions and Considerations**

While Streamlit web deployment offers a convenient way to share your chatbot (The chatbot explained here is web-based), it’s important to remember that uploaded data is not stored locally on the user’s machine. This is a critical consideration for handling sensitive enterprise data. For such scenarios, it’s advisable to run a local version of the app on localhost (e.g. a shared server). This approach ensures that all data remains within your own infrastructure.

Another aspect to consider is version control and collaboration. When deploying your StreamLit app on the web, you’ll have to link it with your Github project repository. This facilitates version control and collaboration among team members. However, running the app locally does not necessitate such a linkage. You can simply utilize the `streamlit run` command to execute the app directly.

**Streamlit RAG Chatbot Steps and Components**

1- Import necessary libraries :

```python #=================# Import Libraries#=================import streamlit as stimport pandas as pdimport os# from statsmodels.tsa.arima_model import ARIMA# import statsmodels.api as smfrom langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent# from langchain.llms import OpenAIfrom openai import OpenAIfrom langchain.document_loaders import PyPDFLoaderfrom PyPDF2 import PdfReaderfrom langchain.vectorstores import FAISSfrom langchain.text_splitter import CharacterTextSplitter# from langchain.embeddings.openai import OpenAIEmbeddingsfrom langchain.chains.question_answering import load_qa_chainfrom langchain.chains import RetrievalQAfrom langchain.chat_models import ChatOpenAIfrom langchain.agents import initialize_agentfrom langchain.agents import AgentTypefrom langchain.agents import Toolfrom langchain.embeddings import HuggingFaceEmbeddingsfrom io import BytesIOfrom uuid import uuid4from dotenv import main ```

2- Set the UI environment (background, title and logo):

* _st.markdown_ is a streamlit function used to set the background using a chosen image, but you can make it a plain color instead if you want.
* _st.title_ and _st.sidebar.image_ functions are used to set the title and side logo image respectively.

``` #=================# Background Image , Chatbot Title and Logo#=================page_bg_img = '''<style>.stApp {background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url("https://imageio.forbes.com/specials-images/imageserve/6271151bcd7b0b7ffd1fa4e2/Artificial-intelligence-robot/960x0.jpg");background-size: cover;}</style>'''st.markdown(page_bg_img, unsafe_allow_html=True)st.title("Gen AI RAG Chatbot")try : image_url = "logo-new.png" st.sidebar.image(image_url, caption="", use_column_width=True)except : image_url = "https://static.vecteezy.com/system/resources/previews/010/794/341/non_2x/purple-artificial-intelligence-technology-circuit-file-free-png.png" st.sidebar.image(image_url, caption="", use_column_width=True) ```

3- Insert necessary API keys and Upload the files:

* It’s better of course to let the users insert their own Open AI keys through the _st.sidebar.text_input_ tool and not use your own key as an environment variable.
* File formats supported by the chatbot so far are : .csv, .pdf and .txt, but you can add more like web pages, word files, ppts, etc. The format is explicitly chosen here using a select box tool.
* The function _validatFormat()_ is to make sure that the uploaded file is the same as the selected format.
* _selectPDFAnalysis()_ function is called only if the user has uploaded more than 1 pdf file prompting him to choose either to merge them or compare between them in his question.
* _save_uploadedfile()_ function is used to save whatever files are uploaded and it runs automatically once the uploading takes place.

```python #=================# API Key and Files Upload#=================openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")os.environ["OPENAI_API_KEY"] = openai_api_keyfile_format = st.sidebar.selectbox("Select File Format", ["CSV", "PDF", "TXT"])if file_format == "TXT" : file_format = "plain"uploaded_files = st.sidebar.file_uploader("Upload a file", type=["csv", "txt", "pdf"], accept_multiple_files=True)def validateFormat(file_format,uploaded_files) : """ Checks if the format of uploaded files matches the selected format. Args: file_format (str): The selected file format (CSV, PDF, TXT). uploaded_files (list): A list of uploaded files. Returns: bool: True if all file formats match, False otherwise. """ for file in uploaded_files : if str(file_format).lower() not in str(file.type).lower(): return False return Truedef selectPDFAnalysis() : """ Prompts the user to select the type of PDF analysis (Compare or Merge). Returns: str: The selected analysis type ("Compare" or "Merge"). """ type_pdf = st.selectbox("Select Anaylsis Type on PDFs", ["Compare","Merge"]) if type_pdf=="Compare" : st.write("Analysis Comparing PDFs") return "Compare" else : st.write("Analysis Merging PDFs") return "Merge"def save_uploadedfile(uploadedfile): """ Saves the uploaded file to the current directory. Args: uploaded_file (streamlit.UploadedFile): The uploaded file object. Returns: str: A success message indicating the file has been saved. """ with open(os.path.join(uploadedfile.name),"wb") as f: f.write(uploadedfile.getbuffer()) return st.success("Saved File") ```

4- Direct the chatbot into the correct action based on the file format:

* The chat history is maintained and displayed using _history_func()_
* _CSVAnalysis()_ function uses a csv agent to analyze your file, give you insights and answer your questions. No embedding is required here.
* _MergePDFAnalysis()_ function is used to merge multiple pdf files based on the user choice. HuggingFace Embedding is used here with OpenAI LLM.
* _ComparePDFAnalysis()_ function is used to compare multiple pdf files based on the user choice. HuggingFace Embedding is used here with an OpenAI Agent.
* _TextAnalysis()_ function is used to chat with your text file, analyze it and give you insights and answers to your questions. HuggingFace Embedding is used here with OpenAI LLM.
* All above functions support Text-To-Speech functionality to the answer.

```python #=================# Answer Generation Functions Based on Uploaded File Format#=================def history_func(answer,q): """ Creates and manages the chat history in the Streamlit session state. Args: answer (str): The answer generated by the LLM. q (str): The user's question. """ # if there's no chat history in the session state, create it if 'history' not in st.session_state: st.session_state.history = '' # the current question and answer value = f'Q: {q}
A: {answer}' st.session_state.history = f'{value}
{"-" * 100}
{st.session_state.history}' h = st.session_state.history # text area widget for the chat history st.text_area(label='Chat History', value=h, key='history', height=400) def CSVAnalysis(uploaded_file) : """ Performs analysis on a CSV file and allows users to ask questions. Args: uploaded_file (streamlit.UploadedFile): The uploaded CSV file. """ df = pd.read_csv(uploaded_file) left_column,right_column = st.columns(2) with left_column: st.header("Dataframe Head") st.write(df.head()) with right_column: st.header("Dataframe Tail") st.write(df.tail()) save_uploadedfile(uploaded_file) fileName = uploaded_file.name st.write("fileName is " + fileName) user_query = st.text_input('Enter your query') agent = create_csv_agent(ChatOpenAI(temperature=0),fileName,verbose=True,max_iterations=100) if st.button("Answer My Question"): st.write("Running the query " , user_query) response = agent.run(user_query) st.text_area('LLM Answer: ', value=response, height=400) sound_file = BytesIO() client = OpenAI() aud = client.audio.speech.create( model="tts-1", voice="alloy", input=response) aud.stream_to_file("output.mp3") st.audio("output.mp3") history_func(response,user_query) def MergePDFAnalysis(uploaded_files) : """ Merges the text content of multiple PDFs and allows users to ask questions. Args: uploaded_files (list): A list of uploaded PDF files. """ raw_text = '' for file in uploaded_files: pdf_reader = PdfReader(file) temp_text = '' for i, page in enumerate(pdf_reader.pages): text = page.extract_text() if text: temp_text += text raw_text += temp_text # Split the text into smaller chunks for indexing text_splitter = CharacterTextSplitter( separator="
", chunk_size=1000, chunk_overlap=200, length_function=len, ) texts = text_splitter.split_text(raw_text) # Download embeddings from OpenAI embeddings = HuggingFaceEmbeddings( model_name="sentence-transformers/all-mpnet-base-v2", # Provide the pre-trained model's path model_kwargs={'device':'cpu'}, # Pass the model configuration options encode_kwargs={'normalize_embeddings': False}) docsearch = FAISS.from_texts(texts, embeddings) st.subheader("Enter a question:") question = st.text_input("Question") if st.button("Answer My Question"): # Perform question answering docs = docsearch.similarity_search(question) chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff") answer = chain.run(input_documents=docs, question=question) st.subheader("Answer:") st.text_area('LLM Answer: ', value=answer, height=400) sound_file = BytesIO() client = OpenAI() aud = client.audio.speech.create( model="tts-1", voice="alloy", input=answer) aud.stream_to_file("output.mp3") st.audio("output.mp3") history_func(answer,question) def ComparePDFAnalysis(uploaded_files) : """ Compares the text content of multiple PDFs and allows users to ask questions about each PDF. Args: uploaded_files (list): A list of uploaded PDF files. """ tools = [] llm = ChatOpenAI(temperature=0) for file in uploaded_files: st.write("File name is ", file.name) save_uploadedfile(file) loader = PyPDFLoader(file.name) pages = loader.load_and_split() text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) docs = text_splitter.split_documents(pages) embeddings = HuggingFaceEmbeddings( model_name="sentence-transformers/all-mpnet-base-v2", # Provide the pre-trained model's path model_kwargs={'device':'cpu'}, # Pass the model configuration options encode_kwargs={'normalize_embeddings': False}) retriever = FAISS.from_documents(docs, embeddings).as_retriever() function_name = file.name.replace('.pdf', '').replace(' ', '_')[:64] tools.append(Tool(name=function_name,description=f"useful when you want to answer questions about {function_name}",func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever))) agent = initialize_agent( agent=AgentType.OPENAI_FUNCTIONS, tools=tools, llm=llm, verbose=True, ) question = st.text_input("Question") if st.button("Answer My Question"): st.write("Running the query") response = agent.run(question) st.text_area('LLM Answer: ', value=response, height=400) sound_file = BytesIO() client = OpenAI() aud = client.audio.speech.create( model="tts-1", voice="alloy", input=response) aud.stream_to_file("output.mp3") st.audio("output.mp3") history_func(response,question) def TextAnalysis(uploaded_files) : """ Performs analysis on a text file and allows users to ask questions. Args: uploaded_files (list): A list of uploaded text files. """ raw_text = '' for file in uploaded_files: temp_text = file.read().decode("utf-8") raw_text += temp_text # Split the text into smaller chunks for indexing text_splitter = CharacterTextSplitter( separator="
", chunk_size=1000, chunk_overlap=200, length_function=len, ) texts = text_splitter.split_text(raw_text) # Download embeddings from OpenAI embeddings = HuggingFaceEmbeddings( model_name="sentence-transformers/all-mpnet-base-v2", # Provide the pre-trained model's path model_kwargs={'device':'cpu'}, # Pass the model configuration options encode_kwargs={'normalize_embeddings': False}) docsearch = FAISS.from_texts(texts, embeddings) st.subheader("Enter a question:") question = st.text_input("Question") if st.button("Answer My Question"): # Perform question answering docs = docsearch.similarity_search(question) chain = load_qa_chain(ChatOpenAI(temperature=0), chain_type="stuff") answer = chain.run(input_documents=docs, question=question) st.subheader("Answer:") st.text_area('LLM Answer: ', value=answer, height=400) sound_file = BytesIO() client = OpenAI() aud = client.audio.speech.create( model="tts-1", voice="alloy", input=answer) aud.stream_to_file("output.mp3") st.audio("output.mp3") history_func(answer,question) ```

5- Execution (Generation) part:

```json #=================# Answer Generation#================= if uploaded_files: if validateFormat(file_format,uploaded_files) :# st.write("Format is valid") if file_format=="CSV" : if len(uploaded_files)>1 : st.write("Only 1 CSV file can be uploded") else :# st.write("CSV Analysis") for file in uploaded_files : CSVAnalysis(file) elif file_format == "PDF" : if len(uploaded_files) > 1 : select = selectPDFAnalysis() if(select=="Compare") : ComparePDFAnalysis(uploaded_files) else : MergePDFAnalysis(uploaded_files) else :# st.write(" Single pdf analysis ") MergePDFAnalysis(uploaded_files) else : TextAnalysis(uploaded_files) # st.write(" Text Analysis ") else : st.write("Formats are not valid") ```

This is how the output will look like:

![image](https://miro.medium.com/v2/resize:fit:700/1*htWxZhff8SeEklXlSuJoVg.png)

Feel free to try the chatbot [here](<https://gen-ai-chatbot.streamlit.app/>).

The full GitHub Repo can be accessed [here](<https://github.com/hanantabak2/RAG_chatbot_on_Streamlit_with_Speech_Functionality/tree/main>).

*Edit : Three weeks after publishing this article, I wrote a new one on how to trace the costs generated by this RAG app using LangSmith Costs Tracing feature [here](</me/stats/post/2109157116a7>).

In the next articles, I’ll try more advanced techniques like:

* Using Unstructured libraries for better ingestion of unstructured files.
* Multi-modal RAGs
* Using LangSmith for tracing and validation
* LLMOps
* Hybrid approach of Finetuning + RAG to empower the performance.
* and many more, so stay tuned!

If you found this article insightful, feel free to share it with your network and leave your thoughts in the comments. Let’s continue the conversation!

— — — — — — — — — — — — — — — — — — — — — — — — — — — —

Feel free to check [My LinkedIn Page](<https://www.linkedin.com/in/hanan-tabak/>).

If you need BSc, MSc or PhD scholarships, check [how I got my Master of Data Science Scholarship paying only 11% of the total fees](</@hanan.tabak/how-i-was-accepted-in-a-scholarship-for-a-master-of-data-science-paying-only-25-of-total-fees-6b2d6dc6c248>) article.
