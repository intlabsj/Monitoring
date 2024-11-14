import os, time, shutil

import pandas as pd
from FileEventEmitter import EventMaker

import pyproj

class StopEventEmitter:
    def __init__(self, car_id, fpath, stime):
        self.fpath = fpath
        self.car_id = car_id
        self.LoadingCecker()
        self.stime = stime

    def LoadingCecker(self):
        self.filelist = os.listdir(self.fpath)
        exts = ('.jpg', 'png')
        self.dir_size = 0

        while True:
            time.sleep(1)
            dir_size = self.get_dir_size()
            if dir_size == self.dir_size: break
            self.dir_size = dir_size

        self.imglist = [f for f in os.listdir(self.fpath) if f.endswith(exts)]

    def get_dir_size(self):
        total = 0
        with os.scandir(self.fpath) as entries:
            for entry in entries:
                total += entry.stat().st_size if entry.is_file() else self.get_dir_size()
        return total

    def MakeStopEvent(self, event):
        rsts = pd.read_csv(os.path.join(self.fpath, "result.csv"))

        p1 = pyproj.CRS("EPSG:32652")
        p2 = pyproj.CRS("epsg:4326")

        lati, longi = pyproj.transform(p1, p2, *rsts.values[-1][1:3])

        spath = self.stime + "_Monitored.jpg"
        if len(self.imglist) > 0:
            if event == "object":
                shutil.copy2(os.path.join(self.fpath, self.imglist[-1]),
                            os.path.join("data/output/stop/etc", self.car_id, spath))
            elif event == "vehicle":
                shutil.copy2(os.path.join(self.fpath, self.imglist[-1]),
                            os.path.join("data/output/stop/car", self.car_id, spath))

        return EventMaker(car_id=self.car_id, dtime=self.stime.replace('_', ':'), reason=event, fpath=spath, latitude=lati, longitude=longi)