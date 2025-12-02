from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from datetime import datetime
from database import Database
from components import RoundedInput, RoundedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button

Builder.load_string("""
<InputScreen>:
    name: 'input'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: root.date_label
            color: 0,0,0,1
            bold: True
            size_hint_y: None
            height: 40
            canvas.before:
                Color:
                    rgba: 1, 1, 0.9, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10,]
                Color:
                    rgba: 0,0,0,1
                Line:
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 10)
                    width: 1

        RoundedInput:
            id: cat_input
            hint_text: 'Kategori (misal: makan, belanja)'

        RoundedInput:
            id: amount_input
            hint_text: 'Nominal'
            input_filter: 'int'

        RoundedInput:
            id: note_input
            hint_text: 'Catatan (Opsional)'

        Widget: 

        RoundedButton:
            text: 'save'
            size_hint_y: None
            height: '50dp'
            bg_color: [0, 0, 0, 1]
            on_release: root.save_data()
        
        Button:
            text: 'Kembali'
            size_hint_y: None
            height: '40dp'
            color: 0.5, 0.5, 0.5, 1
            background_normal: ''
            background_color: 0,0,0,0
            on_release: app.root.current = 'main'
""")

class InputScreen(Screen):
    trx_type = StringProperty('pemasukan')
    date_label = StringProperty('')

    def on_pre_enter(self):
        self.date_label = datetime.now().strftime("%A, %d %b %Y")

    def save_data(self):
        cat = self.ids.cat_input.text
        amt = self.ids.amount_input.text
        note = self.ids.note_input.text
        
        if cat and amt:
            uid = App.get_running_app().user_id
            db = Database()
            db.add_transaction(uid, self.trx_type, cat, int(amt), note, self.date_label)
            
            # Reset form
            self.ids.cat_input.text = ""
            self.ids.amount_input.text = ""
            self.ids.note_input.text = ""
            
            # Kembali ke main & refresh home
            app = App.get_running_app()
            app.root.current = 'main'
            if hasattr(app, 'main_screen'):
                app.main_screen.refresh_home()