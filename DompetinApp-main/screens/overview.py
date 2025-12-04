from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from database import Database

Builder.load_string("""
<BudgetProgressItem>:
    orientation: 'vertical'
    size_hint_y: None
    padding: [30, 20]
    spacing: 20
    canvas.before:
        Color:
            rgba:  1, 1, 1, 0.6
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]
    

    BoxLayout:
        size_hint_y: 0.6
        Label:
            text: root.b_name
            color: 0,0,0,1
            bold: True
            halign: 'left'
            text_size: self.size
            valign: 'middle'
        Label:
            text: root.b_status
            color: 0.4, 0.4, 0.4, 1
            font_size: '12sp'
            halign: 'right'
            text_size: self.size
            valign: 'middle'

    BoxLayout:
        size_hint_y: 0.4
        padding: [0, 10, 0, 5]
        canvas:
            Color:
                rgba: 0.9, 0.9, 0.9, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [5,]
            Color:
                rgba: root.bar_color
            RoundedRectangle:
                pos: self.pos
                size: (self.width * root.percent_val, self.height)
                radius: [5,]

<OverviewContent>:
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
        text: 'Ringkasan Budget'
        color: 0,0,0,1
        font_size: '20sp'
        bold: True
        size_hint_y: None
        height: 40
        halign: 'left'
        text_size: self.size

    Label:
        text: 'Pantau penggunaan anggaran Anda di sini.'
        color: 0.5, 0.5, 0.5, 1
        font_size: '12sp'
        size_hint_y: None
        height: 20
        halign: 'left'
        text_size: self.size

    ScrollView:
        BoxLayout:
            id: overview_list
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            spacing: 10
            padding: [0, 10]
""")

class BudgetProgressItem(BoxLayout):
    from kivy.properties import StringProperty, NumericProperty, ListProperty
    b_name = StringProperty("")
    b_status = StringProperty("")
    percent_val = NumericProperty(0)
    bar_color = ListProperty([0.2, 0.8, 0.2, 1])

class OverviewContent(BoxLayout):
    def update_overview(self):
        uid = App.get_running_app().user_id
        if not uid: return
        
        db = Database()
        data = db.get_budget_progress(uid)
        
        container = self.ids.overview_list
        container.clear_widgets()
        
        if not data:
            lbl = Label(text="Belum ada data anggaran.", color=(0,0,0,0.5), size_hint_y=None, height=50)
            container.add_widget(lbl)
            return

        for item in data:
            p = item['percent']
            if p > 1.0:
                color = [0.9, 0.3, 0.3, 1] 
                p_display = 1.0 
            elif p > 0.75:
                color = [0.95, 0.7, 0.1, 1] 
                p_display = p
            else:
                color = [0.2, 0.8, 0.4, 1] 
                p_display = p

            status_txt = f"Rp {item['spent']:,} / Rp {item['limit']:,}"
            
            widget = BudgetProgressItem()
            widget.b_name = item['name']
            widget.b_status = status_txt
            widget.percent_val = p_display
            widget.bar_color = color
            
            container.add_widget(widget)