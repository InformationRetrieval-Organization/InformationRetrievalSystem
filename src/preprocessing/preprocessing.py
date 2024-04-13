import re
from typing import Dict, List, Set
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from db.processed_posts import create_one_processed_post, create_many_processed_posts
from db.posts import get_all_posts
import information_retrieval.globals 
from nltk import FreqDist
from datetime import datetime


async def preprocess_documents() -> list[str]:
    """
    Preprocesses the documents in the database and returns a list of tokens.
    """
    # Initialize the variables
    list_of_tokens = []
    processed_posts = []
    term_freq_map = {}
    MAX_COEFFICIENT = 2
        
    # Get the posts from the database
    posts = await get_all_posts()
    posts = [(post.id, post.content, post.title, post.published_on) for post in posts]
    
    # Download the necessary resources
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('words')
    english_words = set(nltk.corpus.words.words())
    english_words.add('korea')

    for post in posts:        
        # Remove special characters and convert to lowercase
        content = post[1].lower() + " " + post[2].lower() # Add the title
        content = re.sub('[–!\"#$%&\'()*+,-./:;<=‘>—?@[\]^_`�{|}~0-9\n’“”]', '', content)
        
        # Remove numerical values
        content = re.sub(r'\d+', '', content)
                        
        # Remove posts with a low english word ratio
        threshold = 0.7
        if not is_english(content, threshold, english_words):
            continue
    
        # Remove non-english words
        content = " ".join(w for w in nltk.wordpunct_tokenize(content) if w.lower() in english_words or not w.isalpha())
        
        # Tokenize the document
        tokens = word_tokenize(content)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]        
        
        # Lemmatize the tokens
        lemmatizer = nltk.stem.WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        # Add to processed_posts list
        processed_posts.append({
            "id": post[0],
            "content": ' '.join(tokens)
        })
        
        # Calculate the date coefficient
        information_retrieval.globals._date_coefficient[post[0]] = calculate_date_coefficient(post[3], MAX_COEFFICIENT)
        
        set_term_freq_map(term_freq_map, tokens)
        
        list_of_tokens.extend(tokens)
    
    # Find tokens that occur only once
    unique_tokens = [key for key, value in term_freq_map.items() if value == 1]
    list_of_tokens = [token for token in list_of_tokens if token not in unique_tokens]
    
    # Calculate SVD and remove the least important tokens
                
    # Create DB entries
    await create_many_processed_posts(processed_posts)

    list_of_tokens = list(set(list_of_tokens))
    information_retrieval.globals._vocabulary = list_of_tokens
    
    print("Length of Vocabulary: " + str(len(list_of_tokens)))
    
    return list_of_tokens

def set_term_freq_map(term_freq_map: Dict[str, int], tokens: List[str]) -> None:
    """
    Set the term frequency map for a document.
    """
    for token in tokens:
        if token in term_freq_map:
            term_freq_map[token] += 1
        else:
            term_freq_map[token] = 1

def is_english(content: str, threshold: float, english_words: Set[str]) -> bool:
    """
    Determine if a document is in English based on the ratio of English words.
    """
    english_words_count = sum(1 for word in content.split() if word in english_words)
    total_words_count = len(content.split())
    
    if total_words_count == 0 or english_words_count == 0: # Avoid division by zero
        return False
    
    return english_words_count / total_words_count >= threshold

def calculate_date_coefficient(post_date: datetime, max_coefficient: int) -> int:
    """
    Calculate the date coefficient for a document.
    """
    oldest_date = datetime(2024, 3, 12)
    newest_date = datetime(2024, 4, 12)
    days_between = (newest_date - oldest_date).days
    coefficient_per_day = (max_coefficient - 1) / days_between
    
    post_date = post_date.replace(tzinfo=None) # Remove timezone info, otherwise the subtraction will fail
    
    days_since_oldest = (post_date - oldest_date).days
    return coefficient_per_day * days_since_oldest + 1

    