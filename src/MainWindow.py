################################################################################
# MainWindow.py
# Main user interface.
# Copyright (C) Kesara Nanayakkara Rathnayake
################################################################################

from gi.repository import Gtk

class MainWindow:
    """
    Main user interface.
    """
    def __init__(self):
        handlers = {
                "onWindowDelete"    : Gtk.main_quit,
                "onMenuQuit"        : Gtk.main_quit,
                "onNumberButtonClick"     : self.number_press
        }
        builder = Gtk.Builder()
        builder.add_from_file("MainWindow.glade")
        builder.connect_signals(handlers)

        self.entry = builder.get_object("entry")
        
        window = builder.get_object("main_window")
        window.show_all()

    def number_press(self, widget, data=None):
        if widget.get_label == '.' and not('.' in self.entry.get_text()):
            self.entry.set_text(self.entry.get_text() + ".0")
        else:
            self.entry.set_text(self.entry.get_text() + widget.get_label())

if __name__ == "__main__":
    mw = MainWindow()
    Gtk.main()
