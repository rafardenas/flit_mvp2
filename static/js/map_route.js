var myoptions = {
    center : { lat: 19.4326, lng: -99.1332 },
    zoom : 5,
    // mapTypeId: google.maps.MapTypeId.ROADMAP
    
};

let map;
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), myoptions);
};

// directions service
var directionsService = new google.maps.directionsService();

// directions render object
var directionsDisplay = new google.maps.DirectionsRenderer();

// bind renderer with the map
directionsDisplay.setMap(map);

 








