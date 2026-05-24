---
domain: github.com
fetch_date: '2026-05-18T12:36:17.535764'
status: ok
url: https://github.com/QiuYannnn/Local-File-Organizer
---

Tired of digital clutter? Overwhelmed by disorganized files scattered across your computer? Let AI do the heavy lifting! The Local File Organizer is your personal organizing assistant, using cutting-edge AI to bring order to your file chaos - all while respecting your privacy.

Before:

```
/home/user/messy_documents/
├── IMG_20230515_140322.jpg
├── IMG_20230516_083045.jpg
├── IMG_20230517_192130.jpg
├── budget_2023.xlsx
├── meeting_notes_05152023.txt
├── project_proposal_draft.docx
├── random_thoughts.txt
├── recipe_chocolate_cake.pdf
├── scan0001.pdf
├── vacation_itinerary.docx
└── work_presentation.pptx
0 directories, 11 files
```


After:

```
/home/user/organized_documents/
├── Financial
│ └── 2023_Budget_Spreadsheet.xlsx
├── Food_and_Recipes
│ └── Chocolate_Cake_Recipe.pdf
├── Meetings_and_Notes
│ └── Team_Meeting_Notes_May_15_2023.txt
├── Personal
│ └── Random_Thoughts_and_Ideas.txt
├── Photos
│ ├── Cityscape_Sunset_May_17_2023.jpg
│ ├── Morning_Coffee_Shop_May_16_2023.jpg
│ └── Office_Team_Lunch_May_15_2023.jpg
├── Travel
│ └── Summer_Vacation_Itinerary_2023.docx
└── Work
├── Project_X_Proposal_Draft.docx
├── Quarterly_Sales_Report.pdf
└── Marketing_Strategy_Presentation.pptx
7 directories, 11 files
```


**[2024/09] v0.0.2**:

- Featured by Nexa Gallery and Nexa SDK Cookbook!
- Dry Run Mode: check sorting results before committing changes
- Silent Mode: save all logs to a txt file for quieter operation
- Added file support:
`.md`

, .`excel`

,`.ppt`

, and`.csv`

- Three sorting options: by content, by date, and by type
- The default text model is now Llama3.2 3B
- Improved CLI interaction experience
- Added real-time progress bar for file analysis

Please update the project by deleting the original project folder and reinstalling the requirements. Refer to the installation guide from Step 4.

- Copilot Mode: chat with AI to tell AI how you want to sort the file (ie. read and rename all the PDFs)
- Change models with CLI
- ebook format support
- audio file support
- video file support
- Implement best practices like Johnny Decimal
- Check file duplication
- Dockerfile for easier installation
- People from Nexa is helping me to make executables for macOS, Linux and Windows

This intelligent file organizer harnesses the power of advanced AI models, including language models (LMs) and vision-language models (VLMs), to automate the process of organizing files by:

-
Scanning a specified input directory for files.

-
Content Understanding:

**Textual Analysis**: Uses the Llama3.2 3B to analyze and summarize text-based content, generating relevant descriptions and filenames.**Visual Content Analysis**: Uses the LLaVA-v1.6 , based on Vicuna-7B, to interpret visual files such as images, providing context-aware categorization and descriptions.

-
Understanding the content of your files (text, images, and more) to generate relevant descriptions, folder names, and filenames.

-
Organizing the files into a new directory structure based on the generated metadata.


The best part? All AI processing happens 100% on your local device using the Nexa SDK. No internet connection required, no data leaves your computer, and no AI API is needed - keeping your files completely private and secure.

**Images:**`.png`

,`.jpg`

,`.jpeg`

,`.gif`

,`.bmp`

**Text Files:**`.txt`

,`.docx`

,`.md`

**Spreadsheets:**`.xlsx`

,`.csv`

**Presentations:**`.ppt`

,`.pptx`

**PDFs:**`.pdf`


**Operating System:**Compatible with Windows, macOS, and Linux.**Python Version:**Python 3.12**Conda:**Anaconda or Miniconda installed.**Git:**For cloning the repository (or you can download the code as a ZIP file).

For SDK installation and model-related issues, please post on here.


Before installing the Local File Organizer, make sure you have Python installed on your system. We recommend using Python 3.12 or later.

You can download Python from the official website.

Follow the installation instructions for your operating system.

Clone this repository to your local machine using Git:

`git clone https://github.com/QiuYannnn/Local-File-Organizer.git`

Or download the repository as a ZIP file and extract it to your desired location.

Create a new Conda environment named `local_file_organizer`

with Python 3.12:

`conda create --name local_file_organizer python=3.12`

Activate the environment:

`conda activate local_file_organizer`

To install the CPU version of Nexa SDK, run:

`pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/cpu --extra-index-url https://pypi.org/simple --no-cache-dir`

For the GPU version supporting Metal (macOS), run:

`CMAKE_ARGS="-DGGML_METAL=ON -DSD_METAL=ON" pip install nexaai --prefer-binary --index-url https://nexaai.github.io/nexa-sdk/whl/metal --extra-index-url https://pypi.org/simple --no-cache-dir`

For detailed installation instructions of Nexa SDK for **CUDA** and **AMD GPU** support, please refer to the Installation section in the main README.

-
Ensure you are in the project directory:

`cd path/to/Local-File-Organizer`

Replace

`path/to/Local-File-Organizer`

with the actual path where you cloned or extracted the project. -
Install the required dependencies:

pip install -r requirements.txt


**Note:** If you encounter issues with any packages, install them individually:

`pip install nexa Pillow pytesseract PyMuPDF python-docx`

With the environment activated and dependencies installed, run the script using:

`python main.py`

-
**SDK Models:**- The script uses
`NexaVLMInference`

and`NexaTextInference`

models usage. - Ensure you have access to these models and they are correctly set up.
- You may need to download model files or configure paths.

- The script uses
-
**Dependencies:****pytesseract:**Requires Tesseract OCR installed on your system.**macOS:**`brew install tesseract`

**Ubuntu/Linux:**`sudo apt-get install tesseract-ocr`

**Windows:**Download from Tesseract OCR Windows Installer

**PyMuPDF (fitz):**Used for reading PDFs.

-
**Processing Time:**- Processing may take time depending on the number and size of files.
- The script uses multiprocessing to improve performance.

-
**Customizing Prompts:**- You can adjust prompts in
`data_processing.py`

to change how metadata is generated.

- You can adjust prompts in

This project is dual-licensed under the MIT License and Apache 2.0 License. You may choose which license you prefer to use for this project.

- See the MIT License for more details.
