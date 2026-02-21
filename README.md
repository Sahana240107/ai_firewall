# 🛡️ Redactron

An AI-powered browser extension that detects and redacts sensitive information from your prompts in real time — before they ever reach an AI system. Redactron combines a fine-tuned ML model with a Chrome extension to protect your privacy across every AI platform.

🌐 **Website:** [sahana240107.github.io/Redactron](https://sahana240107.github.io/Redactron)  
📦 **Releases:** [github.com/Sahana240107/Redactron/releases](https://github.com/Sahana240107/Redactron/releases)

---

## 📁 Project Structure

```
Redactron/
├── ai_firewall_extension/      # Chrome browser extension
│   ├── background.js
│   ├── content.js
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   └── popup.css
├── ai_firewall_ml/             # ML model + FastAPI backend
│   ├── app.py                  # FastAPI server
│   ├── predict.py              # Inference + redaction logic
│   ├── train.py                # Model training script
│   ├── clean_dataset.py        # Dataset preprocessing
│   ├── dataset.csv             # Raw training dataset
│   ├── dataset_clean.csv       # Cleaned training dataset
│   ├── download_model.py       # Model download helper
│   ├── model/                  # Trained model files (hosted on Hugging Face)
│   └── requirements.txt
└── README.md
```

---

## 🧩 Installing the Extension (Easiest Way)

The extension is distributed via **GitHub Releases** and linked from the **GitHub Pages** landing site — no Chrome Web Store needed.

1. Visit the landing page: [sahana240107.github.io/Redactron](https://sahana240107.github.io/Redactron)
2. Click **Download Extension** — this downloads `redactron.zip` directly from [GitHub Releases](https://github.com/Sahana240107/Redactron/releases/latest)
3. Unzip the downloaded file
4. Open Chrome and go to `chrome://extensions/`
5. Enable **Developer Mode** (top right toggle)
6. Click **Load unpacked**
7. Open the unzipped folder and select the **inner folder** that contains `manifest.json` directly inside it
8. Redactron will appear in your toolbar — you're protected! 🛡️

> The extension connects to the deployed backend automatically — no local setup needed.

---

## ⚙️ Local Development Setup

### Prerequisites
- Python 3.10+
- Google Chrome
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/Sahana240107/Redactron.git
cd Redactron
```

### Step 2: Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
cd ai_firewall_ml
pip install -r requirements.txt
```

### Step 4: Download the model files

The model is hosted on Hugging Face. Run this to download it locally:

```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sahana-24/ai-firewall-model', local_dir='./model')"
```

> View the model on Hugging Face: [sahana-24/ai-firewall-model](https://huggingface.co/sahana-24/ai-firewall-model)

### Step 5: Start the local API server

```bash
python -m uvicorn app:app --reload
```

The API will start at `http://localhost:8000`

> If running locally, update the API URL in `content.js` from the deployed URL back to `http://127.0.0.1:8000`

---

## 🚀 Deployed Backend

The backend is live and publicly deployed on Hugging Face Spaces:

```
https://sahana-24-redactron-api.hf.space
```

Test it directly:
```bash
curl -X POST https://sahana-24-redactron-api.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "my email is test@gmail.com"}'
```

API docs available at: [sahana-24-redactron-api.hf.space/docs](https://sahana-24-redactron-api.hf.space/docs)

---

## 🧠 Model Training (Optional)

To retrain the model on your own dataset:

```bash
cd ai_firewall_ml
python train.py
```

The trained model will be saved to the `results/` and `model/` directories.

---

## 🛡️ How It Works

1. The **Chrome extension** monitors prompts typed into any AI interface in real time
2. The prompt is sent to the **deployed FastAPI backend** on Hugging Face Spaces
3. A **fine-tuned DistilBERT model** classifies the text as Safe, PII, or Sensitive
4. A **regex rule engine** catches structured patterns like emails, phone numbers, and API keys
5. If flagged, the extension **alerts the user** via a popup with a Redact button
6. On clicking Redact, sensitive parts are replaced with placeholders like `[EMAIL]`, `[PHONE]`, `[API_KEY]`
7. The user can continue with the cleaned, safe prompt

---

## 📦 Tech Stack

- **Model:** HuggingFace Transformers — fine-tuned DistilBERT classifier
- **Backend:** FastAPI + Uvicorn, deployed on Hugging Face Spaces (Docker)
- **Extension:** Vanilla JS, Chrome Extensions API (Manifest V3)
- **Training:** HuggingFace Trainer API
- **Model Hosting:** Hugging Face Hub
- **Landing Page:** GitHub Pages
- **Extension Distribution:** GitHub Releases

---

## 👩‍💻 Author

**Sahana** — [github.com/Sahana240107](https://github.com/Sahana240107)

---

## 📄 License

This project is for educational purposes.