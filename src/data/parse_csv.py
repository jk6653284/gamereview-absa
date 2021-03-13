"""
Parse csv files downloaded using selenium to a single data source for use
For now, create a single df, since this is how I will work
IF too big, dump it as a numpy array (although I assume memory usage will still be high since it's not a number...)
"""

# imports
import os,sys
import csv
import pandas as pd
from pandas.errors import ParserError
import pickle
import glob

# get logger and utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from logger import logger_data


def read_clean_df(df_path):
    df = pd.read_csv(df_path
                     ,usecols=['Game','Publication', 'Is Top Critic?','Normalized Score','Rating','Recommendation','Language','Quote']
                     ,engine='python'
                     ,error_bad_lines=False
                     )
    logger_data.debug(f"Read file {df_path}.")
    df = df[df.Language == 'English']
    return df.reset_index(drop=True)


def concat_to_single_csv(all_dls):
    # initiate empty dfs
    final_df = pd.DataFrame()
    failed_files = []
    for i, df_path in enumerate(all_dls):
        try:
            final_df = pd.concat([final_df, read_clean_df(df_path)])
        except BaseException:
            logger_data.error(f"Cannot read: {df_path}.",
                              exc_info=True)
            failed_files.append(df_path.split("/")[-1])
            continue

    logger_data.info(f"Final dataframe shape: {final_df.shape}")
    logger_data.info(f"Total {len(failed_files)} out of {len(all_dls)} files failed to load.")
    logger_data.info(f"Total {final_df.Game.nunique()} out of {len(all_dls)} unique games in final df.")
    pickle.dump(failed_files,
                open(os.path.join(os.path.dirname(__file__),"failed_files.txt"),'wb')
                )
    return final_df


def main():
    dl_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "csvs"))
    all_dls = glob.glob(f"{dl_dir}/*.csv")
    logger_data.info(f"Concatenating {len(all_dls)} csv files from {dl_dir}.")
    final_dfs = concat_to_single_csv(all_dls)
    save_name = os.path.join(os.path.dirname(__file__),"all_data_raw.csv")
    final_dfs.to_csv(save_name,index=False)
    logger_data.info(f"Final dataframe saved at {save_name}.")


if __name__ == '__main__':
    main()