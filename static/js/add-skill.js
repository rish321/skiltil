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

        console.log(controlForm);
        console.log(currentEntry);
        console.log(newEntry);

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
    }).on('click', '#submit-skills', function (e) {
        console.log("submitted list");
        if (selectedStrings.length <= 0)
            return false;
        var myJsonString = JSON.stringify(selectedStrings);

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