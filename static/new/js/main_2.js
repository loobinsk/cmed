/**
 * Created by PekopT on 04.12.14.
 */
 function timerIncrement() {
    jQuery.ajax({
        url: "/account/timer/",
        type: "post",
        data: {
            id: $("#object_id").val()
        }
    });
}

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

$(function () {
    $.fn.serializeObject = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
    $(".del-image").on('click', function (e) {
        if (e.target == this) {
            var imageId = $(this).attr('rel');
            Dajaxice.lichnie.deleteImage(Dajax.process, {
                image_id: imageId
            });
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $(".photos a, .slide a").hover(function (e) {
        $(this).find(".del-image").show();
    }, function () {
        $(this).find(".del-image").hide();
    });

    $("#group-users").on('click', function (e) {
        $(".info.groups .box.popup").toggle();
        e.preventDefault();
    });

    //hide it when clicking anywhere else except the popup and the trigger
    $(document).on('click', function (event) {
        if (!$(event.target).parents().addBack().is('#group-users')) {
            $(".info.groups .box.popup").hide();
        }
    });
    // Prevent events from getting pass .popup
    $(".info.groups .box.popup").click(function (e) {
        e.stopPropagation();
    });

    $(".content-block-top-block-1-filed-search").on('click', function () {
        $(this).closest('form').submit();
    });





    $('.rss_source').click(function(e){
        var cntlink = $(this).data('cntlink');
        $.get(cntlink);
    });

    $(document).on('click', '.delete_comment', function(e) {
        var comment_id = $(this).data('comment');
        var url = $(this).data('url');
        var csrftoken = getCookie('csrftoken');
        var postData = {'comment_id': comment_id,
        'csrfmiddlewaretoken': csrftoken
    };
    var self = this;
    $.post(url, postData, function(data) {
        if (data == 'OK') {
            location.reload();
        } else {
            alert('Невозможно удалить');
            $(self).hide();
        }
    });
});

    $(document).on('click', '.delete_post', function(e) {
        e.preventDefault();
        var post_id = $(this).data('post');
        var url = $(this).data('url');
        var post_type = $(this).data('type');
        var csrftoken = getCookie('csrftoken');
        var postData = {'post_id': post_id,
        'type': post_type,
        'csrfmiddlewaretoken': csrftoken
    };
    var self = this;
    $.post(url, postData, function(data) {
        if (data == 'OK') {
            if ($(self).data('to_main')) {
                location.href = '/';
            } else {
                location.reload();
            }
        } else {
            alert('Невозможно удалить');
            $(self).hide();
        }
    });
});
});


var showLoader = function (status) {
    if (status) {
        if ($('#preloader').length == 0) {
            $('<div id="preloader" title="Ожидайте..."/>').appendTo($('body'));
        }
    }
    else {
        $('#preloader').remove();
    }
}



// Кнопка наверх


$(document).ready(function() { 
  var button = $('#button-up'); 
  $(window).scroll (function () {
    if ($(this).scrollTop () > 300) {
      button.fadeIn();
    } else {
      button.fadeOut();
    }
});  
button.on('click', function(){
$('body, html').animate({
scrollTop: 0
}, 800);
return false;
});      
});

//Поиск

$(document).ready(function() {
     
            $(".fa-search").click(function() {
               $(".content-block-top-block-2-filed").toggle();
               $(".form-filed-9").focus();
             });
 
        });




