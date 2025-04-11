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
    folium.Marker([47.50239, 19.039462],
                   popup=folium.Popup('Főkukac', max_width=300),
                   icon=folium.Icon(color="red", prefix='fa',icon='turtle')).add_to(marker_cluster)

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
