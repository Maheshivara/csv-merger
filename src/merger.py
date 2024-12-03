import pandas as pd
from datetime import datetime
from pathlib import Path


def merge_csv(file_paths, left_on, right_on, output_path, left_columns, right_columns):
    dataframes = [pd.read_csv(file) for file in file_paths]

    if left_on not in left_columns:
        left_columns.append(left_on)
        remove_left_on = True
    else:
        remove_left_on = False

    if right_on not in right_columns:
        right_columns.append(right_on)
        remove_right_on = True
    else:
        remove_right_on = False

    merged_df = dataframes[0][left_columns]
    for df in dataframes[1:]:
        merged_df = merged_df.merge(
            df[right_columns], how="left", left_on=left_on, right_on=right_on
        )

    if remove_left_on:
        merged_df.drop(columns=[left_on], inplace=True)
    if remove_right_on:
        merged_df.drop(columns=[right_on], inplace=True)

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = Path(output_path, f"merged_{now}.csv")
    merged_df.to_csv(output_file, index=False)
