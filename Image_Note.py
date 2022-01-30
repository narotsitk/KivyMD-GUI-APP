from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.imagelist import SmartTile
from kivymd.uix.tab import MDTabsBase

Builder.load_file("Image_Note.kv")


class Image_Note_Create(Screen):
    pass



class Image_List(SmartTile, ButtonBehavior):
    def __init__(self, path, **kwargs):
        super(Image_List, self).__init__(**kwargs)
        self.source = path
        self.size_hint_y = None
        self.height = "240dp"
    def remove_image(self, widget):
        self.parent.remove_widget(widget)


class Image_Note_Tab(MDFloatLayout, MDTabsBase):
    data = {
        'Upload from Device': 'upload',
        'Take a picture': 'camera-plus',
    }
    def __init__(self,**kw):
        super(Image_Note_Tab, self).__init__(**kw)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

    def callback(self,instance):
        if instance.icon == 'upload':
            self.file_manager_open()

    def file_manager_open(self):
        self.file_manager.show('/Users/Dell/Desktop')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        self.add_image(path)
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()
    def add_image(self,path):
        self.ids.image_list.add_widget(Image_List(path = path))