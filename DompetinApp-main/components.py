from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.lang import Builder
from kivy.app import App
from kivy.utils import get_color_from_hex

# --- Style Global untuk Components ---
Builder.load_string("""
<RoundedInput>:
    orientation: 'vertical'
    size_hint_y: None
    height: '50dp'
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [15,]
        Color:
            rgba: 0.8, 0.8, 0.8, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 15)
            width: 1
    TextInput:
        id: ti
        hint_text: root.hint_text
        text: root.text
        # Mengambil value boolean dari list property agar aman
        password: root.password
        input_filter: root.input_filter
        background_color: 0,0,0,0
        foreground_color: 0,0,0,1
        cursor_color: 0,0,0,1
        padding: [15, 15, 15, 10] 
        multiline: False
        on_text: root.text = self.text

<RoundedButton>:
    background_normal: ''
    background_color: 0,0,0,0
    color: 1, 1, 1, 1
    bold: True
    canvas.before:
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]

<NavButton>:
    orientation: 'vertical'
    on_release: app.change_screen(root.text)
    canvas.before:
        Color:
            rgba: 0,0,0,0 
        Rectangle:
            pos: self.pos
            size: self.size
            
    Label:
        text: root.icon_text
        font_size: '20sp'
        bold: True
        # Logika warna: Gunakan index [0] jika is_active berupa list
        color: root.color_active if root.is_active[0] else root.color_inactive
        size_hint_y: 0.6
    Label:
        text: root.text
        font_size: '10sp'
        color: root.color_active if root.is_active[0] else root.color_inactive
        size_hint_y: 0.4
""")

class RoundedButton(Button):
    bg_color = ListProperty([0.2, 0.6, 0.8, 1])

class RoundedInput(BoxLayout):
    hint_text = StringProperty('')
    text = StringProperty('')
    password = BooleanProperty(False)
    input_filter = StringProperty(None, allownone=True)

class NavButton(ButtonBehavior, BoxLayout):
    text = StringProperty('')
    icon_text = StringProperty('')
    # Warna default (Biru vs Abu-abu)
    color_active = ListProperty([0.2, 0.6, 0.85, 1])  # Hex #3498db
    color_inactive = ListProperty([0.58, 0.64, 0.65, 1]) # Hex #95a5a6
    
    # Gunakan ListProperty untuk boolean agar kompatibel dengan KV binding yang kompleks
    is_active = ListProperty([False])