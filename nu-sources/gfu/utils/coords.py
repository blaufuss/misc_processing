# -*-coding:utf8-*-

r"""
This file is part of SkyLab

Skylab is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


coords
======

Coordinate transformation methods and similar methods.

"""

import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

import healpy as hp
import numpy as np
from pyslalib import slalib as sl

icecube_longitude = 0.0
icecube_latitude = -1.5707963267948966
icecube_depth = 1084.

antares_longitude = 0.1076117657
antares_latitude = 0.74698201212
antares_depth = 0.

gmst = np.vectorize(sl.sla_gmst, otypes=[np.float],
                    doc=("Calculate Greenwich mean standard "+
                         "time with numpy support"))

dh2e = np.vectorize(sl.sla_dh2e, otypes=[np.float, np.float],
                    doc=("Convert Horizon to Equatorial coordinates. "+
                         "Input azimuth, elevation and obs. latitude in rad."))

de2h = np.vectorize(sl.sla_de2h, otypes=[np.float, np.float],
                    doc=("Convert Equatorial to Horizontal coordinates. "+
                         "Input hour angle, decl. and obs. latitude in rad."))

dtt = np.vectorize(sl.sla_dtt, otypes=[np.float],
                   doc="Convert from modified julian date to terrestial time")

gal = np.vectorize(sl.sla_eqgal, otypes=[np.float, np.float])


def angular_distance(z1, a1, z2, a2):
    r""" Calculate angular distance between two points on a sphere.
    All angles are supposed to be in radians and zenith

    Parameters
    ----------
    z1, z2 : array-like
        zenith coordinates of point 1 and 2

    a1, a2 : array-like
        azimuth coordinates of point 1 and 2

    Returns
    -------
    delta_psi : array_like
        Angular distance of point 1 and point 2

    """
    if np.any(z1 < 0.) or np.any(z2 < 0):
        logger.warn("Found negative zenith values. "+
                    "Declination yields wrong results!")
    return np.arccos(np.cos(a1-a2)*np.sin(z1)*np.sin(z2)+np.cos(z1)*np.cos(z2))


def galactic(*args):
    r""" Calculate galactic coordinates. Input can be given in equatorial
    or IceCube coordinates
        Equatorial  : right ascension, declination
        IceCube     : azimuth, zenith, time

    Returns
    -------
    lon : array_like
        Longitude of coordinates

    lat : array_like
        Latitude of coordinates

    """
    if len(args) > 3 or len(args) < 2:
        raise ValueError(
                "Method accepts only 2 (Equatorial) or 3 (IC) coordinates"
                        )
    ra = np.asarray(args[0])
    dec = np.asarray(args[1])
    if len(args) > 2:
        # Transform from IceCube to equatorial coordinates
        ra, dec = local2eq(dec, ra, args[2])
    lon, lat =  gal(ra, dec)
    return lon, lat


def inv_galactic(lon, lat):
    r""" Calculate equatorial coordinates from galactic ones.

    Inverse function to `galactic` in this package.

    """
    lon = np.asarray(lon)
    lat = np.asarray(lat)

    eq = np.array([sl.sla_galeq(lo, la) for lo, la in zip(lon, lat)])
    return eq[:, 0], eq[:, 1]


def local2eq(zenith, azimuth, time_MJD, epoch=2000.,
             obs_lon=icecube_longitude, obs_lat=icecube_latitude, nut=True):
    r""" Transform local coordinates to equatorial ones.

    Code similar to coordinate-service: $SVN/projects/coordinate-service

    Parameters
    ----------
    zenith : array-like
        Zenith values

    azimuth : array-like
        Azimuth values

    time_MJD : array-like
        MJD time values

    epoch : int
        Epoch for transformation to correct for nutation and precession

    obs_lon/lat : float
        Longitude and latitude values of the detector

    nut : bool
        Whether or not to correct for nutation and precession

    """
    loc_zenith = periodic(zenith, [0., np.pi])
    loc_azimuth = periodic(azimuth, [0., 2.*np.pi])

    # IceCube coordinate system differs from the slalib one
    # y-axis points towards Greenwhich, x-Axis towards East
    sla_azimuth = np.pi/2 - loc_azimuth
    sla_zenith = loc_zenith
    # elevation or altitude
    elevation = np.pi/2. - sla_zenith

    # convert from horizontal (local) coordinates to equatorial
    ha, dec = dh2e(sla_azimuth, elevation, obs_lat)

    # convert ha and dec in [0, 2pi), [-pi, pi], respectively
    ha = periodic(ha, [0., 2.*np.pi])
    dec = periodic(dec, [-np.pi/2., np.pi/2.])

    # calculate greenwhich mean sidereal time
    time_gmst = gmst(time_MJD) + obs_lon

    ra = time_gmst - ha
    ra = periodic(ra, [0., 2.*np.pi])

    if not nut:
        return ra, dec

    jd = time_MJD + (1./3600./24.)*dtt(time_MJD)

    # create correction matrix for nutation of Earth axis
    corr = np.array(
            [sl.sla_prenut(epoch, jd_i) for jd_i in jd],
            dtype=np.float)
    # turn spherical coordinates into a vector for transformation
    vector = np.array([np.cos(dec)*np.cos(ra),
                       np.cos(dec)*np.sin(ra),
                       np.sin(dec)]).T
    # solve linear equation M.X=Y for X
    mean_vector = np.linalg.solve(corr, vector)

    xout = mean_vector[:, 0]
    yout = mean_vector[:, 1]
    zout = mean_vector[:, 2]


    ra_J2000 = np.arctan2(yout, xout)
    dec_J2000 = np.arcsin(zout)

    ra_J2000 = periodic(ra_J2000, [0., 2.*np.pi])
    dec_J2000 = periodic(dec_J2000, [-np.pi/2., np.pi/2.])

    return ra_J2000, dec_J2000


def periodic(vals, bounds, n=1000):
    r""" For periodic variables like angles or else, adjust the values to a
    given value_range from zero to period
    """
    assert(len(bounds) == 2. and bounds[1] > bounds[0])
    period = bounds[1] - bounds[0]
    i = 0
    # vals should be within 0 and 2pi
    while np.any(np.logical_or(vals < bounds[0], vals >= bounds[1])):
        logger.debug("Number of values to move: {0:d}".format(
            np.sum(np.logical_or(vals < bounds[0], vals >= bounds[1]))))
        vals[vals < 0.] += period
        vals[vals >= period] -= period
        i += 1
        if i > n:
            raise StandardError(
                    "Correction exceeded {0:d} iterations".format(n))

    logger.debug(
            "Needed {0:d} iterations to move values into bounds".format(i))

    return vals


