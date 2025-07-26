import pandas as pd

data_df = pd.read_csv("data_prepared.csv")

def valid_user(curp):
    user_row = data_df[data_df["curp"] == curp]
    if not user_row.empty:
        name = user_row["valid_name"].values[0]
        level = user_row["level"].values[0]
        score = user_row["score"].values[0]
        return [True, name, level, score]
    else:
        return [False, '', '', '']
