from flask import Blueprint, request
from information_retrieval.boolean_model import boolean_search

boolean_search_blueprint = Blueprint('boolean_search', __name__)

# Boolean Model endpoint
# http://127.0.0.1:5000/search/boolean?q=your_search_term
# TODO: Implement proper api endpoint, see GitHub issue for more details:
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/5
@boolean_search_blueprint.route('/search/boolean', methods=['GET'])
def search_boolean():
    query = request.args.get('q')
    
    search_results = boolean_search(query)
    
    return {'results': search_results}