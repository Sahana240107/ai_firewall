import pandas as pd
import numpy as np
import torch

from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


# -----------------------------
# 1️⃣ Load Clean Dataset
# -----------------------------
df = pd.read_csv("dataset_clean.csv")

# Ensure correct types
df["text"] = df["text"].astype(str)
df["label"] = df["label"].astype(int)

print("Dataset shape:", df.shape)
print("Class distribution:\n", df["label"].value_counts())


# -----------------------------
# 2️⃣ Stratified Train/Test Split
# -----------------------------
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df["text"].tolist(),
    df["label"].tolist(),
    test_size=0.2,
    stratify=df["label"],   # VERY IMPORTANT
    random_state=42
)


# -----------------------------
# 3️⃣ Load Tokenizer
# -----------------------------
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")


# -----------------------------
# 4️⃣ Tokenize Data
# -----------------------------
train_encodings = tokenizer(
    train_texts,
    truncation=True,
    padding=True,
    max_length=128
)

val_encodings = tokenizer(
    val_texts,
    truncation=True,
    padding=True,
    max_length=128
)


# -----------------------------
# 5️⃣ Convert to HF Dataset
# -----------------------------
train_dataset = Dataset.from_dict({
    "input_ids": train_encodings["input_ids"],
    "attention_mask": train_encodings["attention_mask"],
    "labels": train_labels
})

val_dataset = Dataset.from_dict({
    "input_ids": val_encodings["input_ids"],
    "attention_mask": val_encodings["attention_mask"],
    "labels": val_labels
})


# -----------------------------
# 6️⃣ Load Model
# -----------------------------
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=3
)


# -----------------------------
# 7️⃣ Metrics Function
# -----------------------------
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="weighted",
        zero_division=0
    )

    acc = accuracy_score(labels, predictions)

    return {
        "accuracy": acc,
        "f1": f1,
        "precision": precision,
        "recall": recall,
    }


# -----------------------------
# 8️⃣ Training Arguments
# -----------------------------
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",          # <-- changed
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
    seed=42,
)


# -----------------------------
# 9️⃣ Trainer
# -----------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
)


# -----------------------------
# 🔟 Train
# -----------------------------
trainer.train()


# -----------------------------
# 11️⃣ Final Evaluation
# -----------------------------
metrics = trainer.evaluate()
print("\nFinal Evaluation Metrics:")
print(metrics)


# -----------------------------
# 12️⃣ Save Model
# -----------------------------
model.save_pretrained("./model")
tokenizer.save_pretrained("./model")

print("\nTraining complete. Best model saved in ./model")