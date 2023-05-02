import xarray as xr
import pyorc
#import cartopy
#import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from factory import Factory, Root
from devcontroller import DeviceController
from application import Application
from basic_model import Picture


import os
#os.chdir("C:/Users/Flavio Amorim/Documents/00-PUC/23.1/DM-Helio/code/pyorc/examples/ngwerere/")


import kivy
kivy.require('1.0.6')  # replace with your current kivy version !


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from random import randint
#from kivy.Image import Image
from matplotlib.colors import Normalize

class MyWidget(Widget):
    pass

class LoginScreen(GridLayout):
    pass
class LoginScreen2(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)
class Test(GridLayout):
    def build(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Button(text='Hello World'))



class PyorcApp(App):

    def build(self):

        self.index = 0
        self.factory = Factory()
        self.factory.provider.addSingletonInstance(Root, self.root)
        # = self.factory.provider.get(DeviceController)
        self.application = self.factory.provider.get(Application)
        self.controller = self.application.device
        self.controller.listen(self.run2)
    count = 1
    def run2(self, video):
        if self.count == 1:
            self.step1()
        if self.count == 2:
            self.step2()
        if self.count == 3:
            self.step3()
        if self.count == 4:
            self.step4()
        self.count=self.count+1

    def step1(self):
        self.step1b(self.controller.get_video())
    def step1b(self, video):
        self.application.get_video_and_configure_camera(video)
        #try:
        #    #return Button(text=dir)
        #    #return Test()
        #    #return LoginScreen()
        #    return Picture(source="ngwerere_camconfig.jpg")
        
        #except Exception as e:
        #    Logger.exception('Pictures: Unable to load <%s>' % "ngwerere_camconfig.jpg")
        ##return MyWidget()
        ##picture = Picture(source="ngwerere_camconfig.jpg", rotation=randint(-30, 30))
        
        #return picture

    def step2(self):
        self.application.process_video_piv()
        return
        with ProgressBar():
            results = delayed_obj.compute()

    def step3(self):
        self.application.filter_velocity_noise()
        
    def step4(self):
        self.application.plot_velocity()

    def take_picture(self):
        self.controller.take_picture()
        #self.run2()

    def sample(self):
        self.application.AskToSelectOrTakeVideo()
        ## With a video Selected
        self.application.GetFirstFrameAndAskToMarkPoints()
        ##

    
if __name__ == '__main__':
    PyorcApp().run()
