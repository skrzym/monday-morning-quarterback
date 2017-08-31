// Disable the submit button on page load
document.getElementById('submit-button').disabled = true;

// Perform CSS and HTML class changes when selecting one of the guess options.
// If runValidation passes, enable the submit button.
$(function () {
    $('.btn-radio').click(function(e) {
      $('.btn-radio').not(this).removeClass('active')
    		.siblings('input').prop('checked',false)
        .siblings('.img-radio').css('opacity','0.75')
				.parent('#well').css('border','3px solid rgb(245,245,245)');
    	$(this).addClass('active')
        .siblings('input').prop('checked',true)
    		.siblings('.img-radio').css('opacity','1')
				.parent('#well').css('border','3px solid #0c7cd5');
    });
});


$(function () {
    $('.btn-radio').click(function(e) {
		runValidation()
	});
});

$(function () {
	$('.form-control').click(function(e){
		runValidation()
	});
});

function runValidation(){
	console.log('running validation check');
	if (validateSelects() && document.getElementsByClassName('active').length > 0) {
		document.getElementById('submit-button').disabled = false
	};
};

function validateSelects(){
	var selectIDs = [
	'select-down',
	'select-quarter',
	'select-clock',
	'select-yards',
	'select-field',
	'select-score',
	];
	
	for (i = 0; i < selectIDs.length; i++){
		if (document.getElementById(selectIDs[i]).selectedIndex < 0){
			return false
		};
	};
	return true
};