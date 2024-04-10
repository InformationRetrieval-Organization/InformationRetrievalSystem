import requests
import json
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import os

base_url = "http://127.0.0.1:5000"
boolean_api_url = f"{base_url}/search/boolean"
vector_space_url = f"{base_url}/search/vector-space"

# TODO: mark the relevant documents for each query manually
# https://github.com/InformationRetrieval-Organization/InformationRetrievalSystem/issues/8
queries = ['korea', 'election', 'korea election', 'president', 'parties', 'president parties']


def evaluate_search_model(relevant_docs, retrieved_docs):
    """
    Calculate recall, precision, and F1 score
    """
    relevant_retrieved_docs = set(relevant_docs).intersection(set(retrieved_docs))

    true_positives = len(relevant_retrieved_docs)
    false_positives = len(retrieved_docs) - true_positives
    false_negatives = len(relevant_docs) - true_positives

    recall = true_positives / (true_positives + false_negatives) if relevant_docs else 0
    precision = (
        true_positives / (true_positives + false_positives) if retrieved_docs else 0
    )
    f1 = (
        2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    )

    return recall, precision, f1


def call_boolean_api(query):
    """
    Call Boolean API
    """
    url = f"{boolean_api_url}"
    body = [{"operator": "AND", "value": word} for word in query.split()]
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(body), headers=headers)
    response.raise_for_status()

    return response.json()


def call_vector_space_api(query):
    """
    Call Vector Space API
    """
    query_string = "+".join(query.split())
    url = f"{vector_space_url}?q={query_string}"
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def calculate_temporal_relevance(retrieved_docs):
    """
    Calculate temporal relevance
    """
    if not retrieved_docs:
        return None

    current_date = datetime.now()

    # get all publication dates
    publication_dates = [
        datetime.strptime(doc["published_on"], "%Y-%m-%d %H:%M:%S%z")
        for doc in retrieved_docs
    ]

    # calculate average publication date
    average_publication_date = sum(
        (
            pub_date - datetime(1970, 1, 1, tzinfo=timezone.utc)
            for pub_date in publication_dates
        ),
        timedelta(0),
    ) / len(publication_dates)

    difference_in_days = (current_date - average_publication_date).day

    return difference_in_days


def get_relevant_docs(query, ground_truth_df):
    """
    Get relevant documents for a given query from the ground truth DataFrame.
    """
    relevant_docs = ground_truth_df[ground_truth_df["query"] == query][
        "document_id"
    ].tolist()
    return relevant_docs


if __name__ == "__main__":
    """
    Evaluate Boolean and Vector Space Models
    """
    print("Evaluating Boolean and Vector Space Models")
    print("===========================================")

    # Load ground truth data
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "src/evaluation", "ground_truth.csv")
    ground_truth_df = pd.read_csv(file_path)

    results = []

    for query in queries:
        print(f"Query: {query}")

        # Get relevant documents from ground truth
        relevant_docs = get_relevant_docs(query, ground_truth_df)

        # Call Boolean and Vector Space APIs
        boolean_api_response = call_boolean_api(query)
        vector_space_api_response = call_vector_space_api(query)

        # Get retrieved documents
        boolean_retrieved_docs = sorted([int(doc["id"]) for doc in boolean_api_response])
        vector_space_retrieved_docs = sorted([int(doc["id"]) for doc in vector_space_api_response])

        # Calculate recall, precision, and F1 score
        boolean_recall, boolean_precision, boolean_f1 = evaluate_search_model(
            relevant_docs, boolean_retrieved_docs
        )
        vector_space_recall, vector_space_precision, vector_space_f1 = (
            evaluate_search_model(relevant_docs, vector_space_retrieved_docs)
        )

        # Calculate temporal relevance
        boolean_temporal_relevance = calculate_temporal_relevance(boolean_api_response)
        vector_space_temporal_relevance = calculate_temporal_relevance(
            vector_space_api_response
        )

        results.append(
            {
                "query": query,
                "boolean_recall": boolean_recall,
                "boolean_precision": boolean_precision,
                "boolean_f1": boolean_f1,
                "boolean_temporal_relevance": boolean_temporal_relevance,
                "vector_space_recall": vector_space_recall,
                "vector_space_precision": vector_space_precision,
                "vector_space_f1": vector_space_f1,
                "vector_space_temporal_relevance": vector_space_temporal_relevance,
            }
        )

    df = pd.DataFrame(results)
    print(df)
    print(df.describe())

    axes = df.set_index("query").plot(kind="bar", subplots=True, layout=(2, 4), legend=False)

    # Loop over the axes and remove the x-label
    for ax in axes.flatten():
        ax.set_xlabel("")

    plt.tight_layout()
    plt.show()
