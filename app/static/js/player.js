/**
 * Created by lulzs on 26-Apr-17.
 */
var players = plyr.setup();
var auto_grow_inputs = [].slice.call(document.getElementsByClassName('autogrow'));
for (var i = 0; i < auto_grow_inputs.length; i++) {
    auto_grow_inputs[i].onkeyup = function () {
        var val_length = this.value.length;
        this.setAttribute('size', (val_length > 5 ? val_length : 5));
    }
    auto_grow_inputs[i].addEventListener('focus change', function () {
        if (this.value.length <= 0)
            this.setAttribute('size', 5);
    });
}
(function () {
    var id = 'player'
    var player = document.getElementById(id);
    var toggle_sidebar = document.getElementById('player-toggle-sidebar');
    toggle_sidebar.onclick = function () {
        var sidebar = player.dataset.sidebar;
        if (sidebar == 'true') {
            player.setAttribute('data-sidebar', 'false');
        }
        else {
            player.setAttribute('data-sidebar', 'true');
        }
    }
})();

(function () {
    var submit = document.getElementById('player_submit');
    submit.onclick = function (e) {
        players[0].pause()
        var blank = 0
        $('.subfiller__text>input').each(function () {
            if ($(this).val().trim().toLowerCase() == "") {
                blank = blank + 1
            }
        })
        blank = blank > 0 ? "You have " + blank + " spaces left unanswered" : ""
        swal({
                title: "Are you sure you want to finish?",
                text: blank,
                type: "info",
                showCancelButton: true,
                closeOnConfirm: false,
                showLoaderOnConfirm: true,
            },
            function () {
                var correct = 0
                var wrong = 0
                setTimeout(function () {

                    $('.subfiller__text>input').each(function () {
                        if ($(this).val().trim().toLowerCase() == $(this).attr('data-answer').trim().toLowerCase()) {
                            $(this).addClass('correct')
                            correct = correct + 1
                        } else {
                            $(this).addClass('wrong')
                            wrong = wrong + 1
                        }
                    })
                    var score = parseInt(correct / (correct + wrong) * 100)
                    var message = "You got this"
                    if (score < 10) {
                        message = "Fighting on you, try again!"
                    } else if (score <= 50) {
                        message = "Slightly lower, try one more time!"
                    } else if (score <= 80) {
                        message = "You do quite well, relax and try again to get a higher score!"
                    } else {
                        message = "You are excellent!"
                    }
                    swal({
                        title: message,
                        text: '<div class="profile__hearly hearly"><img class="hearly__icon" src="https://hearly.me/assets/imgs/ear.png" alt=""><div class="hearly__progress progress" data-percent="60"><div class="progress__bar" style="width: ' + score + '%"></div></div> <p class="hearly__status">' + score + '%</p></div>',
                        html: true,
                        confirmButtonText: "Enjoy video, Again!"
                    }, function() {
                        players[0].stop();
                        players[0].play();
                        document.getElementById('player').dataset.sidebar = 'false';
                    });
                }, 2000);
            })
    }
})();

var nowActive = "0";
$('.sublist__item').click(function () {
    players[0].seek(parseFloat($(this).data('cue').split("-")[0]));
});
$('input').focusin(function () {
    players[0].pause()
})

$("input").keypress(function (e) {
    if (e.which == 13) {
        players[0].seek(parseFloat($(this).parent().parent().data('cue').split("-")[0]));
        players[0].play();
    }
});

function getCurTime() {
    if ($('#player').attr('data-sidebar') == 'true') {
        $('.sublist__item').each(function (index, value) {
            var _datacue = $(this).data('cue');
            var start = parseFloat(_datacue.split("-")[0]);
            var end = parseFloat(_datacue.split("-")[1]);
            var currentTime = players[0].getCurrentTime();
            if (currentTime >= start && currentTime < end) {
                if (nowActive !== $(this).data('cue')) {
                    $(".sublist__item").removeClass("active");
                    $(this).addClass("active");
                    document.getElementById($(this).attr('id')).scrollIntoViewIfNeeded();
                    nowActive = $(this).data('cue');
                }
            }
        });
    }
}
window.setInterval(function () {
    getCurTime();
}, 100);

$('.mdi-close').click(function (e) {
    $('.subfiller__text>input').each(function () {
        if ($(this).val().trim().toLowerCase() !== "") {
            e.preventDefault();
            swal({
                title: 'Submit your assignment?',
                text: "If you leave now, your current assignment will not be saved!",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, leave now!'
            }, function (isConfirm) {
                if (isConfirm) {
                    window.location = window.location.origin + '/home'
                }
            });
        }
    })
});
