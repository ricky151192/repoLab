function initMap() {
    var mapDiv = document.getElementById('map');
    var map = new google.maps.Map(mapDiv, {
        center: {lat: 45.4773, lng: 9.1815},
        zoom: 14
      });
    return map;
}

function readCsv(map) {
    $.ajax({
        url : "routes-list.csv",
        dataType: "text",
        success : function(result) {
            var csv_str_list = result.split("\n");
            var index = 0;
            var coord = [];
            coord[index]= [];

            for(var i = 1; i < csv_str_list.length; i+=1) {
                var line = csv_str_list[i].split(",");
                if (line[0] == index) {
                    // rischio = parseInt(line[10]) # TODO: per adesso si usa solo la velocità
                    velocitaLimite = parseInt(line[7]);
                    velocitaRilevata = parseInt(line[8]);
                    diff = Math.abs(velocitaRilevata - velocitaLimite);
                    if (diff > 20) {
                        diff = 19;
                    }
                    coord[index].push({lat: parseFloat(line[5]), lng: parseFloat(line[6]), title: line[4], velDiff: diff});
                } else {
                    index += 1;
                    coord[index] = [];
                }
            }

            var rainbow = new Rainbow(); 
            rainbow.setNumberRange(0, 20);
            rainbow.setSpectrum('#FF0000', '#00FF00');
            for (var n = 0; n < coord.length; n += 1) {
                putPolyline(map, coord[n], rainbow, 'yellow');
            }
                
            //$('#csv_dump').append("<p>" + line[1] + "</p>");
        }
    });
}

// test marker
function putMarker(map,lat, lng, title){
    var myLatLng = {lat: parseFloat(lat), lng: parseFloat(lng)};

  var marker = new google.maps.Marker({
      position: myLatLng,
      map: map,
      title: title,
  });
  return marker;
}

function putPolylinePoint(map, point, marker_type) {
    if (point.velDiff < (20 / 3)) {
        marker_type = 'green';
    } else if (point.velDiff > ((20 / 3) * 2)) {
        marker_type = 'yellow';
    } else {
        marker_type = 'red';
    }


    var polylineMarker = new google.maps.Marker({
        position: point,
        map: map,
        title: point.title,
        icon: 'images/map-marker-' + marker_type + '-s.png'
    });

    // put label on single marker
    var infowindow = new google.maps.InfoWindow({
        content: '<div id="content">' + point.title + '(' + point.velDiff + ')</div>'
      });
    polylineMarker.addListener('click', function() {
        infowindow.open(map, polylineMarker);
    });
}

function putPolyline(map, points, rainbow, marker_type){
    // put polyline
    var i;
    for(i = 0; i < (points.length - 1); i += 1) {
        var line_color = '#' + rainbow.colourAt(points[i+1].velDiff);
        var polyline = new google.maps.Polyline({
            path: [ points[i], points[i + 1] ],
            geodesic: true,
            strokeColor: line_color,
            strokeOpacity: 1.0,
            strokeWeight: 2
        });
        polyline.setMap(map);
    }

    // put marker on polyline
    for (i = 0; i < points.length; i += 1) {
        putPolylinePoint(map, points[i], marker_type);
    }
}

function loadGoogleMap() {
    var map = initMap();

    readCsv(map);

    /*
    putMarker(map,45.4773,9.1815,"marker1");
    putMarker(map,45.4773+0.1,9.1815,"marker2");
    putMarker(map,45.4773+0.3,9.1815,"marker3");
    */
}
