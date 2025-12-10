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
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
                source: "Asset/cobabg.png"
                    
            Color:
                rgba: 0.98, 0.94, 0.85, 0.2  
            Rectangle:
                pos: self.pos
                size: self.size

        # ======================= HEADER (DOMPETIN DIHAPUS) ======================
        BoxLayout:
            size_hint_y: None
            height: "100dp"
            spacing: 20
            Image:
                padding: 0,1
                source: 'Asset/logodompetin.png'
                size_hint_x: None
                width: '100dp'
                fit_mode: 'contain'
            Label:
                padding: 0,1
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
            
            # Total Saldo (VERTICAL)
            # Total Saldo
            BoxLayout:
                orientation: 'vertical'
                padding: "10dp"
                size_hint_y: 0.8
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 0.6
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [20]
                
                Label:
                    text: "Total Saldo"
                    bold: True
                    font_size: "18sp"
                    color: 0, 0.25, 0, 1
                Label:
                    text: root.txt_saldo
                    font_size: "22sp"
                    bold: True
                    color: 0,0,0,

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
                            rgba: 0.88, 0.93, 0.83, 0.6
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [20]
                    Label:
                        text: "Pemasukan"
                        bold: True
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
                            rgba: 0.88, 0.93, 0.83, 0.6
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [20]
                    Label:
                        text: "Pengeluaran"
                        bold: True
                        font_size: "18sp"
                        color: 0,0,0,1
                    Label:
                        text: root.txt_pengeluaran
                        font_size: "22sp"
                        bold: True
                        color: 0.9, 0.2, 0.2, 1

        # ======================= BUTTONS ============================
        BoxLayout:
            size_hint_y: None
            height: "60dp"
            spacing: 10
            RoundedButton:
                text: "+ Pemasukan"
                bg_color: [0.2, 0.75, 0.3, 0.7]
                on_release: app.open_input('pemasukan')
            RoundedButton:
                text: "- Pengeluaran"
                bg_color: [0.9, 0.25, 0.25, 0.7]
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
        if not uid:
            return
        
        db = Database()
        inc, exp, bal = db.get_summary(uid)
        
        self.txt_pemasukan = f"Rp {inc:,}"
        self.txt_pengeluaran = f"Rp {exp:,}"
        self.txt_saldo = f"Rp {bal:,}"

        # ===== AMBIL DATA TRANSAKSI =====
        rows = db.get_recent_transactions(uid)

        # Bersihkan UI
        self.ids.history_box.clear_widgets()

        # Tampilkan setiap transaksi
        for r in rows:
            trans_id = r[0]
            tanggal = r[1]
            kategori = r[2]
            jumlah = r[3]
            tipe = r[4]

            color_hex = '#2ecc71' if tipe == 'pemasukan' else '#e74c3c'
            op = '+' if tipe == 'pemasukan' else '-'

            item = BoxLayout(size_hint_y=None, height='40dp', padding=[10,0], spacing=10)

            # ====== LABEL KIRI ======
            lbl_cat = Label(
                text=f"{kategori}\n[size=10]{tanggal}[/size]",
                markup=True,
                color=(0,0,0,1),
                halign='left',
                valign='middle'
            )
            lbl_cat.bind(size=lbl_cat.setter('text_size'))

            # ====== LABEL JUMLAH ======
            lbl_amt = Label(
                text=f"{op} Rp {jumlah:,}",
                color=get_color_from_hex(color_hex),
                halign='right',
                valign='middle',
                bold=True
            )
            lbl_amt.bind(size=lbl_amt.setter('text_size'))

            # ====== TOMBOL HAPUS ======
            btn_del = RoundedButton(
                text="Hapus",
                bg_color=[0.9, 0.2, 0.2, 0.7],
                size_hint_x=None,
                width="70dp",
                on_release=lambda inst, tid=trans_id: self.delete_item(tid)
            )

            item.add_widget(lbl_cat)
            item.add_widget(lbl_amt)
            item.add_widget(btn_del)
            self.ids.history_box.add_widget(item)

    # =====================================================
    # FUNGSI HAPUS TRANSAKSI
    # =====================================================
    def delete_item(self, trans_id):
        db = Database()
        db.delete_transaction(trans_id)

        # Refresh UI setelah hapus
        self.update_data()