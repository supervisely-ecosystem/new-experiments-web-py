# coding: utf-8

# docs
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

from sly_sdk.annotation.json_geometries_map import GET_GEOMETRY_FROM_STR
from sly_sdk.geometry.alpha_mask import AlphaMask
from sly_sdk.geometry.bitmap import Bitmap
from sly_sdk.geometry.geometry import Geometry
from sly_sdk.geometry.point_location import PointLocation
from sly_sdk.geometry.polygon import Polygon
from sly_sdk.geometry.polyline import Polyline
from sly_sdk.geometry.rectangle import Rectangle


def _geometry_to_mask_base(
    geometry_type: Union[AlphaMask, Bitmap],
    geometry: Geometry,
    radius: Optional[int] = 0,
    crop_image_shape: Optional[Tuple] = None,
) -> List[Union[AlphaMask, Bitmap]]:

    thickness = radius + 1

    bbox = geometry.to_bbox()
    extended_bbox = Rectangle(
        top=bbox.top - radius,
        left=bbox.left - radius,
        bottom=bbox.bottom + radius,
        right=bbox.right + radius,
    )

    # Set appropriate fill value and color for the geometry type
    if isinstance(geometry, AlphaMask):
        fill_value, color = 0, 255
    else:
        fill_value, color = False, True

    bitmap_data = np.full(shape=(extended_bbox.height, extended_bbox.width), fill_value=False)
    geometry = geometry.translate(-extended_bbox.top, -extended_bbox.left)
    geometry.draw(bitmap_data, color=True, thickness=thickness)

    origin = PointLocation(extended_bbox.top, extended_bbox.left)
    bitmap_geometry = geometry_type(data=bitmap_data, origin=origin)
    if crop_image_shape is not None:
        crop_rect = Rectangle.from_size(*crop_image_shape)
        return bitmap_geometry.crop(crop_rect)
    return [bitmap_geometry]


def geometry_to_bitmap(
    geometry: Geometry, radius: Optional[int] = 0, crop_image_shape: Optional[Tuple] = None
) -> List[Bitmap]:
    """
    Args:
        geometry: Geometry type which implemented 'draw', 'translate' and 'to_bbox` methods
        radius: half of thickness of drawed vector elements
        crop_image_shape: if not None - crop bitmap object by this shape (HxW)
    Returns:
        Bitmap (geometry) object
    """

    return _geometry_to_mask_base(Bitmap, geometry, radius, crop_image_shape)


def geometry_to_alpha_mask(
    geometry: Geometry, radius: Optional[int] = 0, crop_image_shape: Optional[Tuple] = None
) -> List[AlphaMask]:
    """
    Args:
        geometry: Geometry type which implemented 'draw', 'translate' and 'to_bbox` methods
        radius: half of thickness of drawed vector elements
        crop_image_shape: if not None - crop bitmap object by this shape (HxW)
    Returns:
        AlphaMask (geometry) object
    """

    return _geometry_to_mask_base(AlphaMask, geometry, radius, crop_image_shape)


def get_effective_nonoverlapping_masks(
    geometries: List[Geometry], img_size: Optional[Tuple[int, int]] = None
) -> Tuple[List[Bitmap], np.ndarray]:
    """
    Find nonoverlapping objects from given list of geometries
    :param geometries: list of geometry type objects(Point, Polygon, PolyLine, Bitmap etc.)
    :param img_size: tuple or list of integers
    :return: list of bitmaps, numpy array
    """
    if img_size is None:
        if len(geometries) > 0:
            common_bbox = Rectangle.from_geometries_list(geometries)
            img_size = (common_bbox.bottom + 1, common_bbox.right + 1)
        else:
            img_size = (0, 0)
    canvas = np.full(shape=img_size, fill_value=len(geometries), dtype=np.int32)

    for idx, geometry in enumerate(geometries):
        geometry.draw(canvas, color=idx)
    result_masks = []
    for idx, geometry in enumerate(geometries):
        effective_indicator = canvas == idx
        if np.any(effective_indicator):
            result_masks.append(Bitmap(effective_indicator))
        else:
            result_masks.append(None)
    return result_masks, canvas


def deserialize_geometry(geometry_type_str: str, geometry_json: Dict) -> Geometry:
    """
    Get geometry from json format
    :param geometry_type_str: str
    :param geometry_json: geometry in json format
    :return: geometry type object(Point, Polygon, PolyLine, Bitmap etc.)
    """
    geometry_type = GET_GEOMETRY_FROM_STR(geometry_type_str)
    geometry = geometry_type.from_json(geometry_json)
    return geometry


def geometry_to_polygon(geometry: Geometry, approx_epsilon: Optional[int] = None) -> List[Geometry]:
    if type(geometry) not in (Rectangle, Polyline, Polygon, Bitmap, AlphaMask):
        raise KeyError(
            "Can not convert {} to {}".format(geometry.geometry_name(), Polygon.__name__)
        )

    if type(geometry) == Rectangle:
        return [Polygon(geometry.corners, [])]

    if type(geometry) == Polyline:
        return [Polygon(geometry.exterior, [])]

    if type(geometry) == Polygon:
        return [geometry]

    if type(geometry) in [AlphaMask, Bitmap]:
        new_geometries = geometry.to_contours()
        if approx_epsilon is None:
            approx_epsilon = 1

        new_geometries = [g.approx_dp(approx_epsilon) for g in new_geometries]
        return new_geometries
