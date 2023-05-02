

from devcontroller import DeviceController

class MockDevController(DeviceController):
    def __init__(self, root):
        super().__init__(root)
        pass

    def get_video(self):
        video_file = "ngwerere_20191103.mp4"
        return video_file
    def get_picture(self):
        video_file = "ngwerere_20191103.mp4"
        return video_file
    def take_picture(self):
        print("Ola")
        self.callback(self.get_picture())
    def take_video(self):
        print("Ola")
        self.callback(self.get_video())