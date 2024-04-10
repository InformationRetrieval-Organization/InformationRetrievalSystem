import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from db.processed_posts import create_one_processed_post, create_many_processed_posts
from db.posts import get_all_posts
import information_retrieval.globals 
from nltk import FreqDist

async def preprocess_documents() -> list[str]:
    """
    Preprocesses the documents in the database and returns a list of tokens.
    """
    list_of_tokens = []
    processed_posts = []
    total_string = ""
    
    # Get the posts from the database
    posts = await get_all_posts()
    posts = [(post.id, post.content) for post in posts]
    
    # Download the necessary resources
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('words')
    
    for post in posts:
        total_string += post[1].lower()
        
        # Remove special characters and convert to lowercase
        content = re.sub('[!\"#$%&\'()*+,-./:;<=>—?@[\]^_`{|}~0-9\n’“”]', '', post[1].lower())
        
        # Remove posts with non ascii characters
        if not is_english(post[1]):
            continue
        
        # Remove numerical values
        content = re.sub(r'\d+', '', content)
    
        # Remove non-english words
        english_words = set(nltk.corpus.words.words())
        english_words.add('korea')
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
        
        list_of_tokens.extend(tokens)
    
    # Create DB entries
    await create_many_processed_posts(processed_posts)

    list_of_tokens = list(set(list_of_tokens))
    information_retrieval.globals._vocabulary = list_of_tokens
    
    print("Length of Vocabulary: " + str(len(list_of_tokens)))
    
    return list_of_tokens

def is_english(s):
    return s.ascii()

