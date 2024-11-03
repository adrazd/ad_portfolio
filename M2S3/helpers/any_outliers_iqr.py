import pandas as pd


def any_outliers_iqr(df: pd.DataFrame, col_name: str, print_flag: bool = True) -> pd.DataFrame:
    """
    This function uses IQR method for identification of outliers in a column of DataFrame.

    Parameters:
    df          pd.DataFrame    The DataFrame where we are looking for outliers
    col_name    str             column of the DataFrame in which we are looking for outliers
    print_flag  bool            flag, indicating whether to print outlier information

    Returns:
    df_outliers pd.DataFrame    Prints text message for user if there are any top or bottom
                                outliers in the specified column. Returns a DataFrame with
                                all outliers from initial DataFrame.
    """
    df_outliers = pd.DataFrame()

    min_value = df[col_name].min()
    max_value = df[col_name].max()

    q1 = df[col_name].quantile(0.25)
    q3 = df[col_name].quantile(0.75)

    iqr = q3 - q1

    bottom_limit = round(q1 - 1.5 * iqr, 6)
    top_limit = round(q3 + 1.5 * iqr, 6)

    if bottom_limit <= min_value and top_limit >= max_value:
        print(f"There are no outliers in '{col_name}'.") if print_flag else None

    if bottom_limit > min_value:
        lower_rows = df[df[col_name] < bottom_limit]
        lower_count = lower_rows.shape[0]
        (
            print(
                f"There are {int(lower_count)} bottom outliers in '{col_name}' below {bottom_limit}"
            )
            if print_flag
            else None
        )
        df_outliers = pd.concat([df_outliers, lower_rows])

    if top_limit < max_value:
        upper_rows = df[df[col_name] > top_limit]
        upper_count = upper_rows.shape[0]
        (
            print(
                f"There are {int(upper_count)} top outliers in '{col_name}' above {top_limit}"
            )
            if print_flag
            else None
        )

        df_outliers = pd.concat([df_outliers, upper_rows])

    df_output = df_outliers.sort_values(by=col_name, ascending=False)

    return df_output

