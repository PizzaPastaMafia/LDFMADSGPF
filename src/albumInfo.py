import gi
from PIL import Image
import requests
from io import BytesIO

from lastfm import LastFm

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

import os

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Lorenzo Del Forno Music Album Database Super Graphical Python Frontend")
        self.resize(300,300)
        self.connect("key-press-event", self.on_key_event)
        scrolledwindow = Gtk.ScrolledWindow()

        #self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        #self.add(self.box)

        self.grid = Gtk.Grid()
        self.add(grid)

        self.albumTitleBar = Gtk.SearchBar()

        #self.box.pack_start(self.albumTitleBar, True, True, 0)
        self.grid.attach(self.albumTitleBar, 0, 0, 1, 1)

        self.albumName = Gtk.SearchEntry()
        self.albumTitleBar.connect_entry(self.albumName)
        self.albumTitleBar.add(self.albumName)
        self.label = Gtk.Label(label=self.albumName)
        grid.attach(self.label, 0, 1, 1, 1)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()


    def on_key_event(self, widget, event):
        shortcut = Gtk.accelerator_get_label(event.keyval, event.state)

        if shortcut in ("Ctrl+F", "Ctrl+Mod2+F"):
            if self.albumTitleBar.get_search_mode():
                self.albumTitleBar.set_search_mode(False)
            else:
                self.albumTitleBar.set_search_mode(True)
                if shortcut in ("Return"):
                    self.label = Gtk.Label(label=self.albumName)
                    self.grid.attach(self.label, 0, 1, 1, 1)

        

    def on_button1_clicked(self, widget):
       self.lfm.toDatabase()

    def spawnAlbum(self.albumName, artistName):
        self.lfm = LastFm()
        self.lfm.setAlbumInfo(self.albumName, artistName)
        self.lfm.downloadCover()
        self.img = Gtk.Image.new_from_file(os.path.join("../pics/", self.lfm.getImgName()))
        self.box.pack_start(self.img, True, True, 0)

        #songList = lfm.getSongList()
        #for song in songList:
        #    scrolledwindow.add(Gtk.Label(song))

        self.button1 = Gtk.Button(label="Add Album to Library")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.box.pack_start(self.button1, True, True, 0)

    def main(self):
        Gtk.main()
