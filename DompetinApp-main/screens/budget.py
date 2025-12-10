from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from database import Database
from components import RoundedInput, RoundedButton

Builder.load_string("""
<BudgetContent>:
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
    
    Label:
        text: 'Buat Anggaran Baru'
        bold: True
        color: 0,0,0,1
        size_hint_y: None
        height: 30
        halign: 'left'
        text_size: self.size

    RoundedInput:
        id: bud_name
        hint_text: 'Nama anggaran'
    RoundedInput:
        id: bud_period
        hint_text: 'Periode'
    RoundedInput:
        id: bud_amount
        hint_text: 'Nominal'
        input_filter: 'int'
    
    RoundedButton:
        text: 'Save'
        size_hint_y: None
        height: '40dp'
        bg_color: [0, 0, 0, 1]
        on_release: root.save_budget()

    Label:
        text: 'Daftar Anggaran'
        color: 0,0,0,1
        bold: True
        size_hint_y: None
        height: 30
        halign: 'left'
        text_size: self.size

    ScrollView:
        BoxLayout:
            id: budget_list
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
""")

class BudgetContent(BoxLayout):
    def save_budget(self):
        name = self.ids.bud_name.text
        amt = self.ids.bud_amount.text
        period = self.ids.bud_period.text
        
        if name and amt:
            uid = App.get_running_app().user_id
            db = Database()
            db.add_budget(uid, name, int(amt), period)
            self.update_list()
            
            self.ids.bud_name.text = ""
            self.ids.bud_amount.text = ""
            self.ids.bud_period.text = ""

    def update_list(self):
        uid = App.get_running_app().user_id
        if not uid: return
        db = Database()
        rows = db.get_budgets(uid)
        self.ids.budget_list.clear_widgets()
        
        for r in rows:
            item = Label(text=f"{r[0]} ({r[2]}) : Rp {r[1]:,}", color=(0,0,0,1), size_hint_y=None, height='30dp')
            self.ids.budget_list.add_widget(item)