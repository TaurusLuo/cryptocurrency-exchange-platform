	jQuery(".preloaderimg").fadeOut(150);
	jQuery(".preloader").fadeOut(350).delay(200, function(){
		jQuery(this).remove();
	});