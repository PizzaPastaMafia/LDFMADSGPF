import gi
from PIL import Image
from io import BytesIO
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf

class AlbumWindow(Gtk.Window):
    self.albumName = ""
    self.artistName = ""
    def __init__(self, albumName, artistName):
        Gtk.Window.__init__(self)
        title = self.albumName + " - " + self.artistName
        self.set_title(title)
        self.albumBox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.img = Gtk.Image.new_from_file(os.path.join("./pics/", self.lfm.getImgName()))

        #songList = lfm.getSongList()
        #for song in songList:
        #    scrolledwindow.add(Gtk.Label(song))

        button1 = Gtk.Button(label="Add Album to Library")

        self.albumBox.pack_start(self.img, True, True, 0)
        self.albumBox.pack_start(button1, True, True, 0)

        self.add(albumBox)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()
