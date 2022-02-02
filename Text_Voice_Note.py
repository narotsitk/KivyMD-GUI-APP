import time

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ThreeLineAvatarIconListItem, TwoLineAvatarListItem, TwoLineAvatarIconListItem
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.tab import MDTabsBase

Builder.load_file("Text_Voice_Note.kv")


item_list_object = None
note_no = 0
class MyItem(ThreeLineAvatarIconListItem):
    title = None
    notes = None
    def __init__(self, title, notes , time_stamp, obj, **kwargs):
        super(MyItem, self).__init__(**kwargs)
        self.title = title
        self.notes = notes
        self.time_stamp = time_stamp
        self.obj = obj
        self.add_text()


    def add_text(self):
        if self.title != "":
            self.text = self.title
            self.secondary_text = self.notes
            self.tertiary_text = self.time_stamp
        elif self.title == "":
            self.text = self.notes
            self.tertiary_text = self.time_stamp

    def remove_note(self,widget):
        self.obj.ids.selection_list.remove_widget(widget)
        if self.text != "Welcome To Notes":
            recycle_bin = self.obj.obj.parent.get_screen("Recycle_Bin")
            recycle_bin.add_deleted_items(widget)




    def on_callback(self):
        global item_list_object
        item_list_object = self
        self.obj.obj.parent.add_widget(Text_Note_Screen(name="Text_Note", title=self.title, notes=self.notes, obj=self.obj))
        self.obj.obj.parent.current = "Text_Note"




class Text_Voice_Note_Tab(BoxLayout,MDTabsBase):
    data = { 'Add Text Note':'note-plus',
             "AddVoice Note":'microphone-plus',
            }

    def __init__(self,obj,**kw):
        super(Text_Voice_Note_Tab, self).__init__(**kw)
        self.obj = obj

        self.ids.selection_list.add_widget(Welcome_Note())



    def callback(self,instance):
        if instance.icon == 'note-plus':
            self.obj.parent.add_widget(Text_Note_Screen(name = "Text_Note", title = "",notes = "",obj = self))
            self.obj.parent.current = "Text_Note"




class Text_Note_Screen(Screen):

    def __init__(self,title,notes,obj,**kwargs):
        super(Text_Note_Screen, self).__init__(**kwargs)
        self.ids.title.text = title
        self.ids.notes.text = notes
        self.obj = obj
        self.timeStr = time.ctime()
        if notes != "":
            self.previous_note = True
        else:
            self.previous_note = False

    def add_widget_on_toolbar(self,text):
        if text != "":
            self.Notes = text
            right_action_items = [["check",lambda x: self.save_notes()]]
            self.ids.md_tool_bar.right_action_items = right_action_items

        elif text == "":
           self.ids.md_tool_bar.right_action_items = []

    def save_notes(self):
        global item_list_object
        self.parent.current = "Main"
        title = self.ids.title.text
        notes = self.ids.notes.text
        if self.previous_note == False:
            self.obj.ids.selection_list.add_widget(MyItem(title = title, notes = notes, time_stamp= self.timeStr, obj = self.obj))
        else:
            if title != "":
                item_list_object.text = title
                item_list_object.secondary_text = notes
            elif title == "":
                item_list_object.text = notes

            item_list_object.title = title
            item_list_object.notes = notes
            item_list_object.tertiary_text = self.timeStr

        self.parent.remove_widget(self.parent.get_screen("Text_Note"))

    def return_back(self):

        self.parent.current = "Main"
        self.parent.remove_widget(self.parent.get_screen("Text_Note"))

class Welcome_Note(TwoLineAvatarIconListItem):

    def remove_this(self):
        self.parent.remove_widget(self)

