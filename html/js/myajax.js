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
$(function()
    {
        $('#newfs-form').submit(function(event){
	    event.preventDefault();
	    var drivename=$("#drive-name").val();
	    var drivesize=$("#drive-size").val();
	    var username=sessionStorage.getItem("username");
		alert(drivename);
            $.ajax({
                url: "/cgi-bin/staas/new_storage_fixed.py",
                type: "post",
                datatype:"json",
                data: {'drive-name':drivename,'drive-size':drivesize,'username':username},
				beforeSend: function(){
					$('#btn-create-drv').attr('disabled',true);
					$("#btn-create-drv").attr('value', 'Creating your drive...');
				},
				success: function(response){

					if(response.status==1){
						console.log("Drive creation success");
						console.log(response.filename);
					}else if(response.status==0){
						console.log("Drive cannot be created!");
					}else{
						console.log(response.result);
					}
                },
				complete: function() {
					$('#btn-create-drv').attr('disabled',false);
					$("#btn-create-drv").attr('value', 'Create your Drive');
			}
			});
		});
    });
$(function()
    {
        $('#create-atom-form').submit(function(event){
	    event.preventDefault();
	    var os=$("input:radio[name=os]:checked").val();
	    var grp=$("input:radio[name=grp]:checked").val();
 	    var atomname=$("#atomname").val();
 	    var username=sessionStorage.getItem("username");
            $.ajax({
                url: "/cgi-bin/iaas/create-atom.py",
                type: "get",
                datatype:"json",
                data: {'os':os,'grp':grp,'atomname':atomname,'username':username},
				beforeSend: function(){
					$('#submit-atom').attr('disabled',true);
					$("#submit-atom").attr('value', 'Creating...');
					$("#tab_d_head").css('display','block');
				},
				success: function(response){
					if(response.status==0){
					console.log("Error");
					}
					else if(response.status==2){
					alert("Server Error");
					}else{
						$(".loader").css('display','none');
						$('.check-success').css('stroke-dashoffset', 0);
						console.log(response.status);
							window.location.href = "iaas_dashboard.html";
					}
                },
				complete: function() {
						$('#submit-atom').attr('disabled',false);
						$("#submit-atom").attr('value', 'Submit');
					}
					});
				});
    });



