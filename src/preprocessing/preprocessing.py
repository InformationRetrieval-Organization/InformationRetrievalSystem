import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from db.processed_posts import create_processed_post
from db.posts import get_all_posts
import information_retrieval.globals 

async def preprocess_documents() -> list[str]:
    """
    Preprocesses the documents in the database and returns a list of tokens.
    """
    list_of_tokens = []
    
    # Get the posts from the database
    posts = await get_all_posts()
    posts = [(post.id, post.content) for post in posts]
    
    # Download the necessary resources
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('stopwords')

    for post in posts:
        # Remove special characters and convert to lowercase
        content = re.sub('[!\"#$%&\'()*+,-./:;<=>—?@[\]^_`{|}~0-9\n’“”]', '', post[1].lower())
        if not isEnglish(content):
            continue
        
        # Tokenize the document
        tokens = word_tokenize(content)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]

        # Lemmatize the tokens
        lemmatizer = nltk.stem.WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        #create DB entry
        await create_processed_post(
                id=post[0],
                content=' '.join(tokens)
            )
        list_of_tokens.extend(tokens)
    
    list_of_tokens = list(set(list_of_tokens))
    information_retrieval.globals._vocabulary = list_of_tokens
    
    return list_of_tokens

def isEnglish(s):
  return s.isascii()
