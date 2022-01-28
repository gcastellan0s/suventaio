(function($) {
  "use strict";
var styles =  [
    {
        "featureType": "water",
        "stylers": [
            {
                "hue": "#ffe500"
            },
            {
                "saturation": -20
            },
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry",
        "stylers": [
            {
                "hue": "#ffe500"
            },
            {
                "lightness": -15
            },
            {
                "saturation": 50
            }
        ]
    },
    {
        "featureType": "landscape",
        "stylers": [
            {
                "weight": 0.1
            },
            {
                "hue": "#ffe500"
            },
            {
                "saturation": 50
            },
            {
                "lightness": 10
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "elementType": "labels",
        "stylers": [
            {
                "hue": "#ffe500"
            },
            {
                "saturation": 50
            },
            {
                "lightness": -10
            },
            {
                "weight": 2
            }
        ]
    },
    {
        "featureType": "poi",
        "stylers": [
            {
                "hue": "#ffe500"
            },
            {
                "saturation": 75
            },
            {
                "lightness": -10
            }
        ]
    },
    {
        "featureType": "transit.station.airport",
        "stylers": [
            {
                "hue": "#ffe500"
            },
            {
                "saturation": 50
            },
            {
                "lightness": -10
            }
        ]
    },
    {}
]
google.maps.event.addDomListener(window, 'load', init);    

function init() {
	$('.map-frame-event').each(function(){
		var zoom = parseInt($(this).find('.map-zoom').val());
		var lat = $(this).find('.map-lat').val();
		var lng = $(this).find('.map-lng').val();
		var iconImg = $(this).find('.map-icon-img').val();
		var iconTitle = $(this).find('.map-icon-title').val();
		var position = new google.maps.LatLng(20.987677,-89.6303537);
		var mapOptions = {
			zoom: 13,
			center: position,
			styles: styles,
			draggable: false,
		};
		var mapElement = this;
		var map = new google.maps.Map(mapElement, mapOptions);
		var marker1 = new google.maps.Marker({
			position: new google.maps.LatLng(20.9656989, -89.6391481),
			map: map,
			title: iconTitle,
			icon: iconImg
		});
		var marker2 = new google.maps.Marker({
			position: new google.maps.LatLng(20.9974765,-89.6444657),
			map: map,
			title: iconTitle,
			icon: iconImg
		});
		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(20.9953246,-89.6279612),
			map: map,
			title: iconTitle,
			icon: iconImg
        });
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(21.0059444, -89.6477553),
            map: map,
            title: iconTitle,
            icon: iconImg
        });
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(20.9991544, -89.6727765),
            map: map,
            title: iconTitle,
            icon: iconImg
        });
		$(this).parents('.experience-spoiler').click(function(){
			google.maps.event.trigger(map, 'resize');
			map.setCenter(position);
		})
	});
}
})(jQuery);