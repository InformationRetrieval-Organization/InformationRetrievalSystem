import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from src.db.processed_posts import create_one_processed_post, create_many_processed_posts
from src.db.posts import get_all_posts
import src.information_retrieval.globals 
from nltk import FreqDist

async def preprocess_documents() -> list[str]:
    """
    Preprocesses the documents in the database and returns a list of tokens.
    """
    list_of_tokens = []
    processed_posts = []
    term_freq_map = {}
        
    # Get the posts from the database
    posts = await get_all_posts()
    posts = [(post.id, post.content) for post in posts]
    
    # Download the necessary resources
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('words')
    english_words = set(nltk.corpus.words.words())
    english_words.add('korea')

    for post in posts:        
        # Remove special characters and convert to lowercase
        content = re.sub('[–!\"#$%&\'()*+,-./:;<=‘>—?@[\]^_`�{|}~0-9\n’“”]', '', post[1].lower())
        
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
        
        for token in tokens:
            if token in term_freq_map:
                term_freq_map[token] += 1
            else:
                term_freq_map[token] = 1
        
        list_of_tokens.extend(tokens)
    
    # Find tokens that occur only once
    unique_tokens = [key for key, value in term_freq_map.items() if value == 1]
        
    list_of_tokens = [token for token in list_of_tokens if token not in unique_tokens]
    
    # Create DB entries
    await create_many_processed_posts(processed_posts)

    list_of_tokens = list(set(list_of_tokens))
    src.information_retrieval.globals._vocabulary = list_of_tokens
    
    print("Length of Vocabulary: " + str(len(list_of_tokens)))
    
    return list_of_tokens

def is_english(content, threshold, english_words):
    english_words_count = sum(1 for word in content.split() if word in english_words)
    total_words_count = len(content.split())
    
    if total_words_count == 0 or english_words_count == 0: # Avoid division by zero
        return False
    
    return english_words_count / total_words_count >= threshold
    

