import os
import uuid
import time
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.tab import MDTabsBase
from kivymd.utils.fitimage import FitImage

Builder.load_file("Image_Note.kv")
image_list_object = None
picture_path = None

class Image_Note_Create(Screen):
    def __init__(self,obj,image_path, note, **kw):
        super(Image_Note_Create, self).__init__(**kw)
        self.path = image_path
        self.obj = obj
        self.note = note
        self.image = FitImage(
            source = image_path,
            size_hint_y = .5,
            pos_hint = {'top': 1}
        )
        self.ids.image_note.text = note
        self.ids.r_layout.add_widget(self.image)

    def add_widget_toolbar(self, text):
        self.note_text = text
        if text != "":
            right_action_items = [["check", lambda x: self.save_notes()]]
            self.ids.md_tool_bar.right_action_items = right_action_items
        elif text == "":
            self.ids.md_tool_bar.right_action_items = []

    def save_notes(self):
        global image_list_object, previous_note
        if self.note == "":
            previous_note = False
        elif self.note != "":
            previous_note = True
        timestr = strtime = time.strftime("%H:%M  %a, %b %d %Y  ", time.localtime())
        if previous_note == False:
            print(self.obj)
            self.parent.current = "Main"
            self.obj.ids.image_list.add_widget(Image_List(path=self.path, label_text = self.note_text, time_stamp = strtime, parent_obj = self.parent))
        else:
            image_list_object.text = self.note_text[:25] + f"...\nAdded: {strtime}"
            image_list_object.note = self.note_text

        self.parent.remove_widget(self.parent.get_screen("Image_Note_Create"))

    def return_back(self):
        self.parent.current = "Main"
        self.parent.remove_widget(self.parent.get_screen("Image_Note_Create"))


class Image_List(SmartTileWithLabel, ButtonBehavior):
    note = None
    dialog = None
    del_widget = None
    def __init__(self, path, label_text,time_stamp,parent_obj, **kwargs):
        super(Image_List, self).__init__(**kwargs)
        self.obj = parent_obj
        self.source = path
        self.size_hint_y = None
        self.note = label_text
        self.time_stamp = time_stamp
        self.height = "240dp"
        self.text = label_text[:25]+f"...\nAdded: {self.time_stamp}"

    def on_press_image(self):
        global image_list_object, display, pressed
        image_list_object = self
        self.obj.add_widget(Image_Note_Create(name = "Image_Note_Create", obj = self.obj, image_path = self.source, note = self.note))
        self.obj.current = "Image_Note_Create"

    def on_press_delete(self, widget):
        self.del_widget = widget
        self.show_confirmation_dialog()


    def dialog_close(self,obj):
        self.dialog.dismiss(force=True)
        #self.obj.current = "Main"
        #self.obj.remove_widget(self.obj.get_screen("Image_Note_Create"))

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Do you want to delete ?",
                type="custom",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color= "Primary",
                        on_press = self.dialog_close,

                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_press = self.remove_image_note,
                        on_release = self.dialog_close,
                    ),
                ],
            )
        self.dialog.open()

    def remove_image_note(self,obj):
        if self.del_widget.source[:6] == "Images":
            print(self.del_widget.source)
            os.remove(self.del_widget.source)
        
        self.parent.remove_widget(self.del_widget)

class Image_Note_Tab(MDFloatLayout, MDTabsBase):
    data = {
        'Upload from Device': 'upload',
        'Take a picture': 'camera-plus',
    }
    def __init__(self,obj,**kw):
        super(Image_Note_Tab, self).__init__(**kw)
        self.manager_open = False
        self.obj = obj
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        self.ids.image_list.add_widget(Image_Note())

    def callback(self,instance):
        if instance.icon == 'upload':
            self.file_manager_open()
        elif instance.icon == 'camera-plus':
            self.obj.parent.add_widget(CameraScreen(name = "Camera_Screen", obj = self))
            self.obj.parent.current = "Camera_Screen"

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
        self.obj.parent.add_widget(Image_Note_Create(name = "Image_Note_Create", obj = self, image_path = path, note = ""))
        self.obj.parent.current = "Image_Note_Create"
        #self.add_image(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

class KivyCamera(Image):

    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture

        Clock.schedule_interval(self.update, 1.0 / fps)


    def update(self, dt):
        global capture_frame
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
            capture_frame = frame

class CameraScreen(Screen):
    def __init__(self,obj,**kw):
        super(CameraScreen, self).__init__(**kw)
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture =self.capture, fps = 40)
        self.add_widget(self.my_camera)
        self.image = None
        self.tick_button = None
        self.close_button = None
        self.obj = obj

    def Call_Back(self):
        self.capture.release()
        self.parent.current = "Main"
        self.parent.remove_widget(self.parent.get_screen("Camera_Screen"))

    def save_photo(self,instance):
        self.Call_Back()
        self.parent.add_widget(Image_Note_Create(name="Image_Note_Create", obj= self.obj, image_path=picture_path, note=""))
        self.parent.current = "Image_Note_Create"

    def unsave_photo(self,instance):
        global picture_path
        self.remove_widget(self.image)
        self.remove_widget(self.click_button)
        self.remove_widget(self.close_button)
        os.remove(picture_path)

    def click_picture(self):
        global picture_path
        filename = uuid.uuid4().hex
        if not os.path.exists('Images'):
            os.mkdir("Images")

        cv2.imwrite(f"Images/{str(filename)}.png", capture_frame)
        picture_path = f"Images/{str(filename)}.png"

        self.image = FitImage(
            source = picture_path,
            radius = (0,0,0,0),
        )
        self.click_button = MDFillRoundFlatIconButton(icon="check-outline", text = "Save",pos_hint={"center_y": self.y + .1, "center_x": self.x + .15},
                                         on_press=self.save_photo)
        self.close_button = MDFillRoundFlatIconButton(icon="close-outline", text = "Unsave", pos_hint={"center_y": self.y + .1, "center_x": self.x + .83},
                                         on_press=self.unsave_photo)
        self.add_widget(self.image)
        self.add_widget(self.click_button)
        self.add_widget(self.close_button)




class Image_Note(TwoLineAvatarIconListItem):

    def remove_this(self):
        self.parent.remove_widget(self)
