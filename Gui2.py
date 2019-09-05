# -*- coding: utf-8 -*-

import tkinter as tk
import os
from Settings import Settings
from Database import Database

class Page(tk.Frame):
    def __init__(self, *args, db=None, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.db = db
        self.configure(bg="white")
    def show(self):
        self.lift()

class LyricsDb(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.build()
        self.found_songs = {}
        items = self.search_songs(sort_by_title=True)
        self.populate_lbx_songsfound(items)

    def build(self):
        CONFIG_DEFAULT_LABEL = {"bg":      "white",
                                "anchor":  tk.W,
                                "justify": tk.LEFT,
                                "font":    "Calibri 12 bold"}
        CONFIG_DEFAULT_ENTRY = {"bg":      "white",
                                "justify": tk.LEFT,
                                "font":    "Calibri 12"}
        CONFIG_DEFAULT_LISTBOX = {"bg":      "white",
                                 "font":    "Calibri 12"}
        DEFAULT_PADDING_X = 0
        
        self.rowconfigure(10, weight=1)

        # =====================================================================
        #   Column
        # =====================================================================
        COL = 0
        #self.columnconfigure(COL+1, weight=1)

        # Label: Artist
        self.lab_artist = tk.Label(self, text="Artist",
                                  **CONFIG_DEFAULT_LABEL)
        self.lab_artist.grid(row=0, column=COL, padx=DEFAULT_PADDING_X, 
                             sticky=tk.W)
        
        # Entry: Artist
        self.artist_in = tk.StringVar()
        self.artist_in.trace_add("write", self.event_search_songs)
        self.ent_artist = tk.Entry(self, textvariable=self.artist_in,
                                   **CONFIG_DEFAULT_ENTRY)
        self.ent_artist.grid(row=1, column=COL, columnspan=2, sticky=tk.W+tk.E, 
                             padx=DEFAULT_PADDING_X)
        
        # Label: Record Title
        self.lab_rectitle = tk.Label(self, text="Record Title",
                                     **CONFIG_DEFAULT_LABEL)
        self.lab_rectitle.grid(row=2, column=COL, sticky=tk.W, 
                               padx=DEFAULT_PADDING_X)
        
        # Entry: Record Title
        self.rectitle_in = tk.StringVar()
        self.rectitle_in.trace_add("write", self.event_search_songs)
        self.ent_rectitle = tk.Entry(self, textvariable=self.rectitle_in,
                                   **CONFIG_DEFAULT_ENTRY)
        self.ent_rectitle.grid(row=3, column=COL, columnspan=2, sticky=tk.W+tk.E,
                               padx=DEFAULT_PADDING_X)
        
        # Label: Song Title
        self.lab_songtitle = tk.Label(self, text="Song Title",
                                      **CONFIG_DEFAULT_LABEL)
        self.lab_songtitle.grid(row=4, column=COL, sticky=tk.W, 
                                padx=DEFAULT_PADDING_X)
        
        # Entry: Song Title
        self.songtitle_in = tk.StringVar()
        self.songtitle_in.trace_add("write", self.event_search_songs)
        self.ent_songtitle = tk.Entry(self, textvariable=self.songtitle_in,
                                      **CONFIG_DEFAULT_ENTRY)
        self.ent_songtitle.grid(row=5, column=COL, columnspan=2, sticky=tk.W+tk.E, 
                                padx=DEFAULT_PADDING_X)
        
        # Label: <SPACE>
        self.lab_space1 = tk.Label(self, text="",
                                   **CONFIG_DEFAULT_LABEL)
        self.lab_space1.grid(row=6, column=COL, sticky=tk.W, 
                             padx=DEFAULT_PADDING_X)
        
        # Label: Songs Found
        self.lab_songsfound = tk.Label(self, text="Songs Found",
                                       **CONFIG_DEFAULT_LABEL)
        self.lab_songsfound.grid(row=7, column=COL, sticky=tk.W+tk.E, 
                                 padx=DEFAULT_PADDING_X)
        
        # Listbox: Songs Found
        self.lbx_songsfound = tk.Listbox(self,
                                         selectmode=tk.SINGLE,
                                         width=45,
                                         **CONFIG_DEFAULT_LISTBOX)
        self.lbx_songsfound.grid(row=8, column=COL, rowspan=10, columnspan=2, 
                                 sticky=tk.W+tk.E+tk.N+tk.S, 
                                 padx=DEFAULT_PADDING_X)
        self.lbx_songsfound.bind("<<ListboxSelect>>", self.event_select_song)

        # =====================================================================
        #   Column
        # =====================================================================
        COL += 2
        
        # Scrollbar: Songs Found
        self.scb_songsfound = tk.Scrollbar(self)
        self.scb_songsfound.grid(row=8, column=COL, rowspan=10, sticky="ns")
        self.lbx_songsfound.configure(yscrollcommand=self.scb_songsfound.set)
        self.scb_songsfound.configure(command=self.lbx_songsfound.yview)
                
        # =====================================================================
        #   Column
        # =====================================================================
        COL += 1
        
        # Label: <SPACE>
        self.lab_space3 = tk.Label(self, text="",
                                   width=10,
                                   **CONFIG_DEFAULT_LABEL)
        self.lab_space3.grid(row=1, column=COL)    

        # =====================================================================
        #   Column
        # =====================================================================
        COL += 1
        self.columnconfigure(COL+1, weight=1)
        
        # Label: Lyrics
        self.lab_lyrics = tk.Label(self, text="<Selected Song>",
                                  **CONFIG_DEFAULT_LABEL)
        self.lab_lyrics.grid(row=0, column=COL, sticky=tk.W+tk.E, 
                             padx=DEFAULT_PADDING_X)
        
        # Listbox: Lyrics
        self.lbx_lyrics = tk.Listbox(self,
                                     selectmode=tk.SINGLE,
                                     width=60,
                                     **CONFIG_DEFAULT_LISTBOX)
        self.lbx_lyrics.grid(row=1, column=COL, rowspan=17, columnspan=2, 
                             sticky=tk.W+tk.E+tk.N+tk.S, padx=DEFAULT_PADDING_X)

        # =====================================================================
        #   Column
        # =====================================================================
        COL += 2
        
        # Scrollbar: Songs Found
        self.scb_lyrics = tk.Scrollbar(self)
        self.scb_lyrics.grid(row=1, column=COL, rowspan=17, sticky="ns")
        self.lbx_lyrics.configure(yscrollcommand=self.scb_lyrics.set)
        self.scb_lyrics.configure(command=self.lbx_lyrics.yview)

    def populate_lbx_songsfound(self, items):
        """
        Adds song names to 'Songs Found' listbox. Saves listbox index and
        song ID to a dictionary for use in other methods.

        Args:
            items: (List) of tuples (song_id, song_name, ...) 
        
        Returns:
            -
        
        Raises:
            -
        """
        self.lbx_songsfound.delete(0, tk.END)
        self.found_songs = dict([(idx, item[0]) 
                                for idx, item in enumerate(items)])
        for item in items:
            self.lbx_songsfound.insert(tk.END, item[1])

    def populate_lbx_lyrics(self, lyrics):
        """
        Writes lyrics of a song to 'Lyrics' listbox.

        Args:
            lyrics: (String) Lines are assumed to be separated by the substring
                    "\r\n"
        
        Returns:
            -
        
        Raises:
            -
        """
        self.lbx_lyrics.delete(0, tk.END)
        for line in lyrics.split("\r\n"):
            self.lbx_lyrics.insert(tk.END, " " + line)
    
    def search_songs(self, song_title="", record="", artist="", 
                     sort_by_title=False):
        """
        Queries database to find IDs and titles of songs matching the
        input criteria

        Args:
            song_title:    (String)
            record:        (String)
            artist:        (String)
            sort_by_title: (Boolean)
        
        Returns:
            (List) of tuples (song_id, song_name)
        
        Raises:
            -
        """
        sql = (f"SELECT id, song_title FROM Songs "
               f"WHERE (song_title LIKE '%{song_title}%') "
               f"AND (record LIKE '%{record}%') "
               f"AND (artist LIKE '%{artist}%')")
        if sort_by_title:
            sql += " ORDER BY song_title ASC"
        items = self.db.query_db(sql)
        return items
    
    def event_select_song(self, evt):
        """
        Event that fires when a song is selected from the 'Songs Found'
        listbox. Writes the selected song's lyrics to 'Lyrics' listbox.

        Args:
            evt: (Event)
        
        Returns:
            -
        
        Raises:
            -
        """
        w = evt.widget
        try:
            index = int(w.curselection()[0])
            # event occasionally fires even if it's not the listbox
            # that's clicked-on. In that case nothing should happen.
        except(IndexError):
            return
        value = w.get(index)
        song_id = self.found_songs[index]
        self.lab_lyrics.config(text=value)
        sql = f"SELECT lyrics FROM Songs WHERE id={song_id}"
        lyrics = self.db.query_db(sql)[0][0]
        self.populate_lbx_lyrics(lyrics)

    def event_search_songs(self, *args):
        """
        Event that fires when the text in any of the entry fields is changed.
        Writes all songs matching the input criteria to 'Songs Found' listbox.

        Args:
            *args: ~Not used~
        
        Returns:
            -
        
        Raises:
            -
        """
        song_title = self.ent_songtitle.get()
        record = self.ent_rectitle.get()
        artist = self.ent_artist.get()
        items = self.search_songs(song_title, record, artist)        
        self.populate_lbx_songsfound(items)

class Preferences(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.build()

    def on_click(self, event):
        print("clicked!")
    def on_doubleclick(self, event):
        print("double clicked!")

    def build(self):
        self.label = tk.Label(self, text="SETTINGS", bg="grey")
        self.label.pack(side="top", fill="both", expand=True)
        self.label.bind("<Button-1>", self.on_click)
        self.label.bind("<Double-1>", self.on_doubleclick)

class Webcrawler(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        self.label = tk.Label(self, text="WEBCRAWLER", bg="blue")
        self.label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, db, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        PADDING = {"padx": 25, "pady":25}
        
        pge_lyricsdb = LyricsDb(self, db=db, **PADDING)
        pge_crawler = Webcrawler(self, db=db, **PADDING)
        pge_settings = Preferences(self, db=db, **PADDING)

        headerframe = tk.Frame(self, bg="white", **PADDING)
        container = tk.Frame(self)
        headerframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        pge_lyricsdb.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pge_crawler.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        pge_settings.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        lab = tk.Label(headerframe, text="Lyrics Database", bg="white",
                       anchor=tk.W, justify=tk.LEFT,
                       font="Calibri 35 bold italic")
        btn_lyricsdb = tk.Button(headerframe, text="HOME",
                                 command=pge_lyricsdb.lift)
        btn_crawler =  tk.Button(headerframe, text="Webcrawler", 
                                 command=pge_crawler.lift)
        btn_settings = tk.Button(headerframe, text="Settings", 
                                 command=pge_settings.lift)

        lab.pack(side="left")
        btn_settings.pack(side="right")
        btn_crawler.pack(side="right")
        btn_lyricsdb.pack(side="right")

        pge_lyricsdb.show()

if __name__ == "__main__":
    settings = Settings()
    db_name = settings.get("main", "db_name")
    db = Database(os.getcwd() + db_name, fill_with_examples=False)
    
    root = tk.Tk()
    main = MainView(root, db=db)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1000x600")
    root.mainloop()