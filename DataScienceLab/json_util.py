import pandas as pd
import json

def flatten_json(json_obj):
    '''
    Flatten an abritary json structure to a 2D dataframe.
    Subdicts will be expanded to columns and lists will be expanded as rows.
    INPUT:
    - json_obj: List of dicts with json data
    OUTPUT:
    - df: Dataframe with normalized and exploded data
    '''
    def list_cols(df):
        '''
        Return a list of the list-type columns in the provided dataframe
        '''
        record_list = []
        for col in df.columns:
            if df[col].dropna().shape[0] > 0:
                if type(df[col].dropna().iloc[0]) is list:
                    record_list.append(col)
        return record_list
    def dict_cols(df):
        '''
        Return a list of the dict-type columns in the provided dataframe
        '''
        record_list = []
        for col in df.columns:
            if df[col].dropna().shape[0] > 0:
                if type(df[col].dropna().iloc[0]) is dict:
                    record_list.append(col)
        return record_list

    def explode_json(df):
        '''
        Expand dataframe with dicts as columns and lists as rows until no more dicts/lists are present in dataset.
        '''
        cols = list(df.columns)
        # initialize new_cols with something that won't match column names
        new_cols = ['totallynotacolumn']
        while cols!=new_cols:  # keep going untill column names stop changing
            cols = list(df.columns)
            lists = list_cols(df)
            for rec in lists:
                df = df.explode(rec)
            dicts = dict_cols(df)
            for col in dicts:
                df = pd.concat([df.drop([col], axis=1), df[col].apply(pd.Series).add_prefix(col+'.')], axis=1)
            new_cols = list(df.columns)

        return df

    df = pd.json_normalize(json_obj)
    df = explode_json(df)

    return df