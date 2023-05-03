import xarray as xr
import pyorc
import matplotlib.pyplot as plt
from basic_model import Picture
from matplotlib.colors import Normalize
#import cartopy
#import cartopy.crs as ccrs

from  kivy.uix.image import Image
from dask.diagnostics import ProgressBar
import os

class Application:
    def __init__(self, device):
        self.device = device
        self.root = device.root

    def get_video_and_configure_camera(self, video):
        # uncomment line below if you want to view coordinates interactively
        dir=os.getcwd()
        #video_file = self.controller.get_video()
        video_file = video
        video = pyorc.Video(video_file, start_frame=0, end_frame=1)
        frame = video.get_frame(0, method="rgb")
        # plot frame on a notebook-style window
        f = plt.figure(figsize=(10, 6))
        #picture = Image(source=filename, rotation=randint(-30, 30))
        plt.imshow(frame)
        self.saveAndAdd("1.1.jpg")
        gcps = self._mark_points_in_Picture(frame)

        f = plt.figure(figsize=(16, 9))
        plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
        plt.legend()

        plt.imshow(frame)
        self.saveAndAdd("1.2.jpg")
        gcps["dst"] = self._enter_world_coordinates()
        gcps["z_0"] = self._enter_z0()
        height, width = frame.shape[0:2]
        #cam_config = pyorc.CameraConfig(height=height, width=width, gcps=gcps, crs=32735)
        cam_config = pyorc.CameraConfig(gcps=gcps, crs=32735)
        if 0==1:
            ax = cam_config.plot(tiles="GoogleTiles", tiles_kwargs={"style": "satellite"})
            print(ax)
            print("Tiles gootle print")
            self.saveAndAdd("1.2b.jpg")
        corners = [
            [292, 817],
            [50, 166],
            [1200, 236],
            [1600, 834]
        ]
        #cam_config.set_bbox_from_corners(corners)
        cam_config.set_corners(corners)
        cam_config.resolution = 0.01
        cam_config.window_size = 25
        f = plt.figure(figsize=(10, 6))
        plt.imshow(frame)
        
        plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
        plt.plot(*zip(*corners), "co", label="Corners of AOI")
        plt.legend()
        self.saveAndAdd("1.3.jpg")

        #ax1 = cam_config.plot(tiles="GoogleTiles", tiles_kwargs={"style": "satellite"})
        #f = plt.figure()
        #ax2 = plt.axes()
        #ax2.imshow(frame)
        #cam_config.plot(ax=ax2, camera=True)

        #plt.savefig(self.pathOf("ngwerere_camconfig.jpg"), bbox_inches="tight", dpi=72)


        cam_config.to_file(self.pathOf("ngwerere.json"))
        #plt.savefig("3.jpg", bbox_inches="tight", dpi=72)
        #self.root.add_widget(Picture(source="3.jpg", center=self.root.center))

        return
    
    def pathOf(self,name):
        ret =  self.device.pathOf(name)
        print("Path returned "+ret)
        return ret

    def saveAndAdd(self, name):
        name=self.pathOf(name)
        plt.savefig(name, bbox_inches="tight", dpi=72)
        self.root.add_widget(Picture(source=name, center=self.root.center))
        #self.root.add_widget(Image(source=name, size=self.root.size, center=self.root.center))
        
    
    def _mark_points_in_Picture(self,frame):
        gcps = dict(
            src=[
                [1421, 1001],
                [1251, 460],
                [421, 432],
                [470, 607]
            ]
        )
        return gcps

    def _enter_world_coordinates(self):
        return [
            [642735.8076, 8304292.1190],  # lowest right coordinate
            [642737.5823, 8304295.593],  # highest right coordinate
            [642732.7864, 8304298.4250],  # highest left coordinate
            [642732.6705, 8304296.8580]  # highest right coordinate
        ]
    def _enter_z0(self):
        return 1182.2
    def process_video_piv(self):
        
        cam_config = pyorc.load_camera_config(self.pathOf("config2.json"))
        video_file = self.pathOf("ngwerere_20191103.mp4")
        video = pyorc.Video(video_file, camera_config=cam_config, start_frame=0, end_frame=125)
        print(video)
        da = video.get_frames()
        da[0].frames.plot(cmap="gray")
        self.saveAndAdd("2.1.jpg")
        #plt.imshow(frame)
        #plt.savefig("2.jpg", bbox_inches="tight", dpi=72)

        da_norm = da.frames.normalize()
        da_norm[0].frames.plot(cmap="gray")
        f = plt.figure(figsize=(16, 9))
        da_norm_proj = da_norm.frames.project()
        da_norm_proj[0].frames.plot(cmap="gray")
        self.saveAndAdd("2.2.jpg")


        print("PreGeograph")
        da_rgb = video.get_frames(method="rgb")
        da_rgb_proj = da_rgb.frames.project()

        if 0==1:
            p = da_rgb_proj[0].frames.plot(mode="geographical")
        
            print("PreCartoImport")
            import cartopy.io.img_tiles as cimgt
            import cartopy.crs as ccrs
            tiles = cimgt.GoogleTiles(style="satellite")
            print("Preaxis")
            p.axes.add_image(tiles, 19)
            p.axes.set_extent([
                da_rgb_proj.lon.min() - 0.0001,
                da_rgb_proj.lon.max() + 0.0001,
                da_rgb_proj.lat.min() - 0.0001,
                da_rgb_proj.lat.max() + 0.0001],
                crs=ccrs.PlateCarree()
            )
            self.saveAndAdd("5b.jpg")

        piv = da_norm_proj.frames.get_piv()
        delayed_obj = piv.to_netcdf(self.pathOf("ngwerere_piv.nc"), compute=False)
        print(delayed_obj)
    
    def filter_velocity_noise(self):
        
        
        f = plt.figure(figsize=(10, 6))
        ds = xr.open_dataset(self.pathOf("ngwerere_piv.nc"))
        video_file = self.pathOf("ngwerere_20191103.mp4")
        video = pyorc.Video(video_file, start_frame=0, end_frame=125)
        video.camera_config = ds.velocimetry.camera_config
        da_rgb = video.get_frames(method="rgb")
        da_rgb_proj = da_rgb.frames.project()
        p = da_rgb_proj[0].frames.plot()
        self.saveAndAdd("3.1.jpg")
        ds_mean = ds.mean(dim="time", keep_attrs=True)
        ds_mean.velocimetry.plot.pcolormesh(
            ax=p.axes,
            alpha=0.3,
            cmap="rainbow",
            add_colorbar=True,
            vmax=0.6
        )
        ds_mean.velocimetry.plot(
            ax=p.axes,
            color="w",
            alpha=0.5,
            width=0.0015,
        )
        self.saveAndAdd("3.2.jpg")

        ds_filt = ds.velocimetry.filter_temporal()
        ds_mean_filt = ds_filt.mean(dim="time", keep_attrs=True)
        p = da_rgb_proj[0].frames.plot()
        ds_mean_filt.velocimetry.plot(
            ax=p.axes,
            alpha=0.4,
            cmap="rainbow",
            scale=20,
            width=0.0015,
            norm=Normalize(vmax=0.6, clip=False),
            add_colorbar=True
        )
        self.saveAndAdd("3.3.jpg")

        import numpy as np
        ds_filt2 = ds.velocimetry.filter_temporal(kwargs_angle=dict(angle_tolerance=0.5*np.pi))
        ds_filt2.velocimetry.filter_spatial(filter_nan=False, inplace=True, kwargs_median=dict(wdw=2))
        ds_mean_filt2 = ds_filt2.mean(dim="time", keep_attrs=True)
        p = da_rgb_proj[0].frames.plot()

        ds_mean_filt2.velocimetry.plot(
            ax=p.axes,
            alpha=0.4,
            cmap="rainbow",
            scale=20,
            width=0.0015,
            norm=Normalize(vmax=0.6, clip=False),
            add_colorbar=True
        )
        self.saveAndAdd("3.4.jpg")

        #p = da_rgb_proj[0].frames.plot(mode="geographical")
        
        p = da_rgb[0].frames.plot(mode="camera")
        ds_mean_filt2.velocimetry.plot(
            ax=p.axes,
            mode="camera",
            alpha=0.4,
            cmap="rainbow",
            scale=200,
            width=0.0015,
            norm=Normalize(vmin=0., vmax=0.6, clip=False),
            add_colorbar=True
        )
        self.saveAndAdd("3.5.jpg")
        ds_filt2.velocimetry.set_encoding()
        ds_filt2.to_netcdf(self.pathOf("ngwerere_filtered.nc"))
        frame = video.get_frame(0, method="rgb")
        #da_rgb_proj[0].frames.to_video("3-1.mp4")
        #print(da_rgb_proj[0].frames)
        #plt.imshow(frame)
        p.axes.figure.savefig(self.pathOf("3-1.jpg"), dpi=200)

    def plot_velocity(self):
        
        import pandas as pd
        ds = xr.open_dataset(self.pathOf("ngwerere_filtered_input.nc"))

        # also open the original video file
        video_file = self.pathOf("ngwerere_20191103.mp4")
        video = pyorc.Video(video_file, start_frame=0, end_frame=1)

        # borrow the camera config from the velocimetry results
        video.camera_config = ds.velocimetry.camera_config

        # get the frame as rgb
        da_rgb = video.get_frames(method="rgb")

        cross_section = pd.read_csv(self.pathOf("ngwerere_cross_section.csv"))
        x = cross_section["x"]
        y = cross_section["y"]
        z = cross_section["z"]
        cross_section2 = pd.read_csv(self.pathOf("ngwerere_cross_section_2.csv"))
        x2 = cross_section2["x"]
        y2 = cross_section2["y"]
        z2 = cross_section2["z"]


        ds_points = ds.velocimetry.get_transect(x, y, z, crs=32735, rolling=4)
        ds_points2 = ds.velocimetry.get_transect(x2, y2, z2, crs=32735, rolling=4)
        ds_points_q = ds_points.transect.get_q()
        ds_points_q2 = ds_points2.transect.get_q()
        ax = plt.axes()
        ds_points_q["v_eff"].isel(quantile=2).plot(ax=ax)
        ds_points_q2["v_eff"].isel(quantile=2).plot(ax=ax)
        plt.grid()

        from matplotlib.colors import Normalize
        norm = Normalize(vmin=0., vmax=0.6, clip=False)
        p = da_rgb[0].frames.plot(mode="camera")
        ds.mean(dim="time", keep_attrs=True).velocimetry.plot(
            ax=p.axes,
            mode="camera",
            cmap="rainbow",
            scale=200,
            width=0.001,
            alpha=0.3,
            norm=norm,
        )
        ds_points_q.isel(quantile=2).transect.plot(
            ax=p.axes,
            mode="camera",
            cmap="rainbow",
            scale=100,
            width=0.003,
            norm=norm,
        )
        ds_points_q2.isel(quantile=2).transect.plot(
            ax=p.axes,
            mode="camera",
            cmap="rainbow",
            scale=100,
            width=0.003,
            norm=norm,
            add_colorbar=True
        )
        p.axes.figure.savefig(self.pathOf("ngwerere.jpg"), dpi=200)
        
        self.root.add_widget(Picture(source=self.pathOf("ngwerere.jpg"), center=self.root.center))
        
        norm = Normalize(vmin=0, vmax=0.6, clip=False)
        ds_mean = ds.mean(dim="time", keep_attrs=True)
        p = da_rgb.frames.project()[0].frames.plot(mode="local")
        
        self.saveAndAdd("4.2.jpg")
        ds_points_q.isel(quantile=2).transect.plot(
            ax=p.axes,
            mode="local",
            cmap="rainbow",
            scale=10,
            width=0.003,
            norm=norm,
            add_colorbar=True,
        )
        ds_points_q2.isel(quantile=2).transect.plot(
            ax=p.axes,
            mode="local",
            cmap="rainbow",
            scale=10,
            width=0.003,
            norm=norm,
            add_colorbar=True,
        )
        ds_mean.velocimetry.plot.streamplot(
            ax=p.axes,
            mode="local",
            density=3.,
            minlength=0.05,
            linewidth_scale=2,
            cmap="rainbow",
            norm=norm,
            add_colorbar=True
        )
        ds_points_q.transect.get_river_flow()
        print(ds_points_q["river_flow"])
        ds_points_q2.transect.get_river_flow()
        print(ds_points_q2["river_flow"])
        self.saveAndAdd("4.3.jpg")
        
    
    def camera_calibration(self):
        return
        import matplotlib.pyplot as plt
        import cv2
        import copy
        import glob
        import numpy as np
        import os
        f = plt.figure()
        fn = os.path.join("camera_calib","camera_calib_720p.mkv")
        vid = pyorc.Video(fn, start_frame=0, end_frame=5)
        frame = vid.get_frame(0, method="rgb")
        plt.imshow(frame)
        self.saveAndAdd("5.1.jpg")
        cam_config = pyorc.CameraConfig()

        #cam_config.set_lens_calibration(fn, chessboard_size=(11, 8), frame_limit=50)
        cam_config.set_lens_calibration(fn, chessboard_size=(9, 6), plot=False, to_file=True)

        print(f"Camera Matrix: {cam_config.camera_matrix}")
        print(f"Distortion coefficients: {cam_config.dist_coeffs}")

        paths = glob.glob(os.path.join("camera_calib", "*.png"))

        cols = 3
        rows = int(np.ceil(len(paths)/cols))
        rows, cols
        f = plt.figure(figsize=(16, 3*rows))
        for n, fn in enumerate(paths):
            ax = plt.subplot(rows, cols, n + 1)
            img = cv2.imread(fn)
            # switch colors
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ax.imshow(img)
            ax.tick_params(
                left=False,
                right=False,
                labelleft=False,
                labelbottom=False,
                bottom=False,
            )
        import cv2
        import matplotlib.pyplot as plt
        fn = os.path.join("camera_calib","camera_calib_720p.mkv")

        # open without camera configuration
        vid = pyorc.Video(fn)
        frame = vid.get_frame(0, method="rgb")

        # open the video once more
        vid_undistort = pyorc.Video(fn, camera_config=cam_config, start_frame=0, end_frame=5)
        # extract the first frame once more
        frame_undistort = vid_undistort.get_frame(0, method="rgb")
        diff = np.mean(np.int16(frame) - np.int16(frame_undistort), axis=-1)

        f = plt.figure(figsize=(16, 16))
        ax1 = plt.axes([0.05, 0.45, 0.3, 0.2])
        ax2 = plt.axes([0.45, 0.45, 0.3, 0.2])
        ax3 = plt.axes([0.1, 0.05, 0.6, 0.4])
        cax = plt.axes([0.75, 0.1, 0.01, 0.2])
        ax1.set_title("Original")
        ax2.set_title("Undistorted")
        ax3.set_title("Difference")
        ax1.imshow(frame)
        ax2.imshow(frame_undistort)

        # make some modern art for the difference
        p = ax3.imshow(diff, cmap="RdBu", vmin=-100, vmax=100)
        plt.colorbar(p, cax=cax, extend="both")
        
        self.saveAndAdd("5.2.jpg")