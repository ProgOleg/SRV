jQuery(document).ready(function($) {
	function set_option_atribut(data){
		//data - селектора поля инпут возврщенный событием
		//апендит datalist по 'name' attr(data)
		//forma ajax запроса = data-ajax_url = "URL"
		var val = data.value;
		var element = data.name
		var form = $(data).data('ajax_url')
		$.get(form,{'val': val}, function(data) {
			console.log(data)
			var obj = $(`#${element}`);
			var item = $.map(data, function(item, index) {
				return $('<option>').attr('value', item)});
			obj.empty()
			obj.append(item)
			
		});
	}

	$('input[name="select_type_sparpart"]').on('input',function(data){
		var data = this
		set_option_atribut(data)
	});

	$('input[name="select_applience"]').on('input',function(data){
		var data = this
		set_option_atribut(data)
	});

	$('input[name="select_manufacturer"]').on('input',function(data){
		var data = this
		set_option_atribut(data)
	});





});