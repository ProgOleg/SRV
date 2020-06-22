$('document').ready(function(){

	$('#role').change(function(event) {
		console.log($(this).val())
		var value = $(this).val()
		var obj = $('#discount')
		if (value == 'MA') { obj.val(25) }
		else if (value == 'CL') { obj.val(0) }
	});





})