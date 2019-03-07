$('document').ready(function(){
	function set_option_atribut(data){
		//data - селектора поля инпут возврщенный событием
		//апендит datalist по 'name' attr(data)
		var val = data.value;
		var element = data.name
		var form = $('div[data-ajax-url]').data('ajax-url');
		$.get(form,{'field': element,'val': val}, function(data) {
			if ('error' in data){
				alert(data['error'])
			}
			else{
				var obj = $(`#${element}`) ;
				var item = $.map(data, function(item, index) {
					return $('<option>').attr('value', item)
				});
				obj.empty()
				obj.append(item)
			}
		});
	}
	
	$('input[name="manufacturer"]').on('input',function(data){
		var data = this
		set_option_atribut(data)
	});

	$('input[name="type_appliances"]').on('input',function(data){
		var data = this
		set_option_atribut(data)
	});
	
	$('#form_submit').submit(function(event) {
		var mod = $('input[name="mod"]');
		var pnc = $('input[name="pnc"]');
		var type_appliances = $('input[name="type_appliances"]');
		var manufacturer = $('input[name="manufacturer"]');
		var form = this.action;
		var data = {'mod':mod.val(),'pnc':pnc.val(),'type_appliances':type_appliances.val(),'manufacturer':manufacturer.val()};

		$.post(form, data, function(data){
			$('input.is-invalid').each(function(index, el) {
				$(this).removeClass('is-invalid');
			});
			$('div.invalid-feedback').remove()
			
			if ('error'in data){
				if ('manufacturer' in data['error']){
					manufacturer.addClass('is-invalid')
					manufacturer.after($('<div>').addClass('invalid-feedback').text(`${data['error']['manufacturer']}`))
				}
				else if('type_appliances' in data['error']){
					type_appliances.addClass('is-invalid')
					type_appliances.after($('<div>').addClass('invalid-feedback').text(`${data['error']['type_appliances']}`))
				}
				else{
					console.log(data['error'])
				}	
			}
		});
		return false;

	});
})
