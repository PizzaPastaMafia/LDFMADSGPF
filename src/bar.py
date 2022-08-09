import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MainWindow(Gtk.Window):


    def __init__(self):
        super().__init__(title="search")
        self.add(self.box)
        self.add_searchBar()
        
    def add_searchBar(self):
        self.box = Gtk.Box(spacing=6)
        self.entry = Gtk.Entry()
        self.button = Gtk.Button(label="search")
        self.button.connect("clicked", self.show_entry)

        self.box.pack_start(self.entry, True, True, 0)
        self.box.pack_start(self.button, True, True, 0)


    def show_entry(self, widget):
        print(self.entry.get_text())
        self.label = Gtk.Label(label=self.entry.get_text())
        self.box.pack_start(self.entry, True, True, 0)
        self.show_all()


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()