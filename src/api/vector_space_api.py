from flask import Blueprint, request
from src.information_retrieval.vector_space_model import search_vector_space
import nltk
from src.api.schemas import ObjectSchema
from src.db.posts import get_all_posts

vector_space_search_blueprint = Blueprint('vector_space_search', __name__)

@vector_space_search_blueprint.route('/search/vector-space', methods=['GET'])
async def search_vector_space_model():
    """
    Search the Vector Space Model for the given query.
    url: http://127.0.0.1:5000/search/vector-space?q=your_search_term
    """
    query = request.args.get('q')
    
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatized_query = list()
    
    for word in query.split():
        word = lemmatizer.lemmatize(word.lower())
        lemmatized_query.append(word)
                
    id_list = await search_vector_space(lemmatized_query)
        
    posts = await get_all_posts()
    filtered_posts = [post for post in posts if post.id in id_list]
    filtered_posts = sorted(filtered_posts, key=lambda x: id_list.index(x.id))
        
    object_schema = ObjectSchema()
    json_string = object_schema.dumps(filtered_posts, many=True)
    
    return json_string
