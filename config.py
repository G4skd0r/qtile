# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ---------IMPORTS---------------------

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, extension, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy

import iwlib

# For the "Fn" keys
from libqtile.dgroups import simple_key_binder

from libqtile.log_utils import logger

import platform
import sys

# -----------CONFIG--------------------

mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(),desc="Toggle to the previous layout"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),



    ## Open my Software
    Key([mod], "t", lazy.spawn("telegram")),
    Key([mod], "a", lazy.spawn("atom")),
    Key([mod], "s", lazy.spawn("spotify")),
    Key([mod], "f", lazy.spawn("firefox")),

    ### Dmenu
     Key([mod], "d", lazy.run_extension(extension.DmenuRun(
        dmenu_prompt=">",
        font="Hack",
        fontsize="12",
        background="#15181a",
        foreground="#f6f6f6",
        selected_background="#7ac5cd",
        selected_foreground="#243b3d",
    ))),

    ## Sound Keys

    ### Raise/Lower Volumen
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute")),

    ### Stop, Next and Previous XF86AudioLowerVolume
    Key([], "XF86AudioPlay", lazy.function("playpause")),
    # Key([], "XF86AudioNext", lazy.function(next_prev("next"))),
    # Key([], "XF86AudioPrev", lazy.function(next_prev("prev"))),


    ## Brightness Keys

    Key([], "XF86KbdBrightnessUp", lazy.spawn("maclight keyboard up")),
    Key([], "XF86KbdBrightnessDown", lazy.spawn("maclight keyboard down")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("maclight screen up")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("maclight screen down")),

    ## Layouts

    ### MonadTall
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),



]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),

        # # mod1 + shift + letter of group = move focused window to group
        Key([mod, "control","shift"], i.name, lazy.window.togroup(i.name),
            desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(
    border_focus="#7ac5cd",
    border_normal="#15181a",
    margin=5,
    name="master",
    single_border_width=1,
    single_margin=5
    ),
    layout.Max(
    border_focus="#7ac5cd",
    border_normal="#15181a"
    ),
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Hack',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                "",
                font = "FontAwesome",
                fontsize = "14",
                foreground = "#7ac5cd"
                ),
                widget.GroupBox(font='Hack',
                active='#7ac5cd',
                inactive='#bfbfbf'
                ),
                widget.Prompt(),
                widget.WindowName(),
                widget.CurrentLayout(padding='3'),
                # hours
                widget.Clock(
                format='%H:%M',
                font='Hack',
                fontsize='14',
                ),
                # days
                widget.Clock(
                format='%d-%m-%Y',
                font="Hack",
                fontsize="14",
                ),
                #widget.Notify(),
                widget.BatteryIcon(),
                widget.Volume(),
                widget.Wlan(
                disconnected_message='睊',
                fontsize='14'
                ),
                widget.QuickExit(
                font='FontAwesome',
                default_text='' #Power-off Icon
                ),
            ],
            24,
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# -------- FUNCTIONS ---------
# last_playing = 'spotify'
#
# def playpause(qtile):
#     global last_playing
#     if qtile.widgetMap['clementine'].is_playing() or last_playing == 'clementine':
#         qtile.cmd_spawn("clementine --play-pause")
#         last_playing = 'clementine'
#     if qtile.widgetMap['spotify'].is_playing or last_playing == 'spotify':
#         qtile.cmd_spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")
#         last_playing = 'spotify'
#
# def next_prev(state):
#     def f(qtile):
#         if qtile.widgetMap['clementine'].is_playing():
#             qtile.cmd_spawn("clementine --%s" % state)
#         if qtile.widgetMap['spotify'].is_playing:
#             cmd = "Next" if state == "next" else "Previous"
#             qtile.cmd_spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.%s" % cmd)
#     return f




# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
