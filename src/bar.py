import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):


    def __init__(self):
        super().__init__(title="search")
        self.add_searchBar()

    
        
    def add_searchBar(self):
        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)
        self.entry = Gtk.Entry()
        self.button = Gtk.Button(label="search")
        self.button.connect("clicked", self.showAlbum(self.entry))

        self.box.pack_start(self.entry, True, True, 0)
        self.box.pack_start(self.button, True, True, 0)

    def showAlbum(self, albumName):
        self.albumLayout = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.albumLAyout(LastFm().setAlbumInfo(albumName, artistName).getImgName(), True, True, 0)
        self.add(albumName, True, True, 0)
        self.add(artistName, True, True, 0)


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()