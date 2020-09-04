jQuery(document).ready(function($) {

	//ЖЕСТКО КОДИРОВАНЫЙ URL
	var url_incoming = '/incoming_list/'
	var discount = $('#discount').val()
	if (parseFloat(discount) === 0){discount=false}

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

	function renderNewDetailTableV2(data){
		// ожидает JSON 
		$('#new_detail_table').removeClass('remoove');
		$.each(data,function(index, el) {
			var data_array = data[index]
			var obj = $('<tr/>',{'id':data_array['id']});
			var id = data_array['id'];
			var sale_price = data_array['sale_price']
			var detail_attach__detail_name__name = $('<td>').text(data_array['detail_attach__detail_name__name'])
			var detail_attach__detail_name__part_num = $('<td>').text(data_array['detail_attach__detail_name__part_num']) 
			var detail_attach__detail_name__specification = $('<td>').text(data_array['detail_attach__detail_name__specification']) 
			var normalize_incoming_price = $('<td>').attr({'data-normalize_incoming_price_pk': id,'data-value':data_array['normalize_incoming_price']}).text(data_array['normalize_incoming_price']) 
			var quantity = data_array['quantity']

			var sale_price_el = $('<td>').append($('<input/>',{
									'type':'number','step':'0.01','value':sale_price,'min':sale_price,'class':'input_ch form-control',
									'name':'sale_price','data-id':id,'id':`sale_price_${id}`}))
			var quantity_el = $('<td>').append($('<input/>',{
									'type':'number','step':'0.01','value':quantity,'min':'1','class':'input_ch form-control',
									'name':'quantity','data-id':id}))
			var knob_del = $('<td>').append($('<button>').attr({'type':'button','class':'btn btn-outline-danger',
						'id':'but_delete','value':id}).text('Удалить'));
			var knob_hist = $('<td>').append($('<button>').attr({'type':'button','class':'btn btn-outline-info',
				'id':'but_history','value':id, 'data-toggle':"modal",'data-target':"#history_modal"}).text('История'));
			list_field = [detail_attach__detail_name__name,detail_attach__detail_name__part_num,detail_attach__detail_name__specification,quantity_el,normalize_incoming_price,sale_price_el,knob_del,knob_hist]
			$.each(list_field,function(index, elem) {
				obj.append(elem)
			});
			
			obj.append(knob_del);
			obj.append(knob_hist);
			$('#tbody_new_detail').append(obj);
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
									'name':'sale_price','data-id':id,'id':`sale_price_${id}`})))}
				else if(index === 'quantity'){
					obj.append($('<td>').append($('<input/>',{
									'type':'number','step':'0.01','value':el,'min':'0','class':'input_ch form-control',
									'name':'quantity','data-id':id,})))}
				else if(index === 'id'){return}
				else{obj.append($('<td>').text(el))}
			});
			var knob_del = $('<button>').attr({'type':'button','class':'btn btn-outline-danger',
						'id':'but_delete','value':data[i]['id']}).text('Удалить');
			var knob_hist = $('<button>').attr({'type':'button','class':'btn btn-outline-info',
						'id':'but_history','value':data[i]['id'], 'data-toggle':"modal",
						 'data-target':"#history_modal"
					}).text('История');
			obj.append($('<td>').append(knob_del));
			obj.append($('<td>').append(knob_hist));
			$('#tbody_new_detail').append(obj);
		});
	}

	function getNewDetailTable(){
		var url = $('div.container').data('index-url')
		$.get(url, function(data){
			if(data.length>0 === true){renderNewDetailTableV2(data)}	
		});
	}


	function clearInvalidFeedBack(obj){
		obj
	}

	function round(value, decimals) {
    	return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
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
			if (data['error']){alert(data['error'])}
			else{renderNewDetailTableV2(data)}
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

	function change_input_val_quant_saleprice(id,field,new_val,obj,form){

		var data = {'id':id, 'field':field,'new_val':new_val};
		$.post(form,data,function(data,status){
			obj.removeClass('is-invalid');
			obj.next('div').remove()
			if (data['error']){
					obj.addClass('is-invalid')
					obj.after($('<div>').addClass('invalid-feedback').text(`${data['error']}`))
			}
		})
		
	}

	$('#tbody_new_detail').on('change','.input_ch',function(data){
		var obj = $(this)
		var new_val = this['value'];
		var field = this['name'];
		var id = $(this).data('id');
		var form = $('div#new_detail_table').data('ajax-change-quant-price-url');
		change_input_val_quant_saleprice(id,field,new_val,obj,form)
	})	

	$('#save').click(function(event) {
		var payment_status = $('#payment').prop("checked")
		var url = $('div.container').data('index-url')
		$.post(url,{'payment_status': payment_status},function(data,statusText) {
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

	$('#tbody_new_detail').on("click",'#but_history',function(data){
		var url_get_own_coefficient = $('#history_modal').data('ajax_url')
		mat_sales_obj_pk = this.value
		$.get(url_get_own_coefficient, {'mat_sales_obj_pk': mat_sales_obj_pk}, function(data) {
			$('#modal_tbody').empty()
			$.each(data,function(index, eleme) {
				var obj = $('<tr>')
				$.each(this,function(i, el) {
					if (i==0) {return}
						else if(i==4){
							var foo = $('<td>').append($('<a>').attr({'data-value': `${el}`,'href':'#','id':'coefficient_link'}).text(el));
							obj.append(foo)
						}
						else{
							var foo = $('<td>')
							foo.text(el)
							obj.append(foo)
						}
				});
				$('#modal_tbody').append(obj.fadeIn('400'));
			});
		});
	});

	function change_and_validation_valid_data_sale_price_input(coefficient){

		if (discount){

			var disc = discount / 100
			var obj = $(`#sale_price_${mat_sales_obj_pk}`)
			var id = mat_sales_obj_pk
			var field = 'sale_price'
			var form = $('div#new_detail_table').data('ajax-change-quant-price-url');
			var normalize_incoming_price = $(`[data-normalize_incoming_price_pk=${id}]`).data('value')
			normalize_incoming_price = parseFloat(normalize_incoming_price)
			var markup = normalize_incoming_price * coefficient
			var new_val = markup - (markup * disc)
			new_val = round(new_val,2)
			change_input_val_quant_saleprice(id,field,new_val,obj,form)
			obj.val(new_val)
		}
			else{}
		$('#history_modal').modal('hide')

	}


	$('#modal_tbody').on('click', '#coefficient_link', function(event) {
		event.preventDefault();
		var coefficient = $(this).data('value')
		var coefficient = parseFloat(coefficient)
		change_and_validation_valid_data_sale_price_input(coefficient)

	});
	
	$('.modal-body').on('click', '#coefficient_submit', function(event) {

		function add_invalid_feedback(obj,error){
			obj.removeClass('is-invalid');
			obj.next('div').remove()
			if (error){
					obj.addClass('is-invalid')
					obj.after($('<div>').addClass('invalid-feedback').text(error['error']))
			}
		}

		var error = false
		var obj = $('#coefficient_input')
		var coefficient = obj.val()
		var coefficient = parseFloat(coefficient)
		if (coefficient <= 0 || coefficient === NaN){
			add_invalid_feedback(obj,{'error':'Не валидные данные!'})
		}
		else {
			add_invalid_feedback(obj,error)
			change_and_validation_valid_data_sale_price_input(coefficient)
		}
		
	});


	
	$('#but_dropping').click(function(event) {
		$('#filter_table').addClass('remoove')
		
	});


});