$('document').ready(function(){

	// добавляет новые объекты дата атрибуты фильтров
	function set_option_atribut(data){
		//data - селектора поля инпут возврщенный событием
		//апендит datalist по 'name' attr(data)
		//forma ajax запроса = data-ajax_url = "URL"
		var val = data.value;
		var element = data.name
		var form = $(data).data('ajax_url')
		$.get(form,{'val': val}, function(data) {
			var obj = $(`#${element}`);
			var item = $.map(data, function(item, index) {
				return $('<option>').attr('value', item)});
			obj.empty()
			obj.append(item)
			
		});
	}

	function add_specification(data){
		var url = $('#url_specification').data('ajax_url')
		$.post(url, data, function(data, textStatus, xhr) {
			console.log(textStatus)
		});
	}

	// Cелекторы полей фильтра
	$('input[name="attachment_part"]').on('input',function(data){
		var data = this
		set_option_atribut(data)
	});

	$('input[name="attachment_appliances"]').on('input',function(data){
		var data = this
		set_option_atribut(data)
	});

	$('input[name="attachment_manufacturer"]').on('input',function(data){
		var data = this
		set_option_atribut(data)
	});



	$('#save_type_spar_part').click(function(event) {
		var data = {'type_spar_part' : $('input[name="type_spar_part"]').val()}
		add_specification(data)
		
	});

	$('#save_type_appliances').click(function(event) {
		var data = {'type_appliances' : $('input[name="type_appliances"]').val()}
		add_specification(data)
		
	});

	$('#save_manufacturer').click(function(event) {
		var data = {'manufacturer' : $('input[name="manufacturer"]').val()}
		add_specification(data)
		
	});




})