import tkinter as tk
import pandas as pd
import numpy as np
import re


class DataTable(tk.Frame):

    class DataColumn():
        def __init__(self, header, searchvar, searchbox, data):
            self.header = header
            self.searchvar = searchvar
            self.searchbox = searchbox
            self.data = data
    
    def __init__(self, *args, df, rowselectcommand=None, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.data_full = df
        self.data_filtered = self.data_full
        self.rowselectcommand = rowselectcommand

        # Shared scrollbar
        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.tablecolumns = []

        # Button to reset search boxes        
        self.btn_reset = tk.Button(self, text="x", 
                                   command=self.clear_search_boxes)
        
        for i, col in enumerate(self.data_full.columns):
            # Table Header
            lab = tk.Label(self, text=col, font="Calibri 12 bold")
            lab.grid(row=0, column=i, sticky=tk.W+tk.E,)
            lab.bind("<Button-1>", self.event_label_click)
            lab.bind("<Double-Button-1>", self.event_label_doubleclick)

            # Search box
            txtvar = tk.StringVar()
            txtvar.trace_add("write", self.event_search)
            ent = tk.Entry(self, textvariable=txtvar)
            ent.grid(row=1, column=i, sticky=tk.W+tk.E,)

            # Table Columns
            lbx = tk.Listbox(self, exportselection=False,
                         yscrollcommand=lambda x, y, i=i: self.yscroll(i, x, y))
            lbx.grid(row=2, column=i, rowspan=10, sticky=tk.W+tk.E,)
            lbx.bind("<<ListboxSelect>>", self.event_row_select)

            self.tablecolumns.append(self.DataColumn(header=lab, searchvar=txtvar,
                                                searchbox=ent, data=lbx))

        self.btn_reset.grid(row=1, column=len(self.data_full.columns))

        self.scrollbar.config(command=self.yview)
        self.scrollbar.grid(row=2, column=len(self.data_full.columns), 
                            rowspan=10, sticky="ns")

        for i in range(len(self.data_full.columns)):
            self.columnconfigure(i, weight=1)

        self.populate_table()

    def yscroll(self, i, *args):
        for col in self.tablecolumns:
            lbx_active = self.tablecolumns[i].data
            lbx = col.data
            if not lbx is lbx_active:
                if lbx.yview()!=lbx_active.yview():
                    lbx.yview_moveto(args[0])
                self.scrollbar.set(*args)

    def yview(self, *args):
        for col in self.tablecolumns:
            col.data.yview(*args)
    
    def event_row_select(self, evt):
        w = evt.widget
        try:
            idx_selected = int(w.curselection()[0])
        except(IndexError):
            return
        for col in self.tablecolumns:
            lbx = col.data
            if not lbx is w:
                self.deselect_all(lbx)
                lbx.selection_set(idx_selected)
        if not self.rowselectcommand is None:
            self.rowselectcommand(idx_selected)

    def event_label_click(self, evt):
        w = evt.widget
        self.data_filtered.sort_values(by=w.cget("text"), 
                                       ascending=True,
                                       inplace=True)
        self.populate_table()

    def event_label_doubleclick(self, evt):
        w = evt.widget
        self.data_filtered.sort_values(by=w.cget("text"), 
                                       ascending=False,
                                       inplace=True)
        self.populate_table()

    def event_search(self, *args):
        criteria = []
        for col in self.tablecolumns:
            header = col.header.cget("text")
            val = col.searchbox.get()
            d_type = self.data_full[header].dtype
            if val!="":
                criteria.append((header, val, d_type))
        if len(criteria)==0:
            self.reset_search()
        else:
            elements = []
            for header, val, d_type in criteria:
                if np.issubdtype(d_type, np.number):
                    pattern = r"([>?|<?]=?)?(\d+[.\d]*)"
                    m = re.match(pattern, val)
                    if m is None:
                        pass
                    elif m.group(2) is None:
                        pass
                    elif m.group(1) is None:
                        elements.append(f"{header} == {m.group(2)}")
                    else:
                        elements.append(f"{header} {m.group(1)} {m.group(2)}")
                else:
                    elements.append(f"{header}.str.contains('{val}')" )
            query = " and ".join(elements)
            if query!="":
                try:
                    self.data_filtered = self.data_full.query(query, 
                                                              engine="python")
                except(AttributeError):
                    self.data_filtered = pd.DataFrame(columns=self.data_full.columns)
                self.populate_table()

    def reset_search(self):
        self.data_filtered = self.data_full
        self.populate_table()

    def populate_table(self):
        for col in self.tablecolumns:
            lbx = col.data
            lbx.delete(0, tk.END)
            for x in self.data_filtered[col.header.cget("text")]:
                lbx.insert("end", x) 

    def deselect_all(self, lbx):
        idx_selected = lbx.curselection()
        if len(idx_selected)>0:
            lbx.selection_clear(idx_selected)

    def clear_search_boxes(self):
        for col in self.tablecolumns:
            col.searchvar.set("")
        self.reset_search()

if __name__ == "__main__":
    df = pd.read_csv("songs.csv")
    df = df[["Album", "Artist", "Title", "Year"]]
    root = tk.Tk()
    main = DataTable(root, df=df, rowselectcommand=lambda x: print(x))
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()