// Create the Google Map…
var startingLocation = new google.maps.LatLng(41.919, -87.69);
var map = new google.maps.Map(d3.select("#map").node(), {
  zoom: 12,
  center: startingLocation,
  mapTypeId: google.maps.MapTypeId.TERRAIN
});

var mover = new google.maps.Marker({
    map: map,
    position: startingLocation,
    draggable: true,
    title: 'Drag me',
});

var transit_time = 10;

var overlay;

function OTPOverlay() {
    var _data = null;
    var _div = null;
    var _projection = null;

      function transform(d) {
        d = new google.maps.LatLng(d[1], d[0]);
        d = _projection.fromLatLngToDivPixel(d);
        return d3.select(this)
            .style("left", (d.x - padding) + "px")
            .style("top", (d.y - padding) + "px");
      }

      this.onAdd = function() {
        _div = d3.select(this.getPanes().overlayLayer).append("div")
            .attr("class", "stations");

      }

      this.draw = function() {
          _projection = this.getProjection(),
              padding = 10;

          var marker = _div.selectAll("svg")
              .data(_data)
              .each(transform) // update existing markers
            .enter().append("svg:svg")
              .each(transform)
              .attr("class", "marker");

          // Add a circle.
          marker.append("svg:circle")
              .attr("r", 1)
              .attr("cx", padding)
              .attr("cy", padding)
              .attr("fill", "blue");

      }

      this.update = function(data) {
        if( _data ) {
            _data.length = 0;
        }
        _data = data;
        if( _div ) {
            _div.selectAll("svg")
                .data(_data)
                .each(transform)
        }
      }

      this.onRemove = function() {
        _div.remove();
      }
}
OTPOverlay.prototype = new google.maps.OverlayView();

var url = 'http://localhost:8000/otp.json?latitude=' + startingLocation.lat() + '&longitude=' + startingLocation.lng() + '&transit_time=' + transit_time;
var overLayer = new OTPOverlay();
d3.json(url, function(data) {
    overLayer.update(data);
    overLayer.setMap(map);
});

google.maps.event.addListener(mover, 'dragend', function(event) {
    var url = 'http://localhost:8000/otp.json?latitude=' + event.latLng.lat() + '&longitude=' + event.latLng.lng() + '&transit_time=' + transit_time;
    d3.json(url, function(data) {
        overLayer.setMap(null);
        overLayer.update(data);
        overLayer.setMap(map);
    });
});

