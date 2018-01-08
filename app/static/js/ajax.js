/**
 * Created by SteveDien on 21-Apr-17.
 */

$(function () {
    $('button').click(function (event) {
        // Prevent submit form
        event.preventDefault()
    })
    $("#btn-login").click(function (event) {
        // Sign in process
        // Get data to post
        var email = $('input[name=email]').val().trim()
        var password = $('input[name=password]').val().trim()

        // Validation
        flag = email != "" && password != ""
        if (!flag) {
            if (email == "") {
                $('input[name=email]').notify("You must enter email", 'info')
            }
            if (password == "") {
                $('input[name=password]').notify("You must enter password", 'info')
            }
        } else {

            //Send ajax request
            $.ajax({
                url: '/auth/ajax/login',
                data: $('#form-login').serialize(),
                type: 'POST',
                success: function (response) {
                    data = JSON.parse(response)
                    if (data.status == 'OK') {
                        $.notify(data.content, 'success')
                        setTimeout(function () {
                            window.location = window.location.origin + '/home'
                        }, 2000);
                    } else {
                        $.notify(data.content, 'error')
                    }
                },
                error: function (error) {
                    console.log(error)
                }
            })
        }
    })
    $("#btn-register").click(function () {
        // Register process
        // Get data to post
        var fullname = $('input[name=fullname]').val().trim()
        var email = $('input[name=email]').val().trim()
        var password = $('input[name=password]').val().trim()
        var password = $('input[name=password]').val().trim()
        var password = $('input[name=coupon_code]').val().trim()

        // Send post request
        $.ajax({
            url: '/auth/ajax/register',
            data: $('#form-register').serialize(),
            type: 'POST',
            success: function (response) {
                data = JSON.parse(response)
                if (data.status == 'OK') {
                    $.notify(data.content, 'success')
                    setTimeout(function () {
                        window.location = window.location.origin + '/home'
                    }, 2000);
                } else {
                    $.notify(data.content, 'error')
                }
            },
            error: function (error) {
                console.log(error)
            }
        })
    })
})
