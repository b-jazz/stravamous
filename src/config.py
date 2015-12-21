from configurati import optional

debug = optional(type=bool, default=False)

# all files that will used by stravamous will be stored here, including any user-specified configuration files
storage = {'root_path': optional(type=str, default='~/.stravamous'),
           'db': optional(type=str, default='progress.db'),
           'config': optional(type=str, default='config'),  # TODO: pull this out if unused.
           'backup_path': optional(type=str, default='input_files'),
           'input_filename_re': optional(type=str, default=r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}.fit$'),
           'output_filename_format': optional(type=str, default='%Y-%M-%D'),
           'converted_path': optional(type=str, default='converted_files'),
           'spliced_path': optional(type=str, default='spliced_files')}

# How often do you want to stat the filesystem and see if your device is mounted.
pollworker = {'frequency': optional(type=float, default=60.0)}

# The goal is to run continuously and as soon as you plug in your GPS, it will notice it and convert
# the file for you.
run_options = {'once': optional(type=int, default=0)}

gps = {'mount_path': optional(type=str, default='/Volumes/GARMIN'),
       'tracks_path': optional(type=str, default='Garmin/Activities'),
       'unmount': optional(type=int, default=1),
       'unmount_cmd': optional(type=str, default='/bin/umount'),
       'unmount_subcmd': optional(type=str, default=None)}

gpsbabel = {'exe': optional(type=str, default='/Applications/GPSBabelFE.app/Contents/MacOS/gpsbabel')}

splices = {'root_path': optional(type=str, default='~/.stravamous/splices'),
           'precision': optional(type=int, default=25),
           'outbounds': optional(type=list, default=[]),
           'inbounds': optional(type=list, default=[])}
