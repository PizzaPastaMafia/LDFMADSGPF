import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from database import *
from lastfm import LastFm
import albumInfo

class AlbumIcon(Gtk.Box):
    def __init__(self, albumName, artistName):
        super.__init__(self, spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(LastFm().setAlbumInfo(albumName, artistName).getImgName(), True, True, 0)
        self.add(albumName, True, True, 0)
        self.add(artistName, True, True, 0)

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Lorenzo Del Forno Music Album Database Super Graphical Python Frontend")
        self.grid = Gtk.Grid()
        self.addAlbumBtn = Gtk.Button(label="Add Album") 
        self.addAlbumBtn.connect("clicked", self.showWindow)
        self.add(self.addAlbumBtn)
        #for album in Album.select():
        #    self.add(AlbumIcon(album.title, album.artist))

        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    def showWindow(self, widget):
        win = albumInfo.MyWindow()
        win.show()
        #albumInfo.main()

    def main(self):
        Gtk.main()

        
        