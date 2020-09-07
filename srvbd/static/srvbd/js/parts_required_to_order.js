jQuery(document).ready(function($) {


	function renderNewDetailTableV2(data){
		// ожидает JSON 
		
		$.each(data,function(index, el) {
			var data_array = data[index]
			var id = data_array['detail_name__pk'];
			var obj = $('<tr/>',{'id':id});
			var detail_name__pk = $('<td>').text(id)
			var detail_name__name = $('<td>').text(data_array['detail_name__name'])
			var detail_name__part_num = $('<td>').text(data_array['detail_name__part_num'])
			var detail_name__attachment_part__type_spar_part = $('<td>').text(data_array['detail_name__attachment_part__type_spar_part']) 
			var option_button = $('<td>').append(`<div class='dropdown'><button type="button" class=' btn btn-info btn-sm dropdown-toggle'  id='dropdownMenuButton' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false'>Действие</button><div class='dropdown-menu' aria-labelledby='dropdownMenuButton'><a class='dropdown-item' href='#'>Инф. запчасти</a><a class='dropdown-item' href='#'>История приходов</a><a class='dropdown-item' href='#'>История расходов</a></div></div>`)

			list_field = [detail_name__pk,detail_name__name,detail_name__part_num,detail_name__attachment_part__type_spar_part,option_button]
			
			$.each(list_field,function(index, elem) {
				obj.append(elem)
			});
			
			$('#tbody_detail').append(obj);
		});
	}

	function getNewDetailTable(){
		var url = $('#tbody_detail').data('ajax_url')
		$.get(url, function(data){
			if(data.length>0 === true){renderNewDetailTableV2(data)}	
		});
	}


	getNewDetailTable()







});