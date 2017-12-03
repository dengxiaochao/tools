import time
from baidupcsapi import PCS

class SyncPan(object):
    """
    BaiduNetDisk one-way sync
    Parse remote paths' incremental dir files, download to local
    """
    pcs = None
    sync_paths = None
    period = 10

    def _init_(self, username, password, sync_paths=None, period=10):
        self.pcs = PCS(username, password)
        if sync_paths is not None:
            self.sync_paths = sync_paths
        self.period = period

    def run(self):
        next_run = time.time
        while True:
            now = time.time
            if now < next_run:
                time.sleep(0.1)
                continue
            next_run = now + self.period
            self.sync_all()
            pass
        pass

    def sync_all(self):
        for path in self.sync_paths:
            self.sync_one(path)
            pass
        pass

    def sync_one(self, path):
        pass


