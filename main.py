from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty
from components import RoundedButton, RoundedInput, NavButton
from screens.login import LoginRegisterScreen   # <-- hanya ini!
from screens.input import InputScreen
from screens.home import HomeContent
from screens.budget import BudgetContent
from screens.akun import AkunContent
from screens.overview import OverviewContent
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior

# --- KONFIGURASI WINDOW ---
Window.maximize()
Window.clearcolor = (0.97, 0.97, 0.97, 1)

# --- DESAIN ---
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

            SidebarItem:
                icon: "Asset/home.png"
                text: "Home"
                state: 'down'
                on_release: app.change_screen('Home')

            SidebarItem:
                icon: "Asset/overview.png"
                text: "Overview"
                on_release: app.change_screen('Overview')

            SidebarItem:
                icon: "Asset/budgeting.png"
                text: "Budgeting"
                on_release: app.change_screen('Budget')

            Widget:
                size_hint_y: 1

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


<SidebarItem@ToggleButtonBehavior+BoxLayout>:
    group: 'menu_utama'
    allow_no_selection: False
    orientation: "vertical"
    spacing: 5
    size_hint_y: None
    height: dp(85)
    padding: [0, dp(10), 0, dp(8)]
    spacing: dp(2)

    canvas.before:
        Color:
            rgba: (0, 0, 0, 0.15) if self.state == 'down' else (0, 0, 0, 0)
        RoundedRectangle:
            pos: self.x + dp(14), self.y + dp(1)
            size: self.width - dp(20), self.height - dp(10)
            radius: [dp(25),]
        Color:
            rgba: (0.74, 0.72, 0.67, 1) if self.state == 'down' else (0, 0, 0, 0)
        RoundedRectangle:
            pos: self.x + dp(10), self.y + dp(5)
            size: self.width - dp(20), self.height - dp(10)
            radius: [dp(25),]

    icon: ""
    text: ""

    Image:
        source: root.icon
        size_hint_y: 0.7
        color: (0.2, 0.2, 0.2, 1) if root.state == 'down' else (0, 0, 0, 1)

    Label:
        text: root.text
        font_size: "12sp"
        size_hint_y: 0.3
        color: (0,0,0,1) if root.state == 'down' else (0,0,0,0.5)
        bold: True if root.state == 'down' else False 
""")

# --- LOGIKA MAIN SCREEN ---
class MainScreen(Screen):
    title = StringProperty("DOMPETIN")

    def show_content(self, tab_name):
        container = self.ids.content_area
        container.clear_widgets()

        if tab_name == 'home':
            self.title = "DOMPETIN"
            c = HomeContent()
            c.update_data()
            container.add_widget(c)

        elif tab_name == 'overview':
            self.title = "Overview Budget"
            c = OverviewContent()
            c.update_overview()
            container.add_widget(c)

        elif tab_name == 'budget':
            self.title = "Budgeting"
            c = BudgetContent()
            c.update_list()
            container.add_widget(c)

        elif tab_name == 'akun':
            self.title = "Akun"
            c = AkunContent()
            c.load_info()
            container.add_widget(c)


class DompetinApp(App):
    user_id = None
    username = StringProperty("")
    current_tab = StringProperty("home")
    main_screen = None

    def build(self):
        sm = ScreenManager()

        sm.add_widget(LoginRegisterScreen(name='login'))
        self.main_screen = MainScreen(name='main')
        sm.add_widget(self.main_screen)
        sm.add_widget(InputScreen(name='input'))

        return sm   # <-- penting!!

    def change_screen(self, tab_name):
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
        scr = self.main_screen.manager.get_screen('input')
        scr.trx_type = type
        self.main_screen.manager.current = 'input'

    def logout(self):
        self.user_id = None
        self.username = ""
        self.current_tab = "home"
        self.main_screen.manager.current = 'login'


if __name__ == '__main__':
    DompetinApp().run()
