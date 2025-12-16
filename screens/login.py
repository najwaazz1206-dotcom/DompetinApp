from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from database import Database
from components import RoundedInput, RoundedButton
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.properties import BooleanProperty


KV = """
<LoginRegisterScreen>:
    is_login: True

    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "Asset/cobabgawal2.png"

    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)

        Image:
            source: "Asset/logoawal.png"
            size_hint: (None, None)
            size: (dp(300), dp(170))
            pos_hint: {"center_x": 0.5}
            allow_stretch: True

        BoxLayout:
            id: form_area
            orientation: "vertical"
            size_hint: (None, None)
            width: min(root.width * 0.85, dp(380))
            height: self.minimum_height
            pos_hint: {"center_x": 0.5}
            padding: dp(30)
            spacing: dp(15)

            canvas.before:
                Color:
                    rgba: 1, 1, 1, 0.85
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [20,]

            Label:
                id: form_title
                text: "Masuk Akun" if root.is_login else "Daftar Akun"
                font_size: dp(22)
                bold: True
                color: 0.1, 0.3, 0.1, 1
                size_hint_y: None
                height: dp(30)

            RoundedInput:
                id: input_user
                hint_text: "Username"
                size_hint_y: None
                height: dp(48)
                multiline: False

            RoundedInput:
                id: input_pass
                hint_text: "Password"
                password: True
                size_hint_y: None
                height: dp(48)
                multiline: False

            RoundedButton:
                id: main_button
                text: "MASUK" if root.is_login else "DAFTAR"
                size_hint_y: None
                height: dp(50)
                bg_color: [0.1, 0.3, 0.1, 1]
                color: 1, 1, 1, 1
                bold: True
                on_release:
                    root.do_login() if root.is_login else root.do_register()

            Button:
                text: "Belum punya akun? Daftar" if root.is_login else "Sudah punya akun? Login"
                size_hint_y: None
                height: dp(35)
                background_color: (0,0,0,0)
                color: (0.2, 0.4, 0.2, 1)
                on_release: root.switch_form()
            
            Label:
                text: "developed by: Najwa|Syifa|Zaqia"
                font_size: dp(14)
                bold: True
                color: 0.1, 0.3, 0.1, 1
                size_hint_y: None
                height: dp(20)

"""

Builder.load_string(KV)


class LoginRegisterScreen(Screen):
    is_login = BooleanProperty(True)   # True = Login form, False = Register form

    def show_alert(self, message):
        Popup(
            title="Informasi",
            content=Label(text=message, color=(1, 0, 0, 1)),
            size_hint=(0.7, 0.3),
            auto_dismiss=True
        ).open()

    def switch_form(self):
        """Switch login <-> register"""
        self.is_login = not self.is_login

        # Reset input fields
        self.ids.input_user.text = ""
        self.ids.input_pass.text = ""

    def do_login(self):
        user = self.ids.input_user.text.strip()
        pwd = self.ids.input_pass.text.strip()

        if not user or not pwd:
            self.show_alert("Username dan password tidak boleh kosong.")
            return

        db = Database()
        user_id = db.login_user(user, pwd)

        if not user_id:
            self.show_alert("Username atau password salah!")
            return

        app = App.get_running_app()
        app.user_id = user_id
        app.username = user
        app.root.current = "main"

        if hasattr(app, 'main_screen'):
            app.main_screen.show_content('home')

    def do_register(self):
        user = self.ids.input_user.text.strip()
        pwd = self.ids.input_pass.text.strip()

        if not user or not pwd:
            self.show_alert("Username dan password wajib diisi.")
            return

        db = Database()
        success = db.register_user(user, pwd)

        if not success:
            self.show_alert("Username sudah digunakan!")
            return

        self.show_alert("Pendaftaran berhasil! Silakan login.")
        self.switch_form()
