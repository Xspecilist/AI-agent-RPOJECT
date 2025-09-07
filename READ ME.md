# AI Research Agent

An AI-powered research assistant web app built for the **HCL x GUVI Hackathon**.  
The app fetches relevant URLs, extracts article content, and generates concise research summaries.

---

## 🚀 Features
- Web search integration with **Brave API**.
- Content extraction using **Trafilatura**.
- Text summarization using **DistilBART (HuggingFace)**.
- Frontend in **React.js**.
- Backend with **FastAPI**.
- Export summaries as **PDF/Word** (client-side using `html2pdf.js`).
- Country-specific search filtering.

---

## 🛠️ Tech Stack
- **Frontend:** [React.js](https://react.dev/) + [html2pdf.js](https://www.npmjs.com/package/html2pdf.js)
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Web Search API:** [Brave Search API](https://brave.com/search/api/)
- **Content Extraction:** [Trafilatura](https://github.com/adbar/trafilatura)
- **Summarization Model:** [DistilBART (HuggingFace)](https://huggingface.co/sshleifer/distilbart-cnn-12-6)

---

## ⚠️ Important note about API keys
**This project stores the Brave API key directly in the source code** (hard-coded). This was done for the hackathon demo convenience, but it is not secure for production. If you publish this repository, remove or rotate any exposed keys and consider using environment variables or a secrets manager.

File & location used (example):
```
backend/main.py  # search for BRAVE_API_KEY or x-subscription-token
```

---

## ⚙️ Setup Instructions (Complete)
> These steps assume you have Python 3.10+ and Node.js/npm installed.

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ai-research-agent.git
cd ai-research-agent
```

### 2. Backend Setup (FastAPI)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** The Brave API key is currently hard-coded in `backend/main.py`. You can run the server as-is for the demo, but remember this key is sensitive.

Run the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```

Open http://127.0.0.1:8000/docs to view Swagger UI.

### 3. Frontend Setup (React)
```bash
cd frontend
npm install
npm start
```

The frontend should open at http://localhost:3000 (or http://localhost:5173 depending on tooling). It will call the backend at `http://localhost:8000` by default.

---

## 📦 Files to include
- `backend/requirements.txt` — Python dependencies.
- `frontend/package.json` — Node dependencies & start scripts.
- `README.md` — this file.

---

## 📋 `requirements.txt` (backend)
Copy this file to `backend/requirements.txt`:
```
fastapi>=0.95.0
uvicorn[standard]>=0.22.0
requests>=2.28.0
trafilatura>=0.9.0
transformers>=4.30.0
torch>=2.0.0
python-multipart>=0.0.6
```

> If you run into large wheel builds for `torch`, consider installing a CPU-only wheel appropriate for your platform, e.g.: `pip install torch --index-url https://download.pytorch.org/whl/cpu`.

---

## 🧩 `package.json` (frontend)
Use this minimal `package.json` in `frontend/package.json` (adjust `name` and `author` as needed):

```json
{
  "name": "ai-research-agent-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test --env=jsdom",
    "eject": "react-scripts eject"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "html2pdf.js": "^0.10.1"
  },
  "devDependencies": {
    "react-scripts": "5.0.1"
  }
}
```

> If you prefer Vite, replace scripts and use `vite`, `@vitejs/plugin-react` and adjust start/build commands accordingly.

---

## 🔧 How the system works (process)
1. **Query**: User submits a topic via the React frontend.
2. **Search**: Backend calls Brave Search API for top results (you selected 7 results per query).
3. **Scrape**: Trafilatura extracts clean text from each URL.
4. **Summarize**: DistilBART summarizer runs locally on combined extracted text to produce a unified summary.
5. **Display & Export**: Frontend displays the combined summary and allows export (PDF via `html2pdf.js`).

---

## 🔐 Security reminder
- Hard-coding secrets is **not recommended**. For the judges/demo it's acceptable, but for any published repo:
  - Remove the key from source control immediately.
  - Use environment variables or secrets management (e.g., `.env` or cloud secret manager) in real deployments.

---

## 📚 References & Links
- Brave Search API docs: https://brave.com/search/api/
- FastAPI docs: https://fastapi.tiangolo.com/
- Trafilatura: https://github.com/adbar/trafilatura
- DistilBART: https://huggingface.co/sshleifer/distilbart-cnn-12-6
- html2pdf.js: https://www.npmjs.com/package/html2pdf.js

---

## 📝 License
MIT License

---

If you want, I can now generate the actual `requirements.txt` and `package.json` files and add them to the repo or provide ready-to-download files.

