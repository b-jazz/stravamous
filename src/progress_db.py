__author__ = 'bryce'

import logging
import os
import pickle


class ProgressDB(object):

    def __init__(self, config):
        self.logger = logging.getLogger()

        self.db_path = os.path.join(config.storage.root_path, config.storage.db)
        self.db_path = os.path.expanduser(self.db_path)
        try:
            db_file = open(self.db_path, 'rb')
        except IOError as exception:
            self.logger.debug('DB file at {0} isn\'t readable: {1}. Using empty set of processed files.'.format(self.db_path, exception))
            self.progress_dict = {}
        else:
            unpickler = pickle.Unpickler(db_file)
            self.progress_dict = unpickler.load()
            db_file.close()

    def _write(self):
        self.logger.debug('Writing out new pickled version of progress database.')
        with open(self.db_path, 'wb') as fd:
            pickle.dump(self.progress_dict, fd)

    def add(self, entry):
        self.logger.debug('Appending ({0}) to progress_list.'.format(entry))
        self.progress_dict[os.path.basename(entry)] = entry
        self._write()

    def exists(self, entry):
        if os.path.basename(entry) in self.progress_dict:
            return True
        return False

    def dump(self):
        self.logger.debug('Dumping database entries: ({0})'.format(self.progress_dict))

