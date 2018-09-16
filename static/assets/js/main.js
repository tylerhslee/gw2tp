//Bootstrap Select

jQuery(document).ready(function( $ ) {
$('.selectpicker').selectpicker({
  style: 'btn-select',
  size: 4
});
});


//CounterUp
jQuery(document).ready(function( $ ) {
  $('.counter').counterUp({
    delay: 1,
    time: 800
  });
});

//WOW Scroll Spy
var wow = new WOW({
    //disabled for mobile
    mobile: false
});
wow.init();

// Page Loader
$(window).load(function() {
  "use strict";
  $('#loader').fadeOut();
});


/* ==========================================================================
   New Products Owl Carousel
   ========================================================================== */
  $("#new-products").owlCarousel({
      navigation: true,
      pagination: true,
      slideSpeed: 1000,
      stopOnHover: true,
      autoPlay: true,
      items: 5,
      itemsDesktopSmall: [1024, 3],
      itemsTablet: [600, 1],
      itemsMobile: [479, 1]
  });

/* ==========================================================================
   Touch Owl Carousel
   ========================================================================== */
$(".touch-slider").owlCarousel({
    navigation: false,
    pagination: true,
    slideSpeed: 1000,
    stopOnHover: true,
    autoPlay: true,
    items: 1,
    itemsDesktopSmall: [1024, 1],
    itemsTablet: [600, 1],
    itemsMobile: [479, 1]
});

$('.touch-slider').find('.owl-prev').html('<i class="fa fa-angle-left"></i>');
$('.touch-slider').find('.owl-next').html('<i class="fa fa-angle-right"></i>');

$('#new-products').find('.owl-prev').html('<i class="fa fa-angle-left"></i>');
$('#new-products').find('.owl-next').html('<i class="fa fa-angle-right"></i>');

var owl;

$(document).ready(function () {

    owl = $("#owl-demo");

    owl.owlCarousel({

        navigation: false, // Show next and prev buttons
        slideSpeed: 300,
        paginationSpeed: 400,
        singleItem: true,
        afterInit: afterOWLinit, // do some work after OWL init
        afterUpdate : afterOWLinit
    });

    function afterOWLinit() {
        // adding A to div.owl-page
        $('.owl-controls .owl-page').append('<a class="item-link" />');
        var pafinatorsLink = $('.owl-controls .item-link');
        /**
         * this.owl.userItems - it's your HTML <div class="item"><img src="http://www.ow...t of us"></div>
         */
        $.each(this.owl.userItems, function (i) {

            $(pafinatorsLink[i])
                // i - counter
                // Give some styles and set background image for pagination item
                .css({
                    'background': 'url(' + $(this).find('img').attr('src') + ') center center no-repeat',
                    '-webkit-background-size': 'cover',
                    '-moz-background-size': 'cover',
                    '-o-background-size': 'cover',
                    'background-size': 'cover'
                })
                // set Custom Event for pagination item
                .click(function () {
                    owl.trigger('owl.goTo', i);
                });

        });
         // add Custom PREV NEXT controls
        $('.owl-pagination').prepend('<a href="#prev" class="prev-owl"/>');
        $('.owl-pagination').append('<a href="#next" class="next-owl"/>');
        // set Custom event for NEXT custom control
        $(".next-owl").click(function () {
            owl.trigger('owl.next');
        });
        // set Custom event for PREV custom control
        $(".prev-owl").click(function () {
            owl.trigger('owl.prev');
        });
    }
});

 // Back Top Link
  var offset = 200;
  var duration = 500;
  $(window).scroll(function() {
    if ($(this).scrollTop() > offset) {
      $('.back-to-top').fadeIn(400);
    } else {
      $('.back-to-top').fadeOut(400);
    }
  });
  $('.back-to-top').click(function(event) {
    event.preventDefault();
    $('html, body').animate({
      scrollTop: 0
    }, 600);
    return false;
  })

 $('.list,switchToGrid').click(function(e) {
    e.preventDefault();
    $('.grid').removeClass("active");
    $('.list').addClass("active");
    $('.item-list').addClass("make-list");
    $('.item-list').removeClass("make-grid");
    $('.item-list').removeClass("make-compact");
    $('.item-list .add-desc-box').removeClass("col-sm-9");
    $('.item-list .add-desc-box').addClass("col-sm-7");
  });
  $('.grid').click(function(e) {
    e.preventDefault();
    $('.list').removeClass("active");
    $(this).addClass("active");
    $('.item-list').addClass("make-grid");
    $('.item-list').removeClass("make-list");
    $('.item-list').removeClass("make-compact");
    $('.item-list .add-desc-box').removeClass("col-sm-9");
    $('.item-list .add-desc-box').addClass("col-sm-7");
  });