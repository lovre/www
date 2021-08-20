
$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});

$(function() {
  $('a.page-scroll').bind('click', function(event) {
    var $anchor = $(this);
    $('html, body').stop().animate({scrollTop: $($anchor.attr('href')).offset().top}, 1500, 'easeInOutExpo');
    event.preventDefault();
  });
});

$(window).scroll(function() {
  if ($(".navbar").offset().top > 50)
    $(".navbar-fixed-top").addClass("top-nav-collapse");
  else
    $(".navbar-fixed-top").removeClass("top-nav-collapse");
});

$('.navbar-collapse ul li a').click(function() {
  $('.navbar-toggle:visible').click();
});

google.maps.event.addDomListener(window, 'load', init);

function init() {
  var options = {
    disableDefaultUI: true, zoom: 4,
    center: new google.maps.LatLng(46.049999, 14.469052),
    styles: [
      { "featureType": "water",
      "elementType": "geometry",
      "stylers": [{ "color": "#000000" }, { "lightness": 17 }]},
      { "featureType": "landscape",
      "elementType": "geometry",
      "stylers": [{ "color": "#000000" }, { "lightness": 20 }]},
      { "featureType": "road.highway",
      "elementType": "geometry.fill",
      "stylers": [{ "color": "#000000" }, { "lightness": 17 }]},
      { "featureType": "road.highway",
      "elementType": "geometry.stroke",
      "stylers": [{ "color": "#000000" }, { "lightness": 29 }, { "weight": 0.2 }]},
      { "featureType": "road.arterial",
      "elementType": "geometry",
      "stylers": [{ "color": "#000000" }, { "lightness": 18 }]},
      { "featureType": "road.local",
      "elementType": "geometry",
      "stylers": [{ "color": "#000000" }, { "lightness": 16 }]},
      { "featureType": "poi",
      "elementType": "geometry",
      "stylers": [{ "color": "#000000" }, { "lightness": 21 }]},
      { "elementType": "labels.text.stroke",
      "stylers": [{ "visibility": "on" }, { "color": "#000000" }, { "lightness": 16 }]},
      { "elementType": "labels.text.fill",
      "stylers": [{ "saturation": 36 }, { "color": "#000000" }, { "lightness": 40 }]},
      { "elementType": "labels.icon",
      "stylers": [{ "visibility": "off" }]},
      { "featureType": "transit",
      "elementType": "geometry",
      "stylers": [{ "color": "#000000" }, { "lightness": 19 }]},
      { "featureType": "administrative",
      "elementType": "geometry.fill",
      "stylers": [{ "color": "#000000" }, { "lightness": 20 }]},
      { "featureType": "administrative",
      "elementType": "geometry.stroke",
      "stylers": [{ "color": "#000000" }, { "lightness": 17 }, { "weight": 1.2 }]}
    ]};
  new google.maps.Marker({
    map: new google.maps.Map(document.getElementById('map'), options),
    position: new google.maps.LatLng(46.049999, 14.469052),
    icon: 'img/marker.png'
  });
}
