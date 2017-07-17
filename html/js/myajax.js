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
						window.location.href = "staas_dashboard.html";
					}else if(response.status==0){
						console.log("Drive cannot be created!");
					}else{
						console.log(response.status);

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
        $('#newbs-form').submit(function(event){
	    event.preventDefault();
	    var drivename=$("#drive-name").val();
	    var drivesize=$("#drive-size").val();
	    var username=sessionStorage.getItem("username");
		alert(drivename);
            $.ajax({
                url: "/cgi-bin/staas/new_storage_bulk.py",
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
						window.location.href = "staas_dashboard.html";
					}else if(response.status==0){
						console.log("Drive cannot be created!");
					}else{
						console.log(response.status);

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
        $('#newblock-form').submit(function(event){
	    event.preventDefault();
	    var partname=$("#part-name").val();
	    var partsize=$("#part-size").val();
	    var username=sessionStorage.getItem("username");
		alert(partname);
            $.ajax({
                url: "/cgi-bin/staas/new_block.py",
                type: "post",
                datatype:"json",
                data: {'part-name':partname,'part-size':partsize,'username':username},
				beforeSend: function(){
					$('#btn-create-part').attr('disabled',true);
					$("#btn-create-part").attr('value', 'Creating your partition...');
				},
				success: function(response){

					if(response.status==1){
						console.log("Partition creation success");
						console.log(response.filename);
						window.location.href = "staas_dashboard.html";
					}else if(response.status==0){
						console.log("Partition cannot be created!");
					}else{
						console.log(response.status);

					}
                },
				complete: function() {
					$('#btn-create-part').attr('disabled',false);
					$("#btn-create-part").attr('value', 'Create your Partition');
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
						setTimeout(function(){
							window.location.href = "iaas_dashboard.html";
						}, 12000);
					}
                },
				complete: function() {
						$('#submit-atom').attr('disabled',false);
						$("#submit-atom").attr('value', 'Submit');
					}
					});
				});
    });

function fetchatom(){
    var tr="";
    var username=sessionStorage.getItem("username");
    $.ajax({
        url: "/cgi-bin/iaas/atomslist.py",
        type: "post",
        datatype:"json",
        data: {'username':username},
		beforeSend: function(){

		},
		success: function(response){
			for(var i=0;i<response.data.length;i++){
				if(response.data[i][4]=="active"){
					tr += "<tr> <th scope=\"row\">"+response.data[i][0]+"</th>  <td>"+response.data[i][1]+"</td> <td>"+response.data[i][2]+"</td> <td><a href=\""+response.data[i][3]+"\" > "+response.data[i][3]+"</a> </td> <td id=\"active-atom\">"+response.data[i][4]+"</td> <td> <a href=\"/iaas/qrcodes/"+username+"_"+response.data[i][1]+".png\" data-toggle=\"tooltip\" title=\"Qrcode for your atom!\"><i class=\"fa fa-qrcode\"></i></a> &nbsp; <a name=\"reboot\" id=\""+response.data[i][5]+"\" data-toggle=\"tooltip\" title=\"Reboot your Atom!\"><i class=\"fa fa-refresh\"></i></a> &nbsp; <a name=\"power\" id=\""+response.data[i][5]+"\" data-toggle=\"tooltip\" title=\"Power On/Off your atom!\"><i class=\"fa fa-power-off\"></i></a> &nbsp; <a name=\"delete\" id=\""+response.data[i][5]+"\" data-toggle=\"tooltip\" title=\"Delete Atom!\"><i class=\"fa fa-times\"></i></a> &nbsp; </td>  </tr>";

				}else{
					tr += "<tr> <th scope=\"row\">"+response.data[i][0]+"</th>  <td>"+response.data[i][1]+"</td> <td>"+response.data[i][2]+"</td> <td><a href=\""+response.data[i][3]+"\" > "+response.data[i][3]+"</a> </td> <td id=\"inactive-atom\">"+response.data[i][4]+"</td> <td> <a href=\"/iaas/qrcodes/"+username+"_"+response.data[i][1]+".png\" data-toggle=\"tooltip\" title=\"Qrcode for your atom!\"><i class=\"fa fa-qrcode\"></i></a> &nbsp; <a name=\"reboot\" id=\""+response.data[i][5]+"\" data-toggle=\"tooltip\" title=\"Reboot your Atom!\"><i class=\"fa fa-refresh\"></i></a> &nbsp; <a name=\"power\" id=\""+response.data[i][5]+"\" data-toggle=\"tooltip\" title=\"Power On/Off your atom!\"><i class=\"fa fa-power-off\"></i></a> &nbsp; <a name=\"delete\" id=\""+response.data[i][5]+"\" data-toggle=\"tooltip\" title=\"Delete Atom!\"><i class=\"fa fa-times\"></i></a> &nbsp; </td>  </tr>";

				}

			}
			if(tr==""){
				document.getElementById("list-msg").innerHTML="You don't have any atoms currently!";
			}else{
				document.getElementById("atom_row").innerHTML=tr;
			}

			  $( document ).ready(function() {
    			$('a[name="delete"],a[name="reboot"],a[name="power"]').click(function(event) {
                event.preventDefault();
				var id=this.id;
				var name=this.name;
				if(name=="delete"){
					dtitle="Destroy atom?";
					dmessage="Are you sure you want to delete your selected atom? This cannot be undone.";
				}else if(name=="reboot"){
					dtitle="Reboot atom? It may take few minutes to reboot!";
					dmessage="Are you sure you want to reboot your selected atom?";
				}else if(name=="power"){
					dtitle="Poweroff/on atom?";
					dmessage="Are you sure you want to shutdown/poweron your selected atom?";
				}
                bootbox.confirm({
					title: dtitle,
					message: dmessage,
					buttons: {
						cancel: {
							label: '<i class="fa fa-times"></i> Cancel'
						},
						confirm: {
							label: '<i class="fa fa-check"></i> Confirm'
						}
					},
					callback: function (result) {

						if(result==true){
							actionatom(id,name,username);
						}
					}
				});
    		  });

			});
		}
	});

}
function actionatom(id,action,username){
	var c_username=sessionStorage.getItem("username");
	if(c_username==username){

		 $.ajax({
			url: "/cgi-bin/iaas/iaas-action.py",
			type: "post",
			datatype:"json",
			data: {'aid':id,'action':action,'username':username},

			success: function(response){
					if(response.status==1){
							window.location.href = "iaas_dashboard.html";
					}else{
						console.log(response.status);
					}
			}
		});
	}else{
		console.log("Unauthorized access!");
	}
}
function fetchstorage(){
    var tr="";
    var username=sessionStorage.getItem("username");
    $.ajax({
        url: "/cgi-bin/staas/storagelist.py",
        type: "post",
        datatype:"json",
        data: {'username':username},
		beforeSend: function(){

		},
		success: function(response){
			for(var i=0;i<response.data.length;i++){
			   if(response.data[i][2]=="expandable"){
			   	 	tr += "<tr> <th scope=\"row\">"+response.data[i][0]+"</th>  <td>"+response.data[i][1]+"</td> <td>"+response.data[i][2]+"</td> <td> <a href=\"staas/"+response.data[i][0]+"_"+username+".tar\" download data-toggle=\"tooltip\" title=\"Download file to access!\"><i class=\"fa fa-download\"></i></a> &nbsp; <a data-toggle=\"modal\" data-target=\"#extend-modal\" id="+response.data[i][3]+" data-toggle=\"tooltip\" title=\"Expand this storage!\"><i class=\"fa fa-pencil\"></i></a> &nbsp; <a name='delete' id="+response.data[i][3]+" data-toggle=\"tooltip\" title=\"Delete this storage!\"><i class=\"fa fa-times\"></i></a> &nbsp;</td>  </tr>";

			   }else{
					tr += "<tr> <th scope=\"row\">"+response.data[i][0]+"</th>  <td>"+response.data[i][1]+"</td> <td>"+response.data[i][2]+"</td> <td> <a href=\"staas/"+response.data[i][0]+"_"+username+".tar\" download data-toggle=\"tooltip\" title=\"Download file to access!\"><i class=\"fa fa-download\"></i></a> &nbsp; <a name='delete' id="+response.data[i][3]+" data-toggle=\"tooltip\" title=\"Delete this storage!\"><i class=\"fa fa-times\"></i></a> &nbsp;</td>  </tr>";

			   }

			}
			if(tr==""){
				document.getElementById("list-msg").innerHTML="You don't have any storage currently!";
			}else{
				document.getElementById("st_row").innerHTML=tr;
			}
			$('a[name="delete"]').click(function(event) {
                event.preventDefault();
				var id=this.id;
                bootbox.confirm({
					title: "Destroy storage?",
					message: "Are you sure you want to delete your storage? This cannot be undone.",
					buttons: {
						cancel: {
							label: '<i class="fa fa-times"></i> Cancel'
						},
						confirm: {
							label: '<i class="fa fa-check"></i> Confirm'
						}
					},
					callback: function (result) {

						if(result==true){
							deletestorage(id,username);
						}
					}
				});
       		});

		}
	});
}

function deletestorage(id,username){
	var c_username=sessionStorage.getItem("username");
	if(c_username==username){

		 $.ajax({
			url: "/cgi-bin/staas/storagedelete.py",
			type: "post",
			datatype:"json",
			data: {'sid':id,'username':username},

			success: function(response){
				if(response.status==0){
					console.log("User does not exist!");
					}
					else if(response.status==1){
							alert("Deleted");
							window.location.href = "staas_dashboard.html";
					}else{
						console.log(response.status);
					}
			}
		});
	}else{
		console.log("Unauthorized access!");
	}
}
$(function() {
	$('#extend-modal').on('show.bs.modal', function(e) {

        var $modal = $(this),
            id = e.relatedTarget.id;
          $('#extend-storage-form').submit(function(event) {
              	event.preventDefault();
			  	var c_username=sessionStorage.getItem("username");
			  	var exsize=$("#ex_size").val();
			  	console.log(id);
				if(c_username==username){

					 $.ajax({
						url: "/cgi-bin/staas/storageextend.py",
						type: "post",
						datatype:"json",
						data: {'sid':id,'username':username,'ex-size':exsize},

						success: function(response){
							if(response.status==0){
								console.log("User does not exist!");
								}
								else if(response.status==1){
										alert("Extented");
										window.location.href = "staas_dashboard.html";
								}else{
									console.log(response.status);
								}
						}
					});
				}else{
					console.log("Unauthorized access!");
				}
          });


    });
});
//<!--paas-->
 $("#paas-list a").on('click', function(event) {
         event.preventDefault();
 		 alert(this.id);
		 $.ajax({
			url: "/cgi-bin/paas/reqservice.py",
			type: "post",
			datatype:"json",
			data: {'serv-type':this.id,'username':username},

			success: function(response){
				if(response.status==1){
						window.location.href=response.surl;
					}else{
						console.log(response.status);
					}
			}
		});

	});
