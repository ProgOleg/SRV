$('document').ready(function(){

	var page = 1
	var data = null
	//ЖЕСТКО КОДИРОВАНЫЙ URL
	var filter_url = '/ajax_detail_in_stock_filter/'
	var url_incoming = '/incoming_list/'


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

	function render(data){
		console.log(data)
		$.each(data,function(index, el) {
			var obj = $('<tr/>');
			$.each(this,function(i, elem) {
				if (i == 'attach_for_incoming__id') {}
				else {
					var foo = $('<td>')
					if(i == 'date_and_exch'){
						foo.append($(`<a href=${url_incoming + data[index]['attach_for_incoming__id']} >${elem}</a>`))
					}
					else {
						foo.text(elem)
					}
					obj.append(foo)
				}	
			});
			$('#table_body').append(obj)
		});
	}

	function new_detail_table(ind,data){
		var url = filter_url + ind + '/'
		$.get(url,data, function(data) {
			render(data)
		}).fail(function(){
			return null
		})
		
	};

	$(window).scroll(function(event) {
		if ($(window).scrollTop() + $(window).height() >= $(document).height()){
			page += 1
			new_detail_table(page,data)
			console.log(page)
		}
	});

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

	new_detail_table(page,data)


	$('#filter_form').submit(function(event){
		/*
		event.preventDefault();
		page = 1
		var filter_filds = $(this).serializeArray()
		//var data = JSON.stringify(filter_filds)
		var data = []
		data.push({'filter': filter_filds})
		data.push({'page':{'name':'page','value':page}})

		console.log(data)
		data = JSON.stringify(data)
		$.get(filter_url,data, function(data) {
			$('#filter_table_body').empty()
			render(data)
			//$('#filter_table_body').append(obj.fadeIn('400'));
		});
		*/
		event.preventDefault();
		page = 1
		data = $(this).serializeArray()
		//var filter_filds = JSON.stringify(data)
		$('#table_body').empty()
		new_detail_table(page,data)
	});




});