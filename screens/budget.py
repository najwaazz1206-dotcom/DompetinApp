from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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
            
            # reset input
            self.ids.bud_name.text = ""
            self.ids.bud_amount.text = ""
            self.ids.bud_period.text = ""

    def update_list(self):
        uid = App.get_running_app().user_id
        if not uid:
            return
        
        db = Database()
        rows = db.get_budgets(uid)
        self.ids.budget_list.clear_widgets()
        
        for r in rows:
            budget_id = r[0]
            name = r[1]
            amount = r[2]
            period = r[3]
            
            row_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing=10)

            label = Label(
                text=f"{name} ({period}) : Rp {amount:,}",
                color=(0,0,0,1),
                halign='left',
                valign='middle'
            )
            label.bind(size=label.setter('text_size'))

            delete_btn = RoundedButton(
                text="Hapus",
                size_hint_x=None,
                width="70dp",
                height="32dp",
                bg_color=[1, 0, 0, 1],     
                radius=[12, 12, 12, 12] 
            )
            delete_btn.bind(on_release=lambda btn, bid=budget_id: self.delete_budget(bid))

            row_box.add_widget(label)
            row_box.add_widget(delete_btn)
            
            self.ids.budget_list.add_widget(row_box)

    def delete_budget(self, budget_id):
        uid = App.get_running_app().user_id
        db = Database()

        if db.delete_budget(budget_id, uid):
            self.update_list()
