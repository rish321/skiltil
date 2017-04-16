(function($) {
  $.fn.simpleDivXScroll = function (options) {

    //console.log("here also");

    // declare sensible defaults
    // scrollLength -> specifies the amount to be scrolled in one click
    // provide negative value to enable to scroll to left
    // scrollAnimationLength -> specifies the animation duration for scroll
    var defaultOptions = {
      length: 300,
      direction: 'right',
      animationLength: 400,
    }

    // merge default options with user specified options
    var opts = $.extend(defaultOptions, options);

    // get the current scroll position
    var currentPosition = this.scrollLeft();

    // calculate the position to scroll to
    var scrollLength = opts.direction == 'left' ? -opts.length : opts.length
    var newPosition = currentPosition + scrollLength;

    this.animate({
      scrollLeft: newPosition
    }, opts.animationLength);

    // allow jQuery chaining
    return this;
  }
})(jQuery);
