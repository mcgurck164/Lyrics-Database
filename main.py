# -*- coding: utf-8 -*-

from Database import Database
from Song import Song

DB_NAME = "songs.db"

if __name__ == "__main__":
    db = Database(DB_NAME)
    s1 = Song(artist="Wizo",
              record="Herrénhandtasche",
              year=1994,
              song_title="Quadrat im Kreis",
              lyrics="Hin und wieder stell ich fest, dass ich nicht mehr ...",
              link_to_lyrics="somewhere")
    print(db.add_song(s1))
