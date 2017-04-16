$(function () {
    // add event handler for right scrolling
    $(document).on('click', '.right-scroll-btn', function (event) {
        //console.log($('.scrolling-carousel'));
        $('.scrolling-carousel').simpleDivXScroll();
    });
    // add event handle for left scrolling
    $(document).on('click', '.left-scroll-btn', function (event) {
        $('.scrolling-carousel').simpleDivXScroll({direction: 'left'});
    });
});
