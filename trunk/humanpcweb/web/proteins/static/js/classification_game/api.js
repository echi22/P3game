
Api= {


get_game_instance:function(amount, callback ){
  $.ajax({
  url: '/classification_game/get_game_instance',
  dataType: 'json',
  data: { "amount": amount},
  success: callback
});

//  jQuery.getJSON('/classification_game/get_game_instance',{ "amount": amount},callback,function(data,textStatus) {
//    Log.debug( " hello ");
//    alert( " hello ");
//    callback(data);
//  });
}
}