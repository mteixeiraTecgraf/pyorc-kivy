import xarray as xr
import pyorc
import matplotlib.pyplot as plt
from basic_model import Picture
from matplotlib.colors import Normalize

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
        self.saveAndAdd("1.jpg")
        gcps = self._mark_points_in_Picture(frame)

        f = plt.figure(figsize=(16, 9))
        plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
        plt.legend()

        plt.imshow(frame)
        self.saveAndAdd("2.jpg")
        gcps["dst"] = self._enter_world_coordinates()
        gcps["z_0"] = self._enter_z0()
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
        #cam_config.set_bbox_from_corners(corners)
        cam_config.set_corners(corners)
        cam_config.resolution = 0.01
        cam_config.window_size = 25
        f = plt.figure(figsize=(10, 6))
        plt.imshow(frame)
        
        plt.plot(*zip(*gcps["src"]), "rx", markersize=20, label="Control points")
        plt.plot(*zip(*corners), "co", label="Corners of AOI")
        plt.legend()
        self.saveAndAdd("3.jpg")

        cam_config.to_file("ngwerere.json")
        #plt.savefig("3.jpg", bbox_inches="tight", dpi=72)
        #self.root.add_widget(Picture(source="3.jpg", center=self.root.center))

        return
    
    def saveAndAdd(self, name):
        plt.savefig(name, bbox_inches="tight", dpi=72)
        self.root.add_widget(Picture(source=name, center=self.root.center))
        
    
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
        
        cam_config = pyorc.load_camera_config("config2.json")
        video_file = "ngwerere_20191103.mp4"
        video = pyorc.Video(video_file, camera_config=cam_config, start_frame=0, end_frame=125)
        print(video)
        da = video.get_frames()
        da[0].frames.plot(cmap="gray")
        self.saveAndAdd("4.jpg")
        #plt.imshow(frame)
        #plt.savefig("2.jpg", bbox_inches="tight", dpi=72)

        da_norm = da.frames.normalize()
        da_norm[0].frames.plot(cmap="gray")
        f = plt.figure(figsize=(16, 9))
        da_norm_proj = da_norm.frames.project()
        da_norm_proj[0].frames.plot(cmap="gray")
        self.saveAndAdd("5.jpg")

        piv = da_norm_proj.frames.get_piv()
        delayed_obj = piv.to_netcdf("ngwerere_piv.nc", compute=False)
        print(delayed_obj)
    
    def filter_velocity_noise(self):
        
        
        f = plt.figure(figsize=(10, 6))
        ds = xr.open_dataset("ngwerere_piv.nc")
        video_file = "ngwerere_20191103.mp4"
        video = pyorc.Video(video_file, start_frame=0, end_frame=125)
        video.camera_config = ds.velocimetry.camera_config
        da_rgb = video.get_frames(method="rgb")
        da_rgb_proj = da_rgb.frames.project()
        p = da_rgb_proj[0].frames.plot()
        self.saveAndAdd("6.jpg")
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
        self.saveAndAdd("7.jpg")

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
        self.saveAndAdd("8.jpg")

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
        self.saveAndAdd("9.jpg")

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
        self.saveAndAdd("10.jpg")
        ds_filt2.velocimetry.set_encoding()
        ds_filt2.to_netcdf("ngwerere_filtered.nc")
        frame = video.get_frame(0, method="rgb")
        #da_rgb_proj[0].frames.to_video("3-1.mp4")
        #print(da_rgb_proj[0].frames)
        #plt.imshow(frame)
        p.axes.figure.savefig("3-1.jpg", dpi=200)

    def plot_velocity(self):
        
        import pandas as pd
        ds = xr.open_dataset("ngwerere_filtered_input.nc")

        # also open the original video file
        video_file = "ngwerere_20191103.mp4"
        video = pyorc.Video(video_file, start_frame=0, end_frame=1)

        # borrow the camera config from the velocimetry results
        video.camera_config = ds.velocimetry.camera_config

        # get the frame as rgb
        da_rgb = video.get_frames(method="rgb")

        cross_section = pd.read_csv("ngwerere_cross_section.csv")
        x = cross_section["x"]
        y = cross_section["y"]
        z = cross_section["z"]
        cross_section2 = pd.read_csv("ngwerere_cross_section_2.csv")
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
        p.axes.figure.savefig("ngwerere.jpg", dpi=200)
        
        self.root.add_widget(Picture(source="ngwerere.jpg", center=self.root.center))
        