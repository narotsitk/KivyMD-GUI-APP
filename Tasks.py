from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tab import MDTabsBase
from kivy.factory import Factory
Builder.load_file("Tasks.kv")

custom_sheet = None
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    task= None
    def __init__(self,**kw):
        super(ListItemWithCheckbox, self).__init__(**kw)
    def remove_task(self):
        self.parent.remove_widget(self)

    def active_box(self,checkbox, value):
        if value:
            self.task = self.text
            self.text = f"[s]{self.task}[/s]"
            self.theme_text_color = "Hint"
            self.secondary_theme_text_color = "Custom"
            self.secondary_text_color = (0,1,0,1)
            self.secondary_text = "Completed"
        else:
            self.text = self.task
            self.theme_text_color = "Primary"
            self.secondary_theme_text_color= "Error"
            self.secondary_text= "Not Completed"

class RightCheckbox(IRightBodyTouch,MDCheckbox):
    pass

class ContentCustomSheet(BoxLayout):
    def __init__(self,obj,**kw):
        super(ContentCustomSheet, self).__init__(**kw)
        self.obj = obj

    def Save_Task(self):
        print("Task Saved")
    def dismiss_bottom_sheet(self):
        custom_sheet.dismiss()

    def save_task(self):
        if self.ids.task_field.text == '':
            self.ids.task_field.hint_text = 'First Enter a task !!'
            self.ids.task_field.hint_text_color = (1,0,0,1)
        else:

            self.obj.ids.task_scroll.add_widget(ListItemWithCheckbox(text = self.ids.task_field.text, secondary_theme_text_color = "Error",secondary_text = 'Not Completed'))
            custom_sheet.dismiss()





class Tasks_Tab(MDTabsBase):
    data = {'Create New Task': 'format-list-checks'}

    def CallBack(self,widget):
        global custom_sheet
        custom_sheet = MDCustomBottomSheet( duration_opening = 0.01,radius_from = "top", screen = Factory.ContentCustomSheet(obj = self))
        custom_sheet.open()

    def Save_Task(self):
        print("Save Tasks")



