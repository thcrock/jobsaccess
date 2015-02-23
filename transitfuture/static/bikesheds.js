var startingLocation = [41.9174, -87.6881];
var map = L.map('map', {
    center: startingLocation,
    zoom: 12,
    maxZoom: 18
});

var OpenStreetMap_Mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


var quickness_overlay;
var safety_overlay;
var mover = L.marker(startingLocation, { draggable: true }).addTo(map);
var speed = 8;
var transit_time = 30;

function buildurl(lat, lon, safety, quick, slope, speed, time) {
    var full_prefix = 'http://' + domain + ':' + port;
    var url = full_prefix + '/bikeshed.json?latitude=' + lat + '&longitude=' + lon + '&transit_time=' + time + '&safety=' + safety + '&quick=' + quick + '&slope=' + slope + '&bike_speed=' + speed;
    return url;
}

var quicknessCallback = function(data) {
    if(quickness_overlay && map.hasLayer(quickness_overlay)) {
        map.removeLayer(quickness_overlay);
    }
    quickness_overlay = L.geoJson(data, { style: { "color": "#FF0000" }}).addTo(map);
};

var safetyCallback = function(data) {
    if(safety_overlay && map.hasLayer(safety_overlay)) {
        map.removeLayer(safety_overlay);
    }
    safety_overlay = L.geoJson(data, { style: { "color": "#00FF00" }}).addTo(map);
};

var safe_url = buildurl(startingLocation[0], startingLocation[1], 1.0, 0.0, 0.0, speed, transit_time);
var quick_url = buildurl(startingLocation[0], startingLocation[1], 0.0, 1.0, 0.0, speed, transit_time);
d3.json(safe_url, safetyCallback);
d3.json(quick_url, quicknessCallback);
mover.on('dragend', function(e) {
    var safe_url = buildurl(mover.getLatLng().lat, mover.getLatLng().lng, 1.0, 0.0, 0.0, speed, transit_time);
    var quick_url = buildurl(mover.getLatLng().lat, mover.getLatLng().lng, 0.0, 1.0, 0.0, speed, transit_time);
    d3.json(safe_url, safetyCallback);
    d3.json(quick_url, quicknessCallback);
});

