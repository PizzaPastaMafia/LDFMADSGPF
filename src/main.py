import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#import albumInfo
from library import MainWindow

def main():
    win = MainWindow()
    Gtk.main()

if __name__=="__main__":
    main()
