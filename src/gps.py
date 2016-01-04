import subprocess
import logging
import re
import os


class GPS(object):

    def __init__(self, config):
        self.logger = logging.getLogger()
        print(__name__)
        self.logger.info('name is {0}'.format(__name__))
        self.logger.info('logging level is {0}'.format(self.logger.getEffectiveLevel()))
        self.config = config
        self.tracks_re = re.compile(self.config.input_filename_re)

    @property
    def mounted(self):
        self.logger.debug('calling gps.mounted()')
        try:
            stats = os.statvfs(self.config.mount_path)
            self.logger.debug('Found GPS at path: %s with blocks free: %s',
                              self.config.mount_path,
                              stats.f_bfree)
        except OSError:
            self.logger.debug('Unable to locate GPS at path: {0}'.format(self.config.mount_path))
            return False
        return True

    @property
    def tracks(self):
        tracks_path = os.path.expandvars(os.path.join(self.config.mount_path, self.config.tracks_path))
        self.logger.debug('Looking up activities in path: {0}'.format(tracks_path))
        try:
            raw_tracks = os.listdir(tracks_path)
        except FileNotFoundError:
            self.logger.error('Expected to find the GPS mounted at {0}, but could not find it.'.format(tracks_path))
            return []
        tracks = [os.path.join(tracks_path, track) for track in raw_tracks if self.tracks_re.match(track)]
        for track in tracks:
            self.logger.debug('Found track file: {0}'.format(track))
        return tracks

    def unmount(self):
        """
        :rtype:None
        """
        self.logger.debug('Attempting to unmount the GPS.')
        # diskutil unmount /Volumes/GARMIN or umount /media/user/GARMIN
        unmount_subcmd = self.config.unmount_subcmd
        cmd = [self.config.unmount_cmd]
        if unmount_subcmd:
            cmd.append(unmount_subcmd)
        cmd.append(self.config.mount_path)

        sub = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            (stderr, stdout) = sub.communicate(timeout=30)
        except subprocess.TimeoutExpired as ex:
            self.logger.error(ex)
            sub.kill()
            (stderr, stdout) = sub.communicate()

        # TODO: check return value and possibly provide more info to user

        if stderr:
            # TODO: double check how to deal with a stream object
            self.logger.error('unmount "error": {0}'.format(stderr.decode()))
        if stdout:
            self.logger.debug('unmount output: {0}'.format(stdout.decode()))
