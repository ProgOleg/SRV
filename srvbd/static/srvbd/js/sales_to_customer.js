jQuery(document).ready(function($) {

	//ЖЕСТКО КОДИРОВАНЫЙ URL
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


	function renderNewDetailTable(data){
		//$('#tbody_new_detail').empty();
		$('#new_detail_table').removeClass('remoove');
		$.each(data,function(i, e) {
			var id = this['id'];
			var obj = $('<tr/>',{'id':data[i]['id']});
			$.each(this,function(index, el) {
				if(index === 'sale_price'){
					obj.append($('<td>').append($('<input/>',{
									'type':'number','step':'0.01','value':el,'min':el,'class':'input_ch form-control',
									'name':'sale_price','data-id':id})))}
				else if(index === 'quantity'){
					obj.append($('<td>').append($('<input/>',{
									'type':'number','step':'0.01','value':el,'min':'0','class':'input_ch form-control',
									'name':'quantity','data-id':id,})))}
				else if(index === 'id'){return}
				else{obj.append($('<td>').text(el))}
			});
			var knob = $('<button>').attr({'type':'button','class':'btn btn-outline-danger',
						'id':'but_delete','value':data[i]['id']}).text('Удалить');
			obj.append($('<td>').append(knob));
			$('#tbody_new_detail').append(obj);
		});
	}

	function getNewDetailTable(){
		var url = $('div.container').data('index-url')
		$.get(url, function(data){
			if(data.length>0 === true){renderNewDetailTable(data)}	
		});
	}


	function clearInvalidFeedBack(obj){
		obj
	}
	

	getNewDetailTable()

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
		
	$('#filter_form').submit(function(event) {
		event.preventDefault();
		var data = $(this).serializeArray()
		var url = this.action
		$.get(url,data, function(data) {
			console.log(data)
			$('#filter_table_body').empty()
			$('#filter_table').removeClass('remoove')
			$.each(data,function(index, el) {
				var obj = $('<tr>')
				$.each(this,function(i, elem) {
					var foo = $('<td>')
					if (i == 'id') {}
						else if (i == 'attach_for_incoming__id') {}
						else if (i == 'date_and_exch') {
							foo.append($(`<a href=${url_incoming + data[index]['attach_for_incoming__id']} >${elem}</a>`))
							obj.append(foo)
						}
						else {
							foo.text(elem)
							obj.append(foo)
						}
						
				});
				knob = $('<button>').attr({'type':'button','class':'btn btn-outline-info',
						'id':'but_add','value':data[index]['id']}).text('Добавить');
				obj.append($('<td>').append(knob));
				$('#filter_table_body').append(obj.fadeIn('400'));
			});
		});
	});

	$('#filter_table_body').on('click','#but_add',function(event){
		var val = this.value;
		var url = $('#filter_table_body').data('ajax_url');
		$.post(url, {'value': val}, function(data){
			console.log(data)
			if (data['error']){alert(data['error'])}
			else{renderNewDetailTable(data)}
		});
	});

	$('#tbody_new_detail').on("click",'#but_delete',function(data){
		var id = this['value']
		var form = $('#tbody_new_detail').data('form-action')
		$.post(form,{'delete_obj':id},function(data,textStatus){
			if(textStatus === 'success'){
				$(`tr#${id}`).fadeOut('300',function(){this.remove()})
				if ($('#tbody_new_detail').children('tr').length>0){}
				else{$('#new_detail_table').addClass('remoove')}
			}
		});
	});	

	$('#tbody_new_detail').on('change','.input_ch',function(data){
		var obj = $(this)
		var new_val = this['value'];
		var field = this['name'];
		var id = $(this).data('id');
		var form = $('div#new_detail_table').data('ajax-change-quant-price-url');
		var data = {'id':id, 'field':field,'new_val':new_val};
		$.post(form,data,function(data,status){
			console.log(data)
			obj.removeClass('is-invalid');
			obj.next('div').remove()
			if (data['error']){
					obj.addClass('is-invalid')
					obj.after($('<div>').addClass('invalid-feedback').text(`${data['error']}`))
			}
		})
	})	

	$('#save').click(function(event) {
		var payment_status = $('#payment').prop("checked")
		var url = $('div.container').data('index-url')
		$.post(url,{'payment_status': payment_status},function(data,statusText) {
			console.log(data)
			console.log(statusText)
			if (statusText === 'success' && data){
				if ('quant_val_error' in data){
					$(`#${data['quant_val_error']}`).addClass('error')
					alert('Количесвто одной из продаваемых запчастей привышает фактическое кол-во на складе!')
				}
				else if ('url' in data) {
					var url = data['url']
					$(location).attr('href',url);
				}
				else if ('error_status' in data) {
					alert(data['error_status'])
				}
				else {
					$('<tr>').removeClass('error')
				}
			}
		});
	});

	
	


});