import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://storage.googleapis.com/uber-data-engineering-project-surya1/uber_data.csv'
    # Pandas can read cloud storage URLs directly and efficiently
    return pd.read_csv(url, sep=',')