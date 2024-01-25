/**
*
* -----------------------------------------------------------------------------
*
* Template : Kbiz - Creative HTML5 Template
* Author : backtheme
* Author URI : https://backtheme.com/ 

* -----------------------------------------------------------------------------
*
**/

(function($) {
    "use strict";

    // pisticky Menu
    var header = $('.back-header');
    var win = $(window);
    win.on('scroll', function() {
        var scroll = win.scrollTop();
        if (scroll < 100) {
           header.removeClass("back-sticky");
        } else {
           header.addClass("back-sticky");
        }
    });

    //Menu Code Here
    $("#backmenu").jkResponsiveMenu({
        resizeWidth: '991', 
        animationSpeed: 'medium', 
        accoridonExpAll: false 
    });

    //Menu Active Here
    var path = window.location.href; 
    $('.back-menus li a').each(function() {
        if (this.href === path) {
            $(this).addClass('back-current-page');
        }
    });

    // wow init
    new WOW().init({
        offset: 0,
    });


    //Taggle Js
    $('#menu-btn').on('click', function(e) {
        $(this).toggleClass("back__close");
        e.preventDefault();
    });

    // Home Slider Part
    if ($('.home-slider-part').length) {
        $('.home-slider-part').owlCarousel({
            loop:true,
            items:1,
            margin:0,
            autoplay:false,
            slideSpeed : 800,
            nav:true,
            dots:true,
            responsive:{
                0:{
                    dots:false,
                    nav:false,
                },
                768:{
                    dots:true,
                },
            }
        })
    }

    // Case Studies Part
    if ($('.case-studies-slider').length) {
        $('.case-studies-slider').owlCarousel({
            loop:true,
            items:5,
            margin:30,
            autoplay:false,
            slideSpeed : 300,
            nav:false,
            dots:false,
            responsive:{
                0:{
                    items:1,
                },
                767:{
                    items:2,
                },
                1024:{
                    items:3,
                },
                1400:{
                    items:4,
                },
                1600:{
                    items:5,
                },
            }
        })
    }

    // Case Studies Part
    if ($('.case-studies-slider2').length) {
        $('.case-studies-slider2').owlCarousel({
            loop:true,
            items:3,
            margin:30,
            autoplay:false,
            slideSpeed : 300,
            nav:false,
            dots:false,
            responsive:{
                0:{
                    items:1,
                },
                767:{
                    items:2,
                },
                1024:{
                    items:2,
                },
                1400:{
                    items:3,
                },
                1600:{
                    items:3,
                },
            }
        })
    }

    // Service Part
    if ($('.service-slider').length) {
        $('.service-slider').owlCarousel({
            loop:true,
            items:3,
            margin:30,
            autoplay:false,
            slideSpeed : 300,
            nav:false,
            dots:false,
            responsive:{
                0:{
                    items:1,
                    center: false,
                },
                575:{
                    items:1,
                    center: false,
                },
                768:{
                    items:2,
                    center: false,
                },
                1200:{
                    items:3,
                },
            }
        })
    }

    // Team Slider Part
    if ($('.team-slider').length) {
        $('.team-slider').owlCarousel({
            loop:true,
            items:3,
            margin:30,
            autoplay:false,
            slideSpeed : 300,
            nav:false,
            dots:false,
            responsive:{
                0:{
                    items:1,
                },
                575:{
                    items:2,
                },
                767:{
                    items:2,
                },
                1024:{
                    items:3,
                },
            }
        })
    }

    // Client Slider Part
    if ($('.client-slider').length) {
        $('.client-slider').owlCarousel({
            loop:true,
            items:3,
            margin:30,
            autoplay:false,
            slideSpeed : 300,
            nav:false,
            dots:true,
            center: true,
            responsive:{
                0:{
                    items:1,
                    center: false,
                },
                575:{
                    items:1,
                    center: false,
                },
                767:{
                    items:1,
                    center: false,
                },
                1200:{
                    items:3,
                },
            }
        })
    }


    // Client Slider Part
    if ($('.logo-slider').length) {
        $('.logo-slider').owlCarousel({
            loop:true,
            items:4,
            margin:30,
            autoplay:true,
            slideSpeed : 300,
            nav:false,
            dots:true,
            center: false,
            responsive:{
                0:{
                    items:2,
                    center: false,
                },
                575:{
                    items:3,
                    center: false,
                },
                767:{
                    items:4,
                    center: false,
                },
                1200:{
                    items:4,
                },
            }
        })
    }

    //filter js
    var pifilter = $('.back-grid');
    if(pifilter.length){
        $('.back-grid').imagesLoaded(function() {
            $('.back-filter').on('click', 'button', function() {
                var filterValue = $(this).attr('data-filter');
                $grid.isotope({
                    filter: filterValue
                });
            });
            var $grid = $('.back-grid').isotope({
                itemSelector: '.grid-item',
                percentPosition: true,
                masonry: {
                    columnWidth: '.grid-item',
                }
            });
        });
    }

    // Blog Slider Part
    if ($('.blog-slider').length) {
        $('.blog-slider').owlCarousel({
            loop:true,
            items:3,
            margin:30,
            autoplay:false,
            slideSpeed : 300,
            nav:false,
            dots:true,
            center: true,
            responsive:{
                0:{
                    items:1,
                    center: false,
                },
                575:{
                    items:1,
                    center: false,
                },
                768:{
                    items:2,
                    center: false,
                },
                1200:{
                    items:3,
                },
            }
        })
    }


    //Footer Sticky
    if (window.matchMedia('(min-width: 991px)').matches){
        $(document).ready(function(){
            var footer_heights=$("#back-footer").height();
            $(".back-wrapper").css({
                'padding-bottom' : footer_heights
            });
        });

        $(document).ready(function(){
            $(window).on("scroll", function() {
                    var footer_height = $( ".footer-sticky" ).outerHeight();
                    var dim_height = $(".back-footer").outerHeight();
                    var scrollHeight = $(document).height();
                    var scrollPosition = $(window).height() + $(window).scrollTop();
                    if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
                        // when scroll to bottom of the page
                        $(".back-footer").removeClass("dim-fixed");
                        $(".back-footer").addClass("dim-static").css({
                        'bottom': footer_height,
                        });

                    }else{
                        $(".back-footer").removeClass("dim-static");
                        $(".back-footer").addClass("dim-fixed").css({'bottom': 0,});
                    }
            });
        }); //Document Ready function end
    }

    //Search
    var icon_search = $('#icon_search');
    if(icon_search.length){
        $('#icon_search, #icon_searchs, #search-close, .back-search-overlay').on('click',function(e){
            e.preventDefault();
            $('body').toggleClass('search-expanded');
            
        });
    }

    // Flex Slider
    var flexsliders = $('.back-flexslider');
    if(flexsliders.length){
        jQuery('.back-flexslider').flexslider({
            animation: "slide",
            controlNav: "thumbnails"
        });
    }

    // Sticky Sidebar
    var contentsticky = $('.back-content-sticky');
    if(contentsticky.length) {
        $('.back-content-sticky, .back-sidebar-sticky').theiaStickySidebar({
            additionalMarginTop: 140,
            additionalMarginBottom: 20,
        });
    }

    //Video PopUp 
    var popup = $('.popup-video');
    if(popup.length) {
        $('.popup-video').magnificPopup({
            disableOn: 10,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        }); 
    }

    // Counter Up
    if ($('.back-count').length) {  
        $('.back-count').counterUp({
            delay: 20,
            time: 1500
        });
    }

    //preloader
    $(window).on( 'load', function() {
        $("#back__preloader").delay(1000).fadeOut(400);
        $("#back__preloader").delay(1000).fadeOut(400);
    })

    // scrollTop init
    var pitotop = $('#backscrollUp'); 
    if(pitotop.length){   
        win.on('scroll', function() {
            if (win.scrollTop() > 350) {
                pitotop.fadeIn();
            } else {
                pitotop.fadeOut();
            }
        });
        pitotop.on('click', function() {
            $("html,body").animate({
                scrollTop: 0
            }, 500)
        });
    }

})(jQuery);
