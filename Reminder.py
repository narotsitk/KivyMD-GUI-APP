from datetime import datetime, time, timedelta

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.tab import MDTabsBase

Builder.load_file("Reminder.kv")
class Reminder_Tab(MDTabsBase):
    data= {'Set New Reminder':"bell"}
    def __init__(self,**kw):
        super(Reminder_Tab, self).__init__(**kw)
        self.ids.Reminder_list.add_widget(Reminder_Note())

    def Call_Back(self,instance):
        self.add_widget(Reminder_Adder(obj = self))


class Reminder_Adder(MDRelativeLayout):
    Reminder = None
    def __init__(self,obj,**kw):
        super(Reminder_Adder, self).__init__(**kw)
        self.obj = obj


    def set_error_message(self, instance_textfield):
        self.screen.ids.text_field_error.error = True

    def show_time_picker(self):
        if ( self.ids.Reminder_note_text.text != ""):
            time_picker = MDTimePicker()
            time_picker.bind(on_save = self.save_Reminder)
            time_picker.open()
        else:
            self.ids.Reminder_note_text.hint_text = "First write a Reminder"
            self.ids.Reminder_note_text.hint_text_color = (1,0,0,1)

    def get_Reminder(self,text):
        self.Reminder = text


    def remove_Reminder_creator(self):
        self.parent.remove_widget(self)

    def save_Reminder(self,instance,time_selected):
        now = datetime.now()
        t1 = timedelta(hours = time_selected.hour, minutes= time_selected.minute,seconds = time_selected.second)
        t2 = timedelta(hours = now.hour,minutes = now.minute,seconds= now.second)
        if ( t1 > t2 ):
            schedule_time = t1-t2
        else:
            schedule_time = t2 - t1
        print(schedule_time)
        schedule_time = schedule_time.total_seconds()
        print(schedule_time)
        self.parent.ids.Reminder_list.add_widget(Reminder_List(Reminder=self.Reminder,time = str(time_selected), schedule_time = schedule_time , obj = self.parent))
        self.parent.remove_widget(self)

class Reminder_Note(TwoLineAvatarIconListItem):

    def remove_this(self):
        self.parent.remove_widget(self)


class Reminder_List(TwoLineAvatarIconListItem):
    dialog = None
    def __init__(self,Reminder,time,schedule_time,obj,**kw):
        super(Reminder_List, self).__init__(**kw)
        self.text = Reminder
        self.secondary_text = time
        self.obj = obj
        self.schedule_time = schedule_time
        Clock.schedule_once(self.set_Reminder, schedule_time)



    def remove_Reminder(self):
        Clock.unschedule(self.set_Reminder)
        self.obj.ids.Reminder_list.remove_widget(self)

    def set_Reminder(self,dt):
            self.sound = SoundLoader.load('Sound/Retro_Game.wav')
            if self.sound:
                    self.show_alert_dialog()
                    self.sound.play()

    def dialog_close(self, obj):
        self.dialog.dismiss(force=True)
        self.sound.stop()
        self.obj.ids.Reminder_list.remove_widget(self)

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = "Reminder: ",
                text = self.text,
                buttons=[
                    MDFlatButton(
                        text="Ok",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press = self.dialog_close
                    ),
                ],
            )
        self.dialog.open()



