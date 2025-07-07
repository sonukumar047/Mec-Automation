# 📁 NX CAD Automation Chatbot

This project is a **Streamlit-based frontend** connected to a **locally hosted LLM (via Ollama)** that generates **NX Open API** automation code from natural language prompts.

---

## 📦 Project Structure (mkdir format)

```bash
nx_cad_chatbot/
├── app.py                    # 🎯 Main Streamlit app that runs the chatbot
├── requirements.txt          # 📦 List of required Python packages
├── README.md                 # 📘 This detailed documentation
├── .gitignore                # 🚫 Ignore Python cache, venv, etc.
├── nx_open_sample_dataset.json  # 📚 Optional dataset for sample prompts
└── .streamlit/
    └── secrets.toml          # 🔐 (Optional) Streamlit secrets config
```

---

## 🚀 Features

- ✅ Generate Siemens NX Open API code from natural language
- 🔄 Support for multiple languages: **Python**, **C++**, **VB.NET**
- 🧠 Powered by a **local LLM** using Ollama (e.g., `llama3.2:3b`)
- 💾 Download generated code
- 🧪 Prompt examples for inspiration
- 🧱 Simple UI built with Streamlit

---

## 🔧 Setup Instructions

### 📁 1. Clone the repository

```bash
git clone https://github.com/your-username/nx_cad_chatbot.git
cd nx_cad_chatbot
```

### 🐍 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 📦 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 🤖 4. Run the Ollama LLM backend

Make sure [Ollama](https://ollama.com/) is installed and you’ve pulled a supported model:

```bash
ollama run llama3.2:3b
```

> ⚠️ The model must be running on `http://localhost:11434`

---

## 🚦 Run the Streamlit Chatbot

```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501](http://localhost:8501)

---

## 💡 Example Prompts

Try any of the following:
- `"Create a block of 100x50x25 mm and drill a hole of 10 mm diameter at the center top face."`
- `"Make a cylinder of 30 mm diameter and 40 mm height along Z-axis."`
- `"Add 4 holes of 5 mm diameter at the corners of a 60x60 mm square plate."`

---

## 🧠 How It Works

1. User selects a **target programming language**
2. Enters a **CAD task in natural language**
3. App sends prompt to **Ollama** using `requests`
4. Receives **clean code** in NX Open API
5. Shows and allows **code download**

---

## 📄 requirements.txt

```txt
streamlit
requests
```

Add more packages as needed (like `openai`, etc.).

---

## 📁 .gitignore

```gitignore
__pycache__/
*.pyc
venv/
*.env
.streamlit/secrets.toml
```

---

## 📚 Sample Dataset

Enable "Show sample dataset prompts" in the app to view contents from `nx_open_sample_dataset.json`.

---

## 📝 License

This project is licensed under the **MIT License**.

---

## 🙋‍♂️ Author

**Sonu Kumar**  
GitHub: https://github.com/sonukumar047
Email: sonuhits047@gmail.com

---

