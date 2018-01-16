var map;
function initMap() {
    const montreal = {lat:45.5017, lng:-73.5673};
    map = new google.maps.Map(document.getElementById('map'), {
        center: montreal,
        zoom: 12
    });
    var marker = new google.maps.Marker({
        position: montreal,
        map: map
    });
}