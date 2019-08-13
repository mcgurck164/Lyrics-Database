# -*- coding: utf-8 -*-

import pandas as pd
import os
from Database import Database
#from Song import Song

DB_NAME = "songs.db"

def setup_db():
    db = Database(DB_NAME, fill_with_examples=False, reset_existing=True)
    df = pd.read_csv(os.getcwd() + "//songs.csv")
    db.add_from_dataframe(df, col_artist="Artist", col_record="Album",
                          col_year="Year", col_song_title="Title",
                          col_lyrics="Lyrics", col_link_to_lyrics="Link")

def check_db():
    db = Database(DB_NAME)
    return db.query_db()
if __name__ == "__main__":
    setup_db()
    qry = check_db()
    print(qry[5])