import gi
from PIL import Image
import requests
from io import BytesIO

from lastfm import LastFm

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

#from album import AlbumWindow

import os

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Lorenzo Del Forno Music Album Database Super Graphical Python Frontend")
        self.resize(300,300)
        #self.connect("key-press-event", self.on_key_event)
        scrolledwindow = Gtk.ScrolledWindow()
        self.mainBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.mainBox)

        self.add_searchBar()

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def showAlbum(self):
        self.albumWindow = Gtk.Window()
        self.albumWindow.albumBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.albumWindow.img = Gtk.Image.new_from_file(os.path.join("../pics/", self.lfm.getImgName()))

        #songList = lfm.getSongList()
        #for song in songList:
        #    scrolledwindow.add(Gtk.Label(song))

        button1 = Gtk.Button(label="Add Album to Library")

        self.albumWindow.albumBox.pack_start(self.albumWindow.img, True, True, 0)
        self.albumWindow.albumBox.pack_start(button1, True, True, 0)

        self.albumWindow.add(self.albumWindow.albumBox)

        self.albumWindow.show_all()

        #self.mainBox.pack_start(self.albumBox, True, True, 0)

    def add_searchBar(self):
        self.searchBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)

        self.albumSearch = Gtk.Entry()
        self.artistSearch = Gtk.Entry()
        self.button = Gtk.Button(label="search")
        self.button.connect("clicked", self.searchAlbum)

        self.searchBox.pack_start(self.albumSearch, True, True, 0)
        self.searchBox.pack_start(self.artistSearch, True, True, 0)
        self.searchBox.pack_start(self.button, True, True, 0)

        self.mainBox.pack_start(self.searchBox, True, True, 0)
        self.show_all()

       

    #def on_button1_clicked(self, widget):
    #   self.lfm.toDatabase()

    def searchAlbum(self, widget):
        self.lfm = LastFm()
        self.lfm.setAlbumInfo(self.albumSearch.get_text(), self.artistSearch.get_text())
        self.lfm.lastfm_get(self.lfm.payload)
        self.lfm.downloadCover()

        self.showAlbum()



    def main(self):
        Gtk.main()