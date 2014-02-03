
import gpxpy.gpx


def trim_first_20(gpx):
    """
    :type gpx: GPX

    Assume that there is only one track and only one track segement. Remove the first twenty track
    points from that track segment.
    """
    if gpx.tracks[0] and gpx.tracks[0].segments[0] and len(gpx.tracks[0].segments[0].points) > 20:
        #gpx.tracks[0].segments[0].points = gpx.tracks[0].segments[0].points[20:]
        gpx.tracks[0].segments[0].get_nearest_location()
        for i in xrange(20):
            gpx.tracks[0].segments[0].points.pop(0)
        print('inside trim_first_20, new length is: {0}'.format(len(gpx.tracks[0].segments[0].points)))
    else:
        print('NOT ENOUGH POINTS')
        pass


