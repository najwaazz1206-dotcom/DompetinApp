from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from database import Database
from components import RoundedInput, RoundedButton  

KV = """
<LoginScreen>:
    name: 'login'

    canvas.before:
        Color:
            rgba: 0.98, 0.94, 0.85, 1   # Background cream
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        spacing: dp(20)

        # ===================== LOGO =========================
        BoxLayout:
            orientation: 'vertical'
            size_hint: None, None
            width: min(root.width * 0.5, dp(400))
            height: dp(140)
            pos_hint: {"center_x": 0.5}

        Image:
            source: "Asset/wallet_logo.png"
            size_hint_y: None
            height: dp(180)    
            allow_stretch: True
            keep_ratio: True


        Widget:

        # ============ CARD HIJAU UTAMA ======================
        BoxLayout:
            orientation: "vertical"
            size_hint: None, None
            width: min(root.width * 0.75, dp(520))
            height: dp(270)
            padding: dp(25)
            spacing: dp(18)
            pos_hint: {"center_x": 0.5}

            canvas.before:
                Color:
                    rgba: 0, 0.25, 0, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [25]

            Label:
                text: "Akun Dompetin"
                font_size: dp(22)
                bold: True
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(35)

            RoundedInput:
                id: user_input
                hint_text: "username"
                size_hint_y: None
                height: dp(45)

            RoundedInput:
                id: pass_input
                hint_text: "password"
                password: True
                size_hint_y: None
                height: dp(45)

            RoundedButton:
                text: "Login"
                size_hint_y: None
                height: dp(50)
                color: 0, 0.25, 0, 1
                bg_color: [0.8, 0.8, 0.8, 1]
                font_size: dp(18)
                on_release: root.do_login()

        Widget:
"""

Builder.load_string(KV)

class LoginScreen(Screen):
    def do_login(self):
        user = self.ids.user_input.text
        pwd = self.ids.pass_input.text

        if not user or not pwd:
            return

        db = Database()
        db.register_user(user, pwd)
        user_id = db.login_user(user, pwd)

        if user_id:
            app = App.get_running_app()
            app.user_id = user_id
            app.username = user
            app.root.current = 'main'

            if hasattr(app, 'main_screen'):
                app.main_screen.show_content('home')


class DompetApp(App):
    def build(self):
        return LoginScreen()


if __name__ == "__main__":
    DompetApp().run()
