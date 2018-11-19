(function() {
    'strict'

    window.chessPy = {
        'alert': function(message, alertType, dismissTime, classes) {
            if (++(window.chessPy._alertCnt) > window.chessPy._alertLimit) {
                window.chessPy._alertQueue.push(arguments);
            } else {
                window.chessPy._showAlert.apply(this, arguments);
            }
        },
        '_showAlert': function(message, alertType, dismissTime, classes) {
            message = message || '{{ utils.gettext("Oops! Something went wrong!") }}';
            alertType = alertType || 'info';
            if (dismissTime === undefined) {
                dismissTime = 5000;
            }
            var $alert = $('<div/>').
                addClass('alert alert-' + alertType).
                addClass(classes).
                attr('role', 'alert').
                html(message).
                css('display', 'none').
                prependTo('#messages-panel')
                .animate({
                    opacity: 'show',
                    height: 'show',
                    padding: 'show'
                },
                400,
                'swing',
                setTimeout(function() {
                        if (dismissTime !== 0) {
                            window.chessPy.removeAlert($alert);
                        }
                }, dismissTime)
            );
        },
        'removeAlert': function($alert) {
            $alert.fadeOut(function() {
                $alert.remove();
                --(window.chessPy._alertCnt);
                args = window.chessPy._alertQueue.shift();
                if (args !== undefined) {
                    window.chessPy._showAlert.apply(this, args);
                }
            });
        },
        '_alertLimit': 3,
        '_alertCnt': 0,
        '_alertQueue': []
    }
})();
