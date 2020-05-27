$('document').ready(function() {
	
	$('#save').click(function(event) {
		var url = $('#parts').data('ajax_url')
		var parts = $('#parts').find('[name=quantity]')
		var data = []
		parts.each(function(index, el) {
			var id = $(this).data('part-id')
			var val = this.value
			if (val > 0){data.push({'id':id,'value':val})}
		});
		data = JSON.stringify(data)
		$.post(url, {'data': data}, function(data, textStatus, xhr) {
			console.log(data)
			console.log(textStatus)
			console.log(xhr.status)
			console.log(data['data'])
			if (xhr.status == 200 ){$(location).attr('href',data['data'])}
		});
	});
		
	$('#return_all').click(function(event) {
		$('[name=quantity]').each(function(index, el) {
			el.value = el.max
		});
	});







})