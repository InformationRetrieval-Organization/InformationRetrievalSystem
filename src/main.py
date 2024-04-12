import asyncio
from flask import Flask
from api.vector_space_api import vector_space_search_blueprint
from api.boolean_api import boolean_search_blueprint
from information_retrieval.vector_space_model import build_vector_space_model
from information_retrieval.boolean_model import build_boolean_model
from preprocessing.preprocessing import preprocess_documents
from db.helper import init_database
import information_retrieval.globals
from flask_cors import CORS
from config import FLASK_ENV

app = Flask(__name__)
app.register_blueprint(vector_space_search_blueprint)
app.register_blueprint(boolean_search_blueprint)

# Enable CORS for the Flask app
CORS(app)

async def main():
    """
    Main function to run the Flask app
    """
    print("Flask app started.")

    await init_database()

    information_retrieval.globals.init()
    await preprocess_documents() 
    await build_boolean_model()
    await build_vector_space_model()

    if FLASK_ENV == 'development':
        app.run()

# Run the main function when the script is imported
asyncio.run(main())