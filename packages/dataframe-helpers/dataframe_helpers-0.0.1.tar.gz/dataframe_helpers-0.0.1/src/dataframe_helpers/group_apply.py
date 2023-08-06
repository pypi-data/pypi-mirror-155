import pandas as pd


def group_apply(df, group_col, output_col,  func):
    df2 = df.groupby(group_col).apply(func )
    dummyVariableName = 'internal_dummy_name'
    df3 = df2.reset_index(name=dummyVariableName)
    df3[output_col ] = pd.DataFrame(df3[dummyVariableName].to_list(), columns=output_col )
    df3.drop(dummyVariableName, axis=1, inplace=True)
    return df3
