# -*- coding: utf-8 -*-

import sqlite3
import os

class Database():
    def __init__(self, name):
        self.name = name
        exists = os.path.isfile(self.name)
        self.connect_db()
        if not exists:
            self.setup_db()
            self.fill_with_examples()
            
    def connect_db(self):
        self.con = sqlite3.connect(self.name)
        self.cur = self.con.cursor()
    
    def setup_db(self):
        # create table Songs
        sql = "CREATE TABLE IF NOT EXISTS Songs ("\
                "id             INTEGER PRIMARY KEY,"\
                "artist         TEXT,"\
                "record         TEXT,"\
                "year           INTEGER,"\
                "song_title     TEXT,"\
                "lyrics         TEXT,"\
                "link_to_lyrics TEXT)"
        self.cur.execute(sql)
        
    def add_song(self, Song=None, artist="", record="", year=0, 
                 song_title="", lyrics="", link_to_lyrics=""):
        if Song is None:
            Song = Song(artist, record, year, 
                        song_title, lyrics, link_to_lyrics)
        if self.exists(Song):
            return False
        sql = "INSERT INTO Songs (artist,"\
                                  "record,"\
                                  "year,"\
                                  "song_title,"\
                                  "lyrics,"\
                                  "link_to_lyrics) "\
              "VALUES (?, ?, ?, ?, ?, ?)"
        vals = (Song.artist, Song.record, Song.year, Song.song_title,
                Song.lyrics, Song.link_to_lyrics)
        self.cur.execute(sql, vals)
        self.con.commit()
        return True
        
    def exists(self, Song):
        sql = "SELECT id FROM Songs WHERE artist=? "\
                                   "AND record=? "\
                                   "AND song_title=?"
        vals = (Song.artist, Song.record, Song.song_title)
        self.cur.execute(sql, vals)
        qry = self.cur.fetchall()
        return (len(qry)>0)
    
    def query_db(self, sql_qry="SELECT * FROM Songs"):
        self.cur.execute(sql_qry)
        return self.cur.fetchall()
    
    def delete_songs_table(self):
        sql = "DROP TABLE Songs"
        self.cur.execute(sql)
    
    def __del__(self):
        self.con.close()
        
    def fill_with_examples(self):
        self.add_song(artist="Bruce Springsteen", 
                      record="The River", 
                      year=1975, 
                      song_title="The River",
                      lyrics="I come from down the valley ...",
                      link_to_lyrics="www.somewhere.com")
        self.add_song(artist="The Gaslight Anthem", 
                      record="The 59 Sound", 
                      year=2008, 
                      song_title="Great Expectations",
                      lyrics="Mary, this station is playing every sad song ...",
                      link_to_lyrics="www.somewhere.com")
        self.add_song(artist="Muff Potter", 
                      record="Von Wegen", 
                      year=2005, 
                      song_title="22 Gleise später",
                      lyrics="Seit unser Karren im Dreck sitzt ...",
                      link_to_lyrics="www.somewhere.com")