################################################################################
# MainWindow.py
# Main user interface.
#
# Copyright (C) 2012 Kesara Nanayakkara Rathnayake
#
# This file is part of GTKalc.
#
# GTKalc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GTKalc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GTKalc.  If not, see <http://www.gnu.org/licenses/>.
#
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
