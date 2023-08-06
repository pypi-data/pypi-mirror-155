import pandas as pd
from pymongo.collection import Collection
import json


def df_2_db(df:pd.DataFrame, collection:Collection) -> None:
    """Inserts dataframe into mongo Collection.

    Args:
        df (pd.DataFrame): Data to insert into collection.
        collection (Collection): Collection to insert data into.
    """
    data_dict = df.to_dict('records')
    collection.insert_many(data_dict)
    
def df_2_json(df:pd.DataFrame) -> str:
    """Converts from dataframe to JSON string.

    Args:
        df (pd.DataFrame): Data.

    Returns:
        str: JSON string data.
    """
    return json.dumps(df.to_numpy().tolist())
    
def db_2_df(collection:Collection) -> pd.DataFrame:
    """Extracts all data from collection and returns as pandas DataFrame.

    Args:
        collection (Collection): Collection to grab all data from.

    Returns:
        pd.DataFrame: Data in collection.
    """
    cursor = collection.find({}, {'_id': 0})
    return pd.DataFrame(list(cursor))
