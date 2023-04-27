import pandas as pd
import streamlit as st


def replace_none(df):
    df = df.fillna(value='')
    return df


def decode_belfius_credit(data):
    n_lines = 5
    counter = 1
    list = []
    list_of_lists = []

    for x in data:
        if counter == n_lines:
            list.append(x)
            list_of_lists.append(list)
            counter = 1
            list = []
        else:
            if 'via' in x:
                list[-1] = list[-1] + '' + x
            else:
                list.append(x)
                counter += 1

    df = pd.DataFrame(list_of_lists, columns=['1', '2', '3', '4', '5'])
    return df