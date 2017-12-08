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

    def path(self):
        return self.meta.get('server_filename')
    def is_dir(self):
        return self.meta.get("isDir")
    def mtime(self):
        return self.meta.get("local_mtime")
    def sub_entries(self):
        return self.meta.get()


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
        local_exist = os.path.exists(lpath)
        if local_exist:
            lmeta = os.stat(lpath)

        if rmeta.is_dir():
            if not local_exist:
                os.mkdir(lpath, 0o755);
            sub_metas = [RemoteMeta(meta) for meta in self.pcs.list_files(rpath).json()['list']]
            for meta in sub_metas:
                self.sync_one(path + "/" + meta.path())
        elif not local_exist or lmeta.st_mtime < rmeta.mtime():
            # if is newer file, download
            response = self.pcs.download(rpath)
            logging.debug("downloading %s", path)
            # todo: get response content to local file


