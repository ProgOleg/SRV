$('document').ready(function() {

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
			var url = 'sales_to_customer/'
			//console.log(i)
			$.each(this,function(index, el) {
				var foo = $('<td>')
				if (index == 4){
					if ( el == true){foo.attr('class', 'bg-success').text(el)}
					else if (el == false) {foo.attr('class', 'bg-danger').text(el)}
				}
				else if (index == 0){foo.append($('<a>').text(el).attr({'href':`${url}${el}`}))}
				else {foo.text(el)}
				obj.append(foo)
			});
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
})