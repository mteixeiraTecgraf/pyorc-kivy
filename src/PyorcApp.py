import xarray as xr
import pyorc
#import cartopy
#import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import os

import os
#os.chdir("C:/Users/Flavio Amorim/Documents/00-PUC/23.1/DM-Helio/code/pyorc/examples/ngwerere/")


import kivy
kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from random import randint
#from kivy.Image import Image

class MyWidget(Widget):
    pass

class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)

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
    count = 0
    def run2(self):
        if self.count == 0:
            self.step1()
        if self.count == 1:
            self.step2()
        self.count=self.count+1
    def step1(self):
        # uncomment line below if you want to view coordinates interactively
        dir=os.getcwd()
        video_file = "ngwerere_20191103.mp4"
        video = pyorc.Video(video_file, start_frame=0, end_frame=1)
        frame = video.get_frame(0, method="rgb")
        # plot frame on a notebook-style window
        f = plt.figure(figsize=(10, 6))
        #picture = Image(source=filename, rotation=randint(-30, 30))
        plt.imshow(frame)
        plt.savefig("1.jpg", bbox_inches="tight", dpi=72)
        self.root.add_widget(Picture(source="1.jpg", center=self.root.center))
        gcps = dict(
            src=[
                [1421, 1001],
                [1251, 460],
                [421, 432],
                [470, 607]
            ]
        )

        f = plt.figure(figsize=(16, 9))
        plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
        plt.legend()

        plt.imshow(frame)
        plt.savefig("2.jpg", bbox_inches="tight", dpi=72)
        self.root.add_widget(Picture(source="2.jpg", center=self.root.center))
        
        gcps["dst"] = [
            [642735.8076, 8304292.1190],  # lowest right coordinate
            [642737.5823, 8304295.593],  # highest right coordinate
            [642732.7864, 8304298.4250],  # highest left coordinate
            [642732.6705, 8304296.8580]  # highest right coordinate
        ]
        gcps["z_0"] = 1182.2
        height, width = frame.shape[0:2]
        #cam_config = pyorc.CameraConfig(height=height, width=width, gcps=gcps, crs=32735)
        cam_config = pyorc.CameraConfig(gcps=gcps, crs=32735)
        if 0==1:
            ax = cam_config.plot(tiles="GoogleTiles", tiles_kwargs={"style": "satellite"})
            corners = [
                [292, 817],
                [50, 166],
                [1200, 236],
                [1600, 834]
            ]
            cam_config.set_bbox_from_corners(corners)
            cam_config.resolution = 0.01
            cam_config.window_size = 25
            f = plt.figure(figsize=(10, 6))
            plt.imshow(frame)
            
            plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
            plt.plot(*zip(*corners), "co", label="Corners of AOI")
            plt.legend()

        cam_config.to_file("ngwerere.json")
        #plt.savefig("3.jpg", bbox_inches="tight", dpi=72)
        #self.root.add_widget(Picture(source="3.jpg", center=self.root.center))

        return
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
        cam_config = pyorc.load_camera_config("config2.json")
        video_file = "ngwerere_20191103.mp4"
        video = pyorc.Video(video_file, camera_config=cam_config, start_frame=0, end_frame=125)
        print(video)
        da = video.get_frames()
        da[0].frames.plot(cmap="gray")
        #plt.imshow(frame)
        #plt.savefig("2.jpg", bbox_inches="tight", dpi=72)

        da_norm = da.frames.normalize()
        da_norm[0].frames.plot(cmap="gray")
        f = plt.figure(figsize=(16, 9))
        da_norm_proj = da_norm.frames.project()
        da_norm_proj[0].frames.plot(cmap="gray")

        piv = da_norm_proj.frames.get_piv()
        delayed_obj = piv.to_netcdf("ngwerere_piv.nc", compute=False)
        print(delayed_obj)
        return
        with ProgressBar():
            results = delayed_obj.compute()
if __name__ == '__main__':
    PyorcApp().run()
