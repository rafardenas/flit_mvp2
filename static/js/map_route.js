var myoptions = {
    center : { lat: 19.4326, lng: -99.1332 },
    zoom : 5,
};


let map;
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), myoptions);
    // bind renderer with the map
    
    // directions service
    var directionsService = new google.maps.DirectionsService();
    // directions render object
    var directionsRenderer = new google.maps.DirectionsRenderer();
    var start = document.getElementById("origin").innerHTML;
    var end = document.getElementById("destination").innerHTML;
    directionsRenderer.setMap(map);
    var request = {
        origin:start,
        destination:end,
        travelMode: 'DRIVING'
    };
    
    // // // Pass the request to the route method
    directionsService.route(request, function(result, status) {
    if (status == 'OK') {
        directionsRenderer.setDirections(result);
    }
    });

    currlat = document.getElementById("currlat").innerHTML;
    currlng = document.getElementById("currlng").innerHTML;
    const myLatLng = { lat: parseFloat(currlat), lng: parseFloat(currlng) };
    const image = "https://img.icons8.com/color/30/000000/truck--v1.png"
    new google.maps.Marker({
        position: myLatLng,
        map,
        title: "Hello World!",
        clickable :true,
        animation: google.maps.Animation.DROP,
        icon: image,
      });
}





