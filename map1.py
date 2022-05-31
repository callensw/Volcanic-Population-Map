]# Import required libraries
import folium
import pandas as pd

# Creating required variables
data = pd.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

# Function for Elevation color determination
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
# Generating map with foliun
map = folium.Map(location = [38.58, -99.09], zoom_start = 5, tiles = "Stamen Terrain")

# Adding population layer to map
fgp = folium.FeatureGroup(name = "Population")

fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgp)

# Adding volcano description  layer to map
fgv = folium.FeatureGroup(name = "My Map")
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location = [lt, ln], radius = 6, popup = folium.Popup(iframe),
    fill_color = color_producer(el), color = 'grey', fill_opacity=0.7))

map.add_child(fgv)

map.add_child(folium.LayerControl())

map.save("index.html")
