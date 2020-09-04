$('document').ready(function() {
	//ЖЕСТКО КОДИРОВАНЫЙ УРЛ!!!!
	var url_sales_to_customer_create = '/sales_to_customer_create/'
	function render_table(data){
		//$('#new_detail_table').removeClass('remoove');
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

	function render(data){
		$.each(data,function(i, elem) {
			//console.log(data)
			//var id = this['id'];
			var obj = $('<tr/>',{id:data[i][0]});
			var name = $('<td/>')
			//ЖЕСТКО КОДИРОВАНЫЙ УРЛ!!!!!!!
			var url = 'sales_invoice/'
			var url_edit = 'sales_to_customer/'
			var url_parts_return = 'parts_return/'
			//console.log(i)
			$.each(this,function(index, el) {
				//console.log(elem[index])
				//console.log(el)
				var foo = $('<td>')

				if (index == 3){
					if ( el == true){foo.attr('class', 'bg-success').text(el)}
					else if (el == false) {foo.attr('class', 'bg-danger').text(el)}
				}
				else if (index == 4){
					if ( el == true){foo.attr('class', 'bg-success').text(el)}
					else if (el == false) {foo.append($(`<input type="checkbox"  id="payment" value =${elem[0]} >`))}
				}//foo.attr('class', 'bg-danger').text(el)
				else if (index == 0){
					if (elem[3] === false){foo.append($('<a>').text(el).attr({'href':`${url_edit}${el}`}))}
					else {foo.append($('<a>').text(el).attr({'href':`${url}${el}`}))}
				}
				else if (index == 1){
					foo.append(`<div class='dropdown'><a class=' dropdown-toggle'  id='dropdownMenuButton' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>${el}</a><div class='dropdown-menu' aria-labelledby='dropdownMenuButton'><a class='dropdown-item' href='${url_sales_to_customer_create+data[i][0]}'>Расходный ордер</a></div></div>`)

				}
				else {foo.text(el)}

				obj.append(foo)
			});
			if (elem[3] == true){obj.append(name.append($(`<a class="btn btn-outline-info" role="button" href="${url_parts_return+elem[0]}" >Возврат</a>`)))}
			else {obj.append(name.append($(`<a class="btn btn-outline-danger" role="button" href="#" disabled >Возврат</a>`)))}
			$('#table_body').append(obj)
			/*
			$.each(function(index, el) {
				if(index === 'person_attach__last_name'){
					name.append(el)
				}
				else if(index === 'person_attach__last_name'){
					name.text(el)
				}
			
			});
			$('<a>').text(el).attr({'class':"dropdown-toggle","id":`dropdownMenuOffset_${data[i][0]}`, "data-toggle":"dropdown", "aria-haspopup":"true", "aria-expanded":"false", "data-offset":"10,20"})
			*/
		});
	}

	function new_detail_table(ind){
		var url = $('#table_body').data('ajax_url')
		$.get(url,{'page': ind}, function(data) {
			render(data)
		}).fail(function(){
			return null
		})
		
	};

	var page = 1
	new_detail_table(page)
	



	$(window).scroll(function(event) {
		if ($(window).scrollTop() + $(window).height() >= $(document).height()){
			page += 1
			new_detail_table(page)
			console.log(page)
		}
	});

	$(document).on('click','#payment', function(event) {
		//event.preventDefault();
		var result_que = confirm('Вы уверенны?')
		var url = $('#table').data('ajax_url')
		var val = this['value']
		if (result_que){
			var result = $(this).prop('checked');
			$.post(url,{'id':val,'status':result}, function(data){});
		}
		else {
			event.preventDefault();
		}
	});

	
})