import gi
import uinput
import time
import os
import configparser


gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, GtkLayerShell


def get_desktop_environment():
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "")
    if desktop_env:
        return desktop_env.upper()
    return ""


DESKTOP_ENV = get_desktop_environment()


def _desktop_tokens():
    return {token for token in DESKTOP_ENV.split(":") if token}


def is_gnome_environment():
    desktop_tokens = _desktop_tokens()
    session_hint = " ".join(
        filter(
            None,
            [
                DESKTOP_ENV,
                os.environ.get("DESKTOP_SESSION", ""),
                os.environ.get("GNOME_DESKTOP_SESSION_ID", ""),
            ],
        )
    ).upper()
    return "GNOME" in desktop_tokens or "GNOME" in session_hint


def is_kde_environment():
    session_hint = " ".join(
        filter(
            None,
            [
                DESKTOP_ENV,
                os.environ.get("DESKTOP_SESSION", ""),
                os.environ.get("KDE_FULL_SESSION", ""),
            ],
        )
    ).upper()
    return "KDE" in session_hint or "PLASMA" in session_hint


def is_wayland_session():
    session_type = os.environ.get("XDG_SESSION_TYPE", "").upper()
    if session_type == "WAYLAND":
        return True
    return bool(os.environ.get("WAYLAND_DISPLAY"))


def configure_gdk_backend():
    if os.environ.get("GDK_BACKEND"):
        return
    if is_gnome_environment() and is_wayland_session():
        os.environ["GDK_BACKEND"] = "x11"


def get_data_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def install_kwin_rule_if_needed():
    if not is_kde_environment():
        return

    local_script = os.path.join(get_data_root(), "scripts", "install-kwin-rule.sh")
    for script_path in (
        local_script,
        "/usr/share/vboard/scripts/install-kwin-rule.sh",
        "./scripts/install-kwin-rule.sh",
    ):
        if os.path.isfile(script_path):
            try:
                subprocess.run(["bash", script_path], check=False)
            except OSError as exc:
                print(f"Warning: Could not run {script_path}: {exc}")
            return

    print("Warning: Could not find a KWin rule installer script.")

# from .environment import configure_gdk_backend

# configure_gdk_backend()

# os.environ['GDK_BACKEND'] = 'x11'

# if os.environ.get("GDK_BACKEND"):
#     return
# if is_gnome_environment() and is_wayland_session():
#     os.environ["GDK_BACKEND"] = "x11"

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib


key_mapping = {uinput.KEY_ESC: "Esc", uinput.KEY_1: "1", uinput.KEY_2: "2", uinput.KEY_3: "3", uinput.KEY_4: "4", uinput.KEY_5: "5", uinput.KEY_6: "6",
    uinput.KEY_7: "7", uinput.KEY_8: "8", uinput.KEY_9: "9", uinput.KEY_0: "0", uinput.KEY_MINUS: "-", uinput.KEY_EQUAL: "=",
    uinput.KEY_BACKSPACE: "Backspace", uinput.KEY_TAB: "Tab", uinput.KEY_Q: "Q", uinput.KEY_W: "W", uinput.KEY_E: "E", uinput.KEY_R: "R",
    uinput.KEY_T: "T", uinput.KEY_Y: "Y", uinput.KEY_U: "U", uinput.KEY_I: "I", uinput.KEY_O: "O", uinput.KEY_P: "P",
    uinput.KEY_LEFTBRACE: "[", uinput.KEY_RIGHTBRACE: "]", uinput.KEY_ENTER: "Enter", uinput.KEY_LEFTCTRL: "Ctrl_L", uinput.KEY_A: "A",
    uinput.KEY_S: "S", uinput.KEY_D: "D", uinput.KEY_F: "F", uinput.KEY_G: "G", uinput.KEY_H: "H", uinput.KEY_J: "J", uinput.KEY_K: "K",
    uinput.KEY_L: "L", uinput.KEY_SEMICOLON: ";", uinput.KEY_APOSTROPHE: "'", uinput.KEY_GRAVE: "`", uinput.KEY_LEFTSHIFT: "Shift_L",
    uinput.KEY_BACKSLASH: "\\", uinput.KEY_Z: "Z", uinput.KEY_X: "X", uinput.KEY_C: "C", uinput.KEY_V: "V", uinput.KEY_B: "B",
    uinput.KEY_N: "N", uinput.KEY_M: "M", uinput.KEY_COMMA: ",", uinput.KEY_DOT: ".", uinput.KEY_SLASH: "/", uinput.KEY_RIGHTSHIFT: "Shift_R",
    uinput.KEY_KPENTER: "Enter", uinput.KEY_LEFTALT: "Alt_L", uinput.KEY_RIGHTALT: "Alt_R", uinput.KEY_SPACE: "Space", uinput.KEY_CAPSLOCK: "CapsLock",
    uinput.KEY_F1: "F1", uinput.KEY_F2: "F2", uinput.KEY_F3: "F3", uinput.KEY_F4: "F4", uinput.KEY_F5: "F5", uinput.KEY_F6: "F6",
    uinput.KEY_F7: "F7", uinput.KEY_F8: "F8", uinput.KEY_F9: "F9", uinput.KEY_F10: "F10", uinput.KEY_F11: "F11", uinput.KEY_F12: "F12",
    uinput.KEY_SCROLLLOCK: "ScrollLock", uinput.KEY_PAUSE: "Pause", uinput.KEY_INSERT: "Insert", uinput.KEY_HOME: "Home",
    uinput.KEY_PAGEUP: "PageUp", uinput.KEY_DELETE: "Delete", uinput.KEY_END: "End", uinput.KEY_PAGEDOWN: "PageDown",
    uinput.KEY_RIGHT: "→", uinput.KEY_LEFT: "←", uinput.KEY_DOWN: "↓", uinput.KEY_UP: "↑", uinput.KEY_NUMLOCK: "NumLock",
    uinput.KEY_RIGHTCTRL: "Ctrl_R", uinput.KEY_LEFTMETA:"Super_L", uinput.KEY_RIGHTMETA:"Super_R"}

class VirtualKeyboard(Gtk.Window):
    def __init__(self):
        super().__init__(title="Virtual Keyboard", name="toplevel")



        


        self.set_border_width(0)
        self.set_resizable(True)
        self.set_keep_above(True)
        self.set_modal(False)
        self.set_focus_on_map(False)
        self.set_can_focus(False)
        self.set_accept_focus(False)
        # self.width=0
        # self.width=150
        # self.height=0
        self.height=150

        self.CONFIG_DIR = os.path.expanduser("~/.config/vboard")
        self.CONFIG_FILE = os.path.join(self.CONFIG_DIR, "settings.conf")
        self.config = configparser.ConfigParser()

        self.bg_color = "0, 0, 0"  # background color
        self.opacity="0.90"
        self.text_color="white"
        self.read_settings()

        self.modifiers = {
            uinput.KEY_LEFTSHIFT: False,
            uinput.KEY_RIGHTSHIFT: False,
            uinput.KEY_LEFTCTRL: False,
            uinput.KEY_RIGHTCTRL: False,
            uinput.KEY_LEFTALT: False,
            uinput.KEY_RIGHTALT: False,
            uinput.KEY_LEFTMETA: False,
            uinput.KEY_RIGHTMETA: False
        }
        self.colors = [
            ("Black", "0,0,0"),
            ("Red", "255,0,0"),
            ("Pink", "255,105,183"),
            ("White", "255,255,255"),
            ("Green", "0,255,0"),
            ("Blue", "0,0,110"),
            ("Gray", "128,128,128"),
            ("Dark Gray", "64,64,64"),
            ("Orange", "255,165,0"),
            ("Yellow", "255,255,0"),
            ("Purple", "128,0,128"),
            ("Cyan", "0,255,255"),
            ("Teal", "0,128,128"),
            ("Brown", "139,69,19"),
            ("Gold", "255,215,0"),
            ("Silver", "192,192,192"),
            ("Turquoise", "64,224,208"),
            ("Magenta", "255,0,255"),
            ("Olive", "128,128,0"),
            ("Maroon", "128,0,0"),
            ("Indigo", "75,0,130"),
            ("Beige", "245,245,220"),
            ("Lavender", "230,230,250")

        ]
        # if (self.width!=0):
        #     self.set_default_size(self.width, self.height)


        # 1. Initialize the window as a layer surface before it is realized
        GtkLayerShell.init_for_window(self)
        
        # 2. Set the layer (BOTTOM or TOP for docks/panels)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        
        # 3. Anchor the window to specific edges (e.g., Bottom, Left, Right creates a bottom panel)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        
        # 4. Force other windows to dodge your dock (reserve screen space)
        # Setting this to the height of your panel prevents windows from overlapping it
        # GtkLayerShell.set_exclusive_zone(self, self.height)
        GtkLayerShell.set_exclusive_zone(self, 50)
        
        # Optional: Select a specific monitor automatically without manual X11 math
        # If left unset, Wayland defaults to the monitor where the pointer is or the primary display
        # display = Gdk.Display.get_default()
        # monitor = display.get_monitor(0) # Get first monitor safely
        # GtkLayerShell.set_monitor(self, monitor)

        # Standard GTK layout setup
        # self.set_default_size(-1, self.height) # Width auto-fills due to anchors, height fixed to 50
        self.set_default_size(-1, self.height) # Width auto-fills due to anchors, height fixed to 50
        # self.set_default_size(200, self.height) # Width auto-fills due to anchors, height fixed to 50
        
        # label = Gtk.Label(label="My Wayland Dock Panel")
        # self.add(label)
        # self.connect("destroy", Gtk.main_quit)
        # self.show_all()


        # # 1. Geometry and Position (e.g., bottom of screen)
        # screen = self.get_screen()
        # active_win = screen.get_active_window()

        # if active_win is not None:
        #     monitor_num = screen.get_monitor_at_window(active_win)
        # else:
        #     # Fallback to the primary monitor or handle the missing window gracefully
        #     monitor_num = 0 
        # # monitor_num = screen.get_monitor_at_window(screen.get_active_window())
        # monitor_geometry = screen.get_monitor_geometry(monitor_num)
        # self.set_default_size(monitor_geometry.width, 200) # Width of screen, 40px tall
        # self.move(monitor_geometry.x, monitor_geometry.y + monitor_geometry.height - 200)


        # # 2. Window Type & Decorations
        # self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        # self.set_decorated(False)
        
        # 3. Focus settings
        # self.set_accept_focus(False)
        # self.set_skip_taskbar_hint(True)
        # self.set_skip_pager_hint(True)
        

        # self.header = Gtk.HeaderBar()
        # self.header.set_show_close_button(True)
        self.buttons=[]
        self.modifier_buttons={}
        self.row_buttons=[]
        self.color_combobox = Gtk.ComboBoxText()
        # Set the header bar as the titlebar of the window
        # self.set_titlebar(self.header)
        self.set_default_icon_name("preferences-desktop-keyboard") 
        # self.header.set_decoration_layout(":minimize,maximize,close")

        # self.create_settings()

        grid = Gtk.Grid()  # Use Grid for layout
        grid.set_row_homogeneous(True)  # Allow rows to resize based on content
        grid.set_column_homogeneous(True)  # Columns are homogeneous
        grid.set_margin_start(3)
        grid.set_margin_end(3)
        grid.set_name("grid")
        self.add(grid)
        self.apply_css()
        self.device = uinput.Device(list(key_mapping.keys()))

        # Define rows for keys
        rows = [
            # ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Delete" ],
            # ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace", "Home" ],
            # ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\", "PageUp"],
            # ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter", "PageDown"],
            # ["Shift_L", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift_R", "↑"],
            # ["Ctrl_L","Super_L", "Alt_L", "Space", "Alt_R", "Super_R", "Ctrl_R", "←", "→", "↓"]
            # ["Shift_L", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "↑", "Shift_R", "End"],
            # ["Ctrl_L","Super_L", "Alt_L", "Space", "Alt_R", "Super_R", "Ctrl_R", "←", "↓", "→"]
            # ["Esc", "Tab",  "/", "-", "PageUp", "Home",  "End"],
            # ["Esc", "Super_L",  "Space",  "←","↑", "↓", "→", "Enter"]
            [  "Space","K",  "J",  "L", "H",";", "M","-","=", "C","S",  "Esc", "←", "→","↑", "↓", "Enter"]
            # ["Esc", "Ctrl_L","Super_L", "Alt_L",  "Alt_R", "Super_R", "Ctrl_R", "Home", "PageUp", "PageDown", "End", "←", "↑", "↓", "→"]
        ]

        # Create each row and add it to the grid
        for row_index, keys in enumerate(rows):
            self.create_row(grid, row_index, keys)


    def create_settings(self):
        self.create_button("☰", self.change_visibility,callbacks=1)
        self.create_button("+", self.change_opacity,True,2)
        self.create_button("-", self.change_opacity, False,2)
        self.create_button( f"{self.opacity}")
        self.color_combobox.append_text("Change Background")
        self.color_combobox.set_active(0)
        self.color_combobox.connect("changed", self.change_color)
        self.color_combobox.set_name("combobox")
        self.header.add(self.color_combobox)


        for label, color in self.colors:
            self.color_combobox.append_text(label)

    def on_resize(self, widget, event):
        self.width, self.height = self.get_size()  # Get the current size after resize
        GtkLayerShell.set_exclusive_zone(self, self.height)



    def create_button(self, label_="", callback=None, callback2=None, callbacks=0):
        button= Gtk.Button(label=label_)
        button.set_name("headbar-button")
        if callbacks==1:
            button.connect("clicked", callback)
        elif callbacks==2:
            button.connect("clicked", callback, callback2)

        if label_==self.opacity:
            self.opacity_btn=button
            self.opacity_btn.set_tooltip_text("opacity")

        self.header.add(button)
        self.buttons.append(button)

    def change_visibility(self, widget=None):
        for button in self.buttons:
            if button.get_label()!="☰":
                button.set_visible(not button.get_visible())
        self.color_combobox.set_visible(not self.color_combobox.get_visible() )

    def change_color (self, widget):
        label=self.color_combobox.get_active_text()
        for label_ , color_ in self.colors:
            if label_==label:
                self.bg_color = color_

        if (self.bg_color in {"255,255,255" ,"0,255,0" , "255,255,0", "245,245,220", "230,230,250", "255,215,0"}):
            self.text_color="#1C1C1C"
        else:
            self.text_color="white"
        self.apply_css()


    def change_opacity(self,widget, boolean):
        if (boolean):
            self.opacity = str(round(min(1.0, float(self.opacity) + 0.01),2))
        else:
            self.opacity = str(round(max(0.0, float(self.opacity) - 0.01),2))
        self.opacity_btn.set_label(f"{self.opacity}")
        self.apply_css()
    def apply_css (self):
        provider = Gtk.CssProvider()


        css = f"""
        headerbar {{
            background-color: rgba({self.bg_color}, {self.opacity});
            border: 0px;
            box-shadow: none;

        }}

        headerbar button{{
            min-width: 40px;
            padding: 0px;
            border: 0px;
            margin: 0px;
        }}

        headerbar .titlebutton {{
            min-width: 50px;  /* Set custom min-width for the close button */
            min-height: 40px
        }}

        headerbar button label{{
        color: {self.text_color};

        }}

        #headbar-button, #combobox button.combo {{
            background-image: none;
        }}

        #toplevel {{
            background-color: rgba({self.bg_color}, {self.opacity});




        }}

        #grid button label{{
            color: {self.text_color};
            font-size: 18px;


        }}

        #grid button {{
                    border: none;
                    background-image: none;
                    padding: 0px;
                    margin: 2px;
            min-height: 42px;
            /*min-height: 72px;*/

                }}
        #grid button.functionrow {{
            min-height: 32px;
            background-color: #111111;

                }}

        button {{
            background-color: transparent;
            background-color: #222222;
            color:{self.text_color};

        }}

       #grid button:hover {{
                    background-color: #004444;
            border: 1px solid #00CACB;
                    border: none; 
        }}

       #grid button.pressed,
       #grid button.pressed:hover {{
            border: 1px solid {self.text_color};
                    border: none; 
                    background-color: #008888;
        }}

       tooltip {{
            color: white;
            padding: 5px;
        }}

       #combobox button.combo  {{

            color: {self.text_color};
            padding: 5px;
        }}


        """


        try:
            provider.load_from_data(css.encode("utf-8"))
        except GLib.GError as e:
            print(f"CSS Error: {e.message}")
        Gtk.StyleContext.add_provider_for_screen(self.get_screen(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def create_row(self, grid, row_index, keys):
        col = 0  # Start from the first column
        width=0


        for key_label in keys:
            key_event = next((key for key, label in key_mapping.items() if label == key_label), None)
            if key_event:

                if key_label in ("Shift_R", "Shift_L", "Alt_L", "Alt_R", "Ctrl_L", "Ctrl_R", "Super_L", "Super_R"):
                    button = Gtk.Button(label=key_label[:-2])
                else:
                    button = Gtk.Button(label=key_label)
  

                if key_label == "CapsLock":
                    button = Gtk.Button(label="⇪")

                if key_label in ("Shift_R", "Shift_L", "Shift"):
                    button = Gtk.Button(label="⇧")
                if key_label in ("Alt_L", "Alt_R", "Alt"):
                    button = Gtk.Button(label="⌥")
                if key_label in ("Ctrl_L", "Ctrl_R", "Ctrl"):
                    button = Gtk.Button(label="^")

                if key_label == "Space":
                    button = Gtk.Button(label="⏯")

                if key_label == "H":
                    button = Gtk.Button(label="⏮")
                if key_label == "K":
                    button = Gtk.Button(label="⏸")
                if key_label == "J":
                    button = Gtk.Button(label="⏪︎")
                if key_label == "L":
                    button = Gtk.Button(label="⏩︎")
                if key_label == ";":
                    button = Gtk.Button(label="⏭")
                if key_label == "S":
                    # button = Gtk.Button(label="⌕")
                    button = Gtk.Button(label="🔍︎")
                    # button = Gtk.Button(label="🔎︎")
# 🔎
# 🔉︎
# 🔎︎
# 🔍︎
                if key_label == "C":
                    # button = Gtk.Button(label="ᴄᴄ")
                    button = Gtk.Button(label="cc")
                    # button = Gtk.Button(label="ᑦᑦ")
                    # button = Gtk.Button(label="ᑕᑕ")

                if key_label == "Esc":
                    # button = Gtk.Button(label="↩")
                    # button = Gtk.Button(label="⬅×")
                    button = Gtk.Button(label="ʙᴀᴄᴋ")


                    # button = Gtk.Button(label="🔙")
                    # 🔉🔈︎

                if key_label == "M":
                    # button = Gtk.Button(label="&#xFE0E;&#x1F507;🔇")
                    # button = Gtk.Button(label="🔇")
                    button = Gtk.Button(label="🔇︎")
                if key_label == "-":
                    # button = Gtk.Button(label="🔉")
                    button = Gtk.Button(label="🔈︎-")
                if key_label == "=":
                    # button = Gtk.Button(label="🔉")
                    button = Gtk.Button(label="🔉︎+")

                    


                if key_label == "Tab":
                    button = Gtk.Button(label="↹")
                if key_label == "PageUp":
                    button = Gtk.Button(label="⎗")
                if key_label =="PageDown":
                    button = Gtk.Button(label="⎘")
                if key_label == "Home":
                    button = Gtk.Button(label="⇱")
                if key_label == "End":
                    button = Gtk.Button(label="⇲")
                if key_label == "Backspace":
                    button = Gtk.Button(label="⌫")
                # if key_label in ("Delete"):
                if key_label == "Delete":
                    button = Gtk.Button(label="⌦")
                    
                # if key_label in ("Enter"):
                if key_label == "Enter":
                    button = Gtk.Button(label="sᴇʟᴇᴄᴛ")
                    # button = Gtk.Button(label="⏎")

                    

 
                if key_label in ("Super_L", "Super_R"):
                    button = Gtk.Button(label="⌘")
                    

                self.modifier_toggle_enable = True;
                # self.modifier_toggle_enable = False;

                button.connect("pressed", self.on_button_press, key_event)
                button.connect("released", self.on_button_release, key_event)
                button.connect("leave-notify-event", self.on_button_release, key_event)
                self.row_buttons.append(button)
                if key_event in self.modifiers:
                    self.modifier_buttons[key_event] = button
                #functionrow
                if key_label == "Space": width=5
                elif key_label == "Esc": width=5
                elif key_label == "Enter": width=5
                # elif key_label == "Esc": width=5
                # elif key_label == "Tab": width=5
                # elif key_label == "CapsLock": width=6
                # elif key_label == "Shift_R" : width=5
                # elif key_label == "Shift_L" : width=8
                # elif key_label == "Backspace": width=6
                # elif key_label == "`": width=3
                # elif key_label == "\\" : width=4
                # elif key_label == "Enter": width=7
                else: width=4

                style_context = button.get_style_context()
                if key_label in ("Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Delete" ):
                    style_context.add_class('functionrow')

                grid.attach(button, col, row_index, width, 1)
                # if key_label == "Esc": col += 10

                col += width  # Skip 4 columns for the space button

    def update_label(self, show_symbols):
        # button_positions = [(0, "` ~"), (1, "1 !"), (2, "2 @"), (3, "3 #"), (4, "4 $"), (5, "5 %"), (6, "6 ^"), (7, "7 &"), (8, "8 *"), (9, "9 ("), (10, "0 )")
        # , (11, "- _"), (12, "= +"),(25,"[ {"), (26,"] }"), (27,"\\ |"), (38, "; :"), (39, "' \""), (49, ", <"), (50, ". >"), (51, "/ ?")]

        button_positions = [(0, "` ~"), (1, "1 !"), (2, "2 @"), (3, "3 #"), (4, "4 $"), (5, "5 %"), (6, "6 ^"), (7, "7 &"), (8, "8 *"), (9, "9 ("), (10, "0 )")
        , (11, "- _"), (12, "= +"),(26,"[ {"), (27,"] }"), (28,"\\ |"), (40, "; :"), (41, "' \""), (52, ", <"), (53, ". >"), (54, "/ ?")]

        # for pos, label in button_positions:
        #     label_parts = label.split()  
        #     if show_symbols:
        #         self.row_buttons[pos+14].set_label(label_parts[1])
        #     else:
        #         self.row_buttons[pos+14].set_label(label_parts[0])

    def update_modifier(self, key_event, value):
      self.modifiers[key_event] = value
      button = self.modifier_buttons[key_event]
      style_context = button.get_style_context()
      if (value):
          style_context.add_class('pressed')
          # style_context.add_class('functionrow')

      else:
          style_context.remove_class('pressed')
          # style_context.remove_class('functionrow')

    def on_button_press(self, widget, key_event):
        # If it's a modifier, toggle state (like Shift, Ctrl, etc.)
        if key_event in self.modifiers:
            if self.modifier_toggle_enable:
                self.update_modifier(key_event, not self.modifiers[key_event])
            else:
                self.update_modifier(key_event, True)

            # prevent both shifts being active at once
            if self.modifiers[uinput.KEY_LEFTSHIFT] and self.modifiers[uinput.KEY_RIGHTSHIFT]:
                self.update_modifier(uinput.KEY_LEFTSHIFT, False)
                self.update_modifier(uinput.KEY_RIGHTSHIFT, False)

            # update label state (caps-like effect)
            if self.modifiers[uinput.KEY_LEFTSHIFT] or self.modifiers[uinput.KEY_RIGHTSHIFT]:
                self.update_label(True)
            else:
                self.update_label(False)
            return  # modifiers don’t repeat

        # Fire key once immediately
        self.emit_key(key_event)

        # Start a one-time delay before repeat kicks in (e.g. 400ms)
        self.delay_source = GLib.timeout_add(400, self.start_repeat, key_event)

    def on_button_release(self, widget, key_event, *args):
        if key_event in self.modifiers:

            if self.modifier_toggle_enable:
                return;
            else:
                self.update_modifier(key_event, False)
        # Cancel both delay and repeat when released
        if hasattr(self, "delay_source"):
            GLib.source_remove(self.delay_source)
            del self.delay_source
        if hasattr(self, "repeat_source"):
            GLib.source_remove(self.repeat_source)
            del self.repeat_source

    def start_repeat(self, key_event):
        # After the delay, start the repeat loop
        self.repeat_source = GLib.timeout_add(100, self.repeat_key, key_event)
        return False  # stop this one-time delay timer

    def repeat_key(self, key_event):
        self.emit_key(key_event)
        return True  # keep repeating

    def emit_key(self, key_event):
        # Apply active modifiers
        for mod_key, active in self.modifiers.items():
            if active:
                self.device.emit(mod_key, 1)

        # Emit the key
        self.device.emit(key_event, 1)
        self.device.emit(key_event, 0)
        self.update_label(False)
        # Release modifiers (so they only act as held while sending this key)
        for mod_key, active in self.modifiers.items():
            if active:
                self.device.emit(mod_key, 0)
                self.update_modifier(mod_key, False)

    def read_settings(self):
        # Ensure the config directory exists
        try:
            os.makedirs(self.CONFIG_DIR, exist_ok=True)
        except PermissionError:
            print("Warning: No permission to create the config directory. Proceeding without it.")

        try:
            if os.path.exists(self.CONFIG_FILE):
                self.config.read(self.CONFIG_FILE)
                self.bg_color = self.config.get("DEFAULT", "bg_color" )
                self.opacity = self.config.get("DEFAULT", "opacity" )
                self.text_color = self.config.get("DEFAULT", "text_color", fallback="white" )
                self.width=self.config.getint("DEFAULT", "width" , fallback=0)
                self.height=self.config.getint("DEFAULT", "height", fallback=0)
                print(f"rgba: {self.bg_color}, {self.opacity}")

        except configparser.Error as e:
            print(f"Warning: Could not read config file ({e}). Using default values.")



    def save_settings(self):

        self.config["DEFAULT"] = {"bg_color": self.bg_color, "opacity": self.opacity, "text_color": self.text_color, "width": self.width, "height": self.height}

        try:
            with open(self.CONFIG_FILE, "w") as configfile:
                self.config.write(configfile)

        except (configparser.Error, IOError) as e:
            print(f"Warning: Could not write to config file ({e}). Changes will not be saved.")


if __name__ == "__main__":
    win = VirtualKeyboard()
    win.connect("destroy", Gtk.main_quit)
    win.connect("destroy", lambda w: win.save_settings())
    win.show_all()
    win.connect("configure-event", win.on_resize)
    win.change_visibility()
    Gtk.main()
