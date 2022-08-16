# This file is part of Trackma.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from gi.repository import GObject, Gdk, Gtk

from trackma import utils


class TrackmaStatusIcon(Gtk.StatusIcon):
    __gtype_name__ = 'TrackmaStatusIcon'

    __gsignals__ = {
        'hide-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'about-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'quit-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
    }
    window = None

    def __init__(self, window=None):
        Gtk.StatusIcon.__init__(self)
        self.set_from_file(utils.DATADIR + '/icon.png')
        self.set_tooltip_text('Trackma GTK')
        self.connect('activate', self._tray_status_event)
        self.connect('popup-menu', self._tray_status_menu_event)
        self.window = window

    def _tray_status_event(self, _widget):
        self.emit('hide-clicked')

    @property
    def selected_show(self):
        if self.window:
            return self.window._main_view.get_selected_show()
        return None

    def _tray_status_menu_event(self, _icon, button, time):
        # Called when the tray icon is right-clicked
        menu = Gtk.Menu()
        mb_show = Gtk.MenuItem("Show/Hide")
        if self.window and self.selected_show:
            mb_play_next = Gtk.ImageMenuItem(
                'Play next', Gtk.Image.new_from_icon_name("media-seek-forward", Gtk.IconSize.MENU))
        if self.window:
            mb_play_random = Gtk.MenuItem("Play random episode")
        mb_about = Gtk.ImageMenuItem(
            'About', Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU))
        mb_quit = Gtk.ImageMenuItem('Quit', Gtk.Image.new_from_icon_name(
            "application-exit", Gtk.IconSize.MENU))

        if self.window and self.selected_show:
            mb_play_next.connect('activate',
                                 lambda *args: self.window._play_next(self.selected_show))
        if self.window:
            mb_play_random.connect('activate',
                                   lambda *args: self.window._play_random())
        mb_show.connect("activate", self._tray_status_event)
        mb_about.connect("activate", self._on_mb_about)
        mb_quit.connect("activate", self._on_mb_quit)

        menu.append(mb_show)
        if self.window and self.selected_show:
            menu.append(mb_play_next)
        if self.window:
            menu.append(mb_play_random)
        menu.append(mb_about)
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(mb_quit)
        menu.show_all()

        menu.popup(None, None, None, self._pos, button, time)

    def _on_mb_about(self, menu_item):
        self.emit('about-clicked')

    def _on_mb_quit(self, menu_item):
        self.emit('quit-clicked')

    @staticmethod
    def _pos(menu, icon):
        return Gtk.StatusIcon.position_menu(menu, icon)

    @staticmethod
    def is_tray_available():
        # Icon tray isn't available in Wayland
        return not Gdk.Display.get_default().get_name().lower().startswith('wayland')
