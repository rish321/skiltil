$(function () {
    selectedStrings = [];
    $(document).on('click', '.btn-add', function (e) {
        e.preventDefault();
        console.log("add ");
        var stringVal = $(this).parents('.entry:first').find('input').val();
        console.log(stringVal);
        console.log(selectedStrings);

        if (stringVal == "" || selectedStrings.indexOf(stringVal) > -1)
            return false;

        selectedStrings.push(stringVal);


        console.log("add ");

        var controlForm = $('.controls form:first'),
            currentEntry = $(this).parents('.entry:first'),
            newEntry = $(currentEntry.clone()).appendTo(controlForm);

        newEntry.find('input').val('');
        controlForm.find('.entry:not(:last) .btn-add')
            .removeClass('btn-add').addClass('btn-remove')
            .removeClass('btn-success').addClass('btn-danger')
            .html('<span class="glyphicon glyphicon-minus"></span>');
        $('.typeahead').trigger('added');

        console.log(selectedStrings);
    }).on('click', '.btn-remove', function (e) {

        console.log(selectedStrings);
        for (var i = selectedStrings.length - 1; i >= 0; i--) {
            if (selectedStrings[i] === $(this).parents('.entry:first').find('input').val()) {
                selectedStrings.splice(i, 1);
                break;
            }
        }
        $(this).parents('.entry:first').remove();


        console.log(selectedStrings);
        e.preventDefault();
        return false;
    }).on('click', '.submit-skills', function (e) {
        if (selectedStrings.length <= 0)
            return false;
        var myJsonString = JSON.stringify(selectedStrings);


        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax({
            url: '/profile/update_skills/',
            type: "POST",
            data: {msg: myJsonString},
            success: function (response) {
                location.reload();
            },
            complete: function () {
            },
            error: function (xhr, textStatus, thrownError) {
            }
        });


    });
});