from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from database import Database
from components import RoundedButton

Builder.load_string("""

<HomeContent>:
    orientation: 'horizontal'

    # ======================= MAIN CONTENT ============================
    BoxLayout:
        orientation: 'vertical'
        padding: [30, 20]
        spacing: 20
        canvas.before:
            Color:
                rgba: 0.97, 0.93, 0.86, 1
            Rectangle:
                pos: self.pos
                size: self.size

        # ======================= HEADER (DOMPETIN DIHAPUS) ======================
        BoxLayout:
            size_hint_y: None
            height: "140dp"
            spacing: 10
            Image:
                source: 'Asset/wallet_logo.png'
                size_hint_x: None
                width: '140dp'
            Label:
                text: "Home"
                font_size: "32sp"
                bold: True
                color: 0,0,0,1
                halign: 'left'
                valign: 'middle'
                text_size: self.size

        # ======================= TOP CARDS ============================
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: "200dp" 
            spacing: 10

            # Pemasukan & Pengeluaran (HORIZONTAL)
            BoxLayout:
                orientation: 'horizontal'
                spacing: 10
                
                # Pemasukan
                BoxLayout:
                    orientation: 'vertical'
                    padding: "15dp"
                    size_hint_y: 0.8
                    canvas.before:
                        Color:
                            rgba: 0.88, 0.93, 0.83, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [20]
                    Label:
                        text: "Pemasukan"
                        font_size: "18sp"
                        color: 0,0,0,1
                    Label:
                        text: root.txt_pemasukan
                        font_size: "22sp"
                        bold: True
                        color: 0.1, 0.5, 0.1, 1

                # Pengeluaran
                BoxLayout:
                    orientation: 'vertical'
                    padding: "15dp"
                    size_hint_y: 0.8
                    canvas.before:
                        Color:
                            rgba: 0.88, 0.93, 0.83, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [20]
                    Label:
                        text: "Pengeluaran"
                        font_size: "18sp"
                        color: 0,0,0,1
                    Label:
                        text: root.txt_pengeluaran
                        font_size: "22sp"
                        bold: True
                        color: 0.9, 0.2, 0.2, 1

            # Total Saldo (VERTICAL)
            # Total Saldo
            BoxLayout:
                orientation: 'vertical'
                padding: "10dp"
                size_hint_y: 0.8
                canvas.before:
                    Color:
                        rgba: 0.88, 0.93, 0.83, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [20]
                
                Label:
                    text: "Total Saldo"
                    font_size: "18sp"
                    color: 0,0,0,1
                Label:
                    text: root.txt_saldo
                    font_size: "22sp"
                    bold: True
                    color: 0,0,0,1

        # ======================= BUTTONS ============================
        BoxLayout:
            size_hint_y: None
            height: "60dp"
            spacing: 10
            RoundedButton:
                text: "+ Pemasukan"
                bg_color: [0.2, 0.75, 0.3, 1]
                on_release: app.open_input('pemasukan')
            RoundedButton:
                text: "- Pengeluaran"
                bg_color: [0.9, 0.25, 0.25, 1]
                on_release: app.open_input('pengeluaran')

        Label:
            text: "Riwayat Transaksi"
            font_size: "20sp"
            bold: True
            color: 0,0,0,1
            size_hint_y: None
            height: "30dp"
            halign: 'left'
            text_size: self.size

        ScrollView:
            bar_width: 8
            scroll_type: ['bars', 'content']
            BoxLayout:
                id: history_box
                orientation: 'vertical'
                padding: [0,10]
                spacing: 10
                size_hint_y: None
                height: self.minimum_height

""")

class HomeContent(BoxLayout):
    txt_pemasukan = StringProperty("Rp 0")
    txt_pengeluaran = StringProperty("Rp 0")
    txt_saldo = StringProperty("Rp 0")

    def update_data(self):
        uid = App.get_running_app().user_id
        if not uid: return
        
        db = Database()
        inc, exp, bal = db.get_summary(uid)
        
        self.txt_pemasukan = f"Rp {inc:,}"
        self.txt_pengeluaran = f"Rp {exp:,}"
        self.txt_saldo = f"Rp {bal:,}"

        rows = db.get_recent_transactions(uid)
        self.ids.history_box.clear_widgets()
        
        for r in rows:
            # r = (date, category, amount, type)
            color_hex = '#2ecc71' if r[3] == 'pemasukan' else '#e74c3c'
            op = '+' if r[3] == 'pemasukan' else '-'
            
            item = BoxLayout(size_hint_y=None, height='40dp', padding=[10,0])
            lbl_cat = Label(text=f"{r[1]}\n[size=10]{r[0]}[/size]", markup=True, color=(0,0,0,1), halign='left', valign='middle')
            lbl_cat.bind(size=lbl_cat.setter('text_size'))
            
            lbl_amt = Label(text=f"{op} Rp {r[2]:,}", color=get_color_from_hex(color_hex), halign='right', valign='middle', bold=True)
            lbl_amt.bind(size=lbl_amt.setter('text_size'))
            
            item.add_widget(lbl_cat)
            item.add_widget(lbl_amt)
            self.ids.history_box.add_widget(item)