"""
Create DataFrame string representations that can be used to create new DataFrames.
"""


import pandas as pd


ALIAS = "pd"


def pdrepr(df: pd.DataFrame) -> str:
    """Create DataFrame string representation that can be used to create a new DataFrame.

    Args:
        df: DataFrame to serialize

    Returns:
        String containing valid Python code that can be pasted into a script file or interpreter,
        or passed to eval(), thereby creating a DataFrame similar to the original.

    Example:
        string_repr = pdrepr(my_df)
        new_df = eval(string_repr)
    """

    index_columns = df.index.names
    df = df.reset_index()
    df = df.drop("index", axis=1, errors="ignore")
    d = df.to_dict(orient="list")
    string = f"{ALIAS}.DataFrame({repr(d)})"
    if sum([idx is not None for idx in index_columns]):
        string += f".set_index({index_columns})"
    return string
