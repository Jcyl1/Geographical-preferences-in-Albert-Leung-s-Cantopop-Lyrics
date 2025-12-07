import json
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification


# Function to predict NER tags for a list of characters using the model and tokenizer
# It tokenizes the input chars, runs inference, then maps predicted IDs to tag strings
def predict_ner(chars, model, tokenizer, id2tag):
    inputs = tokenizer(chars, is_split_into_words=True, return_tensors="pt",
                       truncation=True, padding=True, max_length=512)

    with torch.no_grad():
        logits = model(**inputs).logits

    pred_ids = torch.argmax(logits, dim=-1).squeeze().tolist()
    word_ids = inputs.word_ids()

    tags, seen = [], set()
    for i, word_idx in enumerate(word_ids):
        if word_idx is not None and word_idx not in seen:
            seen.add(word_idx)
            tags.append(id2tag[str(pred_ids[i])])

    return tags

# Main prediction script
if __name__ == "__main__":
    # Step 1: Load tokenizer and model from the specified directory "ner_model"
    tokenizer = AutoTokenizer.from_pretrained("ner_model")
    model = AutoModelForTokenClassification.from_pretrained("ner_model").eval()

    # Step 2: Load the id-to-tag dictionary mapping from JSON file
    with open("id2tag.json", encoding="utf-8") as f:
        id2tag = json.load(f)

    # Step 3: Read input text from "test.txt" line by line
    with open("test.txt", encoding="utf-8") as f:
        lines = f.readlines()  # <--- 修改：使用 readlines() 读取所有行

    # Step 4: store corresponding predicted tags
    all_chars = []  # To store all characters of the text
    all_tags = []   # To store corresponding predicted tags

    # Step 5: For each LINE, predict NER tags and collect results
    for line in lines:
       chars = []
       for ch in line:
           if ch != ' ' and ch != '\t' and ch != '\n' and ch != '\r':
                chars.append(ch)

       if not chars:
           continue

       tags = predict_ner(chars, model, tokenizer, id2tag)
       for ch in chars:
           all_chars.append(ch)
       for tag in tags:
           all_tags.append(tag)


    # Step 6: Output each character and its predicted tag separated by a tab
    with open("result.txt", "w", encoding="utf-8") as f:
       for ch, tag in zip(all_chars, all_tags):
            line = f"{ch}\t{tag}"
            print(line)
            f.write(line + "\n")
