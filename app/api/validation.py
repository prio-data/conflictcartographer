from typing import List,Union,Any,Optional

from pydantic import BaseModel
from utility.geojsontypes import Feature,FeatureCollection,Polygon,MultiPolygon

class CountryProps(BaseModel):
    CNTRY_NAME: str # Restrict this?
    GWCODE: int
    ISO1AL2: Optional[str]

class CountryFeature(Feature):
    geometry: Any #Union[Polygon,MultiPolygon]
    properties: CountryProps

class CountryFeatureCollection(FeatureCollection):
    features: List[CountryFeature]
        
