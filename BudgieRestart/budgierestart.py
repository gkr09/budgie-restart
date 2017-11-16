#!/usr/bin/env python3

# Copyright (C) 2017 Gopikrishnan R

"""
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import subprocess,gi.repository
gi.require_version('Budgie','1.0')
gi.require_version('Gtk','3.0')
from gi.repository import Budgie, GObject, Gtk

class BudgieRestart(GObject.GObject, Budgie.Plugin):

	__gtype_name__ = "BudgieRestart"

	def __init__(self):

		GObject.Object.__init__(self)

	def do_get_panel_widget(self, uuid):

		return BudgieRestartApplet(uuid)


class BudgieRestartApplet(Budgie.Applet):

	box = Gtk.EventBox()
	revealer=Gtk.Revealer()                      # Contains individual restart actions
	button=Gtk.Button()                          # Restart Button, Restarts both panel & WM
	button.set_relief(Gtk.ReliefStyle.NONE)
	button_arrow=Gtk.Button()                    # Down arrow
	button_arrow.set_relief(Gtk.ReliefStyle.NONE)
	img_arrow=Gtk.Image.new_from_icon_name('pan-down-symbolic',Gtk.IconSize.BUTTON)
	revealed=False                               # Whether Gtk.Revealer is open or not.

	def __init__(self,uuid):

		Budgie.Applet.__init__(self)
		self.initUI()

	def initUI(self):

		self.popover = Budgie.Popover.new(self.box)
		self.img = Gtk.Image.new_from_icon_name("budgie-restart", Gtk.IconSize.BUTTON)
		self.button_panel = Gtk.Button(label='Restart Panel')
		self.button_wm = Gtk.Button(label='Restart WM')
		seperator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
		self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)         # To store the Reset(Both) button and arrow
		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)           # Main VBox
		self.vbox_buttons = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)   # Vbox inside revealer

		self.box.set_tooltip_text("Restart Budgie Desktop")
		self.box.add(self.img)
		self.box.connect("button-press-event", self.on_press)

		self.add(self.box)

		self.button_panel.set_relief(Gtk.ReliefStyle.NONE)
		self.button_wm.set_relief(Gtk.ReliefStyle.NONE)
		self.button_wm.connect("clicked",self.restart,False,True)
		self.button_panel.connect("clicked",self.restart,True,False)
		self.vbox_buttons.pack_start(self.button_panel,False,False,0)
		self.vbox_buttons.pack_start(self.button_wm,False,False,0)


		self.button.set_label("Restart Desktop")
		self.button.connect("clicked",self.restart,True,True)
		self.hbox.pack_start(self.button,True,False,5)
		self.hbox.pack_start(seperator,True,False,0)
		self.hbox.pack_end(self.button_arrow,False,False,5)

		self.button_arrow.set_image(self.img_arrow)
		self.button_arrow.connect("clicked",self.revealer_show)


		self.revealer.set_reveal_child(False)
		self.revealer.add(self.vbox_buttons)

		self.vbox.pack_start(self.hbox,False,False,5)
		self.vbox.pack_start(self.revealer,False,False,0)

		self.popover.add(self.vbox)

		self.popover.get_child().show_all()

		self.box.show_all()

		self.show_all()



	def	on_press(self, box, e):

		if e.button != 1:
			return Gdk.EVENT_PROPAGATE

		if self.popover.get_visible():
			self.revealer.set_visible(False)

		else:
			self.revealer.set_reveal_child(False)                                       # Close Revealer (if open) before showing popover
			self.img_arrow.set_from_icon_name('pan-down-symbolic',Gtk.IconSize.BUTTON)  # Reset to pan-down icon
			self.manager.show_popover(self.box)

	def do_update_popovers(self, manager):

		self.manager = manager
		self.manager.register_popover(self.box, self.popover)

	def change_icon(self):
		""" Change arrow to down/up """

		if not self.revealed:
			self.img_arrow.set_from_icon_name('pan-up-symbolic',Gtk.IconSize.BUTTON)
			self.revealed=True

		else:
			self.img_arrow.set_from_icon_name('pan-down-symbolic',Gtk.IconSize.BUTTON)
			self.revealed=False

	def revealer_show(self,button):
		""" Open/Close the revealer """

		if self.revealer.get_reveal_child():
			self.change_icon()
			self.revealer.set_reveal_child(False)

		else:
			self.change_icon()
			self.revealer.set_reveal_child(True)


	def restart(self,button,panel,wm):
		""" Restart the panel,WM or both """

		try:
			if wm:
				subprocess.Popen(['nohup','budgie-wm', '--replace','&'])

			if panel:
				subprocess.Popen(['nohup','budgie-panel', '--replace','&'])

		except subprocess.CalledProcessError:                                  # Notify user about error on running restart commands.
			subprocess.Popen(['notify-send','Budgie Restart: Error !','-i','budgie-desktop-symbolic'])

#END
