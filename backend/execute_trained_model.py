from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Define the Google Drive directory where the final model is saved
model_dir = '../model/bert_final_model/'

# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertForSequenceClassification.from_pretrained(model_dir)

# Set model to evaluation mode
model.eval()

def get_finetuned_bert_sentiment(test_string):
    # Define a test string (e.g., a tweet)
    #test_string = "I love this product, it's amazing!"

    # Tokenize the input string
    inputs = tokenizer(test_string, return_tensors="pt", padding=True, truncation=True, max_length=128)

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Get predicted class (sentiment)
    predictions = torch.argmax(outputs.logits, dim=-1)

    # Map prediction to sentiment (assuming 0=Negative, 1=Neutral, 2=Positive)
    label_map = {0: "Negative", 1: "Positive"}

    # Output the sentiment
    predicted_sentiment = label_map[predictions.item()]
    print(f"Sentiment: {predicted_sentiment}")
    return predicted_sentiment
