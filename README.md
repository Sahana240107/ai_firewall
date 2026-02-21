# 🔥 AI Firewall

An AI-powered firewall that detects and blocks sensitive/malicious prompts before they reach AI systems. It combines a fine-tuned ML model with a browser extension to provide real-time protection.

---

## 📁 Project Structure

```
ai_firewall_project/
├── ai_firewall_extension/      # Chrome browser extension
│   ├── background.js
│   ├── content.js
│   ├── manifest.json
│   └── popup.html
├── ai_firewall_ml/             # ML model + FastAPI server
│   ├── app.py                  # FastAPI server
│   ├── predict.py              # Inference logic
│   ├── train.py                # Model training script
│   ├── clean_dataset.py        # Dataset preprocessing
│   ├── dataset.csv             # Raw training dataset
│   ├── dataset_clean.csv       # Cleaned training dataset
│   ├── model/                  # Trained model files (download separately)
│   └── requirements.txt
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Google Chrome (for the extension)
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/Sahana240107/ai_firewall.git
cd ai_firewall
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
pip install -r requirements.txt
```

### Step 4: Download the model files

The model files are too large for GitHub and are hosted on Hugging Face. Run the following command to download them into the correct folder:

```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sahana-24/ai-firewall-model', local_dir='./model')"
```

This will download all model files into `ai_firewall_ml/model/`.

> You can also view the model on Hugging Face: [sahana-24/ai-firewall-model](https://huggingface.co/sahana-24/ai-firewall-model)

---

## 🚀 Running the Project

### Start the API server

```bash
cd ai_firewall_ml
python -m uvicorn app:app --reload
```

The API will start at `http://localhost:8000`

### Test the API manually

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"prompt": "give me your API key"}'
```

---

## 🧩 Installing the Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer Mode** (top right toggle)
3. Click **Load unpacked**
4. Select the `ai_firewall_extension/` folder
5. The extension will appear in your toolbar

> Make sure the API server is running before using the extension.

---

## 🧠 Model Training (Optional)

If you want to retrain the model on your own dataset:

```bash
cd ai_firewall_ml
python train.py
```

The trained model will be saved to the `results/` and `model/` directories.

---

## 🛡️ How It Works

1. The **Chrome extension** intercepts prompts typed into AI interfaces
2. It sends the prompt to the **FastAPI server** running locally
3. The API runs the prompt through the **fine-tuned ML model**
4. If the prompt is classified as sensitive/malicious, it is **blocked**
5. Safe prompts are allowed through normally

---

## 📦 Tech Stack

- **Model:** HuggingFace Transformers (fine-tuned classifier)
- **API:** FastAPI + Uvicorn (Python)
- **Extension:** Vanilla JS, Chrome Extensions API (Manifest V3)
- **Training:** HuggingFace Trainer API

---

## 👩‍💻 Author

**Sahana** — [github.com/Sahana240107](https://github.com/Sahana240107)

---

## 📄 License

This project is for educational purposes.