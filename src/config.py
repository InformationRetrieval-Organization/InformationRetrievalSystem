from datetime import datetime, time
import os
import sys

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# API Keys
NYT_API_KEY = os.getenv("NYT_API_KEY")
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# File Paths
CWD = os.getcwd()
GUARDIAN_FILE_PATH = os.path.join(CWD, "files", "The Guardian.csv")
NYT_FILE_PATH = os.path.join(CWD, "files", "New York Times.csv")
GNEWS_FILE_PATH = os.path.join(CWD, "files", "GNews.csv")
GROUND_DATASET_FILE_PATH = os.path.join(CWD, "files", "ground_truth.csv")
INVERTED_INDEX_FILE_PATH = os.path.join(CWD, "files", "inverted_index.csv")
EVAL_MEAS_FILE_PATH = os.path.join(CWD, "files", "evaluation_measures.png")
EVAL_DATE_FILE_PATH = os.path.join(CWD, "files", "evaluation_temporal_relevance.png")

# Crawl Dates
try:
    GROUND_DATASET_START_DATE = datetime.combine(
        datetime.strptime(os.getenv("GROUND_DATASET_START_DATE"), "%Y-%m-%d").date(),
        time.min,
    )
    GROUND_DATASET_END_DATE = datetime.combine(
        datetime.strptime(os.getenv("GROUND_DATASET_END_DATE"), "%Y-%m-%d").date(), time.max
    )
except TypeError:
    print("Please provide valid dates in the .env file.")
    sys.exit(1)

# Flask Environment
FLASK_ENV = os.getenv("FLASK_ENV")