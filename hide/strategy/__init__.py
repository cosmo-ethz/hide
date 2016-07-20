from collections import namedtuple


CoordSpec = namedtuple("CoordSpec", ["time", "alt", "az",  "ra", "dec"])
# class CoordSpec(object):
#     def __init__(self, time, az, alt, ra, dec):
#         self.time = time
#         self.az = az
#         self.alt = alt
#         self.ra = ra
#         self.dec = dec