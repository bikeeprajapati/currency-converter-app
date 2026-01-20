
# 💱 Currency Converter (LangChain Tools + FastAPI + Streamlit)

A **GenAI-powered currency converter** that uses **LangChain tool calling**, a **Hugging Face LLM**, **FastAPI backend**, and **Streamlit frontend** to convert currencies via a real external API.

This project demonstrates **real-world GenAI engineering**, including tool binding, API orchestration, environment management, and defensive error handling.

---

## 🚀 Features

- 🤖 **LLM-driven tool calling** using LangChain
- 🔧 Two custom tools:
  - Get currency conversion rate
  - Convert currency amount
- 🌐 **Real currency data** via external API
- ⚡ **FastAPI backend** for API orchestration
- 🖥️ **Streamlit frontend** for interactive UI
- 🔐 Secure environment variable handling (`.env`)
- 🛡️ Defensive error handling (no silent failures)
- 🧪 Debug-friendly logging for learning & development

---

## 🧠 How It Works (Architecture)

```

User (Streamlit UI)
|
v
FastAPI Backend (/convert)
|
v
LangChain LLM (Hugging Face)
|
v
Tool Selection (get_rate / convert_currency)
|
v
Currency API (external)
|
v
Result → FastAPI → Streamlit

```

### Key Idea  
The LLM **does not do the math itself**.  
It decides **which tool to call**, and the tool performs the actual computation using live data.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain**
- **Hugging Face Inference API**
- **FastAPI**
- **Streamlit**
- **Requests**
- **python-dotenv**

---

## 📁 Project Structure

```

currency-converter-app/
│
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── schemas.py              # Pydantic schemas
│   │
│   ├── agents/
│   │   └── currency_agent.py   # LLM + tool binding
│   │
│   ├── tools/
│   │   └── currency_tools.py   # LangChain tools
│   │
│   └── services/
│       └── currency_api.py     # External currency API logic
│
├── frontend/
│   └── app.py                  # Streamlit UI
│
├── .env                        # Environment variables (NOT committed)
├── .gitignore
├── requirements.txt
└── README.md

````

---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/currency-converter-app.git
cd currency-converter-app
````

---

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Create `.env` File

```env
HUGGINGFACE_API_KEY=hf_your_huggingface_key
CURRENCY_API_KEY=cur_live_your_currency_api_key
```

> ⚠️ **Never commit `.env`**
> Make sure `.env` is in `.gitignore`

---

## ▶️ Run the Application

### Start Backend (FastAPI)

```bash
PYTHONPATH=$(pwd) python -m uvicorn backend.main:app
```

Backend runs at:

```
http://127.0.0.1:8000
```

API Docs:

```
http://127.0.0.1:8000/docs
```

---

### Start Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

---

## 🧪 Example Query

```
Convert 100 USD to INR
```

### Example Response

```json
{
  "result": "8321.45"
}
```

---

## 🧩 LangChain Tools Used

### 1️⃣ `get_currency_rate_tool`

Returns the exchange rate between two currencies.

### 2️⃣ `convert_currency_tool`

Uses the exchange rate to convert an amount.

The LLM decides **which tool to call** based on the user’s query.

---

## 🛡️ Error Handling Philosophy

* No silent failures
* External API errors are surfaced clearly
* Missing API keys fail fast with helpful messages
* Defensive JSON parsing for external responses

---

## 🔐 Security Notes

* API keys are **never hardcoded**
* `.env` is excluded via `.gitignore`
* Safe to publish repository publicly

---

## 📌 Why This Project Is Valuable

This project demonstrates:

* ✅ Real **GenAI tool calling**
* ✅ Clean backend architecture
* ✅ Production-style debugging
* ✅ Secure secrets handling
* ✅ Full-stack integration

It goes **beyond tutorials** and reflects **real engineering work**.

---

## 🚧 Possible Improvements

* Add caching for exchange rates
* Add fallback currency APIs
* Add mock mode (run without API keys)
* Convert to LangGraph
* Add unit tests
* Dockerize the app

---

## 📜 License

MIT License

---

## 🙌 Author

**Vicky Prajapati**
GenAI / Backend Developer

---

⭐ If you found this useful, consider starring the repo!


