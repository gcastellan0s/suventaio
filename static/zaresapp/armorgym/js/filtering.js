(function($) {
  "use strict";
  $(window).load(function(){
	var $container = $('#our-class-main');
	$container.isotope({
		itemSelector : '.element-item'
	});
	$('#filters button').click(function(){
		var selector = $(this).attr('data-filter');
		$('#filters button').removeClass('is-checked');
		$(this).addClass('is-checked');
		$container.isotope({ filter: selector });
		return false;
	});
	$('#load-more-class').click(function(){
		$.ajax({
			type: "GET",
			url: 'ajax-class.html',
			cache: false,
			success: function (transport) {
				if(html != transport){
					html = transport;
					var $moreBlocks = $(transport).filter('.element-item');
					$container.append($moreBlocks).isotope('insert', $moreBlocks);
				}
			}
		});
	});
	});
	/** ONE PAGE NAVIGATION ACTIVE */
	$(document).on('scroll',function(){
		$('.one-page .mainnav li a').each(function(){
			var anchor = $(this).attr('href');
			if(anchor.indexOf('#')>=0 &&  $(anchor).length) {
				var el = this;
				var top = $(anchor).offset().top;
				if(anchor=='#home'){
					top = 0;
				}else{
					top -= $('#header').height();
				}
				if($(document).scrollTop() < top + 150 && $(document).scrollTop() > top - 150 ){
					$('.one-page .nav-menu li').removeClass('selected active');
					$(el).parent().addClass('selected active');
				}
			}
		});
	});
})(jQuery);