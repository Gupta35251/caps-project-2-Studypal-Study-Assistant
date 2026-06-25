# caps-project-2-Studypal-Study-Assistant  

# 📚 StudyPal – AI Powered Study Assistant

StudyPal is an AI-powered study assistant built using **Streamlit**, **LangChain**, **ChromaDB**, **Groq LLM**, and **MongoDB**. It enables students to ask questions from their textbooks, receive context-aware answers using Retrieval-Augmented Generation (RAG), and get relevant YouTube video recommendations for further learning.

---

## 🚀 Features

* 📖 Subject and chapter-wise question answering
* 🤖 AI-powered responses using Groq Llama 3.3
* 🔍 Retrieval-Augmented Generation (RAG)
* 🗂️ ChromaDB vector database for semantic search
* 💬 Multi-turn conversational chat with memory
* 📺 YouTube video recommendations based on user queries
* 📝 Automatic conversation title generation
* 🗃️ MongoDB integration for storing chat history
* 📚 Previous conversation history from the sidebar
* ⚡ Fast and interactive Streamlit interface

---

## 🛠️ Tech Stack

* Python 3.11
* Streamlit
* LangChain
* ChromaDB
* HuggingFace Embeddings
* Groq API (Llama 3.3)
* MongoDB
* YouTube Search Python
* Sentence Transformers

---

## 📂 Project Structure

```
StudyPal/
│
├── Data/
├── DB/
├── mongodb/
├── main.py
├── chat_title.py
├── chatbot_utility.py
├── get_yt_video.py
├── vectorize_book.py
├── vectorize_script.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone <repository-url>
cd StudyPal
```

### Create a virtual environment

```bash
conda create -n studypal python=3.11
conda activate studypal
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## ▶️ Run the Application

```bash
streamlit run main.py
```

---

## 🧠 How It Works

1. User selects a subject and chapter.
2. The selected chapter's vector database is loaded.
3. User asks a question.
4. LangChain retrieves the most relevant document chunks from ChromaDB.
5. Groq Llama generates an answer using the retrieved context.
6. Related YouTube videos are recommended.
7. The complete conversation is stored in MongoDB for future access.

---

## 📌 Future Improvements

* User authentication
* PDF upload support
* Voice-based interaction
* Image-based question answering
* Conversation export (PDF)
* Multi-language support

---

## 👨‍💻 Author

**Prince**

Built as an AI-powered educational assistant using modern Retrieval-Augmented Generation (RAG) techniques.
