jQuery(document).ready(function($) {
	
	function get_exchange_rates(){
		var url = $('#exchange_rates').data('ajax-url')
		$.get(url, function(data) {
			console.log(data)
			if(data['exchange_rates']){
				$('#id_exchange_rates').val(data['exchange_rates'])
			}
			else{
				$('#id_exchange_rates').addClass('is-invalid')
			}
		});
	}

	get_exchange_rates()




});