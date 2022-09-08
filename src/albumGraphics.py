import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
from gi.repository import GdkPixbuf
from peewee import *
from database import *
from lastfm import LastFm as lf
import searchAlbum
import database as datab
import os

class AlbumExtended(Gtk.Window):
    def __init__(self, albumName):
        super().__init__()
        self.album = self.queryAlbum(albumName)
        self.set_title(title=self.album.title + " - " + self.album.artist.name)
        self.lf = lf()
        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.lf.setAlbumInfo(name=self.album.title, artist=self.album.artist.name)
        self.box.pack_start(Gtk.Image.new_from_file(os.path.join("../pics/", self.lf.getImgName())), True, True, 0)
        self.box.pack_start(Gtk.Label(label=self.album.title), True, True, 0)
        self.box.pack_start(Gtk.Label(label=self.album.artist.name), True, True, 0)

        self.voteBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        self.voteSelect = Gtk.ComboBox.new_with_entry()
        self.voteSelect.do_format_entry_text(self.voteSelect,"maooo")
        self.voteBox.pack_start(Gtk.Label(label="vote:"), True, True, 0)
        self.voteBox.pack_start(self.voteSelect, True, True, 0)
        self.box.pack_start(self.voteBox, True, True, 0)


        if self.album.favourite:
            self.favouriteButton = Gtk.Button(label="remove to favorites")
        else:
            self.favouriteButton = Gtk.Button(label="add to favorites")

        self.favouriteButton.connect("clicked", self.changeFav)
        
        self.box.pack_start(self.favouriteButton, True, True, 0)

        self.add(self.box)

        self.connect("destroy", self.destroy)
        self.show_all()

    def changeFav(self, widget):
        datab.Album.update(favourite= not(self.album.favourite)).where(datab.Album.title == self.album.title).execute()
        self.destroy()
    
    def queryAlbum(self, albumName):
        
        try:
            datab.db.connect()
        except:
            datab.db.close()
            datab.db.connect()

        rows = datab.Album.select()

        datab.db = SqliteDatabase('albums.db')

        for row in rows:
            if(row.title == albumName):
                return row


class AlbumIcon(Gtk.Button):
    def __init__(self, albumName):
        super().__init__()
        self.album = self.queryAlbum(albumName)
        self.lf = lf()
        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.lf.setAlbumInfo(name=self.album.title, artist=self.album.artist.name)
        img = Gtk.Image.new_from_file(os.path.join("../pics/", self.lf.getImgName()))

        self.box.pack_start(img, True, True, 0)
        self.box.pack_start(Gtk.Label(label=self.album.title), True, True, 0)
        self.box.pack_start(Gtk.Label(label=self.album.artist.name), True, True, 0)

        try:
            datab.db.connect()
        except:
            datab.db.close()
            datab.db.connect()


        checkAlbum = datab.Album.get(datab.Album.title == self.album.title)
        self.box.pack_start(Gtk.Label(label=checkAlbum.vote), True, True, 0)
        self.add(self.box)
        self.connect("clicked", self.extend)
        self.show_all()

    def extend(self, widget):
        win = AlbumExtended(self.album.title)

    def queryAlbum(self, albumName):
        
        try:
            datab.db.connect()
        except:
            datab.db.close()
            datab.db.connect()

        rows = datab.Album.select()

        datab.db = SqliteDatabase('albums.db')

        for row in rows:
            if(row.title == albumName):
                return row

class NotFoundWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Not found")
        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.resize(300,200)
        self.box.pack_start(Gtk.Label("album not found"), True, True, 0)
        ok = Gtk.Button(label="OK")
        ok.connect("clicked", self.kill)
        self.box.pack_start(ok, True, True, 0)

        self.add(self.box)

        self.show_all()

    def kill(self, widget):
        self.destroy()