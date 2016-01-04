import logging
import os
import pickle


class ProgressDB(object):

    def __init__(self, config):
        self.logger = logging.getLogger()

        self.db_path = os.path.expandvars(os.path.join(config.storage_root, config.progress_db))

        try:
            db_file = open(self.db_path, 'rb')
        except IOError as exception:
            self.logger.debug('DB file at {0} isn\'t readable: {1}. Using empty set of processed files.'.format(self.db_path, exception))
            self.progress_dict = {}
        else:
            unpickler = pickle.Unpickler(db_file)
            self.progress_dict = unpickler.load()
            db_file.close()

        self.previous_addition = None

    def _write(self):
        self.logger.debug('Writing out new pickled version of progress database.')
        with open(self.db_path, 'wb') as fd:
            pickle.dump(self.progress_dict, fd)

    def add(self, entry):
        self.logger.debug('Appending previous entry ({0}) to progress_list if it exists.'.format(self.previous_addition))
        if self.previous_addition is not None:
            self.progress_dict[os.path.basename(self.previous_addition)] = self.previous_addition
        self.logger.debug('Remembering new entry ({0}) to add it in the future'.format(entry))
        self.previous_addition = entry
        self._write()

    def exists(self, entry):
        if os.path.basename(entry) in self.progress_dict:
            return True
        return False

    # TODO: It might be handy to reprocess the most recent file on every run.
    #   The reasoning is you might need to make a code tweak and reprocess and don't want to have to mess
    #   with the progress database each time.

    def dump(self):
        self.logger.debug('Dumping database entries: ({0})'.format(self.progress_dict))
