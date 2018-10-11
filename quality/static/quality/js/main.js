

/* Signup Form AJAX */
$('#signupForm').submit(function(e){
	var formId = $(this).attr('id');
	var submitBtn = $(this).find('input[type=submit]');
	$('#user-email-exists-error').css('display','none');
	submitBtn.prop('disabled', true);
	e.preventDefault();
	$.ajax({
		url: "{% url 'user_signup' %}", // the file to call
		type: "POST", // GET or POST
		data: $(this).serialize(), // get the form data
		success: function(signup_response){
			if (signup_response.register == "Success") {
				$('#register-modal').modal('hide');
				submitBtn.prop('disabled', false);
			}
			else if(signup_response.error == "True"){
				$('#register-modal').modal('hide');
				setTimeout(function() {
					$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
				}, 1000);
			}
		},/* end of Success */
		error: function(signup_response) {
			$('#register-modal').modal('hide');
			setTimeout(function() {
				$('#errorModal').modal({backdrop:'static', keyboard:false,show:true});
			}, 1000);
		}/*  end of error */
	});/*./ajax*/
});
/* End of Signup Form */

