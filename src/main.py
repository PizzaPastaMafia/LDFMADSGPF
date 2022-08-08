import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import albumInfo
from library import MainWindow

def main():
    #albumName = input("albumName\n")
    #artistName = input("artistName\n")
    win = MainWindow()
    win.main()
    #win = albumInfo.MyWindow()
    Gtk.main()

if __name__=="__main__":
    main()
