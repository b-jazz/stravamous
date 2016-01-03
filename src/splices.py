
import logging
import os

import gpxpy
import gpxpy.geo
import gpxpy.gpx


class Splices(object):

    def __init__(self, config):
        """
        @param config:
        @type config:
        @return:
        @rtype:
        """
        self.logger = logging.getLogger()
        self.config = config
        self.precision = self.config.splices.precision
        self.splices = dict()
        self.splices['outbound'] = self.discover_splices('outbound')
        self.splices['inbound'] = self.discover_splices('inbound')

        self.logger.debug('inbound splices:  %s' % self.splices['inbound'])
        self.logger.debug('outbound splices: %s' % self.splices['outbound'])

    def discover_splices(self, direction):
        """
        Look in the splices' root directory for direction ("inbound"/"outbound") directories,
        and enumerate through the files alphabetically looking for available splices

        @param direction: "inbound" or "outbound" indicator of direction from start
        @type direction: str
        @return: available splices for that direction, sorted alphetically
        @rtype: list
        """
        direction_path = os.path.expanduser(os.path.join(self.config.splices['root_path'], direction))
        splices = []
        for item in sorted(os.listdir(direction_path)):
            gpx = self.gpx_for_path(os.path.join(direction_path, item))
            if gpx:
                d = dict()
                d['name'] = gpx.tracks[0].name
                d['splice_segment'] = gpx.tracks[0].segments[0]
                # might need to change 'location' below from a GPXTrackPoint to a Location
                d['location'] = self.point_for_segment_direction(d['splice_segment'], direction)
                splices.append(d)
        return splices

    def point_for_segment_direction(self, track_seg, direction):
        """
        Return the last point of an outbound segment, or the first point of an inbound
        segment.

        @param track_seg: segment of interest
        @type track_seg: GPXTrackSegment
        @param direction: 'outbound' or 'inbound'
        @type direction: str
        @return: splice point depending on direction
        @rtype: GPXTrackPoint
        """
        if direction == 'outbound':
            return track_seg.points[-1]
        if direction == 'inbound':
            return track_seg.points[0]


    def gpx_for_path(self, path):
        """
        Given a full path name, attempt to open the file and create a GPX object from it.
        Return None if the path is a directory or not a gpx file, or a gpx file that isn't
        well formed.

        @param path: full pathname to a gpx file
        @type path: str
        @return: a GPX object representing the gpx file
        @rtype: GPX
        """
        if os.path.isdir(path):
            return None

        try:
            gpx_xml = open(path, 'r').read()
        except OSError:
            self.logger.debug('Unable to process gpx file: %s' % path)
            return None

        try:
            gpx = gpxpy.parse(gpx_xml)
        except gpxpy.GPXException as ex:
            self.logger.debug('Unable to parse GPX file: %s. Leaving out of splices. %s' %
                              (path, ex))
            return None

        return gpx

    def outbound_splice_for_gpx(self, g):
        """
        :type g: GPX
        :rtype: (GPXTrackSegment, int, int, int)

        Return the first splice that is within the precision desired of the
        first track and first segment.
        """
        self.logger.debug('Searching for outbound splice for gpx dated: {0}'.format(g.tracks[0].segments[0].points[0].time))
        self.logger.debug('TrksSegsPts: {0}/{1}/{2}'.format(len(g.tracks),
                                                            len(g.tracks[0].segments),
                                                            len(g.tracks[0].segments[0].points)))
        halfway_index = len(g.tracks[0].segments[0].points) // 2
        first_half = gpxpy.gpx.GPXTrackSegment(g.tracks[0].segments[0].points[0:halfway_index])
        for outbound in self.splices['outbound']:
            (location, track_point_no) = first_half.get_nearest_location(outbound['location'])
            dist = location.distance_2d(outbound['location'])
            if dist < self.precision:
                self.logger.debug('Found close splice: name="{name}", outbound[\'location\']={location}, dist={dist}m, (l,n) = {tuple}'.format(
                    name=outbound['name'],
                    location=outbound['location'],
                    dist=dist,
                    tuple=(str(location), track_point_no)
                ))
                results = (outbound['splice_segment'], 0, 0, track_point_no)
                return results
            else:
                self.logger.debug('Too far: {0}m - {1} and {2}'.format(dist, location, outbound['location']))
        return None, None, None, None

    def inbound_splice_for_gpx(self, g):
        """
        :type g: GPX
        :rtype: (GPXTrackSegment, int, int, int)

        Return the first splice that is within the precision desired of the
        first track and first segment.
        """
        self.logger.debug('Searching for inbound splice for gpx dated: {0}'.format(g.tracks[0].segments[0].points[0].time))

        self.logger.debug('TrksSegsPts: {0}/{1}/{2}'.format(len(g.tracks),
                                                            len(g.tracks[0].segments),
                                                            len(g.tracks[0].segments[0].points)))
        halfway_index = len(g.tracks[0].segments[0].points) // 2
        second_half = gpxpy.gpx.GPXTrackSegment(g.tracks[0].segments[0].points[halfway_index:])
        self.logger.debug('Halfway index: {0}, point: {1}'.format(halfway_index, second_half.points[0]))
        for inbound in self.splices['inbound']:
            (location, track_point_no) = second_half.get_nearest_location(inbound['location'])
            dist = location.distance_2d(inbound['location'])
            if dist < self.precision:
                self.logger.debug('Found close splice: name="{name}", inbound[\'location\']={location}, dist={dist}m, (l,n) = {tuple}'.format(
                    name=inbound['name'],
                    location=inbound['location'],
                    dist=dist,
                    tuple=(str(location), track_point_no)
                ))
                results = (inbound['splice_segment'], 0, 0, halfway_index + track_point_no)
                return results
            else:
                self.logger.debug('Too far: {0}m - {1} and {2}'.format(dist, location, inbound['location']))
        return None, None, None, None

    # @property
    # def outbounds(self):
    #    return self.splices.outbounds
