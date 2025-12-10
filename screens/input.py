from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from datetime import datetime
from database import Database
from components import RoundedInput, RoundedButton
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
            hint_text: 'Kategori'
            on_text: root.check_budget_limit()

        RoundedInput:
            id: amount_input
            hint_text: 'Nominal'
            input_filter: 'int'
            on_text: root.check_budget_limit()

        RoundedInput:
            id: note_input
            hint_text: 'Catatan (Opsional)'

        # Warning Budget
        Label:
            id: warn_lbl
            text: root.warning_text
            color: 1,0,0,1
            font_size: "14sp"
            size_hint_y: None
            height: 20

        Widget:

        RoundedButton:
            id: save_btn
            text: 'Save'
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
    warning_text = StringProperty('')
    save_disabled = BooleanProperty(False)

    def on_pre_enter(self):
        self.date_label = datetime.now().strftime("%A, %d %b %Y")
        self.warning_text = ""
        self.ids.save_btn.disabled = False

    # ==========================
    # LOGIKA CEK BUDGET
    # ==========================
    def check_budget_limit(self):
        uid = App.get_running_app().user_id
        if not uid: return

        category = self.ids.cat_input.text.strip()
        amount = self.ids.amount_input.text.strip()

        if not category or not amount:
            self.warning_text = ""
            self.ids.save_btn.disabled = False
            return

        amount = int(amount)
        db = Database()
        budgets = db.get_budget_progress(uid)

        over_limit = False

        for b in budgets:
            b_name = b["name"]
            limit = b["limit"]
            spent = b["spent"]

            # Pencocokan kategori mengandung nama budget
            if b_name.lower() in category.lower():
                total_after = spent + amount

                if total_after > limit:
                    over_limit = True

        if over_limit:
            self.warning_text = "Budget sudah terpenuhi atau melebihi"
            self.ids.save_btn.disabled = True
        else:
            self.warning_text = ""
            self.ids.save_btn.disabled = False

    # ==========================
    # SIMPAN DATA
    # ==========================
    def save_data(self):
        if self.ids.save_btn.disabled:
            return  # tidak boleh save

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

            app = App.get_running_app()
            app.root.current = 'main'

            if hasattr(app, 'main_screen'):
                app.main_screen.show_content('home')