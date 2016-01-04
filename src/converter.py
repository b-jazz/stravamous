import logging
import os
import subprocess


def out_for_in(in_path):
    return '{0}.gpx'.format(os.path.splitext(os.path.basename(in_path))[0])


class Converter(object):

    def __init__(self, config, input_path):
        self.config = config
        self.logger = logging.getLogger()
        self.input_file = input_path
        self.output_file = os.path.expanduser(os.path.join(self.config.storage_root,
                                                           'converted_files',
                                                           out_for_in(self.input_file)))
        self.logger.debug('Created converter object with input_file of {0} and output_file of {1}'.format(self.input_file, self.output_file))
        self.gpx_text = None

    def convert(self):
        command = [self.config.gpsbabel_exe,
                   '-i', 'garmin_fit',
                   '-f', self.input_file,
                   '-o', 'gpx,garminextensions',
                   '-F', self.output_file]
        self.logger.debug('starting subprocess with command: {0}'.format(command))
        try:
            subprocess.call(command)
            self.logger.debug('Happily done with the conversion. No exceptions.')
        except Exception as exception:
            self.logger.error('CONVERTER EXCEPTION: {0}'.format(exception))
            # raise
        else:
            self.logger.debug('Opening {0} for read'.format(self.output_file))
            try:
                self.gpx_text = open(self.output_file, 'r').read()
            except Exception as exception:
                self.logger.error('open().read() exception: {0}, of type: {1}'.format(exception, exception.args))
                raise
