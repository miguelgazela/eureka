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
    console.log('Document is ready!');

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
});
