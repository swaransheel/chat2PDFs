# Smart PDF Assistant

# https://chat2pdfs.streamlit.app/

## Overview

The **Smart PDF Assistant** is a conversational AI tool built with Streamlit that allows users to interact with PDF documents. Users can upload PDF files, extract text from them, and ask questions about the content. The assistant provides clear and detailed answers based on the extracted text.

## Features

- **PDF Upload**: Users can upload multiple PDF files for analysis.
- **Text Extraction**: The tool extracts text from the uploaded PDFs.
- **Conversational Interface**: Users can ask questions related to the PDF content and receive informative responses.
- **Vector Store**: Utilizes FAISS for efficient similarity search and context retrieval.
- **Google Generative AI**: Integrates with Google’s generative AI for answering questions.

![alt text](https://raw.githubusercontent.com/alejandro-ao/ask-multiple-pdfs/refs/heads/main/docs/PDF-LangChain.jpg)
## Technologies Used

- [Streamlit](https://streamlit.io/) - Framework for building web apps.
- [PyPDF2](https://github.com/py-pdf/PyPDF2) - Library for reading PDF files.
- [LangChain](https://langchain.com/) - Framework for building applications with LLMs.
- [FAISS](https://faiss.ai/) - Library for efficient similarity search.
- [Google Generative AI](https://developers.generativeai.google/) - Google’s generative AI for natural language processing.
- [Python Dotenv](https://pypi.org/project/python-dotenv/) - Library for managing environment variables.

## Installation

To run the Smart PDF Assistant, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/smart-pdf-assistant.git
   cd smart-pdf-assistant
   ```
2. Create a virtual environment and activate it:

# On macOS and Linux:
 ```bash
python3 -m venv venv
source venv/bin/activate
```
# On Windows:
 ```bash
python -m venv venv
venv\Scripts\activate
```
3. Install the required packages:
 ```bash
pip install -r requirements.txt
```
4. Set up your environment variables by creating a .env file in the root directory:
 ```bash
GOOGLE_API_KEY=your_google_api_key
```
5. Run the application:
 ```bash
streamlit run app.py
```
## Usage
Upload your PDF files using the file uploader in the sidebar.
Click on "Start Analysis" to extract text from the PDFs.
Ask questions about the PDF content in the text input box and click "Submit" to receive answers.
Example
User: What is the main topic of the document?
Assistant: The main topic of the document is...
