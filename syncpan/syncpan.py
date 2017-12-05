import os
import time
import logging
from baidupcsapi import PCS


class RemoteMeta(object):
    """
     remote metadata
     """
    meta = {}

    def __init__(self, meta_dict):
        self.meta = meta_dict

    def is_dir(self):
        return self.meta.get("isDir")
    def mtime(self):
        return self.meta.get("local_mtime")


class SyncPan(object):
    """
    BaiduNetDisk one-way sync
    Parse remote paths' incremental dir files, download to local
    """
    pcs = None
    sync_paths = None
    period = 10
    remote_root = "/"
    local_root = "/home/pi/pan"

    def __init__(self, username, password, sync_paths=None, period=10):
        self.pcs = PCS(username, password)
        if sync_paths is not None:
            self.sync_paths = sync_paths
        self.period = period

    def run(self):
        next_run = time.time()
        while True:
            now = time.time()
            if now < next_run:
                time.sleep(0.1)
                continue
            next_run = now + self.period
            self.sync_all()
            pass
        pass

    def sync_all(self):
        for path in self.sync_paths:
            try:
                self.sync_one(path)
            except Exception:
                logging.warn("sync %s failed", path)
                pass
            pass
        pass

    def sync_one(self, path):
        rpath = self.remote_root + "/" + path
        lpath = self.local_root + "/" + path
        rmeta = RemoteMeta(self.pcs.meta(rpath).json()['info'][0])
        lmeta = os.stat(lpath)
        # if is file, nop or download
        if not rmeta.is_dir():
            if not os.path.exists(lpath) or lmeta.st_mtime < rmeta.mtime():
                response = self.pcs.download(rpath)
                # todo: get response content to local file



        # if is directory,
        # 1. get local path attributes
        # 2. get remote path attributes
        # 3. if remote is newer, list remote contents
        # 4. recursive sync_one
        pass



