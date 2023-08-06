# GeoJSON Former
Library that creates valid *.geojson files from shapely shapes.

# Dependancies
This component depends on two external python libraries:
* numpy
* shapely

# Supported shapely types
Currently out of all the available shapely types supported ones are:
* Point
* LineString
* Polygon

# Examples of usage
## Adding points
Simple addition of points.
```python
from geojsonformer.geojsonformer import GeoJSON
from shapely.geometry import Point

point1 = Point([22.8515625, 55.3791104480105])
point2 = Point([12.3046875, 51.17934297928927])

# Simply append points to object
gj = GeoJSON()
gj.add_point(point=point1)
gj.add_point(point2)
```
## Adding LineString objects
Addition of LineString which is constructed from multiple points.
```python
from geojsonformer.geojsonformer import GeoJSON
from shapely.geometry import Point, LineString

point1 = Point([22.8515625, 55.3791104480105])
point2 = Point([12.3046875, 51.17934297928927])
linestring = LineString([point1, point2])

# Append linestring to object
gj = GeoJSON()
gj.add_linestring(line_string=linestring)
```
## Adding polygon objects
Constructing a Polygon object and then adding it to object.
```python
from geojsonformer.geojsonformer import GeoJSON
from shapely.geometry.polygon import Polygon

polygon = Polygon([
            [
              24.0765380859375,
              55.22589019607769
            ],
            [
              25.3509521484375,
              55.22589019607769
            ],
            [
              25.3509521484375,
              55.71164005362048
            ],
            [
              24.0765380859375,
              55.71164005362048
            ],
            [
              24.0765380859375,
              55.22589019607769
            ]
          ])
gj = GeoJSON()
gj.add_polygon(polygon=polygon)
```
## Add multiple shapes and write to file
GeoJSON supports adding multiple different shapely objects and then writing them all to a single .geojson file. Correctness of files can be tested on http://geojson.io.
```python
from geojsonformer.geojsonformer import GeoJSON
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon

point1 = Point([22.8515625, 55.3791104480105])
point2 = Point([12.3046875, 51.17934297928927])
point3 = Point([12.3046875, 51.17934297928927])
polygon = Polygon([
        [
            24.0765380859375,
            55.22589019607769
        ],
        [
            25.3509521484375,
            55.22589019607769
        ],
        [
            25.3509521484375,
            55.71164005362048
        ],
        [
            24.0765380859375,
            55.71164005362048
        ],
        [
            24.0765380859375,
            55.22589019607769
        ]
        ])
gj = GeoJSON()
gj.add_point(point=point1)
gj.add_point(point2)
gj.add_point(point3)
gj.add_polygon(polygon=polygon)
gj.add_linestring(line_string=LineString([point1, point2, point3]))
gj.write_to_file(file_path='points.geojson')
```

# Compatability
Compatability is currently restricted to >= python3.10.

### Author
Project is created and maintained by Arminas Šidlauskas. 
