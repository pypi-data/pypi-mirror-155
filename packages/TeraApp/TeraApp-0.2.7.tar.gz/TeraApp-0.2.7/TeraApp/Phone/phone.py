import requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.base import Builder
import os
import time
import sys

os.environ['KIVY_NO_FILELOG'] = '1'

class TeraAppPhone:
  def __init__(self,R,G,B,Icon):

    self.window = GridLayout()
    class TeraAppPhone(App):
      def build(self):
        self.icon = Icon
        Window.clearcolor = (R,G,B,1)
        # add widgets to window


    try:
      print("[+] Starting TeraApp...")
      time.sleep(0.5)
      print("[+] TeraApp Is RUNNING")
      TeraAppPhone().run()
    except:
      print("\n[!] TeraApp Error, Please Check Your Code...")

  # def img(self, image):
  #   self.window.add_widget(Image(source=image))
  #
  # def txtc(self,text,color):
  #   # self.window.add_widget(
  #   #   Label(text=text)
  #   # )
  #   return Label(text="hi")

