from kivy.lang import Builder
from kivymd.uix.tab import MDTabsBase

Builder.load_file("Remainder.kv")
class Remainder_Tab(MDTabsBase):
    data= {'Set New Remainder':"bell"}