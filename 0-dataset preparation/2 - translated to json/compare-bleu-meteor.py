import pandas as pd
import json
import nltk
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer

# Ensure the required NLTK data is available
nltk.download('punkt')
nltk.download('wordnet')

# Initialize the stemmer
stemmer = PorterStemmer()

def get_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word, lang='eng'):
        for lemma in syn.lemmas(lang='eng'):
            synonyms.add(lemma.name())
    return synonyms

def preprocess_tokens(tokens):
    preprocessed_tokens = set()
    for token in tokens:
        stemmed_token = stemmer.stem(token)
        synonyms = get_synonyms(stemmed_token)
        preprocessed_tokens.update(synonyms)
        preprocessed_tokens.add(stemmed_token)
    return preprocessed_tokens

def calculate_meteor(reference, candidate):
    ref_tokens = word_tokenize(reference.lower())
    cand_tokens = word_tokenize(candidate.lower())
    return meteor_score([ref_tokens], cand_tokens)

def calculate_meteor_wordnet(reference, candidate):
    ref_tokens = word_tokenize(reference.lower())
    cand_tokens = word_tokenize(candidate.lower())
    
    ref_preprocessed = preprocess_tokens(ref_tokens)
    cand_preprocessed = preprocess_tokens(cand_tokens)
    
    return meteor_score([list(ref_preprocessed)], list(cand_preprocessed))

def calculate_bleu(reference, candidate):
    ref_tokens = word_tokenize(reference.lower())
    cand_tokens = word_tokenize(candidate.lower())
    smoothing_function = SmoothingFunction().method1
    return sentence_bleu([ref_tokens], cand_tokens, smoothing_function=smoothing_function)

def compare_scores(df):
    comparison_data = []
    for index, row in df.iterrows():
        try:
            original_positive = str(row['original_positive'])
            back_translate_positive = str(row['back_translate_positive'])
            original_negative = str(row['original_negative'])
            back_translate_negative = str(row['back_translate_negative'])
            
            meteor_score_positive = calculate_meteor(original_positive, back_translate_positive)
            bleu_score_positive = calculate_bleu(original_positive, back_translate_positive)
            meteor_wordnet_score_positive = calculate_meteor_wordnet(original_positive, back_translate_positive)
            
            meteor_score_negative = calculate_meteor(original_negative, back_translate_negative)
            bleu_score_negative = calculate_bleu(original_negative, back_translate_negative)
            meteor_wordnet_score_negative = calculate_meteor_wordnet(original_negative, back_translate_negative)
            
            comparison_data.append({
                'original_positive': original_positive,
                'back_translate_positive': back_translate_positive,
                'meteor_score_positive': meteor_score_positive,
                'bleu_score_positive': bleu_score_positive,
                'meteor_wordnet_score_positive': meteor_wordnet_score_positive,
                'original_negative': original_negative,
                'back_translate_negative': back_translate_negative,
                'meteor_score_negative': meteor_score_negative,
                'bleu_score_negative': bleu_score_negative,
                'meteor_wordnet_score_negative': meteor_wordnet_score_negative,
            })
        except Exception as e:
            print(f"Error processing row {index}: {e}")
    
    return pd.DataFrame(comparison_data)

# Read the datasets (amazon-0.csv and amazon-1.csv)
df1 = pd.read_csv('./dataset/amazon-1.csv')
df2 = pd.read_csv('./dataset/amazon-0.csv')

# Concatenate the datasets
df = pd.concat([df1, df2], ignore_index=True)

# Compare METEOR and BLEU scores
comparison_df = compare_scores(df)

# Calculate total average scores combining positive and negative
total_average_scores = {
    'average_meteor': round((comparison_df['meteor_score_positive'].mean() + comparison_df['meteor_score_negative'].mean()) / 2, 4),
    'average_bleu': round((comparison_df['bleu_score_positive'].mean() + comparison_df['bleu_score_negative'].mean()) / 2, 4),
    'average_meteor_wordnet': round((comparison_df['meteor_wordnet_score_positive'].mean() + comparison_df['meteor_wordnet_score_negative'].mean()) / 2, 4)
}

# Print the comparison data
print(comparison_df)

# Print total average scores
print("Total Average Scores:")
for score_type, score in total_average_scores.items():
    print(f"{score_type}: {score}")

# Save comparison data to a JSON file
comparison_df.to_json('./json/comparison_data.json', orient='records', indent=4)

# Save total average scores to a JSON file
with open('./json/total_average_scores.json', 'w') as json_file:
    json.dump(total_average_scores, json_file, indent=4)

print("Comparison data and total average scores successfully written to comparison_data.json and total_average_scores.json")
