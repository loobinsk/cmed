var spec_id = '';
var format = [];
var thisPageNum = 2;
var country = 0;
var town = 0;
var start = 0;
var end = 0;
window.getCookie = function (name) {
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
};

function filter() {
    var uri = $('#checkbox-1').attr('uri');
    format = [];
    var filterVal = document.getElementById('list-first').innerHTML
    $('#filter-value').val(filterVal.replace(/<.*?>/g, ''));
    if ($('#checkbox-2').prop('checked')) {
        format.push($('#checkbox-2').attr('name'));
    }
    if ($('#checkbox-3').prop('checked')) {
        format.push($('#checkbox-3').attr('name'));
    }
    if ($('#checkbox-4').prop('checked')) {
        format.push($('#checkbox-4').attr('name'));
    }
    if ($('#checkbox-5').prop('checked')) {
        format.push($('#checkbox-5').attr('name'));
    }
    if ($('#checkbox-6').prop('checked')) {
        format.push($('#checkbox-6').attr('name'));
    }
    if ($('#checkbox-7').prop('checked')) {
        format.push($('#checkbox-7').attr('name'));
    }
    if ($('#checkbox-8').prop('checked')) {
        format.push($('#checkbox-8').attr('name'));
    }
    if ($('#checkbox-9').prop('checked')) {
        format.push($('#checkbox-9').attr('name'));
    }
    if ($('#checkbox-10').prop('checked')) {
        format.push($('#checkbox-10').attr('name'));
    }
    if ($('#checkbox-11').prop('checked')) {
        format.push($('#checkbox-11').attr('name'));
    }
    if (format.length > 0) {
        $('div.content-block-top-block-1-window-filter').fadeOut();
        $.ajax({
            type: 'get',
			timeout:1000,
            url: uri,
            data: {'spec_id': spec_id, 'format': format.join(), 'country': country, 'town': town, 'start': start, 'end': end},
            success: function (data) {
                $(".content-block-center-item").remove();
                $(data).appendTo(".content-block-center");
                $('.content-block-center-item-content img').each(function (index) {
                    // this.style.width="100%";
                    // this.style.height="100%";
                })
                $('.content-block-center-item-content hr').each(function (index) {
                    this.style.width = "100%";
                });

                $('.archive-link',$(".content-block-center")).appendTo($(".content-block-center"));
                thisPageNum = 2;
                thisWork = 1;
            }
        });
    } else {
        $('div.content-block-top-block-1-window-filter').fadeOut();
        $.ajax({
            type: 'get',
            url: uri,
			timeout:1000,
            data: {'spec_id': spec_id, 'country': country, 'town': town, 'start': start, 'end': end},
            success: function (data) {
                $(".content-block-center-item").remove();
                $(data).appendTo(".content-block-center");
                $('.content-block-center-item-content img').each(function (index) {
                    /*this.style.width = "100%";
                    this.style.height = "100%";*/
                })
                $('.content-block-center-item-content hr').each(function (index) {
                    this.style.width = "100%";
                })
                $('.archive-link',$(".content-block-center")).appendTo($(".content-block-center"));
                thisPageNum = 2;
                thisWork = 1;
            }
        });
    }
}
$(document).ready(function () {

    jQuery(document).ajaxSend(function (event, jqxhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type))) {
            // ERROR Cookie IE
            if (jQuery.browser.msie)
                jqxhr.setRequestHeader("X-CSRFToken", jQuery("input[name='csrfmiddlewaretoken']").val());
            else
                jqxhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    $('iframe').attr('width', '430');

    if(document.getElementById('window-filter'))
        document.getElementById('window-filter').style.top = '-1000px';

    var showMessage = 0;
    var showList = 0;
    var checkBox = 1;
    $('#filter-value').val('Все специальности');
    $('#list-first').html('<span>Все специальности</span>');
    //---------------------------
    // Фильтр публикаций
    //---------------------------

    // Открываем и скрываем окно

    $('#filter').on('click', function () {
        $('div.content-block-top-block-1-window-filter').hide();
        $('#filter-scroll').hide();
        document.getElementById('window-filter').style.top = '8px';
        $('div.content-block-top-block-1-window-filter').fadeIn();
        //$('#list-first').html('<span>Все специальности</span>');
        if (showMessage === 1) {
            $('div.content-block-top-window-message').fadeOut();
            $('#message').html('Напиcать<br>нам');
            $('#message').attr('title', 'Напиcать нам');
            showMessage = 0;
        }
    });


    $('div.content-block-center').on('click', function (hideFilter) {
        var container = $('#filter');
        if (container.has(hideFilter.target).length === 0) {
            $('div.content-block-top-block-1-window-filter').fadeOut();
        }
    })
    $('div.content-block-right').on('click', function (hideFilter) {
        var container = $('#filter');
        if (container.has(hideFilter.target).length === 0) {
            $('div.content-block-top-block-1-window-filter').fadeOut();
        }
    })
    $('div.left-block').on('click', function (hideFilter) {
        var container = $('#filter');
        if (container.has(hideFilter.target).length === 0) {
            $('div.content-block-top-block-1-window-filter').fadeOut();
        }
    })
    $('div.content-block-top-block-2').on('click', function (hideFilter) {
        var container = $('#filter');
        if (container.has(hideFilter.target).length === 0) {
            $('div.content-block-top-block-1-window-filter').fadeOut();
        }
    })
    $('div.content-block-top-block-3').on('click', function (hideFilter) {
        var container = $('#filter');
        if (container.has(hideFilter.target).length === 0) {
            $('div.content-block-top-block-1-window-filter').fadeOut();
        }
    })

    // Открываем и скрываем список

    $('div.content-block-top-block-1-window-filter-content-right-list-all-item').on('click', function () {
        if (showList === 0) {
            $('#filter-scroll').slideDown();
            showList = 1;
        } else {
            $('#filter-scroll').slideUp();
            showList = 0;
        }
    })

    // Выбираем значение из списка

    $('div.filter-scroll-item').on('click', function () {
        var itemID = $(this).attr('id');
        spec_id = $(this).attr('id').substr(5);
        var itemVal = document.getElementById(itemID).innerHTML
        $('#list-first').html(itemVal);
        $('#filter-scroll').slideUp();
        showList = 0;
    })

    // Выбираем чекбоксы

    //$("input[type=checkbox]").prop('checked', true);

    $('#checkbox-1').on('click', function () {
        if (checkBox === 1) {
            $('.content-block-top-block-1-window-filter input[type=checkbox]').prop('checked', false); //$("input[type=checkbox]").prop('checked', false);
            checkBox = 0;
        } else {
            $("input[type=checkbox]").prop('checked', true);
            $('#checkbox-1').prop('checked', true);
            checkBox = 1;
        }
    })

    $("input[type=checkbox]").on('click', function () {
        var itemChecked = $(this).attr('checked');
        if (itemChecked === 'checked') {
            $('#checkbox-1').prop('checked', false);
            //alert(11);
            checkBox = 1;
        } else {
            checkBox = 0;
        }
    })

    // Сохраняем выбор

    $('#save-filter').click(filter);

    //---------------------------
    // Окно отправки сообщения
    //--------------------------

        $('#message').on('click', function () {
        if (showMessage === 0) {
            $('div.content-block-top-window-message').fadeIn();
            $('#message').html('Закрыть<br>окно').attr('title', 'Закрыть окно');
            showMessage = 1;
        } else {
            $('div.content-block-top-window-message').fadeOut();
            $('#message').html('Напиcать<br>нам').attr('title', 'Напиcать нам');
            showMessage = 0;
        }
    });
    $('#message-close-1').on('click', function () {
        $('div.content-block-top-window-message').fadeOut();
        $('#message').html('Напиcать<br>нам').attr('title', 'Напиcать нам');
        showMessage = 0;
    });
    $('div.content-block-top-window-message-close').on('click', function () {
        $('div.content-block-top-window-message').fadeOut();
        $('#message').html('Напиcать<br>нам').attr('title', 'Напиcать нам');
        showMessage = 0;
    });

    //---------------------------
    // Добавление постаю
    //---------------------------

    $('#post-filed-1').on('change', function () {
        var postRubric = $('#post-filed-1').val();
        $('#post-rubric').html('<span>' + postRubric + '</span>')
    });
    $('div.content-block-center-write, .content-block .info-block .btn, .content-block-center-head .add-group').on('click', function () {
        if ($(this).hasClass('savegroup')) {
            var file_0 = $('.content-block-center-write-form-block-2-left-photo-list').children('div[file]')[0];
            if (!file_0) {
                alert('Пожалуйста загрузите картинку!!!');
                return 0;
            }
            Dajaxice.groups.addgroup(Dajax.process, {'Spec_id': $('select[name="spec_id"]').val(), 'Text': $('.form-filed-13').val(), 'Title': $('input[name="title"]').val(), 'File': $(file_0).attr('file')});
        }
        $('div.content-block-center-write').hide();
        $('div.content-block-center-write-form').slideDown();
        $('.content-block .info-block .btn').text('Сохранить').addClass('savegroup');
    })
    $('div.content-block-center-write-form-close').on('click', function () {
        // clear form
        tinymce.get('description').setContent('');
        $(':input','.content-block-center-write-form-block-1')
          .not(':button, :submit, :reset, :hidden')
          .val('')
          .removeAttr('checked')
          .removeAttr('selected');
        $('#post-rubric').html('');

        $('div.content-block-center-write-form').slideUp();
        setTimeout(function () {
            $('div.content-block-center-write').fadeIn();
        }, 300);
        $('.content-block .info-block .btn').text('Создать свою группу').removeClass('savegroup');
    });


    $("#feedback_form").on('submit', function(e) {
        e.preventDefault();
        var fields = $(this).serializeArray();
        var data = {};
        for(var k in fields) {
            data[fields[k]['name']] = fields[k]['value']
        }
        if(!data['text']) {
            alert('Введите текст обращения');
            return;
        }
        if(!data['position']) {
            alert('Введите Вашу должность');
            return;
        }
        if(!data['contact']) {
            alert('Введите Ваши контактные данные: телефон или email');
            return;
        }
        Dajaxice.medtus.feedback(Dajax.process, data);
    })
});

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
