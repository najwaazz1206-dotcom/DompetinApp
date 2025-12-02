from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from components import RoundedButton

Builder.load_string("""
<AkunContent>:
    orientation: 'vertical'
    padding: [30, 20]
    spacing: 20
    canvas.before:
        Color:
            rgba: 0.97, 0.93, 0.86, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: "140dp"
        spacing: 10
        Image:
            source: 'Asset/wallet_logo.png'
            size_hint_x: None
            width: '140dp'
        Label:
            text: "Akun"
            font_size: "32sp"
            bold: True
            color: 0,0,0,1
            halign: 'left'
            valign: 'middle'
            text_size: self.size

    Label:
        text: "Informasi Akun"
        bold: True
        color: 0,0,0,1
        font_size: '18sp'
        size_hint_y: None
        height: 40

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: '100dp'
        padding: 10
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [10,]
        
        Label:
            text: 'Username'
            color: 0.5, 0.5, 0.5, 1
            font_size: '12sp'
        Label:
            id: lbl_username
            text: '---'
            color: 0,0,0,1
            font_size: '20sp'
            bold: True

    RoundedButton:
        text: 'Log out'
        bg_color: [0.9, 0.3, 0.23, 1]
        size_hint_y: None
        height: '50dp'
        on_release: app.logout()

    Widget:
""")

class AkunContent(BoxLayout):
    def load_info(self):
        self.ids.lbl_username.text = App.get_running_app().username