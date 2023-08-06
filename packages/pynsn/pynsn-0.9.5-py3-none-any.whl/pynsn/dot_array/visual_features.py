# calculates visual features of a dot array/ dot cloud

from collections import OrderedDict

import numpy as np
from scipy import spatial
from ..lib import misc
from .convex_hull import ConvexHullDots


class VisualFeatures(object):

    LOG_SIZE = "Log Size"
    TOTAL_SURFACE_AREA = "Total surface area"
    ITEM_DIAMETER = "Mean item diameter"
    ITEM_SURFACE_AREA = "Mean item surface area"
    ITEM_PERIMETER = "Total perimeter"
    TOTAL_PERIMETER = "Mean item perimeter"
    LOG_SPACING = "Log Spacing"
    SPARSITY = "Sparsity"
    FIELD_AREA = "Field area"
    COVERAGE = "Coverage"

    SIZE_FEATURES = (LOG_SIZE, TOTAL_SURFACE_AREA, ITEM_DIAMETER,
                     ITEM_SURFACE_AREA, ITEM_PERIMETER, TOTAL_PERIMETER)

    SPACE_FEATURES = (LOG_SPACING, SPARSITY, FIELD_AREA)

    ALL_FEATURES = SIZE_FEATURES + SPACE_FEATURES + (COVERAGE,)

    @staticmethod
    def are_dependent(featureA, featureB):
        """returns true if both features are not independent"""
        for l in [VisualFeatures.SIZE_FEATURES, VisualFeatures.SPACE_FEATURES]:
            if featureA in l and featureB in l:
                return True
        return False


    def __init__(self, dot_array):
        # dot_array or dot_cloud
        self.da = dot_array
        self._convex_hull = None

    def reset(self):
        """reset to enforce recalculation of certain parameter """
        self._convex_hull = None

    @property
    def convex_hull(self):
        if self._convex_hull is None:
            self._convex_hull = ConvexHullDots(self.da.xy, self.da.diameters)
        return self._convex_hull

    @property
    def mean_item_diameter(self):
        return np.mean(self.da.diameters)

    @property
    def total_surface_area(self):
        return np.sum(self.da.surface_areas)

    @property
    def mean_item_surface_area(self):
        return np.mean(self.da.surface_areas)

    @property
    def total_perimeter(self):
        return np.sum(self.da.perimeter)

    @property
    def mean_item_perimeter(self):
        return np.mean(self.da.perimeter)

    @property
    def field_area(self):
        return self.convex_hull.scipy_convex_hull.volume

    @property
    def numerosity(self):
        return len(self.da.xy)

    @property
    def converage(self):
        """ percent coverage in the field area. It takes thus the item size
        into account. In contrast, the sparsity is only the ratio of field
        array and numerosity

        """

        try:
            return self.total_surface_area / self.field_area
        except:
            return None

    @property
    def logSize(self):
        return misc.log2(self.total_surface_area) + misc.log2(
            self.mean_item_surface_area)

    @property
    def logSpacing(self):
        return misc.log2(self.field_area) + misc.log2(self.sparsity)

    @property
    def sparsity(self):
        return self.field_area / self.numerosity

    @property
    def field_area_full(self):  # TODO not tested
        return self.convex_hull.full_field_area

    def _get_distance_matrix(self, between_positions=False):
        """between position ignores the dot size"""
        dist = spatial.distance.cdist(self.da.xy, self.da.xy)  #
        # matrix with all distance between all points
        if not between_positions:
            # subtract dot diameter
            radii_mtx = np.ones((self.numerosity, 1)) + \
                        self.da.diameters[:, np.newaxis].T / 2
            dist -= radii_mtx  # for each row
            dist -= radii_mtx.T  # each each column
        return dist

    @property
    def expension(self):
        """ maximal distance between to points plus diameter of the two points"""

        dist = self._get_distance_matrix(between_positions=True)
        # add dot diameter
        radii_mtx = np.ones((self.numerosity, 1)) + self.da.diameters[:,
                                                    np.newaxis].T / 2
        dist += radii_mtx  # add to each row
        dist += radii_mtx.T  # add two each column
        return np.max(dist)

    #@property
    #def featureXX_coverage_target_area(self):
    #    """density takes into account the full possible target area (i.e.,
    #        image radius) """
    #    try:
    #        return np.pi * self.da.target_array_radius ** 2 / \
    #            self.total_surface_area
    #    except:
    #        return None # dot defined for DotCloud with no target_array_radius

    def get(self, feature):
        """returns a feature"""

       # Adapt
        if feature == VisualFeatures.ITEM_DIAMETER:
            return self.mean_item_diameter

        elif feature == VisualFeatures.ITEM_PERIMETER:
            return self.mean_item_perimeter

        elif feature == VisualFeatures.TOTAL_PERIMETER:
            return self.total_perimeter

        elif feature == VisualFeatures.ITEM_SURFACE_AREA:
            return self.mean_item_surface_area

        elif feature == VisualFeatures.TOTAL_SURFACE_AREA:
            return self.total_surface_area

        elif feature == VisualFeatures.LOG_SIZE:
            return self.logSize

        elif feature == VisualFeatures.LOG_SPACING:
            return self.logSpacing

        elif feature == VisualFeatures.SPARSITY:
            return self.sparsity

        elif feature == VisualFeatures.FIELD_AREA:
            return self.field_area

        elif feature == VisualFeatures.COVERAGE:
            return self.converage

        else:
            raise ValueError("{} is a unkown visual feature".format(feature))


    def get_features_dict(self):
        """ordered dictionary with the most important feature"""
        rtn = [("Hash", self.da.hash),
               ("Numerosity", self.numerosity),
               (VisualFeatures.TOTAL_SURFACE_AREA, self.total_surface_area),
               (VisualFeatures.ITEM_SURFACE_AREA, self.mean_item_surface_area),
               (VisualFeatures.ITEM_DIAMETER, self.mean_item_diameter),
               (VisualFeatures.ITEM_PERIMETER, self.mean_item_perimeter),
               (VisualFeatures.TOTAL_PERIMETER, self.total_perimeter),
               (VisualFeatures.FIELD_AREA, self.field_area),
               (VisualFeatures.SPARSITY, self.sparsity),
               (VisualFeatures.COVERAGE, self.converage),
               (VisualFeatures.LOG_SIZE, self.logSize),
               (VisualFeatures.LOG_SPACING, self.logSpacing)]
        return OrderedDict(rtn)

    def get_features_text(self, with_hash=True, extended_format=False, spacing_char="."):
        if extended_format:
            rtn = None
            for k, v in self.get_features_dict().items():
                if rtn is None:
                    if with_hash:
                        rtn = "- {}: {}\n".format(k, v)
                    else:
                        rtn = ""
                else:
                    if rtn == "":
                        name = "- " + k
                    else:
                        name = "  " + k
                    try:
                        value = "{0:.2f}\n".format(v)  # try rounding
                    except:
                        value = "{}\n".format(v)

                    rtn += name + (spacing_char * (22 - len(name))) + (" " * (14 - len(value))) + value
        else:
            if with_hash:
                rtn = "ID: {} ".format(self.da.hash)
            else:
                rtn = ""
            rtn += "N: {}, TSA: {}, ISA: {}, FA: {}, SPAR: {:.3f}, logSIZE: " \
                   "{:.2f}, logSPACE: {:.2f} COV: {:.2f}".format(
                self.numerosity,
                int(self.total_surface_area),
                int(self.mean_item_surface_area),
                int(self.field_area),
                self.sparsity,
                self.logSize,
                self.logSpacing,
                self.converage)
        return rtn



