var startingLocation = [41.919, -87.69];
var map = L.map('map').setView(startingLocation, 15);

var OpenStreetMap_Mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


var mover = L.marker(startingLocation, { draggable: true }).addTo(map);

var transit_time = 30;

var url = 'http://23.251.146.21/otp.json?latitude=' + startingLocation[0] + '&longitude=' + startingLocation[1] + '&transit_time=' + transit_time;
var circles = [];
var circleLayerGroup;
var dataCallback = function(data) {
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
            popupText += "Total jobs: " + data[d][3]['C000'];
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
d3.json(url, dataCallback);


