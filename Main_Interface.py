
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.list import OneLineIconListItem, MDList, ThreeLineAvatarIconListItem
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.tab import MDTabsBase
from Image_Note import Image_Note_Tab
from Reminder import Reminder_Tab
from Text_Voice_Note import Text_Voice_Note_Tab
from Tasks import Tasks_Tab
from kivy.core.window import Window
#from kivymd.uix.transition.transition import MDFadeSlideTransition
Builder.load_file("Main_App.kv")
Window.size = [360,640]





class Main_Screen(Screen):
    icons = ["notebook-plus", "image-plus", "bell-plus", 'script-text']
    def __init__(self,**kwargs):
        super(Main_Screen, self).__init__(**kwargs)
        self.on_start()

    def on_start(self):
        for tab_icon in self.icons:
            if tab_icon == "notebook-plus":
                self.ids.tabs.add_widget(Text_Voice_Note_Tab(icon = tab_icon, obj = self))
            elif tab_icon == "image-plus":
                self.ids.tabs.add_widget(Image_Note_Tab(icon = tab_icon, obj = self))
            elif tab_icon == "bell-plus":
                self.ids.tabs.add_widget(Reminder_Tab(icon = tab_icon))
            elif tab_icon == "script-text":
                self.ids.tabs.add_widget(Tasks_Tab(icon = tab_icon))

    def on_tab_switch(self,instance_tabs,instace_tab,instance_tab_level,tab_text):
        if instace_tab.icon == 'notebook-plus':
            self.ids.tool_bar.title = "Text and Voice Note"
        elif instace_tab.icon == "image-plus":
            self.ids.tool_bar.title = "Image Note"
        elif instace_tab.icon == "bell-plus":
            self.ids.tool_bar.title = "Reminder"
        elif instace_tab.icon == 'script-text':
            self.ids.tool_bar.title = "Tasks"

class Nav_Drawer_Content(BoxLayout):
    pass

class DrawerList(MDList):
    icon_items = {"logout-variant": "Logout",
                  "trash-can-outline": "Recycle Bin",
                  "theme-light-dark": "Change Theme",
                  }

    def __init__(self, **kwargs):
        super(DrawerList, self).__init__(**kwargs)
        self.on_start()

    def on_start(self):

        for icon_name in self.icon_items.keys():
            self.add_widget(
                ItemDrawer(icon=icon_name, text=self.icon_items[icon_name])
            )

class Recycle_Bin_Screen(Screen):


    def return_back(self):
        self.parent.current = "Main"
    def add_deleted_items(self,widget):
        self.ids.recycle_bin_list.add_widget(Recycle_Bin_List(text = widget.text, secondary_text =widget.secondary_text, tertiary_text= widget.tertiary_text))

class Recycle_Bin_List(ThreeLineAvatarIconListItem):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    def callback(self,app):
        if self.icon == 'theme-light-dark':
            self.open_theme_changer()
        if self.icon == 'trash-can-outline':
            app.scm.current = 'Recycle_Bin'

    def open_theme_changer(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

class App_Runner(MDApp):
    scm = ScreenManager()
    def build(self):
        self.title = "Notes"
        self.theme_cls.primary_palette = 'Purple'
        self.scm.add_widget(Main_Screen(name = "Main"))
        self.scm.add_widget(Recycle_Bin_Screen(name = 'Recycle_Bin'))

        return self.scm


if __name__ == "__main__":
    App_Runner().run()

