mapboxgl.accessToken = 'pk.eyJ1Ijoibml5YXppc2FoaW4iLCJhIjoiY2t1dnEzNGUyMXhuejJ1cXY4Y2hiNDN4ZCJ9.RZo41tIbfal8CGgX6NVpaw';

var map = new mapboxgl.Map({

    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    zoom: 3,
    center: [18.065816779637135, 59.33167105233925]

});

map.addControl(
    new mapboxgl.GeolocateControl({
        positionOptions: {
            enableHighAccuracy: true
        },
        trackUserLocation: true,
        showUserHeading: true
    })
); 

/*  // Create a default Marker and add it to the map.
const marker1 = new mapboxgl.Marker()
    .setLngLat([12.554729, 55.70651])
    .addTo(map);

    // Create a default Marker, colored black, rotated 45 degrees.
const marker2 = new mapboxgl.Marker({ color: 'blue', rotation: 45 })
.setLngLat([12.65, 55.66])
.addTo(map); */

function addMarker(cord1, cord2, id){

    var color = ["blue", "red", "green", "black", "orange", "purple", "yellow"]

    const marker1 = new mapboxgl.Marker({color : color[id - 1]})
    .setLngLat([cord1, cord2])
    .addTo(map);
}

