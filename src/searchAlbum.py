import gi
from PIL import Image
import requests
from io import BytesIO

from lastfm import LastFm

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

from peewee import *
import database as datab
#from album import AlbumWindow

import os

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("Add Album")
        self.resize(300,200)
        #self.connect("key-press-event", self.on_key_event)
        scrolledwindow = Gtk.ScrolledWindow()
        self.mainBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.mainBox)

        self.add_searchBar()

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def showAlbum(self):
        self.albumWindow = Gtk.Window()
        self.set_title(self.lfm.getAlbumName() + " - " + self.lfm.getArtistName())
        self.albumWindow.albumBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.albumWindow.img = Gtk.Image.new_from_file(os.path.join("../pics/", self.lfm.getImgName()))

        #songList = lfm.getSongList()
        #for song in songList:
        #    scrolledwindow.add(Gtk.Label(song))

        try:
            datab.db.connect()
        except:
            datab.db.close()
            datab.db.connect()


        try:
            checkAlbum = datab.Album.get(datab.Album.title == self.albumSearch.get_text())
            print("found")
            button1 = Gtk.Button(label="This Album is already in library").set_device_enabled(False)
                
        except datab.Album.DoesNotExist:
            print("not found")
            button1 = Gtk.Button(label="Add Album to Library")
            button1.connect("clicked", self.toDatabase)
            #button1.connect("clicked", Gtk.main_quit)

        



        self.albumWindow.albumBox.pack_start(self.albumWindow.img, True, True, 0)
        self.albumWindow.albumBox.pack_start(button1, True, True, 0)

        self.albumWindow.add(self.albumWindow.albumBox)

        self.albumWindow.show_all()

        #self.mainBox.pack_start(self.albumBox, True, True, 0)

    def toDatabase(self, widget):
        artist=datab.Artist.create(name=self.artistSearch.get_text())
        datab.Album.insert(title=self.albumSearch.get_text(), artist=artist).execute()
        datab.db.close()

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