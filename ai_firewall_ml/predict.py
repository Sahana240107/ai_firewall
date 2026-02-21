import torch
import re
import numpy as np
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# ==============================
# CONFIG
# ==============================
MODEL_PATH = "./results/checkpoint-325"  # change if your model folder is different
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==============================
# LOAD MODEL + TOKENIZER
# ==============================
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(DEVICE)
model.eval()

# ==============================
# LABEL MAP (adjust if needed)
# ==============================
label_map = {
    0: "SAFE",
    1: "PII",
    2: "SENSITIVE"
}

# ==============================
# REGEX RULES (Hybrid Layer)
# ==============================
regex_patterns = {
    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone": r"\b\d{10}\b",
    "api_key": r"\b[A-Za-z0-9]{32,}\b"
}


def rule_based_detection(text):
    matches = {}
    for key, pattern in regex_patterns.items():
        found = re.findall(pattern, text)
        if found:
            matches[key] = found
    return matches


# ==============================
# RISK LOGIC
# ==============================
def calculate_risk(label, confidence, rule_matches):

    # Regex match = strong signal
    if rule_matches:
        return 0.95, "BLOCK"

    # Very high confidence sensitive
    if label == "SENSITIVE" and confidence > 0.90:
        return confidence, "BLOCK"

    # High confidence PII
    if label == "PII" and confidence > 0.80:
        return confidence, "REDACT"

    # Otherwise allow
    return confidence, "ALLOW"


# ==============================
# MAIN PREDICT FUNCTION
# ==============================
def predict(text):

    inputs = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt"
    )

    inputs = {key: val.to(DEVICE) for key, val in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]

    predicted_class = np.argmax(probabilities)
    confidence = float(probabilities[predicted_class])

    label = label_map[predicted_class]

    # Hybrid Rule Engine
    rule_matches = rule_based_detection(text)

    risk_score, action = calculate_risk(label, confidence, rule_matches)

    return {
        "input_text": text,
        "predicted_label": label,
        "confidence": round(confidence, 4),
        "risk_score": round(risk_score, 4),
        "action": action,
        "rule_matches": rule_matches
    }


# ==============================
# CLI TESTING
# ==============================
if __name__ == "__main__":

    print("\n🔥 AI Firewall Prediction Console")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("Enter text: ")

        if user_input.lower() == "exit":
            break

        result = predict(user_input)

        print("\n--- RESULT ---")
        for key, value in result.items():
            print(f"{key}: {value}")
        print("----------------\n")