"""
Writes or references some easy BBox for use
"""

"""
Definition of Africa and Africa + Middle East bbox'es based on Remco procedure
"""
import geopandas as gpd
import sqlalchemy as sa
from ingester3.config import source_db_path

def bbox_from_cid(country_id):
    """
    This is a function to find the country polygons based on country_id
    Bounding boxes also available for africa and africa+middle east regions
    :param country_id: 'africa', 'ame' or a country_id as number
    :return: bounding box rounded to 1 decimal point
    """
    BBOX_AFRICA = [-18.5, 52.0, -35.5, 38.0]
    BBOX_AME = [-18.5, 64.0, -35.5, 43.0]
    if country_id == 'africa':
        bbox = BBOX_AFRICA
    else:
        if country_id == "ame":
            bbox = BBOX_AME
        else:
            engine = sa.create_engine(source_db_path)
            gdf_master = gpd.GeoDataFrame.from_postgis("SELECT id as country_id, geom FROM prod.country", engine, geom_col='geom')
            gdf_master = gdf_master.to_crs(4326)
            multipolygon = gdf_master.loc[gdf_master['country_id'] == country_id].geom
            bbox1 = multipolygon.total_bounds
            bbox = [round(bbox1[0]-5,1), round(bbox1[2]+5,1), round(bbox1[1]-5,1), round(bbox1[3]+5,1)]
    return bbox
