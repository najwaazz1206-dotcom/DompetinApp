from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from database import Database
from components import RoundedInput, RoundedButton  

KV = """
<LoginScreen>:
    name: 'login'

    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "Asset/cobabgawal2.png"

    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        # Spacer Atas
        Widget:
            size_hint_y: 0.15

        # --- LOGO ---
        Image:
            source: "Asset/logoawal.png"
            size_hint: (None, None)
            size: (dp(300), dp(170))
            pos_hint: {"center_x": 0.5}
            pos_spec_hint: {"center_y": 0.5}
            allow_stretch: True
            keep_ratio: True

        # --- KARTU LOGIN PUTIH ---
        BoxLayout:
            orientation: "vertical"
            size_hint: (None, None)
            width: min(root.width * 0.85, dp(380))
            height: self.minimum_height # Tinggi otomatis mengikuti isi
            pos_hint: {"center_x": 0.5}
            padding: dp(30)
            spacing: dp(15)

            # Background Kartu Putih + Shadow
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 0.1 # Shadow halus
                RoundedRectangle:
                    pos: self.x + dp(4), self.y - dp(4)
                    size: self.size
                    radius: [20,]
                Color:
                    rgba: 1, 1, 1, 1 # Warna Kartu Putih
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [20,]

            # Judul
            Label:
                text: "Masuk Akun"
                font_size: dp(22)
                bold: True
                color: 0.1, 0.3, 0.1, 1
                size_hint_y: None
                height: dp(30)

            # Input Username
            RoundedInput:
                id: user_input
                hint_text: "Username"
                size_hint_y: None
                height: dp(48)
                multiline: False

            # Input Password
            RoundedInput:
                id: pass_input
                hint_text: "Password"
                password: True
                size_hint_y: None
                height: dp(48)
                multiline: False

            # --- LINK LUPA PASSWORD (Rata Kanan) ---
            BoxLayout:
                size_hint_y: None
                height: dp(20)
                orientation: 'horizontal'
                
                Widget: # Spacer agar teks terdorong ke kanan
                
                Button:
                    text: "Lupa kata sandi?"
                    size_hint_x: None
                    width: dp(120)
                    font_size: dp(12)
                    color: 0.4, 0.4, 0.4, 1 # Abu-abu
                    background_normal: ''
                    background_color: 0, 0, 0, 0 # Transparan
                    on_release: print("Tombol Lupa Password ditekan") 
                    # Ganti print() di atas dengan navigasi screen, misal: root.manager.current = 'forgot_pass'

            # --- TOMBOL LOGIN ---
            RoundedButton:
                text: "MASUK"
                size_hint_y: None
                height: dp(50)
                font_size: dp(16)
                bold: True
                bg_color: [0.1, 0.3, 0.1, 1] 
                color: 1, 1, 1, 1 
                on_release: root.do_login()

            # Spacer pemisah antara tombol login dan daftar
            Widget:
                size_hint_y: None
                height: dp(10)

            # --- BAGIAN DAFTAR (Paling Bawah) ---
            BoxLayout:
                size_hint_y: None
                height: dp(30)
                orientation: 'horizontal'
                spacing: dp(5)
                # Agar posisi di tengah horizontal
                padding: [0, 0, 0, 0] 
                
                # Spacer kiri (untuk centering manual jika perlu, atau gunakan AnchorLayout)
                Widget: 

                Label:
                    text: "Belum punya akun?"
                    font_size: dp(12)
                    color: 0.5, 0.5, 0.5, 1
                    size_hint_x: None
                    width: self.texture_size[0]

                Button:
                    text: "Daftar Sekarang"
                    font_size: dp(12)
                    bold: True
                    color: 0.1, 0.35, 0.1, 1 # Hijau
                    background_normal: ''
                    background_color: 0, 0, 0, 0 # Transparan
                    size_hint_x: None
                    width: dp(100)
                    on_release: print("Pindah ke halaman Daftar")
                    # Ganti print() dengan: root.manager.current = 'register'

                # Spacer kanan
                Widget: 

        # Spacer Bawah Utama
        Widget:
            size_hint_y: 0.3
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
