var BASE_URL = "http://localhost:8000/eureka/";

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
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
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$(document).ready(function(){

    // delete idea handler
    $("#delete_idea").click(function(){
        var idea_id = $(".idea").attr("data-idea-id");
        $.ajax({
            type: "POST",
            url: BASE_URL + "api/ideas/delete/"+idea_id,
            dataType: "json",
            success: function(data){
                if(data['status'] == "success") {
                    window.location = BASE_URL+"ideas";
                } else {
                    $('#delete_idea_modal .modal-body').hide();
                    $('#delete_idea_modal .modal-footer #delete_idea').hide();
                    $('#delete_idea_modal .alert').removeClass('hidden');
                }
            }
        }).fail(function(){
            $('#delete_idea_modal .modal-body').hide();
            $('#delete_idea_modal .modal-footer #delete_idea').hide();
            $('#delete_idea_modal .alert').removeClass('hidden');
        });
    });

    // search user input handler
    $("#find-user-input").bindWithDelay(
        "keyup",
        function() {
            var query = $(this).val().trim().toLowerCase();
            $('.user').each(function(){
                var username = $(this).find('.media-heading a').html().toLowerCase();
                var pos = username.indexOf(query);
                if (pos != -1) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        },
        250, true);

    // activate all tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // show new comment form
    $('.comments>form .init-form').focus(function(){
        var $input = $(this);
        $input.parent().addClass('hidden');
        $input.parent().nextAll('.form-group').each(function(){
            $(this).removeClass('hidden');
        });
        $('.comments>form textarea').focus();
    });

    // new comment cancel button handler
    $('.comments>form button[type="reset"]').click(function(){
        var $btn = $(this);
        $btn.parents('form').children('.form-group').each(function(){
            var $form_group = $(this);

            if($form_group.hasClass('hidden')) {
                $form_group.removeClass('hidden');
            } else {
                $form_group.addClass('hidden');
            }
        });
    });

    // input tags configuration
    var tagsInput = $('#tags-input');
    var ENTER_KEY = 13;
    var COMMA_KEY = 188;

    tagsInput.tagsinput({
        maxTags: 5,
        confirmKeys: [ENTER_KEY, COMMA_KEY],
    });

    // new idea tag input typeahead
    $.get(BASE_URL+'api/tags', function(data){
        $("#tags-typeahead").typeahead({ source:data, items:6 });
    },'json');

    // filter user ideas list
    $('.user-idea-filter').click(function(event){
        event.preventDefault();
        
        var $filter = $(this);
        $('.user-idea-filter').each(function(){
            $(this).removeClass('filter-selected');
        });

        $filter.addClass('filter-selected');

        $('.list-user-item').each(function(){
            var $idea = $(this);

            if(!$idea.hasClass($filter.attr('data-filter'))) {
                $idea.addClass('hidden');
            } else {
                $idea.removeClass('hidden');
            }
        });
    });

    // add the tags to the edit form
    // $('#edit-idea-form .bootstrap-tagsinput').prepend('<span class="tag label brand-bc">Hello</span>');
});

// minimize the header when scrolling down
$(window).scroll(function () {
    if ($(document).scrollTop() < 80) {
        $('#navbar').removeClass('nav-tiny');
    } else if ($(document).scrollTop() >= 144) {
        $('#navbar').addClass('nav-tiny');
    }
});

// marks the user as interested in an idea
function add_interest() {
    var idea_id = $(".idea").attr('data-idea-id');
    $.ajax({
        type: "POST",
        url: BASE_URL + "api/interest/"+idea_id,
        dataType: "json",
        success: function(response){
            if(response['status'] == "success") {
                window.location = BASE_URL+"ideas/"+idea_id;
                // $('.interested .btn').remove();
                var markup = ' \
                <li class="list-group-item"> \
                    <img src="{% gravatar_url ${email} 24 %}" title="${username}"> \
                    <a href="{% url "user" user_id=${id} %}">${username}</a> \
                    <span class="label label-default pull-right" title="${created}">{{${created}|naturaltime}}</span> \
                </li>';

                // $.template( "interested_template", markup);
                // $.tmpl("interested_template", {
                //     'email': response.data.email,
                //     'username': response.data.username,
                //     'id': response.data.id,
                //     'created': response.data.created
                // }).appendTo(".interested .list-group");
            } else {
                alert("Ooops, something went wrong. Please try again later.");
            }
        }
    }).fail(function(){
        alert("Ooops, something went wrong. Please try again later.");
    });
}

function remove_interest(username) {
    var idea_id = $(".idea").attr('data-idea-id');

    $.ajax({
        type: "POST",
        url: BASE_URL + "api/interest/remove/"+idea_id,
        dataType: "json",
        success: function(response){
            if(response['status'] == "success") {
                window.location = BASE_URL+"ideas/"+idea_id;
            } else {
                alert("Ooops, something went wrong. Please try again later.");
            }
        }
    }).fail(function(){
        alert("Ooops, something went wrong. Please try again later.");
    });
}

function editComment(activator, commentId) {
    var $commentBody = $(activator).parents('.comment-body');
    $commentBody.children('.comment-text').addClass('hidden');

    var formFields = ' \
        <div class="form-group"> \
            <textarea name="text" rows="3" class="form-control" required>'+$commentBody.children(".comment-text").text()+'</textarea> \
        </div> \
        <div class="form-group"> \
            <button type="submit" class="btn btn-sm btn-success">Save</button> \
            <button type="reset" class="btn btn-sm btn-default">Cancel</button> \
        </div>';

    $commentBody.children('form').append(formFields);

    // add handler to cancel button
    $commentBody.find('button[type="reset"]').click(function(){
        $commentBody.children('.comment-text').removeClass('hidden');
        $commentBody.children('form').children('.form-group').remove();
    });
}

function like_idea(idea_id) {
    $.ajax({
        type: "POST",
        url: BASE_URL + 'api/ideas/like/' + idea_id,
        dataType: "json",
        success: function(response) {
            if(response['status'] == 'success') {
                window.location = BASE_URL + 'ideas/' + idea_id;
            } else {
                alert('Ooops, something went wrong. Please try again later.');
            }
        }
    }).fail(function() {
        alert('Ooops, something went wrong. Please try again later.');
    });
}

function dislike_idea(idea_id) {
    $.ajax({
        type: "POST",
        url: BASE_URL + 'api/ideas/dislike/' + idea_id,
        dataType: "json",
        success: function(response) {
            if(response['status'] == 'success') {
                window.location = BASE_URL + 'ideas/' + idea_id;
            } else {
                alert('Ooops, something went wrong. Please try again later.');
            }
        }
    }).fail(function() {
        alert('Ooops, something went wrong. Please try again later.');
    });
}

function change_idea_state(idea_id, state) {
    $.ajax({
        type: "POST",
        dataType: "json",
        url: BASE_URL + "api/ideas/state/" + idea_id + "/" + state,
        success: function(response) {
            if(response['status'] == 'success') {
                window.location = BASE_URL + "ideas/" + idea_id;
            } else {
              alert('Ooops, something went wrong. Please try again later.');
            }
        }
    }).fail(function() {
        alert('Ooops, something went wrong. Please try again later.');
    });
}
