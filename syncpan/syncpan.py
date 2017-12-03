from baidupcsapi import PCS

class SyncPan(object):
    """
    BaiduNetDisk one-way sync
    Parse remote paths' incremental dir files, download to local
    """
    pcs = None

    def _init_(self, username, password, sync_paths=None):
        try:
            pcs = PCS(username, password)
            quota = pcs.quota().

