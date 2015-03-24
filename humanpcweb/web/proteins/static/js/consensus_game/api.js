
Api= {

choose_protein:function(selectedId,callback){
    data={selected:selectedId,bet:1, game_instance: App.game_instances_manager.get_game_instance().id, order: App.game_instances_manager.get_proteins_order()};
    $.post("/game/choose",
              data,function(data){
                  var o=jQuery.parseJSON(data);
                  callback(o.profile,o.score);
              }
              );
    
},
get_game_instance_proteins: function(game_instance,callback){
    var urls=_.map(game_instance.proteins,function(p){
        return Config.static_url+"proteins/"+p.name;
    })
    get_all_urls(urls,function(results){
        callback(results);
    })
},
update_game_settings:function(game_settings){
  var data= {spin:(game_settings.spin)? "on": "off"};
  $.post("/game/update_game_settings",
              data
              );
},

choose_level:function(level){
  $.post("/game/choose_level",
              {level: level}
              );
},
json_to_game_instance:function(data,textStatus){
function randomFromTo(from, to){
       return Math.floor(Math.random() * (to - from + 1) + from);
    }
    var result=[];
    for(var j=0; j < data.length; j++){
        var game_instance=data[j];
        var proteins=game_instance.proteins;
        for (var i = 0; i < 3; i++) {
          game_instance.proteins[i]=new Protein (proteins[i].id,proteins[i].code,proteins[i].name,proteins[i].scop.levels[3],proteins[i].cath.levels[3]);
        }
       result.push(new GameInstance(game_instance.id,game_instance.proteins, game_instance.game,game_instance.level,game_instance.votes ,game_instance.scop,game_instance.cath));
    }
    return result;
},


get_game_instances:function( callback ){
	$.ajax({
		  url: '/game/get_game_instances',
		  dataType: 'json',
		  async: false,
		  data: {},
		  success: function(data,textStatus) {
			    callback(Api.json_to_game_instance (data,textStatus));
		  }
		});
},

get_game_score:function(level,game, callback ){
    jQuery.getJSON('/game/get_game_score',{'level':level,'game':game},function(data,textStatus) {
    callback(data);
    });
},
get_game_score_for_game:function(game, callback ){
    jQuery.getJSON('/game/get_game_score_for_game',{'game':game},function(data,textStatus) {
    callback(data);
    });
},
get_game_scores_for_user:function(callback ){
    jQuery.getJSON('/game/get_game_scores_for_user',function(data) {
    	callback(data);
        });
    },
get_game_score_for_game_and_level:function(game,level, callback ){
    jQuery.getJSON('/game/get_game_score_for_game_and_level',{'level':level,'game':game},function(data,textStatus) {
    	
    callback(data);
    });
},
get_game_data:function( callback ){
    jQuery.getJSON('/game/get_game_data',function(data,textStatus) {
    callback(data);
    });
},
create_anonymous_user:function(callback){
   $.post('/users/create_anonymous_user',{},callback);
},
create_account:function(data,callback){
    $.ajax({
    type: "POST",
    url: "/users/register_anonymous",
    data: data,
    success: callback
  });
  
},
modify_data:function(data,callback){
    $.ajax({
    type: "POST",
    url: "/users/modify_data",
    data: data,
    success: callback
  });

},
log_in:function(data,callback){
    $.ajax({
    type: "POST",
    url: "/users/login_user",
    data: data,
    success: callback
  });

},

get_user: function(callback){
    jQuery.getJSON('/users/get_user',function(a,b){
        callback(a);
    });

},
get_highscores:function(level,callback){
    jQuery.getJSON('/game/highscores',{"level":level},function(a){
        callback(a);
    })
},
get_game_settings:function(callback){
    jQuery.getJSON('/game/get_game_settings',{},function(a){
        callback(a);
    })
}
}