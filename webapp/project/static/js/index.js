var cammap;

$(function() {
    cammap = L.map('heat-map', { zoomControl: false }).setView([65.0, 25.5], 10);
    L.control.zoom({ position: 'topleft' }).addTo(cammap);
    var h = 0.0033
    var v = 0.0014
    var ndvi_curr_url = '/static/map_images/heatmap_rgba.png',
        ndvi_month_url = '/static/map_images/heatmap_rgba_month.png',
        ndvi_half_url = '/static/map_images/heatmap_rgba_halfyear.png',
        ndvi_year_url = '/static/map_images/heatmap_rgba_year.png',
        imageBounds = [
                        L.latLng(65.8214035188828 + v, 24.869962219258937 + h),
                        L.latLng(64.8214388312971 + v, 27.213549565024742 + h)
    ];
    
    /*
                            L.latLng(65.8214035188828, 24.869962219258937),
                        L.latLng(64.8214388312971, 27.213549565024742)
    */
/*
    var mapLink = 
            '<a href="http://www.esri.com/">Esri</a>';
    var wholink = 
        'i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community';
    L.tileLayer(
        'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; '+mapLink+', '+wholink,
        maxZoom: 18,
        }).addTo(cammap);
*/
    L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=" +
            "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw", {
                maxZoom: 18,
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                id: 'mapbox.streets'
    }).addTo(cammap);
    
    var ndvi_curr = L.imageOverlay(ndvi_curr_url, imageBounds, { opacity: 0.9 });
    var ndvi_month = L.imageOverlay(ndvi_month_url, imageBounds, { opacity: 0.9 });
    var ndvi_half = L.imageOverlay(ndvi_half_url, imageBounds, { opacity: 0.9 });
    var ndvi_year = L.imageOverlay(ndvi_year_url, imageBounds, { opacity: 0.9 });
    
    var overlayMaps = {
        "NDVI current": ndvi_curr,
        "NDVI month to date": ndvi_month,
        "NDVI half year to date": ndvi_half,
        "NDVI year to date": ndvi_year
    };

    /*
    var pinMaps = {
        "Alerts": alerts
    };*/
    
    L.control.layers(overlayMaps).addTo(cammap);
/*    
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
*/
});
