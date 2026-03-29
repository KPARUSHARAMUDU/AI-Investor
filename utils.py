import pandas as pd

def get_column(data, col_name):
    """
    Safely extract a column from DataFrame (handles MultiIndex + single column cases)
    """

    if isinstance(data.columns, pd.MultiIndex):
        # MultiIndex → find correct column
        for col in data.columns:
            if col[0] == col_name:
                return data[col]

    # Normal case
    if col_name in data.columns:
        col = data[col_name]

        # If still DataFrame → take first column
        if isinstance(col, pd.DataFrame):
            return col.iloc[:, 0]

        return col

    raise KeyError(f"{col_name} not found in data")