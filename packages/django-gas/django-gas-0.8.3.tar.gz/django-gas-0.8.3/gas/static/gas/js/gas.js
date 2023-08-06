var GAS = {
    config: {
        'menuItemSelector': '.dropdown',
        'openedMenuItemClass': 'open',
    },
    init: function() {
        $(document).ready(function(){
            $('.select2').select2({
                width: 'resolve',
            });

            $('#messages .message-close').click(function(event){
                event.preventDefault();
                let $message = $(this).parents('.message');
                $message.remove();
            });
            GAS.toggle(
                GAS.config.menuItemSelector,
                GAS.config.openedMenuItemClass,
            );
        });

        var csrftoken = GAS.getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    },

    select2_ajax: function (selector, command) {
        $(selector).select2({
            ajax: {
                url: '.',
                dataType: 'json',
                delay: 250,
                type: 'POST',
                data: function(params){
                    return $.extend({
                        'command': command,
                        'page': 1,
                    }, params);
                },
                minimumInputLength: 1,
                cache: false
            },
            templateResult: function(item){
                return item.text;
            },
            templateSelection: function(item){
                return item.text;
            },
        });
    },

    getCookie: function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    toggle: function(selector, cssclass) {
        const items = document.querySelectorAll(selector);
        for (const item of items) {
            item.addEventListener('click', function(ev) {
                if (item.classList.contains(cssclass)) {
                    item.classList.remove(cssclass);
                } else {
                    item.classList.add(cssclass);
                }
            });
        }
    }
}

GAS.init();
