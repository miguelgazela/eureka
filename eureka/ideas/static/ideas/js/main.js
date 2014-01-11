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
    $('[data-toggle="tooltip"]').tooltip({'placement': 'bottom'});
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