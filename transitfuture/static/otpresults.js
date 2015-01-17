var startingLocation = [41.919, -87.69];
var map = L.map('map', {
    center: startingLocation,
    zoom: 13,
    maxZoom: 18
});

var OpenStreetMap_Mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var MyOverlay = L.tileLayer('http://localhost:8000/static/tiles/{z}/{x}/{y}.png', { opacity: 0.5}).addTo(map);

var mover = L.marker(startingLocation, { draggable: true }).addTo(map);

var transit_time = 30;

var url = 'http://23.251.146.21/otp.json?latitude=' + startingLocation[0] + '&longitude=' + startingLocation[1] + '&transit_time=' + transit_time;
var circles = [];
var geojsonFeature = {
    "geoId" : "171830103002042",
    "type": "Feature",
    "lat" : 40.30680023587053,
    "lon" : -87.79816266274199,
    "properties" : {
    },
    "geometry" : {
      "type" : "MultiPolygon",
      "coordinates" : [ [ [ [ -87.79859, 40.30732 ], [ -87.79774, 40.307327 ], [ -87.79775, 40.30626 ], [ -87.79831, 40.30628 ], [ -87.79844, 40.30628 ], [ -87.798515, 40.306267 ], [ -87.79858, 40.306248 ], [ -87.79858, 40.306667 ], [ -87.79859, 40.30732 ] ] ] ]
    },
    "centroid" : {
      "type" : "Point",
      "coordinates" : [ -87.79816, 40.3068 ]
    }
};
L.geoJson(geojsonFeature).addTo(map);

var circleLayerGroup;
var dataCallback = function(data) {
    return;
    while(circles.length > 0) {
        circles.pop();
    }
    if(circleLayerGroup) {
        map.removeLayer(circleLayerGroup);
    }
    for (var d in data) {
        var coords = [data[d][1], data[d][2]]
        var popupText = 'Census Block ' + data[d][0] + "<br>";
        var hasJobs = data[d][3] ? true : false;
        if(!hasJobs) {
            popupText += 'No jobs data available';
        } else {
            popupText += "Total jobs: " + data[d][4];
        }

        var options = {
            color: 'blue',
            fillOpacity: hasJobs ? 0.9 : 0.2
        };
        var circle = L.circle(coords, 10, options).bindPopup(popupText);
        circles.push(circle);
    }
    circleLayerGroup = L.layerGroup(circles).addTo(map);
};
mover.on('dragend', function(e) {

    var url = 'http://23.251.146.21/otp.json?latitude=' + mover.getLatLng().lat + '&longitude=' + mover.getLatLng().lng + '&transit_time=' + transit_time;
    d3.json(url, dataCallback);
});
//d3.json(url, dataCallback);


