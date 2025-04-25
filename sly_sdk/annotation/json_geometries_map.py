# coding: utf-8
from sly_sdk.geometry.bitmap import Bitmap
from sly_sdk.geometry.mask_3d import Mask3D
from sly_sdk.geometry.cuboid import Cuboid
from sly_sdk.geometry.point import Point
from sly_sdk.geometry.polygon import Polygon
from sly_sdk.geometry.polyline import Polyline
from sly_sdk.geometry.rectangle import Rectangle
from sly_sdk.geometry.graph import GraphNodes
from sly_sdk.geometry.any_geometry import AnyGeometry
from sly_sdk.geometry.cuboid_3d import Cuboid3d
from sly_sdk.geometry.pointcloud import Pointcloud
from sly_sdk.geometry.point_3d import Point3d
from sly_sdk.geometry.multichannel_bitmap import MultichannelBitmap
from sly_sdk.geometry.closed_surface_mesh import ClosedSurfaceMesh
from sly_sdk.geometry.alpha_mask import AlphaMask
from sly_sdk.geometry.cuboid_2d import Cuboid2d


_INPUT_GEOMETRIES = [
    Bitmap,
    Mask3D,
    Cuboid,
    Point,
    Polygon,
    Polyline,
    Rectangle,
    GraphNodes,
    AnyGeometry,
    Cuboid3d,
    Pointcloud,
    Point3d,
    MultichannelBitmap,
    ClosedSurfaceMesh,
    AlphaMask,
    Cuboid2d,
]
_JSON_SHAPE_TO_GEOMETRY_TYPE = {
    geometry.geometry_name(): geometry for geometry in _INPUT_GEOMETRIES
}


def GET_GEOMETRY_FROM_STR(figure_shape: str):
    """
    The function create geometry class object from given string
    """
    if figure_shape not in _JSON_SHAPE_TO_GEOMETRY_TYPE.keys():
        raise KeyError(
            f"Unknown shape: '{figure_shape}'. Supported shapes: {list(_JSON_SHAPE_TO_GEOMETRY_TYPE.keys())}"
        )
    geometry = _JSON_SHAPE_TO_GEOMETRY_TYPE[figure_shape]
    return geometry
