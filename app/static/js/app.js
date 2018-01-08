jQuery(document).ready(function(){
    $('#search').on("change",function(){
        var val = this.value;
        if (val) {
            $('#search').addClass('active');
        } else {
            $('#search').removeClass('active');
        }
    });

    // Dropdown
    
    // Slider
    
    var movie_slider = $('.owl-carousel');
    movie_slider.owlCarousel({
        loop: false,
        margin: 6,
        mouseDrag: false,
        navText: ["<i class='mdi mdi-chevron-left'>", "<i class='mdi mdi-chevron-right'>", '', ''],
        dots: false,
        nav: true,
        // items: 5,
        items: 8,
        slideBy: 8,
        smartSpeed: 150,
    })
    $(window).trigger('resize');
    $('.movie').hover(function(){
        var content = $(this).children('.movie__content');
        var offset_right = $(window).width() - 
            content.get(0).getBoundingClientRect().left - 
            content.width() - 50;
        var offset_bottom = $(window).height() - 
            content.get(0).getBoundingClientRect().top - 
            content.height() - 50;
            
        // console.log(offset_right);
        // console.log(offset_bottom);
        if (offset_right < 0) {
            $(this).addClass('off-right');
        } else {
            $(this).removeClass('off-right');
        }

        if (offset_bottom < 0) {
            $(this).addClass('off-bot');
        } else {
            $(this).removeClass('off-bot');
        }
    });


    // Auth tab
    $('.auth__tab').click(function(){
        if (! $(this).hasClass('active')) {
            $(this).siblings('.auth__tab').removeClass('active');
            $(this).addClass('active');
        }
    });
    // profile tab
    $('.profile__tab').click(function(){
        if (! $(this).hasClass('active')) {
            $(this).siblings('.profile__tab').removeClass('active');
            $(this).addClass('active');
        }
    });

    // Auth btn
    $('#btn-auth-login').click(function(){
        $('#auth-popup').modal('show');
        $("#auth-popup [for='auth-signin']").trigger('click');
    });
    $('#btn-auth-trial, #btn-register-to-try').click(function(){
        $('#auth-popup').modal('show');
        $("#auth-popup [for='auth-signup']").trigger('click');
    });
    
    // Dropdown
    $('.dropdown').on('click', function(){
        // console.log('gôo');
        ($(this).hasClass('active')) ?
        $(this).removeClass('active') :
        $(this).addClass('active');
    });
    $(document).mouseup(function (e)
    {
        var container = $(".dropdown.active");

        if (!container.is(e.target)
            && container.has(e.target).length === 0)
        {
            container.removeClass('active');
        }
    });
});
