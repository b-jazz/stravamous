
import logging
import os

import gpxpy
import gpxpy.geo
import gpxpy.gpx


class Splices(object):

    def __init__(self, config):
        self.logger = logging.getLogger()
        self.config = config
        self.splices = self.config.splices
        self.precision = self.splices.precision
        self.outbounds = []
        self.inbounds = []
        for outbound in self.splices.outbounds:
            d = dict()
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
        self.logger.debug('outbound_splice_for_gpx named: {0}'.format(g.name))
        for outbound in self.outbounds:
            (location, track_no, track_segment_no, track_point_no) = g.get_nearest_location(outbound['location'])
            dist = location.distance_2d(outbound['location'])
            if dist < self.precision:
                self.logger.debug('found close splice: outbound[\'location\']={0}, (l,t,s,n) = {1}'.format(outbound['location'], (str(location), track_no, track_segment_no, track_point_no)))
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
        self.logger.debug('inbound_splice_for_gpx: {0}'.format(g.name))
        for inbound in self.inbounds:
            (location, track_no, track_segment_no, track_point_no) = g.get_nearest_location(inbound['location'])
            dist = location.distance_2d(inbound['location'])
            if dist < self.precision:
                self.logger.debug('found close splice: inbound[\'location\']={0}, (l,t,s,n) = {1}'.format(inbound['location'], (str(location), track_no, track_segment_no, track_point_no)))
                results = (inbound['splice_segment'], track_no, track_segment_no, track_point_no)
                return results
            else:
                self.logger.debug('too far: {0} meters - {1} and {2}'.format(dist, location, inbound['location']))
        return None, None, None, None

    #@property
    #def outbounds(self):
    #    return self.splices.outbounds
