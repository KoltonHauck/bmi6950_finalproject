# BMI6950 Final Project

## Contributors

| Name         | U#       | e-mail                |
| ------------ | -------- | --------------------- |
| Blake Dahl   | u0160015 | blake.dahl@utah.edu   |
| Kolton Hauck | u1019364 | kolton.hauck@utah.edu |

## Files

| Filename / Folder      | Description                                                                                                                                                     |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| README.md              | Basic information about the repo / project.                                                                                                                     |
| requirements.txt       | Python package requirements to run the app.                                                                                                                     |
| streamlit_test.py      | Python file to run streamlit app.                                                                                                                               |
| files/                 | Knowledge bases and patient files used in app.                                                                                                                  |
| files/patients/        | Patient files. Each folder corresponds to an individual patient.                                                                                                |
| files/knowledge_bases/ | Knowledge Base(s). Each folder corresponds to a knowledge base that can be loaded in the app.<br />Only 'cardiovascular' is implemented with minimal resources. |
| files/archive/         | Old versions of the code, unused utilities, or other unimplemented/untested knowledgebase files for various reasons.                                            |

## Description

Contained in this repository contains the proof-of-concept of supplying clinicians with the resources to make factual and relevant decisions in prescribing and determining the course of action for their patients. This is delivered in a chatbot-like interface. The user can select for specific patients (and only one at a time) along with specific knowledge bases to use as sources to augment the chatbot's response through a RAG approach.

The examples provided here are very basic, as this is just a proof-of-concept.

The UI is delivered through a Python package called [Streamlit](https://streamlit.io/gallery). These apps can be deployed locally or on the Streamlit Cloud.

The backend is developed primarily through [LangChain](https://python.langchain.com/docs/get_started/introduction).

## Instructions

### Getting Started

There are two ways to get started with this.

1. Streamlit Cloud

Simply go here: [BMI6950 Final Project - Streamlit Cloud](https://bmi6950finalproject.streamlit.app/) and enter your OpenAI API Key. Prompt away!

2. Run Locally

First, clone this repo. Change into the main folder of the repo `bmi6950_finalproject/`, install the required python packages listed in `requirements.txt`, then deploy the app using: `streamlit run streamlit_test.py`. Open a browser window to: `http://localhost:8501/`.

### How to Use

An OpenAI API key is required to run this app. To get one, go here: [OpenAI API Key](https://platform.openai.com/api-keys), and click on `Create new secret key`. Once generated, copy and paste it into the sidebar of the app while running. You should be notified when entered.

Once the API key is entered, you can start prompting. This will essentially be just like prompting ChatGPT in the UI. The specific model can be selected for in the sidebar as well.

There is a button at the bottom of the sidebar to clear the chat history.

There is an option to load a patient chart (none by default) and an option to load a knowledge base. Nothing will happen when these selections are made from the dropdown until the `Create VDB` button is selected. Only one patient can be loaded at a time. Only one knowledge base can be loaded at a time. But multiple files from a knowledge base can be selected.

When the `Create VDB` button is pressed, a vector DB will be generated for both the selected patient files and the knowledge base files. These are generated separately and the model has access to these DBs through a `MultiRetrievalQAChain`. (More LangChain chains can be found here: [Chains](https://python.langchain.com/docs/modules/chains)).

## Opportunities for Improvement

* an option to download current chat history
* an option to upload chat history
* expanding knowledge base (specifically within the 'cardiovascular' folder and more high-level topics)
* an option to customize model parameters such as temperature, top-p and top-k
* an option to customize the system prompt of the model
* a physical vector DB, rather one that is run in memory (FAISS was used)
* experimentation with other steps in the Vector DB process (text splitter, embeddings, etc)
* multi-modal implementations, so the model can read images and graphs, such as ECGs and make inferences about those
* a file viewer in the app, so one can see the knowledge base files as well as the patient files
* more complex charts and knowledge bases
* allow for multiple types of files (.pdf, .txt, .json, C-CDA, FHIR
*
