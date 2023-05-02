
from jnius import autoclass, cast
from android import activity, mActivity

from os.path import exists
from kivy.clock import Clock
from functools import partial
from devcontroller import DeviceController
from PIL import Image

Intent = autoclass('android.content.Intent')
MediaStore = autoclass('android.provider.MediaStore')
Uri = autoclass('android.net.Uri')
Environment = autoclass('android.os.Environment')

class AnderoidController(DeviceController):
    def __init__(self, root):
        super().__init__(root)
        self.index = 0
        activity.bind(on_activity_result=self.on_activity_result)


    def get_filename(self):
        while True:
            self.index += 1
            fn = (Environment.getExternalStorageDirectory().getPath() +
                  '/takepicture{}.jpg'.format(self.index))
            if not exists(fn):
                return fn
    def take_picture(self):
        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        self.last_fn = self.get_filename()
        self.uri = Uri.parse('file://' + self.last_fn)
        self.uri = cast('android.os.Parcelable', self.uri)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, self.uri)
        mActivity.startActivityForResult(intent, 0x123)

    def take_video(self):
        intent = Intent(MediaStore.ACTION_VIDEO_CAPTURE)
        self.last_fn = self.get_filename()
        self.uri = Uri.parse('file://' + self.last_fn)
        self.uri = cast('android.os.Parcelable', self.uri)
        intent.putExtra(MediaStore.EXTRA_OUTPUT, self.uri)
        if(True):#intent.resolveActivity)
            mActivity.startActivityForResult(intent, 0x124)
        #  Intent takeVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
        #  if (takeVideoIntent.resolveActivity(getPackageManager()) != null) {
        #      startActivityForResult(takeVideoIntent, REQUEST_VIDEO_CAPTURE);
        #  }
        #  else {
        #  //display error state to the user
        #  }



    def on_activity_result(self, requestCode, resultCode, intent):
        if requestCode == 0x123:
            Clock.schedule_once(partial(self.add_picture, self.last_fn), 0)
        if requestCode == 0x124:
            Clock.schedule_once(partial(self.add_video, self.last_fn), 0)

    def add_picture(self, fn, *args):
        im = Image.open(fn)
        width, height = im.size
        im.thumbnail((width / 4, height / 4), Image.ANTIALIAS)
        im.save(fn, quality=95)
        #self.root.add_widget(Picture(source=fn, center=self.root.center))
        self.callback(fn)

    def add_video(self, fn, *args):
        ## im = Image.open(fn)
        ## width, height = im.size
        ## im.thumbnail((width / 4, height / 4), Image.ANTIALIAS)
        ## im.save(fn, quality=95)
        #self.root.add_widget(Picture(source=fn, center=self.root.center))
        self.callback(fn)
