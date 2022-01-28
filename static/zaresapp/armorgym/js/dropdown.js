(function($) {
  "use strict";
// Dropdown Menu
var dropdown = document.querySelectorAll('.dropdown');
var dropdownArray = Array.prototype.slice.call(dropdown,0);
dropdownArray.forEach(function(el){
	var button = el.querySelector('a[data-toggle="dropdown"]'),
			menu = el.querySelector('.dropdown-nav'),
			arrow = button.querySelector('i.icon-arrow'),
			button_link = $(button).attr('href');

	$(button).on( "click touchend", function(event) {
		if(button_link != '#'){
			window.location.href=button_link;
			event.preventDefault();
			return false;
		}
		if(!menu.hasClass('show')) {
			if(!$(menu).parents('.dropdown-nav').length){
					$('.dropdown-nav').addClass('hide').removeClass('show');
				}
			menu.classList.add('show');
			menu.classList.remove('hide');
			arrow.classList.add('open');
			arrow.classList.remove('close');
			event.preventDefault();
		}
		else {
			menu.classList.remove('show');
			menu.classList.add('hide');
			arrow.classList.remove('open');
			arrow.classList.add('close');
			event.preventDefault();
		}
	});
	
	$(arrow).on( "click touchend", function(event) {
		if(button_link != '#'){
			event.stopPropagation();
			if(!menu.hasClass('show')) {
				if(!$(menu).parents('.dropdown-nav').length){
					$('.dropdown-nav').addClass('hide').removeClass('show');
				}
				menu.classList.add('show');
				menu.classList.remove('hide');
				arrow.classList.add('open');
				arrow.classList.remove('close');
				event.preventDefault();
			}
			else {
				menu.classList.remove('show');
				menu.classList.add('hide');
				arrow.classList.remove('open');
				arrow.classList.add('close');
				event.preventDefault();
			}
		}
	});
});

Element.prototype.hasClass = function(className) {
    return this.className && new RegExp("(^|\\s)" + className + "(\\s|$)").test(this.className);
};
  // Author code here
})(jQuery);