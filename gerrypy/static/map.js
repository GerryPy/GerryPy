var map;
function initMap() {
map = new google.maps.Map(document.getElementById('map'), {
  zoom: 7,
  mapTypeId: 'terrain',
  mapTypeControl: false,
  center: {lat: 39, lng: -105}
});

map.data.loadGeoJson(
    'https://storage.googleapis.com/mapsdevsite/json/google.json');
}