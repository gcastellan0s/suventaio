(function($){

	"use strict";

		function init() {
				new Slideshow(document.querySelector('.mirror_content'));
			}
			
			// Fake loading time..
			var startTime = new Date().getTime();
			imagesLoaded(document.querySelector('main'), function() {
				var elapsed = new Date().getTime() - startTime,
					initFn = function() {
						document.body.classList.remove('loading');
						setTimeout(init, 50);
					};

				if( elapsed > 2000) {
					initFn();
				}
				else {
					setTimeout(initFn, 1000);
				}
		});
	
})(jQuery);



