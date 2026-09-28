from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import torch
import numpy as np

#Load model from checkpoint
model = AutoModelForSequenceClassification.from_pretrained(
    "asadorville/brainpower-deberta-asap1-prompt1"
)

#Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/deberta-v3-base"
)

#Set model to score essay(s)
model.eval()

def score_essay(essay):
    tokenized_essay = tokenize_essay(essay)
    return get_trait_scores(tokenized_essay)

def tokenize_essay(essay):
    tokenized_essay = tokenizer(
        essay,
        return_tensors="pt",
        truncation=True,
        max_length=768,
    )
    return tokenized_essay

def get_trait_scores(tokenized_essay):
    #Get regression scores
    with torch.no_grad():
        outputs = model(**tokenized_essay)

    print("raw scores:", outputs.logits)

    #Clip scores and convert to integers
    scores = np.clip(np.rint(outputs.logits.cpu().numpy()), 1, 6).astype(int)

    #Extract row of traits
    scores = list(scores[0])

    #Assign scores to respective traits
    return {
        "content": int(scores[0]),
        "organization": int(scores[1]),
        "word_choice": int(scores[2]),
        "sentence_fluency": int(scores[3]),
        "conventions": int(scores[4])
    }

