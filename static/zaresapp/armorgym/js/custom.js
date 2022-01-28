(function ($) {
	"use strict";

	$(window).load(function() { 
		$("#preloader").delay(100).fadeOut("slow");
		$("#load").delay(100).fadeOut("slow");
	});


	//jQuery to collapse the navbar on scroll
	$(window).scroll(function() {
		if($(".navbar").length){
			if ($(".navbar").offset().top > 50) {
				$(".navbar-fixed-top").addClass("top-nav-collapse");
			} else {
				$(".navbar-fixed-top").removeClass("top-nav-collapse");
			}
		}
	});

	//jQuery for page scrolling feature - requires jQuery Easing plugin
	$(function() {
		$('.navbar-nav li a,.page-scroll a').bind('click', function(event) {
			var anchor = $(this).attr('href');
			var top = $(anchor).offset().top;
			if(anchor=='#home'){
				top = 0;
			}else{
				top -= $('#header').height();
			}
			$('html, body').stop().animate({
				scrollTop: top
			}, 1500, 'easeInOutExpo');
			event.preventDefault();
		});
		
	});

})(jQuery);
	
