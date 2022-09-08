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




class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Lorenzo Del Forno Music Album Database Super Graphical Python Frontend")
        self.resize(975,975)
        self.grid = Gtk.Grid()
        self.favTrigger = False

        hbar = Gtk.HeaderBar()
        hbar.set_show_close_button(True)
        hbar.props.title = "Lorenzo Del Forno Music Album Database Super Graphical Python Frontend"
        self.set_titlebar(hbar)

        self._search_btn = Gtk.Button()
        search_icn = Gio.ThemedIcon(name="search-symbolic")
        search_img = Gtk.Image.new_from_gicon(search_icn, Gtk.IconSize.BUTTON)
        self._search_btn.set_image(search_img)
        
        self._update_btn = Gtk.Button()
        update_icn = Gio.ThemedIcon(name="reload-symbolic")
        update_img = Gtk.Image.new_from_gicon(update_icn, Gtk.IconSize.BUTTON)
        self._update_btn.set_image(update_img)
        self._update_btn.connect("clicked", self.gtkShowAlbums)

        self._add_btn = Gtk.Button()
        add_icn = Gio.ThemedIcon(name="list-add-symbolic")
        add_img = Gtk.Image.new_from_gicon(add_icn, Gtk.IconSize.BUTTON)
        self._add_btn.set_image(add_img)
        self._add_btn.connect("clicked", self.showWindow)

        self._fav_btn = Gtk.Button()
        fav_icn = Gio.ThemedIcon(name="favourite-symbolic")
        fav_img = Gtk.Image.new_from_gicon(fav_icn, Gtk.IconSize.BUTTON)
        self._fav_btn.set_image(fav_img)
        self._fav_btn.connect("clicked", self.showFavourites)


        hbar.pack_end(self._search_btn)
        hbar.pack_end(self._update_btn)
        hbar.pack_start(self._add_btn)
        hbar.pack_end(self._fav_btn)


        self.scroll = Gtk.ScrolledWindow()
        self.showAlbums(self.favTrigger)

        self.add(self.scroll)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def showFavourites(self, widget):
        self.favTrigger = not(self.favTrigger)
        self.scroll.remove(self.grid)
        self.showAlbums(self.favTrigger)

    def gtkShowAlbums(self, widget):
        self.scroll.remove(self.scroll.get_child())
        tempGrid = Gtk.Grid()

        gridSize = 3

        rowNum = 0
        colNum = 0

        try:
            datab.db.connect()
        except:
            datab.db.close()
            datab.db.connect()

        rows = datab.Album.select()

        datab.db = SqliteDatabase('albums.db')

        for row in rows:

            self.grid.attach(AlbumIcon(row.title), colNum, rowNum, 1, 1)
            
            if colNum == gridSize-1:
                colNum = 0
                rowNum += 1
            else:
                colNum += 1

        self.grid = tempGrid
        self.scroll.add(self.grid)
        self.scroll.show_all()
        
    def showAlbums(self, showFavs):
        tempGrid = Gtk.Grid()

        gridSize = 3

        rowNum = 0
        colNum = 0

        try:
            datab.db.connect()
        except:
            datab.db.close()
            datab.db.connect()

        rows = datab.Album.select()

        datab.db = SqliteDatabase('albums.db')

        for row in rows:
            if((showFavs and row.favourite) or (showFavs == False)):

                tempGrid.attach(AlbumIcon(row.title), colNum, rowNum, 1, 1)
            
            
            if colNum == gridSize-1:
                colNum = 0
                rowNum += 1
            else:
                colNum += 1

        self.grid = tempGrid
        self.scroll.add(self.grid)
        self.scroll.show_all()

                
    def showWindow(self, widget):
        win = searchAlbum.MyWindow()
        win.show()
        #albumInfo.main()

    def main(self):
        Gtk.main()

        
        