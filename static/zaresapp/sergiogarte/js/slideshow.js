
;(function(window) {

	'use strict';

	// Helper vars and functions.
	function extend( a, b ) {
		for( var key in b ) { 
			if( b.hasOwnProperty( key ) ) {
				a[key] = b[key];
			}
		}
		return a;
	}

	function Slideshow(el, options) {
		this.el = el;
		this.options = extend({}, this.options);
		extend(this.options, options);
		this.items = [].slice.call(this.el.querySelectorAll('.mirror_brick'));
		this.itemsTotal = this.items.length;
		this.current = 0;
		this._init();
	}

	Slideshow.prototype.options = {
		duration: {show: 1500, hide: 500},
		delay: {show: 250, hide: 0},
		easing: {show: 'easeOutExpo', hide: 'easeOutExpo'},
		titleAnimation: 'vertical'
	};

	Slideshow.prototype._init = function() {
		var self = this;
		
		// Initialize a MirrorFx instance per item and store the references in an array:
		this.mirrorElems = [];
		this.items.forEach(function(item) {
			self.mirrorElems.push(new MirrorFx(item.querySelector('.mirror')));
		});

		// Show the first item´s images and title:
		this.items[this.current].classList.add('slide--current');
		this.mirrorElems[this.current].show();
		this._showTitle();
	};

	Slideshow.prototype._showTitle = function(pos) {
		this._toggleTitle('show', pos);
	};
	
	Slideshow.prototype._hideTitle = function(pos) {
		this._toggleTitle('hide', pos);
	};

	Slideshow.prototype._toggleTitle = function(action, pos) {
		var pos = pos != undefined ? pos : this.current,
			title = this.items[pos].querySelector('.slide__title');
		
		anime.remove(title);
		var opts = {
			targets: title,
			duration: this.options.duration[action],
			easing: this.options.easing[action],
			delay: this.options.delay[action],
			opacity: action === 'show' ? [0,1] : [1,0]
		};

		if( this.options.titleAnimation === 'vertical' ) {
			opts.translateY = action === 'show' ? [50,0] : [0,50];
		}
		else {
			opts.translateX = action === 'show' ? [50,0] : [0,50];
		}
		
		anime(opts);
	};
	
	window.Slideshow = Slideshow;

})(window);