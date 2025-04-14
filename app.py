from flask import Flask, render_template
from branca.element import Figure
import os

## for data
import pandas as pd  #1.1.5
import numpy as np  #1.21.0

## for plotting
import matplotlib.pyplot as plt  #3.3.2
import seaborn as sns  #0.11.1
import folium  #0.14.0
from folium import plugins
from folium.plugins import LocateControl, MarkerCluster
import plotly.express as px  #5.1.0

## for simple routing
import osmnx as ox  #1.2.2
import networkx as nx  #3.0

## for advanced routing 
from ortools.constraint_solver import pywrapcp  #9.6
from ortools.constraint_solver import routing_enums_pb2

app = Flask(__name__)

def create_map():
    # prg_map=folium.Map(location=[50.0869808355617, 14.420696466020118],zoom_start=16)
    prg_map=folium.Map(location=[47.503910, 19.050760],zoom_start=14)

    responsive_script = """
    <script>
        // Get the map container
        var map = document.querySelector('.folium-map');
        
        // Function to adjust zoom based on screen width
        function adjustZoom() {
            var mapObj = document.querySelector('.folium-map')._leaflet_map;
            if (window.innerWidth < 768) {
                // Mobile view - set zoom to a lower level
                mapObj.setZoom(12);
            } else {
                // Desktop view - use original zoom
                mapObj.setZoom(16);
            }
        }
        
        // Add a listener for map load event
        if (map._leaflet_map) {
            adjustZoom();
        } else {
            map.addEventListener('leaflet.map.init', function() {
                // Run after the map is initialized
                setTimeout(adjustZoom, 100);
            });
        }
        
        // Adjust zoom when window is resized
        window.addEventListener('resize', adjustZoom);
    </script>
    """

    prg_map.get_root().html.add_child(folium.Element(responsive_script))
    
    marker_cluster = MarkerCluster().add_to(prg_map)

    folium.Marker([47.512603, 19.04895],
                   popup=folium.Popup('The Dead Squirell', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='otter')).add_to(marker_cluster),
    folium.Marker([47.5040513, 19.0514726],
                   popup=folium.Popup('Kermit the Frog', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='frog')).add_to(marker_cluster),
    folium.Marker([47.50264113692668, 19.039962542895616],
                   popup=folium.Popup('Főkukac', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='fish')).add_to(marker_cluster),
    folium.Marker([47.505290167783166, 19.03959366517465],
                   popup=folium.Popup('Tank', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='car')).add_to(marker_cluster),
    folium.Marker([47.504784750961186, 19.039689823872752],
                   popup=folium.Popup('Rubik cube', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='cubes')).add_to(marker_cluster),
    folium.Marker([47.4989897265813, 19.0707676486581],
                   popup=folium.Popup('Diver', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='fish')).add_to(marker_cluster),
    folium.Marker([47.50584439836122, 19.052172422007544],
                   popup=folium.Popup('Moon rover', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='car-side')).add_to(marker_cluster),
    folium.Marker([47.50506949923929, 19.049972488786576],
                   popup=folium.Popup('Axe', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='hammer')).add_to(marker_cluster),
    folium.Marker([47.50369371272755, 19.07249530615872],
                   popup=folium.Popup('14-karat Roadster', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='car-side')).add_to(marker_cluster),
    folium.Marker([47.50371019740113, 19.079569975600943],
                   popup=folium.Popup('Noahs Ark', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='ship')).add_to(marker_cluster),      
    folium.Marker([47.49747423597556, 19.051463347995543],
                   popup=folium.Popup('Bear', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='otter')).add_to(marker_cluster),      
    folium.Marker([47.4857364240772, 19.055044513494188],
                   popup=folium.Popup('Franz Joseph', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='person')).add_to(marker_cluster),   
    folium.Marker([47.49047747038775, 19.047098191767173],
                   popup=folium.Popup('Ratatouille', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='otter')).add_to(marker_cluster),   
    folium.Marker([47.53622714729415, 19.057893617791184],
                   popup=folium.Popup('Russian warship', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='ship')).add_to(marker_cluster),   
    folium.Marker([47.51070262788849, 19.056344650664446],
                   popup=folium.Popup('Skála Kópé', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='ship')).add_to(marker_cluster),
    folium.Marker([47.53290675728547, 19.03955468362713],
                   popup=folium.Popup('In Vino VEritas', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='person-rifle')).add_to(marker_cluster),
    folium.Marker([47.507204159185775, 19.031536844779563],
                   popup=folium.Popup('Dogs', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='dog')).add_to(marker_cluster),
    folium.Marker([ 47.514731638791666, 19.082434815341077],
                   popup=folium.Popup('Dracula', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='person')).add_to(marker_cluster),
    folium.Marker([47.50926926464884, 19.045323876064934],
                   popup=folium.Popup('Ushanka', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='hat-cowboy')).add_to(marker_cluster),
    folium.Marker([47.50907113306574, 19.035877393405233],
                   popup=folium.Popup('Paddington', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='bear')).add_to(marker_cluster),
    folium.Marker([47.506815317129444, 19.025463886505808],
                   popup=folium.Popup('Mekk Elek Cert', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='magnet')).add_to(marker_cluster),
    folium.Marker([47.49730006126405, 19.047420132927574],
                   popup=folium.Popup('Baloon Dog', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='dog')).add_to(marker_cluster),
    folium.Marker([47.49791494719889, 19.03984081162018],
                   popup=folium.Popup('Rabbit', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='dog')).add_to(marker_cluster),

    return prg_map

@app.route("/")
def show_map():
    nyc_map = create_map()
    # Save the map as HTML file to render it
    map_html = os.path.join('templates', 'map.html')
    nyc_map.save(map_html)
    return render_template('map.html') 



if __name__ == '__main__':
    app.run(debug=True)
