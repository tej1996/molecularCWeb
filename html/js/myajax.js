$(function()
    {
        $('#login-form').submit(function(event){
	    event.preventDefault();
	    var lusername=$("#lusername").val();
	    var lpassword=$("#lpassword").val();
            $.ajax({
                url: "/cgi-bin/login.py",
                type: "post",
                datatype:"json",
                data: {'lusername':lusername,'lpassword':lpassword},
		beforeSend: function(){
			$('#btn-login').attr('disabled',true);
			$("#btn-login").attr('value', 'Logging in...');		
		},
                success: function(response){
		    if(response.status==1){
			console.log("Login Success!");
			sessionStorage.setItem("status",1);
			sessionStorage.setItem("username", response.username);
			window.location="/dashboard.html";
		    }else if(response.status==0){
			$("#lstatus").text('Invalid username or password,please try again!');
			console.log("Invalid username or password");
		    }else{
			$("#lstatus").text('Unable to take your request! Sorry!');
			console.log("Unable to take your request!Sorry!");
		    }
                },
		complete: function() {
        		$('#btn-login').attr('disabled',false);
			$("#btn-login").attr('value', 'Log In');	
    		}
            });
        });
    });
$(function()
    {
        $('#register-form').submit(function(event){
	    event.preventDefault();

	    var remail=$("#remail").val();
	    var rusername=$("#rusername").val();
	    var rpassword=$("#rpassword").val();
            $.ajax({
                url: "/cgi-bin/register.py",
                type: "post",
                datatype:"json",
                data: {'remail':remail,'rusername':rusername,'rpassword':rpassword},
		beforeSend: function(){
			$('#btn-register').attr('disabled',true);
			$("#btn-register").attr('value', 'Registering you, please wait...');		
		},
                success: function(response){
		    if(response.status==1){
			console.log("Register Success!");
			$("#r-status").text('You are now registered! Please login..');
		    }else if(response.status==0){
			console.log("Username or email exists");
			$("#r-status").text('Username or Email exists,please try again!');
		    }else{
		    	console.log("Unable to take your request!Sorry!");
			$("#r-status").text('Unable to take your request! Sorry!');
		    }
                },
		complete: function() {
        		$('#btn-register').attr('disabled',false);
			$("#btn-register").attr('value', 'Create your Account');	
    		}
            });
        });
    });
