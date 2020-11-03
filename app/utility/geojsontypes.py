from typing import Literal,List,Tuple,Union,Dict
from pydantic import BaseModel

Coord = Tuple[float,float]

class Point(BaseModel):
    type: Literal["Point"]
    coordinates: Coord 

class CoordList(BaseModel):
    coordinates: List[Coord]

class Polygon(CoordList):
    type: Literal["Polygon"] = "Polygon"

class LineString(CoordList):
    type: Literal["LineString"] = "LineString"

class MultiPoint(CoordList):
    type: Literal["MultiPoint"] = "MultiPoint"

class MultiCoordList(BaseModel):
    coordinates: List[List[Coord]]

class MultiPolygon(MultiCoordList):
    type: Literal["MultiPolygon"] = "MultiPolygon"

class MultiLineString(MultiCoordList):
    type: Literal["MultiLineString"] = "MultiLineString"

Geometries = Union[Point,Polygon,LineString,MultiPoint,MultiPolygon,MultiLineString]

class GeometryCollection(BaseModel):
    type: Literal["GeometryCollection"]
    geometries: List[Geometries]

class Feature(BaseModel):
    type: Literal["Feature"]
    properties: Dict[str,Union[str,int,float]]
    geometry: Union[Geometries,GeometryCollection]

class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"]
    features: List[Feature]
