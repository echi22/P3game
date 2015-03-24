User=Base.extend({
   constructor: function(){
     
   }


});

function show_registration(){
  View.hide_proteins();
  $("#registration").dialog( "open");
}
function show_modify_data(){
  View.hide_proteins();
  $("#user_data").dialog( "open");
}
function show_log_in(){
  View.hide_proteins();
  $("#log_in_user").dialog( "open");
}
function show_anonymous(){
  $("#log_in_user").dialog( "close");
  View.hide_proteins();
  $("#insert_name").dialog("open");
}
function check_for_registration_popup(){
  if(App.game_score.attempts > 2){
    if(App.user.username===""){
      $( "#message_box2").html ("<p>You can create an account to save your points by clicking <a href=\"#\" class=\"usersText\" onclick='show_registration()'>HERE </a></p>");
    }
  }
}


function update_user(){

  Api.get_user(function(user){
    App.user=user;
    update_user_gui(user);
  })
}

function log_in_popup() {
  // validate and process form here
  $('.error').hide();
  var username = $("#user_name_login").val();
  if (username == "") {
    $("label#username_error_login").show();
    $("#user_name_login").focus();
    return false;
  }

  var password = $("input#password_login").val();
  if (password == "") {
    $("label#password_error_login").show();
    $("#password_login").focus();
    return false;
  }

  var data={
    username:username,
    password:password,
    type:'ajax'
  };
  $( "#message_box2").html( "");
  Api.log_in(data,function(result){
      $("#data_login").hide();
      $("#login_result").show();
      $("#login_result_span").text(result.result);
      if(result.failed){
        $("#data_login").show();
        $("#play_anonymous").show();
      }else{
            Api.get_user(function(user){
              App.user=user;
              App.user.profile.points=10;
              update_user_gui(user);

            });
            
            setTimeout("close_login();",3000);
      }
      
            
  });

  return false;
}
function close_login(){
     $("#log_in_user").dialog("close");
     View.show_proteins();
}
function close_modify(){
     $("#user_data").dialog("close");
     View.show_proteins();
     $("#modify_data").show();
     $("#modify_result").hide();
     $("#old_password").val();
     $("#password_modify").val();
     $("#password2_modify").val();
     
}
function modify_data() {
  // validate and process form here
  $('.error').hide();
  var username = $("#user_name_modify").val();
  if (username == "") {
    $("label#username_modify_error").show();
    $("#user_name_modify_registration").focus();
    return false;
  }
  var first_name = $("#first_name_modify").val();
  if (username == "") {
    $("label#first_name_modify_error").show();
    $("#first_name").focus();
    return false;
  }
  var email = $("#email_modify").val();
  if (email == "") {
    $("label#email_modify_error").show();
    $("#email_modify").focus();
    return false;
  }
  var password = $("input#password_modify").val();
  if (password == "") {
    $("label#password_modify_error").show();
    $("#password_modify").focus();
    return false;
  }
  var password2 = $("input#password2_modify").val();
  if (password2 == "") {
    $("label#password2_modify_error").show();
    $("#password2_modify").focus();
    return false;
  }
  var old_password = $("input#old_password").val();
  if (password2 == "") {
    $("label#old_password_error").show();
    $("#old_password").focus();
    return false;
  }
  var data={
    username:username,
    old_password:old_password,
    password:password,
    password2:password2,
    first_name:first_name,
    email:email,
    type:'ajax'
  };


  Api.modify_data(data,function(result){

      $("#modify_result").show();
      $("#modify_result_span").text(result.result);
      if(!result.failed){
            $("#modify_data").hide();
            setTimeout("close_modify();",3000);
      }
    Api.get_user(function(user){
      App.user=user;
      update_user_gui(user);
    });
  });

  return false;
}
function create_account() {
  // validate and process form here
  $('.error').hide();
  var username = $("#user_name_registration").val();
  if (username == "") {
    $("label#username_error").show();
    $("#user_name_registration").focus();
    return false;
  }
  var first_name = $("#first_name").val();
  if (username == "") {
    $("label#first_name_error").show();
    $("#first_name").focus();
    return false;
  }
  var email = $("#email").val();
  if (email == "") {
    $("label#email_error").show();
    $("#email").focus();
    return false;
  }
  var password = $("input#password").val();
  if (password == "") {
    $("label#password_error").show();
    $("#password").focus();
    return false;
  }
  var password2 = $("input#password2").val();
  if (password2 == "") {
    $("label#password2_error").show();
    $("#password2").focus();
    return false;
  }
  var data={
    username:username,
    password:password,
    password2:password2,
    first_name:first_name,
    email:email,
    type:'ajax'
  };
  
  
  Api.create_account(data,function(result){

      $("#registration_result").show();
      $("#registration_result_span").text(result.result);
      if(!result.failed){
            $("#registration_data").hide();
            setTimeout("close_registration();",3000);
      }
    Api.get_user(function(user){
      App.user=user;
      update_user_gui(user);
    });
  });
        
  return false;
}
function close_registration(){
     $("#registration").dialog("close");
     View.show_proteins();
}