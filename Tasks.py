from kivy.lang import Builder
from kivymd.uix.tab import MDTabsBase

Builder.load_file("Tasks.kv")
class Tasks_Tab(MDTabsBase):
    data = {'Create New Task': 'format-list-checks'}

