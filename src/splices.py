
import logging
import os

import gpxpy
import gpxpy.geo
import gpxpy.gpx


class Splices(object):

    def __init__(self, config):
        """
        :param config:
        :type config:
        :return:
        :rtype:
        """
        self.logger = logging.getLogger()
        self.config = config
        self.splices = self.config.splices
        self.precision = self.splices.precision
        self.outbounds = []
        self.inbounds = []

        for outbound in self.splices.outbounds:
            d = dict()
            d['name'] = outbound['name']
            d['location'] = gpxpy.geo.Location(outbound['location'][0], outbound['location'][1])
            d['splice_path'] = outbound['splice_path']
            outbound_path = os.path.expanduser(os.path.join(self.splices['root_path'], outbound['splice_path']))
            with open(outbound_path, 'r') as outbound_fd:
                outbound_xml = outbound_fd.read()
                d['splice_segment'] = gpxpy.parse(outbound_xml).tracks[0].segments[0]
                self.outbounds.append(d)
        self.logger.debug('Outbound Splices: {0}'.format(self.outbounds))
        for inbound in self.splices.inbounds:
            d = dict()
            d['name'] = inbound['name']
            d['location'] = gpxpy.geo.Location(inbound['location'][0], inbound['location'][1])
            d['splice_path'] = inbound['splice_path']
            inbound_path = os.path.expanduser(os.path.join(self.splices['root_path'], inbound['splice_path']))
            with open(inbound_path, 'r') as inbound_fd:
                inbound_xml = inbound_fd.read()
                d['splice_segment'] = gpxpy.parse(inbound_xml).tracks[0].segments[0]
                self.inbounds.append(d)
        self.logger.debug('Inbound Splices: {0}'.format(self.inbounds))

    def outbound_splice_for_gpx(self, g):
        """
        :type g: GPX
        :rtype: (GPXTrackSegment, int, int, int)

        Return the first splice that is within the precision desired of the
        first track and first segment.
        """
        self.logger.debug('searching for outbound splice for gpx dated: {0}'.format(g.tracks[0].segments[0].points[0].time))
        for outbound in self.outbounds:
            (location, track_no, track_segment_no, track_point_no) = g.get_nearest_location(outbound['location'])
            dist = location.distance_2d(outbound['location'])
            if dist < self.precision:
                self.logger.debug('found close splice: name="{name}", outbound[\'location\']={location}, dist={dist}, (l,t,s,n) = {quad}'.format(
                    name=outbound['name'],
                    location=outbound['location'],
                    dist=dist,
                    quad=(str(location), track_no, track_segment_no, track_point_no)
                ))
                results = (outbound['splice_segment'], track_no, track_segment_no, track_point_no)
                return results
            else:
                self.logger.debug('too far: {0} meters - {1} and {2}'.format(dist, location, outbound['location']))
        return None, None, None, None

    def inbound_splice_for_gpx(self, g):
        """
        :type g: GPX
        :rtype: (GPXTrackSegment, int, int, int)

        Return the first splice that is within the precision desired of the
        first track and first segment.
        """
        self.logger.debug('searching for inbound splice for gpx dated: {0}'.format(g.tracks[0].segments[0].points[0].time))
        # TODO: only compare second half of segment, but return index based on entire segment
        halfway_index = len(g.tracks[0].segments[0].points) // 2
        second_half = gpxpy.gpx.GPXTrackSegment(g.tracks[0].segments[0].points[halfway_index:])
        for inbound in self.inbounds:
            (location, track_point_no) = second_half.get_nearest_location(inbound['location'])
            dist = location.distance_2d(inbound['location'])
            if dist < self.precision:
                self.logger.debug('found close splice: name="{name}", inbound[\'location\']={location}, dist={dist}, (l,n) = {tuple}'.format(
                    name=inbound['name'],
                    location=inbound['location'],
                    dist=dist,
                    tuple=(str(location), track_point_no)
                ))
                results = (inbound['splice_segment'], 0, 0, halfway_index + track_point_no)
                return results
            else:
                self.logger.debug('too far: {0} meters - {1} and {2}'.format(dist, location, inbound['location']))
        return None, None, None, None

    #@property
    #def outbounds(self):
    #    return self.splices.outbounds

