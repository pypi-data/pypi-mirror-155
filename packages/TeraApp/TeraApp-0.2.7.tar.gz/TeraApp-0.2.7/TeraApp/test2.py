from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory

from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from kivy.base import Builder

kv_string = Builder.load_string("""
BoxLayout:
    BoxLayout:
        canvas:
            Color:
                rgba: 150/255, 150/255, 150/255, 1
            Rectangle:
                pos: self.pos
                size: self.size

        ScrollView:
            id: scrlv

            GridLayout:
                cols: 1
                size_hint_y: None
                height: max(self.minimum_height, scrlv.height)

                BoxLayout:
                    size_hint_y: None
                    height: sized_label.height
                    Label:
                        id: sized_label
                        text: "[b]CurrentHistory:[/b]\\nHeader:"
                        size_hint: (None, None)
                        markup: True
                        size: self.texture_size
                    Label:

                TextInput:
                    size_hint_y: None
                    height: 80
                    hint_text: 'Enter Text Here'
                Label:

    BoxLayout:
        orientation: "vertical"
        size_hint_x: .25

        canvas:
            Color:
                rgba: 240/255, 180/255, 80/255, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "Label 1"
        Label:
            text: "Label 2"
""")



class MyApp(App):

    def build(self):
        return kv_string



if __name__ == '__main__':
    MyApp().run()