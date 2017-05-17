function passEye() {
	$('div.pass-eye-js').each(function() {
		var pass = $(this),
		    passInp = $('input', pass),
		    passToggle = $('a.eye', pass);

		passToggle.on('click', function() {
			var that = $(this),
			    newPassInp = $('<input />'),
			    inputType;

			if ( that.hasClass('open') ) {
				that.removeClass('open');
				inputType = 'password';
			} else {
				that.addClass('open');
				inputType = 'text';
			}

			newPassInp
				.attr({
					type: inputType,
					name: passInp.attr('name'),
					id: passInp.attr('id'),
					class: passInp.attr('class'),
					value: passInp.val()
				})
				.insertBefore(passInp);

			passInp.remove();
			pass.find('span.input-placeholder-text').remove();

			passInp = newPassInp;

			return false;
		});
	});
};

function validateForms() {
	if (typeof $.fn.validate === 'undefined') return;

	$('#validate_pass').validate({
		rules: {
			password: {
				required: true,
				minlength: 6
			},
			password_confirm: {
				required: true,
				equalTo: '#password-field'
			}
		},
		messages: {
			password: {
				required: "Введите пароль",
				minlength: jQuery.format("Пароль должен быть не менее {0} символов")
			},
			password_confirm: {
				required: "Повторите пароль",
				equalTo: "Пароли не совпадают"
			}
		},
		errorPlacement: function(error, element) {
			element.closest('div.row-holder').append(error);
		},
		highlight: function(element, errorClass) {
			var elem = $(element);
			elem.closest('div.row-holder')
				.removeClass('valid')
				.addClass('error');
		},
		unhighlight: function(element, errorClass, validClass) {
			var elem = $(element);
			elem.closest('div.row-holder')
				.addClass('valid')
				.removeClass('error');
		}
	});

	$('form.validate-js').validate({
		invalidHandler: function(e, validator) {
			var errors = validator.numberOfInvalids();
			if (errors) {
				$("span.form-errors").show();
			} else {
				$("span.form-errors").hide();
			}
		},
		errorPlacement: function(error,element) {
			return true;
		},
		highlight: function(element, errorClass) {
			var elem = $(element).closest('div.form-unit');
			elem
				.removeClass('valid')
				.addClass('error');
		},
		unhighlight: function(element, errorClass, validClass) {
			var elem = $(element).closest('div.form-unit');
			elem
				.addClass('valid')
				.removeClass('error');
		}
	});
};

function maskBD() {
	if (typeof $.fn.mask === 'undefined') return;
	$('input.mask-bd').mask(' 99   99   9999');

	$('input.mask-time').mask('99:99 ');
};

function rangeDate() {
	$('div.range-js').each(function() {
		var range = $(this),
		    rangeFrom = $('div.from', range),
		    rangeTo = $('div.to', range),
		    inputFrom = $('<input type="text">').appendTo(rangeFrom),
		    inputFromDay = $('input.day-field', rangeFrom),
		    inputFromMonth = $('input.month-field', rangeFrom),
		    inputFromYear = $('input.year-field', rangeFrom),
		    inputToDay = $('input.day-field', rangeTo),
		    inputToMonth = $('input.month-field', rangeTo),
		    inputToYear = $('input.year-field', rangeTo),
		    inputTo =  $('<input type="text">').appendTo(rangeTo),
		    fromCaller = $('a.btn-calendar', rangeFrom),
		    toCaller = $('a.btn-calendar', rangeTo);

		inputFrom.css({
			float: 'left',
			width: 1,
			height: 1,
			margin: 0,
			padding: 0,
			background: 'none',
			border: 'none',
			fontSize: 0,
			lineHeight: 0
		});

		inputTo.css({
			float: 'left',
			width: 1,
			height: 1,
			margin: 0,
			padding: 0,
			background: 'none',
			border: 'none',
			fontSize: 0,
			lineHeight: 0
		});

		inputFrom.datepicker({
			dateFormat: 'dd.mm.yy',
			firstDay: 1,
			showOtherMonths: true,
            selectOtherMonths: true,
			dayNamesMin: [ "Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб" ],
			monthNames: [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ],
			onSelect: function(dateFromParsed) {
				var dateFrom = dateFromParsed.split('.');
				inputFromDay.val( dateFrom[0] );
				inputFromMonth.val( dateFrom[1] );
				inputFromYear.val( dateFrom[2] );
				dateFrom = dateFrom.reverse().join('.');
				//inputTo.datepicker('option', 'minDate', new Date(dateFrom));
			}
		});
		inputFromDay.on('focus', function() {
			inputFrom.focus();
		});
		inputFromMonth.on('focus', function() {
			inputFrom.focus();
		});
		inputFromYear.on('focus', function() {
			inputFrom.focus();
		});


		inputTo.datepicker({
			dateFormat: 'dd.mm.yy',
			firstDay: 1,
			showOtherMonths: true,
            selectOtherMonths: true,
			dayNamesMin: [ "Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб" ],
			monthNames: [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ],
			onSelect: function(dateToParsed) {
				var dateTo = dateToParsed.split('.');
				inputToDay.val( dateTo[0] );
				inputToMonth.val( dateTo[1] );
				inputToYear.val( dateTo[2] );
				dateTo = dateTo.reverse().join('.');
				//inputFrom.datepicker('option', 'maxDate', new Date(dateTo));
			}
		});
		inputToDay.on('focus', function() {
			inputTo.focus();
		});
		inputToMonth.on('focus', function() {
			inputTo.focus();
		});
		inputToYear.on('focus', function() {
			inputTo.focus();
		});


        //inputFrom.datepicker('option', 'maxDate', new Date());
        //inputTo.datepicker('option', 'minDate', new Date( inputFrom.datepicker('getDate') ));

		fromCaller.on('click', function() {
			inputFrom.focus();
			return false;
		});

		toCaller.on('click', function() {
			inputTo.focus();
			return false;
		});
	});
};

function addField() {
	$('div.link-add-js').each(function() {
		var linkAdd = $(this),
		    fieldAdd = linkAdd.prev('div.link-add-template');

		if ( fieldAdd.length ) {
			$('a', linkAdd).on('click', function() {
				var fieldAddNew = fieldAdd.clone(true).insertAfter(linkAdd);
				return false;
			});
		}
	})
};

function selectSpec() {
	$('div.select_list_js').each(function(index, el) {
		var select_list_js = $(this),
		    select_list_all = $('div.select_list_all', select_list_js),
		    filter_scroll = $('div.filter-scroll', select_list_js)
		    showList = 0;

		select_list_all.html('<span>Выберите специальность</span>');

		function resetSelectSpec(that) {
			if (showList === 0) {
				filter_scroll.slideDown();
				showList = 1;
			} else {
				filter_scroll.slideUp();
				showList = 0;
			}
		}
		select_list_all.on('click', function() {
			resetSelectSpec( $(this) );
		});
		
		$('div.list-scroll-item').on('click', function() {
			select_list_all.html(  $(this).html() );
			filter_scroll.slideUp();
			showList = 0;
		});
	});
		
};

$(function() {
	passEye();
	validateForms();
	maskBD();
	rangeDate();
	addField();
	selectSpec();
});
