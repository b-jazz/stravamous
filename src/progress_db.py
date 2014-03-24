__author__ = 'bryce'

import logging
import os
import pickle


class ProgressDB(object):

    def __init__(self, config):
        self.logger = logging.getLogger()

        db_path = os.path.join(config.storage.root_path, config.storage.db)
        db_path = os.path.expanduser(db_path)
        try:
            db_file = open(db_path, 'r')
        except IOError as exception:
            self.logger.debug('DB file at {0} isn\'t readable: {1}. Using empty set of processed files.'.format(db_path, exception))
            self.progress_list = []
        else:
            unpickler = pickle.Unpickler(db_file)
            self.progress_list = unpickler.load()
            db_file.close()
