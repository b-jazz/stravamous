__author__ = 'bryce'

import logging
import re
import os


class GPS(object):

    def __init__(self, config):
        self.logger = logging.getLogger()
        print(__name__)
        self.logger.info('name is {0}'.format(__name__))
        self.logger.info('level is {0}'.format(self.logger.getEffectiveLevel()))
        self.config = config
        self.tracks_re = re.compile(self.config.storage.input_filename_re)
        pass

    @property
    def mounted(self):
        self.logger.debug('calling gps.mounted()')
        try:
            stats = os.statvfs(self.config.gps.mount_path)
            self.logger.debug('Found GPS at path: {0} with blocks free: {1}'.format(self.config.gps.mount_path,
                                                                                    stats.f_bfree))
        except OSError:
            self.logger.debug('Unable to locate GPS at path: {0}'.format(self.config.gps.mount_path))
            return False
        return True

    @property
    def tracks(self):
        tracks_path = os.path.expanduser(os.path.join(self.config.gps.mount_path, self.config.gps.tracks_path))
        self.logger.debug('Looking up activities in path: {0}'.format(tracks_path))
        raw_tracks = os.listdir(tracks_path)
        tracks = [os.path.join(tracks_path, track) for track in raw_tracks if self.tracks_re.match(track)]
        for track in tracks:
            self.logger.debug('Found track file: {0}'.format(track))
        return tracks

    def unmount(self):
        pass
