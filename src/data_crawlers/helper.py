import pandas as pd
import os

# append the articles to the csv file
def write_to_csv(file_path, articles):
    df = pd.DataFrame(articles)
    if os.path.isfile(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)