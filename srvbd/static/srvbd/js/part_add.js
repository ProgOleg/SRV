$('document').ready(function(){

	// добавляет новые объекты дата атрибуты фильтров
	function set_option_atribut(data){
		// V 2.0 создает <datalist values=id>text<datalist/>
		//data - селектора поля инпут возврщенный событием
		//апендит datalist по 'name' attr(data)
		//forma ajax запроса = data-ajax_url = "URL"
		var val = data.value;
		var element = data.name
		var form = $(data).data('ajax_url')
		$.get(form,{'val': val}, function(data) {
			/*
			console.log(data)
			var obj = $(`#${element}`);
			var item = $.map(data, function(item, index) {
				return $('<option>').attr({'value' :item[0],'label': item[1]}).text(item[1])});
			*/
			var obj = $(`#${element}`);
			var item = $.map(data, function(item, index) {
				return $('<option>').attr('value', item)});
			obj.empty()
			obj.append(item)
			
		});
	}

	function add_specification(data,field_name){
		var url = $('#url_specification').data('ajax_url')
		$.post(url, data, function(data, textStatus, xhr) {
			var curssor = 'id_' + field_name
			var close_but = 'close_' + field_name
			if (data['success'] == 'True'){
				$(`#${curssor}`).removeClass('is-invalid')
				$(`#${field_name}`).remove()
				$(`#${close_but}`).click()
			}
			else if (data['success'] == 'False') {
				if (field_name == 'type_spar_part'){var error_message = data['error_message'].type_spar_part[0]}
				else if (field_name == 'type_appliances') {var error_message = data['error_message'].type_appliances[0]}
				else if (field_name == 'manufacturer') {var error_message = data['error_message'].manufacturer[0]}
				$(`#${field_name}`).remove()
				$(`#${curssor}`).addClass('is-invalid')
				$(`#${curssor}`).after(`<div class="invalid-feedback" id ="${field_name}">${error_message}<div/>`)
			}	
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
		field_name = 'type_spar_part'
		var data = {'type_spar_part' : $('input[name="type_spar_part"]').val()}

		add_specification(data,field_name)
		
	});

	$('#save_type_appliances').click(function(event) {
		field_name = 'type_appliances'
		var data = {'type_appliances' : $('input[name="type_appliances"]').val()}
		add_specification(data,field_name)
		
	});

	$('#save_manufacturer').click(function(event) {
		field_name = 'manufacturer'
		var data = {'manufacturer' : $('input[name="manufacturer"]').val()}
		add_specification(data,field_name)
		
	});




})