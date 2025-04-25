# coding: utf-8

from sly_sdk.geometry.constants import ANY_SHAPE
from sly_sdk.geometry.geometry import Geometry


class AnyGeometry(Geometry):
    """
    AnyGeometry for a single :class:`Label<supervisely.annotation.label.Label>`. :class:`AnyGeometry<AnyGeometry>` class object is immutable.
    """

    @staticmethod
    def geometry_name():
        """
        Geometry name.

        :return: Geometry name
        :rtype: :class:`str`
        """
        return ANY_SHAPE
