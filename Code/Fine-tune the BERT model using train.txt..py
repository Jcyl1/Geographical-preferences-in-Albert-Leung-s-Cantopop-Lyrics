import json
from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForTokenClassification,
    DataCollatorForTokenClassification, TrainingArguments, Trainer
)

# Function to load data and extract token-label sequences.
# Each line contains a word and its NER tag separated by a tab. Sentences are separated by blank lines.
def load_data(path):
    sents, tags = [], []  # Lists to store sentences and corresponding tag sequences
    chars, labels = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:  # End of a sentence
                if chars:  # Avoid appending empty lists
                    sents.append(chars)
                    tags.append(labels)
                    chars, labels = [], []  # Reset for the next sentence
            else:
                word, tag = line.split("\t")  # Split word and NER tag
                chars.append(word)
                labels.append(tag)
    # Add last sentence if file does not end with '。'
    if chars:
        sents.append(chars)
        tags.append(labels)
    return sents, tags

# Function to encode input examples for the model.
# It uses a tokenizer to convert tokens into IDs and aligns word-level labels with subword tokens.
def encode(example):
    enc = tokenizer(
        example["tokens"],
        is_split_into_words=True,  # Input is already tokenized at the word level
        truncation=True,           # Truncate sequences that are too long
        padding='max_length',      # Pad sequences to a fixed length
        max_length=128             # Maximum sequence length
    )
    word_ids = enc.word_ids()  # Map subword tokens to original word indices
    # Assign labels to subword tokens: only label the first subword, others get -100 (ignored in loss)
    enc["labels"] = [
        -100 if i is None else tag2id[example["tags"][i]]
        for i in word_ids
    ]
    return enc

# Main training script
if __name__ == "__main__":
    # Step 1: Load training data and extract all unique tags
    sentences, tags = load_data("train.txt")
    tag2id = {t: i for i, t in enumerate(sorted(set(tag for seq in tags for tag in seq)))}  # Map tag -> ID
    id2tag = {i: t for t, i in tag2id.items()}  # Map ID -> tag
    json.dump(id2tag, open("id2tag.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)  # Save mapping for inference

    # Step 2: Load pretrained BERT model and tokenizer
    model_ckpt = "bert-base-chinese"  # Pretrained model checkpoint
    tokenizer = AutoTokenizer.from_pretrained(model_ckpt)
    model = AutoModelForTokenClassification.from_pretrained(model_ckpt, num_labels=len(tag2id))

    # Step 3: Convert the data into a Hugging Face dataset and apply the encoding function
    ds = Dataset.from_dict({"tokens": sentences, "tags": tags})  # Construct dataset from token/tag lists
    ds = ds.map(encode)  # Tokenize and align labels
    ds = ds.train_test_split(test_size=0.1)  # Split into training and validation sets (90%/10%)

    # Step 4: Define training configuration
    args = TrainingArguments(
        output_dir="ner_model",  # Directory to save the model
        num_train_epochs=5,  # Number of training epochs
        per_device_train_batch_size=8,  # Batch size during training
        per_device_eval_batch_size=8,  # Batch size during evaluation
        learning_rate=2e-5,  # Learning rate
        weight_decay=0.01,  # Weight decay for regularization
        logging_steps=10,  # Log training loss every 10 steps
        save_steps=500,  # Save model every 500 steps
        report_to=[],  # Disable logging to external tools like WandB or TensorBoard
        logging_dir="logs"  # Directory for logs
    )

    # Step 5: Create a Trainer instance and start training
    trainer = Trainer(
        model=model,
        args=args,
        tokenizer=tokenizer,
        data_collator=DataCollatorForTokenClassification(tokenizer),  # Handles padding and label alignment
        train_dataset=ds["train"],
        eval_dataset=ds["test"]
    )

    # Step 6: Train and save the model and tokenizer
    trainer.train()
    model.save_pretrained("ner_model")  # Save model weights
    tokenizer.save_pretrained("ner_model")  # Save tokenizer config
