from fastapi import FastAPI, HTTPException
import spacy
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import torch
from transformers import BertTokenizer, BertForMaskedLM
import torch.nn.functional as F
genai.configure(api_key='AIzaSyBr3fwNEd1FDRqVHOWnch317SCyb7vLTdk')
model = genai.GenerativeModel('gemini-1.5-flash')
# Initialize FastAPI
app = FastAPI()

# Set your OpenAI API key
  # Replace with your actual OpenAI API key

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your React frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load spaCy's English model for NLP tasks
nlp = spacy.load("en_core_web_sm")



# def process_sentence(sentence: str) -> str:
#     response = model.generate_content("Remove all adjectives, adverbs and irrelevant information from: " + sentence)

#     return response.text

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model1 = BertForMaskedLM.from_pretrained("bert-base-uncased")

def get_word_importance(sentence, word_index):
    """
    Masks a specific word in the sentence and checks how well BERT can predict the original word.
    Returns the probability score for the original word.
    """
    # Tokenize the input sentence
    tokens = tokenizer.tokenize(sentence)
    input_ids = tokenizer.encode(sentence, return_tensors="pt")
    
    # Create a copy of the input_ids with the target word masked
    masked_input_ids = input_ids.clone()
    masked_input_ids[0, word_index] = tokenizer.mask_token_id  # Mask the target word
    
    # Get the model's predictions for the masked word
    with torch.no_grad():
        outputs = model1(masked_input_ids)
        predictions = outputs.logits
    
    # Get the probability for the original word at the masked position
    original_word_id = input_ids[0, word_index].item()
    original_word_prob = torch.softmax(predictions[0, word_index], dim=0)[original_word_id].item()

    return original_word_prob

def process_sentence(paragraph, relevance_threshold=0.2):
    """
    Filters irrelevant words using a masked language model (MLM).
    Words that are too easy to predict when masked are considered irrelevant.
    """
    # Tokenize the input paragraph
    tokens = tokenizer.tokenize(paragraph)
    input_ids = tokenizer.encode(paragraph, return_tensors="pt")[0]

    # Initialize list to hold relevant words
    relevant_words = []
    
    # Iterate over each word in the tokenized input
    for idx, token in enumerate(tokens):
        # Skip special tokens like [CLS], [SEP]
        if token in ["[CLS]", "[SEP]"]:
            continue

        # Calculate the word importance using MLM masking
        word_importance = get_word_importance(paragraph, idx + 1)  # Offset by 1 for [CLS] token

        # If the word importance is below the threshold, consider it irrelevant
        if word_importance < relevance_threshold:
            continue

        # Otherwise, add the word to the relevant words list
        relevant_words.append(token)

    # Join the relevant words back into a sentence
    filtered_sentence = tokenizer.convert_tokens_to_string(relevant_words)

    return filtered_sentence



# First API Call: Process sentence using spaCy
@app.get("/chatquery")
async def chatquery(sentence: str):
    try:
        filtered_sentence = process_sentence(sentence)
        return {"filteredSentence": filtered_sentence}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Second API Call: Query chat_query first, then pass its response to OpenAI
@app.get("/query_chat_response")
async def query_chat_response(sentence: str):
    try:
        # Process the sentence using spaCy to get the filtered sentence
        filtered_sentence = process_sentence(sentence)

        response = model.generate_content("Give me a short summary of: " + filtered_sentence)

        # Return the OpenAI response
        return {
            "input_str": sentence,
            "openai_response": response.text
        }

    except Exception as e:
        print(f"Error in OpenAI API: {str(e)}")  # Generic error handling for all exceptions
        raise HTTPException(status_code=500, detail=str(e))

# Third API Call: Query OpenAI directly with an input string
@app.get("/query_openai_direct")
async def query_openai_direct(input_str: str):
    try:
        # Query OpenAI directly with an input string using ChatCompletion API
        response = model.generate_content("Give me a 2 short summary of: " + input_str)

        

        # Return the OpenAI response
        return {
            "input_str": input_str,
            "openai_response": response.text
        }

    except Exception as e:
        print(f"Error in OpenAI API: {str(e)}")  # Generic error handling for all exceptions
        raise HTTPException(status_code=500, detail=str(e))
    
