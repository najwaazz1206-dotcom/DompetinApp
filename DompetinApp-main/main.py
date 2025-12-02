from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty

# --- IMPORT KOMPONEN CUSTOM ---
# Mengambil widget tombol dan input dari file components.py
from components import RoundedButton, RoundedInput, NavButton

# --- IMPORT LAYAR/FITUR ---
# Mengambil logika setiap halaman dari folder screens/
from screens.login import LoginScreen
from screens.input import InputScreen
from screens.home import HomeContent
from screens.budget import BudgetContent
from screens.akun import AkunContent
from screens.overview import OverviewContent  # <-- Fitur baru (pengganti Grafik)

# --- KONFIGURASI WINDOW ---
# Mengatur ukuran agar mirip tampilan HP
Window.size = (360, 640)
Window.clearcolor = (0.97, 0.97, 0.97, 1)

# --- DESAIN LAYOUT UTAMA (MAIN SCREEN) ---
# MainScreen adalah wadah untuk Header, Konten (Home/Overview/dll), dan Footer
Builder.load_string("""
<MainScreen>:
    name: "main"

    BoxLayout:
        orientation: "horizontal"

        # =============== SIDEBAR ===============
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: 0.17
            padding: [15, 25]
            spacing: 25
            canvas.before:
                Color:
                    rgba: 0.90, 0.80, 0.65, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            # ====== MENU ATAS ======
            SidebarItem:
                icon: "Asset/home.png"
                text: "Home"
                on_release: app.change_screen('Home')

            SidebarItem:
                icon: "Asset/overview.png"
                text: "Overview"
                on_release: app.change_screen('Overview')

            SidebarItem:
                icon: "Asset/budgeting.png"
                text: "Budgeting"
                on_release: app.change_screen('Budget')

            # SPACER AGAR AKUN KE BAWAH
            Widget:
                size_hint_y: 1

            # ====== MENU BAWAH ======
            SidebarItem:
                icon: "Asset/akun.png"
                text: "Akun"
                on_release: app.change_screen('Akun')

        # =============== CONTENT AREA ===============
        BoxLayout:
            id: content_area
            orientation: "vertical"
            padding: 10
            spacing: 10


<SidebarItem@ButtonBehavior+BoxLayout>:
    orientation: "vertical"
    spacing: 5
    size_hint_y: None
    height: dp(65)
    background_color: 0,0,0,0

    icon: ""
    text: ""

    Image:
        source: root.icon
        size_hint_y: 0.7

    Label:
        text: root.text
        font_size: "12sp"
        color: 0,0,0,1
        size_hint_y: 0.3
""")

# --- LOGIKA MAIN SCREEN ---
class MainScreen(Screen):
    title = StringProperty("DOMPETIN")
    
    def show_content(self, tab_name):
        """
        Fungsi untuk mengganti isi Content Area berdasarkan tab yang dipilih
        """
        container = self.ids.content_area
        container.clear_widgets()
        
        # 1. Tampilkan HOME
        if tab_name == 'home':
            self.title = "DOMPETIN"
            c = HomeContent()
            c.update_data() # Update angka saldo/transaksi
            container.add_widget(c)
        
        # 2. Tampilkan OVERVIEW (Fitur Baru)
        elif tab_name == 'overview':
            self.title = "Overview Budget"
            c = OverviewContent()
            c.update_overview() # Update progress bar budget
            container.add_widget(c)
            
        # 3. Tampilkan BUDGET
        elif tab_name == 'budget':
            self.title = "Budgeting"
            c = BudgetContent()
            c.update_list() # Update daftar budget
            container.add_widget(c)

        # 4. Tampilkan AKUN
        elif tab_name == 'akun':
            self.title = "Akun"
            c = AkunContent()
            c.load_info() # Tampilkan username
            container.add_widget(c)
    
    def refresh_home(self):
        # Helper function untuk dipanggil setelah input transaksi selesai
        self.show_content('home')

# --- APLIKASI UTAMA ---
class DompetinApp(App):
    user_id = None
    username = StringProperty("")
    current_tab = StringProperty("home") # Tab aktif saat ini
    main_screen = None

    def build(self):
        # Membuat Screen Manager
        sm = ScreenManager()
        
        # Tambahkan Screen 1: Login
        sm.add_widget(LoginScreen(name='login'))
        
        # Tambahkan Screen 2: Main Layout (Wadah utama)
        self.main_screen = MainScreen(name='main')
        sm.add_widget(self.main_screen)
        
        # Tambahkan Screen 3: Input Transaksi (Layar penuh)
        sm.add_widget(InputScreen(name='input'))
        
        return sm

    def change_screen(self, tab_name):
        """
        Dipanggil ketika tombol di Footer ditekan.
        Mengubah variabel current_tab dan memanggil show_content di MainScreen.
        """
        # Mapping teks tombol ke kode internal tab
        mapping = {
            'Home': 'home', 
            'Overview': 'overview', 
            'Budget': 'budget', 
            'Akun': 'akun'
        }
        target = mapping.get(tab_name)
        if target:
            self.current_tab = target
            self.main_screen.show_content(target)

    def open_input(self, type):
        """
        Membuka layar input transaksi (Pemasukan/Pengeluaran)
        """
        scr = self.root.get_screen('input')
        scr.trx_type = type # Set tipe transaksi
        self.root.current = 'input' # Pindah layar

    def logout(self):
        """
        Reset data user dan kembali ke layar Login
        """
        self.user_id = None
        self.username = ""
        self.current_tab = "home"
        self.root.current = 'login'

if __name__ == '__main__':
    DompetinApp().run()