# encoding: utf-8

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
import math

class MainWindow:
    """
    Main user interface.
    """
    def __init__(self):
        handlers = {
                "onWindowDelete"            : Gtk.main_quit,
                "onMenuQuit"                : Gtk.main_quit,
                "onNumberButtonClick"       : self.number_press,
                "onOperationButtonClick"    : self.operation_press,
                "onMemoryButtonClick"       : self.memory_press,
                "onAllCancelButtonClick"    : self.all_cancel
        }
        builder = Gtk.Builder()
        builder.add_from_file("MainWindow.glade")
        builder.connect_signals(handlers)

        self.window = builder.get_object("main_window")
        self.entry = builder.get_object("entry")
        self.status = builder.get_object("statusbar")
        self.history = builder.get_object("history").get_buffer()
        self.value = None
        self.memory = 0
        self.operator = None
        self.entry.set_text("0")
        self.refresh = True
        
        window = builder.get_object("main_window")
        window.show_all()

    def all_cancel(self, widget, data=None):
        """
        Perform all cancel operation.
        """
        self.value = None
        self.operator = None
        self.entry.set_text("0")
        self.refresh = True
        self.status.pop(0)

    def number_press(self, widget, data=None):
        """
        Performs changes on text entry depending on user input.
        """
        if self.refresh and widget.get_label() != "±":
            self.entry.set_text("")
        if widget.get_label() == "±" and not("-" in self.entry.get_text()):
            self.entry.set_text("-" + self.entry.get_text())
        elif widget.get_label() == "±":
            self.entry.set_text(self.entry.get_text()[1:])
        elif widget.get_label() == "." and not("." in self.entry.get_text()):
            if self.refresh:
                self.entry.set_text("0.")
            else:
                self.entry.set_text(self.entry.get_text() + ".")
        else:
            self.entry.set_text(self.entry.get_text() + widget.get_label())
        self.refresh = False

    def memory_press(self, widget, data=None):
        """
        Performs memory operations
        """
        if widget.get_label() == "MC":
            self.memory = 0
            self.status.pop(1)
        elif widget.get_label() == "MR":
            self.entry.set_text(self.format_value(self.memory))
        elif widget.get_label() in ("M+", "M-"):
            if self.value:
                self.operation()
            if widget.get_label() == "M+":
                self.memory += float(self.entry.get_text())
            if widget.get_label() == "M-":
                self.memory -= float(self.entry.get_text())
            self.status.pop(1)
            self.status.push(1, "M={0}".format(
                self.format_value(self.memory)))
        self.refres = True

    def operation_press(self, widget, data=None):
        """
        Handles user inputs on mathematical operations.
        """
        if self.value:
            self.operation()
        if widget.get_label() in ("!n", "√", "x²", "x³"):
            self.operator = widget.get_label()
            self.single_value_operation()
        elif widget.get_label() != "=":
            self.value = float(self.entry.get_text())
            # Set operator
            self.status.push(0, widget.get_label())
            self.operator = widget.get_label()
        self.refresh = True
        
    def single_value_operation(self):
        """
        Perform operations where only one is involved.
        """
        if self.operator == "!n":
            self.history.insert_at_cursor("!{0} = ".format(
                self.entry.get_text()))
            try:
                self.entry.set_text(math.factorial(
                    int(self.entry.get_text())))
            except ValueError:
                Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.CANCEL,
                    "The value must be non-negative integer.")
                self.operator = None
                self.history.insert_at_cursor(
                    "ERROR: The value must be non-negative integer.\n")
                return
            self.history.insert_at_cursor("{0}\n".format(self.entry.get_text()))
        elif self.operator == "√":
            self.history.insert_at_cursor("√{0} = ".format(
                self.entry.get_text()))
            try:
                self.entry.set_text(self.format_value(math.sqrt(
                    float(self.entry.get_text()))))
            except ValueError:
                Gtk.MessageDialog(self.window, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.CANCEL,
                    "The value must be non-negative. Imaginary numbers not supported.")
                self.operator = None
                self.history.insert_at_cursor(
                    "ERROR: The value must be non-negative.\n")
                return
            self.history.insert_at_cursor("{0}\n".format(self.entry.get_text()))
        elif self.operator == "x²":
            self.history.insert_at_cursor("{0}² = ".format(
                self.entry.get_text()))
            self.entry.set_text(self.format_value(pow(float(self.entry.get_text()),
                2)))
            self.history.insert_at_cursor("{0}\n".format(self.entry.get_text()))
        elif self.operator == "x³":
            self.history.insert_at_cursor("{0}³ = ".format(
                self.entry.get_text()))
            self.entry.set_text(self.format_value(pow(float(self.entry.get_text()),
                3)))
            self.history.insert_at_cursor("{0}\n".format(self.entry.get_text()))

        self.operator = None

    def operation(self):
        """
        Perform mathematical operations
        """
        if self.operator == "xⁿ":
            self.history.insert_at_cursor("{0} ^ {1} = ".format(
                self.format_value(self.value), self.entry.get_text()))
        else:
            self.history.insert_at_cursor("{0} {1} {2} = ".format(
                self.format_value(self.value),
                self.operator, self.entry.get_text()))
        if self.operator == "+":
            self.entry.set_text(self.format_value(str(self.value +
                float(self.entry.get_text()))))
        elif self.operator == "-":
            self.entry.set_text(self.format_value(str(self.value -
                float(self.entry.get_text()))))
        elif self.operator == "÷":
            self.entry.set_text(self.format_value(str(self.value /
                float(self.entry.get_text()))))
        elif self.operator == "×":
            self.entry.set_text(self.format_value(str(self.value *
                float(self.entry.get_text()))))
        elif self.operator == "×":
            self.entry.set_text(self.format_value(str(self.value *
                float(self.entry.get_text()))))
        elif self.operator == "xⁿ":
            self.entry.set_text(self.format_value(str(pow(self.value,
                float(self.entry.get_text())))))
        self.history.insert_at_cursor("{0}\n".format(self.entry.get_text()))
        self.value = None
        self.operator = None
        self.status.pop(0)

    def format_value(self, value):
        """
        Remove .0 when applicable.
        """
        value = str(value)
        if value[-2:] == ".0":
            return value[:-2]
        else:
            return value

