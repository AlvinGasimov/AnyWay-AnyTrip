$('.responsive-slider').slick({
    dots: false,
    infinite: false,
    arrows: true,
    speed: 300,
    slidesToShow: 6,
    slidesToScroll: 1,
      
    responsive: [
      {
        breakpoint: 991.98,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: false,
          dots: false
        }
      }, 
      {
        breakpoint: 575.98,
        settings: {
          arrows: false,
          slidesToShow: 2,
          slidesToScroll: 1
        }
      }
  ]
});


$('.simple-slick-slider').slick({
  infinite: true,
  arrows: true,
  slidesToShow: 1,
  slidesToScroll: 1,
});

$('.simple-slick-slider').on('beforeChange', function(event, slick, currentSlide, nextSlide) {
  var slideCount = slick.slideCount;
  var currentIndex = nextSlide + 1;
  $('.simple-slick-slider-index').text(currentIndex + '/' + slideCount);
});

