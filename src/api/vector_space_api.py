from flask import Blueprint, request
from information_retrieval.vector_space_model import search_vector_space

vector_space_search_blueprint = Blueprint('vector_space_search', __name__)

# Vector Space Model endpoint
# http://127.0.0.1:5000/search/vector-space?q=your_search_term
# TODO: Implement proper api endpoint, see GitHub issue for more details:
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/6
@vector_space_search_blueprint.route('/search/vector-space', methods=['GET'])
def search_vector_space_model():
    query = request.args.get('q')

    search_results = search_vector_space(query)
    
    return {'results': search_results}