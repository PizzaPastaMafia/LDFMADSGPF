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
    def __init__(self, album):
        super().__init__()
        self.album = album
        self.set_title(title=album.title + " - " + album.artist.name)
        self.lf = lf()
        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.lf.setAlbumInfo(name=album.title, artist=album.artist.name)
        self.box.pack_start(Gtk.Image.new_from_file(os.path.join("../pics/", self.lf.getImgName())), True, True, 0)
        self.box.pack_start(Gtk.Label(label=album.title), True, True, 0)
        self.box.pack_start(Gtk.Label(label=album.artist.name), True, True, 0)

        self.voteBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        self.voteSelect = Gtk.ComboBox.new_with_entry()
        self.voteSelect.do_format_entry_text(self.voteSelect,"maooo")
        self.voteBox.pack_start(Gtk.Label(label="vote:"), True, True, 0)
        self.voteBox.pack_start(self.voteSelect, True, True, 0)
        self.box.pack_start(self.voteBox, True, True, 0)


        if album.favourite:
            self.favouriteButton = Gtk.Button(label="remove to favorites")
        else:
            self.favouriteButton = Gtk.Button(label="add to favorites")

        self.favouriteButton.connect("clicked", self.changeFav)
        
        self.box.pack_start(self.favouriteButton, True, True, 0)

        self.add(self.box)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def changeFav(self, widget):
        datab.Album.update(favourite= not(self.album.favourite)).where(datab.Album.title == self.album.title).execute()

#class EmptyAlbumIcon(Gtk.button):

class AlbumIcon(Gtk.Button):
    def __init__(self, album):
        super().__init__()
        self.album = album
        self.lf = lf()
        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.lf.setAlbumInfo(name=album.title, artist=album.artist.name)
        img = Gtk.Image.new_from_file(os.path.join("../pics/", self.lf.getImgName()))

        self.box.pack_start(img, True, True, 0)
        self.box.pack_start(Gtk.Label(label=album.title), True, True, 0)
        self.box.pack_start(Gtk.Label(label=album.artist.name), True, True, 0)

        try:
            datab.db.connect()
        except:
            datab.db.close()
            datab.db.connect()


        checkAlbum = datab.Album.get(datab.Album.title == album.title)
        self.box.pack_start(Gtk.Label(label=checkAlbum.vote), True, True, 0)
        self.add(self.box)
        self.connect("clicked", self.extend)
        self.show_all()

    def extend(self, widget):
        win = AlbumExtended(self.album)





class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Lorenzo Del Forno Music Album Database Super Graphical Python Frontend")
        self.resize(1000,1000)
        self.grid = Gtk.Grid()

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
        #self._update_btn.connect("clicked", self.showAlbums)

        self._add_btn = Gtk.Button()
        add_icn = Gio.ThemedIcon(name="list-add-symbolic")
        add_img = Gtk.Image.new_from_gicon(add_icn, Gtk.IconSize.BUTTON)
        self._add_btn.set_image(add_img)
        self._add_btn.connect("clicked", self.showWindow)

        self._fav_btn = Gtk.Button()
        fav_icn = Gio.ThemedIcon(name="favourite-symbolic")
        fav_img = Gtk.Image.new_from_gicon(fav_icn, Gtk.IconSize.BUTTON)
        self._fav_btn.set_image(fav_img)

        hbar.pack_end(self._search_btn)
        hbar.pack_end(self._update_btn)
        hbar.pack_start(self._add_btn)
        hbar.pack_end(self._fav_btn)

        self.showAlbums()

        self.add(self.grid)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def showAlbums(self):


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

        #self.grid.attach(self.EmptyAlbumIcon, colNum, rowNum, 1, 1)
        for row in rows:
            self.grid.attach(AlbumIcon(row), colNum, rowNum, 1, 1)
            
            if colNum == gridSize-1:
                colNum = 0
                rowNum += 1
            else:
                colNum += 1

                
    def showWindow(self, widget):
        win = searchAlbum.MyWindow()
        win.show()
        #albumInfo.main()

    def main(self):
        Gtk.main()

        
        