# encoding: utf-8

################################################################################
# AboutDilog.py
# About dialog UI
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

class AboutDialog:
    """
    About Dialog
    """
    def __init__(self):
        handlers = {
                "onAboutDialogClose" : self.close
        }
        builder = Gtk.Builder()
        builder.add_from_file("AboutDialog.glade")
        builder.connect_signals(handlers)
        self.window = builder.get_object("about_dialog")
        self.window.show_all()

    def close(self, widget, data=None):
        """
        Close about dialog.
        """
        self.window.hide()
        #gtk.main
