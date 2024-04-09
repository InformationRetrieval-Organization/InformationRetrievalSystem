import asyncio
from flask import Flask
from api.vector_space_api import vector_space_search_blueprint
from api.boolean_api import boolean_search_blueprint
from data_crawlers.nyt_data_crawler import crawl_nyt_data
from information_retrieval.vector_space_model import build_vector_space_model
from information_retrieval.boolean_model import build_boolean_model
from preprocessing.preprocessing import preprocess_documents
from db.helper import init_database
import information_retrieval.globals

app = Flask(__name__)
app.register_blueprint(vector_space_search_blueprint)
app.register_blueprint(boolean_search_blueprint)

async def main():
    # init the database
    await init_database()

    # initiate global variables
    information_retrieval.globals.init()

    # preprocessing, stemming, stop words removal
    vocabulary = await preprocess_documents()
    
    # build Boolean model
    await build_boolean_model()
    
    # build the vector space model
    await build_vector_space_model(vocabulary)

    # run the Flask app
    app.run(debug=True)

if __name__ == "__main__":
    asyncio.run(main())