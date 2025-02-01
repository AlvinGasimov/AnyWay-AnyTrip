$('.sl-details').slick({
    dots: false,
    infinite: false,
    arrows: true,
    speed: 300,
    slidesToShow: 5,
    slidesToScroll: 1,
      
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
          infinite: false,
          dots: false
        }
      },
  
      {
        breakpoint: 600,
        settings: {
          arrows: false,
          slidesToShow: 2,
          slidesToScroll: 2
        }
      },
        
      {
        breakpoint: 480,
        settings: {
          arrows: false,
          slidesToShow: 2.5,
          slidesToScroll: 1
        }
      }
  ]
  });