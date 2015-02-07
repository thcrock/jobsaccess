var startingLocation = [41.9174, -87.6881];
var map = L.map('map', {
    center: startingLocation,
    zoom: 13,
    maxZoom: 18
});

var OpenStreetMap_Mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var full_prefix = 'http://' + domain + ':' + port;

var tile_overlay;
var mover = L.marker(startingLocation, { draggable: true }).addTo(map);

var transit_time = 30;

var url = full_prefix + '/otp.json?latitude=' + startingLocation[0] + '&longitude=' + startingLocation[1] + '&transit_time=' + transit_time;

var circleLayerGroup;
var dataCallback = function(data) {
    var lookup_key = data['lookup_key'];
    if(tile_overlay && map.hasLayer(tile_overlay)) {
        map.removeLayer(tile_overlay);
    }
    tile_overlay = L.tileLayer(full_prefix + '/tiles/{z}/{x}/{y}/' + lookup_key, { opacity: 0.5 }).addTo(map);
};

d3.json(url, dataCallback);
mover.on('dragend', function(e) {

    var url = full_prefix + '/otp.json?latitude=' + mover.getLatLng().lat + '&longitude=' + mover.getLatLng().lng + '&transit_time=' + transit_time;
    d3.json(url, dataCallback);
});

