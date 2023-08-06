def convert_df_to_df_list(df, columns):
    """
    First step to set up a Pandas DataFrame into a MongoDB document.
    :param df: Pandas DataFrame.
    :param columns: columns after which we will group by DataFrame. Use list to pass multiple columns.
    :return: a list of grouped DataFrames.
    """
    df_list = [group[1].reset_index(drop=True) for group in df.groupby([columns])]
    return df_list
