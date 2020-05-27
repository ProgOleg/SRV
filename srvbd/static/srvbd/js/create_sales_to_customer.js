$('document').ready(function() {
	/*
	Слушает кнопку чек и делает гет запрос на бек
	запрос на определение валидности введенного телефона
	вывоб соответсвенно сообщения об ошибке или ок
	если чекнутый номер закреплен за клиентом рендерит остальные поля из бд посредством confirm
	*/
	function exchange_rates(){
		//Делает запрос на курс USD по селектору exchange_rate-div и дата атрибуту data-ajax-url
		var url = $('#exchange_rates_div').data('ajax-url')
		console.log(url)
		$.get(url, function(data) {
			if(data['exchange_rates']){
				$('#id_exchange_rates').val(data['exchange_rates'])
			}
			else{
				$('#id_exchange_rates').val('!!!!!')
			}
		});
	}

	$('#role').change(function(event) {
		console.log($(this).val())
		var value = $(this).val()
		var obj = $('#discount')
		if (value == 'MA') { obj.val(25) }
		else if (value == 'CL') { }
	});


	exchange_rates()

	$('#check_but').click(function(event) {
		var url = $(this).data('url');
		var data = {'tell':$('input[name="tell"]').val()};
		var tell_input = $('input[name="tell"]');
		$.get(url,data, function(data) {
			if ('error' in data){
				tell_input.removeClass('is-valid');
				$('div.invalid-feedback').remove();
				tell_input.addClass('is-invalid');
				tell_input.after($('<div>').addClass('invalid-feedback').text(`${data['error']}`));
			}
			else if('message' in data){
				$('div.invalid-feedback').remove();
				tell_input.removeClass('is-invalid');
				tell_input.addClass('is-valid');
			}
			else{
				$('div.invalid-feedback').remove();
				tell_input.removeClass('is-invalid');
				tell_input.addClass('is-valid');
				data = data['0'];
				var last_name = data['last_name'];
				var first_name = data['first_name'];
				var patronymic_name = data['patronymic_name'];
				var tell = data['tell'];
				var addres = data['addres'];
				var email = data['email'];
				var role = data['role'];
				var discount = data['discount'];
				var result = confirm(`Клиент с таким номером телефона уже создан, использовать эти данные?\nФамилия: ${last_name}\nИмя: ${first_name} \nОтчество: ${patronymic_name}\nАдрес: ${addres} \nТелефон: ${tell}`);
				if (result === true){
					$('input[name="last_name"]').val(last_name);
					$('input[name="first_name"]').val(first_name);
					$('input[name="patronymic_name"]').val(patronymic_name);
					tell_input.val(tell);
					$('input[name="addres"]').val(addres);
					$('input[name="email"]').val(email);
					$('select[name="role"]').val(role);	
					$('input[name="discount"]').val(discount);

				}
			};
		});
	});	
});