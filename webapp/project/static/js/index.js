var cammap;

$(function() {
    cammap = L.map('heat-map', { zoomControl: false }).setView([65.1733244, 24.9410248], 4);
    L.control.zoom({ position: 'bottomleft' }).addTo(cammap);
    L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=" +
                "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw", {
                    maxZoom: 18,
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                    id: 'mapbox.streets'
    }).addTo(cammap);
    
    var markers = L.markerClusterGroup();
    var markersCoords = {};
    var geojsonMarkerOptions = {
        radius: 6,
        fillColor: "#f80",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.5
    };

    $.ajax({
        dataType: "json",
        url: "http://tie.digitraffic.fi/api/v1/metadata/camera-stations",
        success: function(data) {
            var geoJsonLayer = L.geoJSON(data, {
                pointToLayer: function (feature, latlng) {
                    if (feature.properties.id) {
                        markersCoords[feature.properties.id] = latlng;
                    }
                    return L.circleMarker(latlng, geojsonMarkerOptions)
                        .on("click", function(e) {
                            updateCameraView(e.target.feature.properties.presets[0].presetId, null);
                        });
                },
                onEachFeature: function (feature, layer) {
                    if (feature.properties) {
                        var content = "<div>" + 
                            "id: " + feature.properties.id + "</br>" +
                            "name: " + feature.properties.name + "</br>" +
                            "cameraType: " + feature.properties.cameraType + "</br>" +
                            "collectionInterval: " + feature.properties.collectionInterval + "</br>" +
                            "collectionStatus: " + feature.properties.collectionStatus + "</br>" +
                            "municipality: " + feature.properties.municipality + "</br>" +
                            "state: " + feature.properties.state + "</br>" +
                            "purpose: " + feature.properties.purpose + "</br>" +
                            "</div>";
                        layer.bindPopup(content);
                    }
                }
            });
            
            markers.addLayer(geoJsonLayer);
            cammap.addLayer(markers);
            //cammap.fitBounds(markers.getBounds());
        },
        error: function(error) {
            console.log(error);
        }
    });
});
