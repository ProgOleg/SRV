$('document').ready(function(){
// Рендерит таблицу с новыми запчастями если они есть в конкретном приходе.
	var url = $('div').data('index-url')
	$.get(url,function(data){
		if ('massage' in data){
		}
		else{
			$('#detail_table').removeClass('remoove')
			$.each(data,function(i,e){
				var id = this['id'];
				obj = $('<tr>').attr({'data-obj_id':id});
				$.each(this,function(i,e){
					if(i === 'id'){
						return true;
					};
					if (i === 'incoming_price'|| i === 'quantity'){
						obj.append($('<td>').append(
							$('<input/>', {
								'type':'number','step':'0.01','value':e,'class':'input_ch','name':i,'data-id':id})
						));
					}
					else{
						obj.append($('<td>').text(e));
					};
				})
				knob = $('<button>').attr({'type':'button','class':'btn btn-outline-danger',
					'id':'but_delete','value':id}).text('Удалить');
				obj.append($('<td>').append(knob));
				$('#tbody_new_detail').append(obj);
			})
		}
	})
// Отправка данных с формы фильтра SparPart и рендерин таблицы отфильтрованых объектов.
	$('#but_filter').click(function(event){
		$('#table_body').empty()
		$('#filter_table').removeClass('remoove')
		var attachment_appliances = $('input[name=attachment_appliances').val();
		var attachment_part = $('input[name=attachment_part').val();
		var attachment_manufacturer = $('input[name=attachment_manufacturer').val();
		var form = $('#form').attr('action');
		var data = {};
		data.attachment_appliances = attachment_appliances;
		data.attachment_part = attachment_part;
		data.attachment_manufacturer = attachment_manufacturer;
		$.ajax({
			url: form,
			method: "GET",
			data: data,
			dataType: "JSON",
			success: function(data){
				$.each(data,function(i,e){
					obj = $('<tr>');
					$.each(this,function(i,e){
						obj.append($('<td>').text(e));
					});
					knob = $('<button>').attr({'type':'button','class':'btn btn-outline-info',
						'id':'but_detail','value':e['id']}).text('Добавить');
					obj.append($('<td>').append(knob));
					$('#table_body').append(obj);
				});
			}
		});
	});
// Добавление объекта в incoming. Рендеринг таблицы с новыми запчастями.	
	$('#table_body').on("click",'#but_detail',function(){
		var data = this.value;
		var form = $('#form_detail').attr('action');
		$.ajax({
			url: form,
			method: "POST",
			data: {'id_spar_part':data},
			dataType: "JSON",
			success: function(data){
				$.each(data,function(i,e){
					if ('error' in data){
						alert(data['error'])
					}
					else{
						$('#detail_table').removeClass('remoove')
						var id = this['id'];
						obj = $('<tr>').attr({'data-obj_id':id});
						$.each(this,function(i,e){
							if(i === 'id'){
								return true;
							};
							if (i === 'incoming_price'|| i === 'quantity'){
								obj.append($('<td>').append(
									$('<input/>', {
										'type':'number','step':'0.01','value':e,'class':'input_ch','name':i,'data-id':id})
								));
							}
							else{
								obj.append($('<td>').text(e));
							};
						})
						knob = $('<button>').attr({'type':'button','class':'btn btn-outline-danger',
							'id':'but_delete','value':id}).text('Удалить');
						obj.append($('<td>').append(knob));
						$('#tbody_new_detail').append(obj);
					};
				})
			}
		})
	})	
//Изменение значения полей цена и кол-во
	$('#tbody_new_detail').on('change','.input_ch',function(data){
		var new_val = this['value'];
		var field = this['name'];
		var id = $(this).data('id');
		var form = $('#form_change_detail').attr('action');
		var data = {'id':id, 'field':field,'new_val':new_val};
		$.post(form,data,function(data){
			if (data){
				console.log('item: '+field+','+'id: '+id+','+'val: '+new_val+'----UPDATING!')
			}
		})
	})	
//Удаление объекта из бд. Удаление строки из таблицы с деталями. Если в таблице нет объектов > таблица скрывается
	$('#tbody_new_detail').on("click",'#but_delete',function(data){
		var id = this['value']
		var form = $('#tbody_new_detail').data('form-action')
		$.post(form,{'delete_obj':id},function(data){
			if(data['error']){
				alert(data['error'])
			}
			else{
				$('[data-obj_id='+id+']').remove()
				if ($('#tbody_new_detail').children('tr').length>0){
					console.log('нихуя!')
				}
				else{
					console.log('хуя!')
					$('#detail_table').addClass('remoove')
				}
			}
		})
	})	
});	

