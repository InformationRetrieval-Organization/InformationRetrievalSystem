from flask import Flask
from api.search_api import search_blueprint
from data_crawlers.nyt_data_crawler import crawl_nyt_data
from information_retrieval.vector_space_model import build_vector_space_model

app = Flask(__name__)
app.register_blueprint(search_blueprint)

if __name__ == "__main__":
    # Crawl data from New York Times and store in database
    crawl_nyt_data()

    # Build the vector space model
    build_vector_space_model()

    # Run the Flask app
    app.run(debug=True)