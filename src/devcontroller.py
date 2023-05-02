
import os

class DeviceController():
    def __init__(self, root):
        self.root = root

    def listen(self, cb):
        self.callback = cb
    def pathOf(self,name):
        os.join(os.getcwd(), "data", name)

    def get_video(self):
        pass
    def take_picture(self):
        pass
    def take_video(self):
        pass
    def __eq__(self, another):
       return hasattr(another, 'root') and self.root == another.root
    def __hash__(self):
       return hash(self.root)

    