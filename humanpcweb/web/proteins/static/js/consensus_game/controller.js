Controller=Base.extend({
	show_correct_interface: function(result,selectedIndex,correctIndex){
		if(result== "Lost"){
			$( "#protein"+ selectedIndex).addClass("incorrect");
            $( "#score_container"+ selectedIndex).addClass("incorrect_bg");
			soundManager.play( "lose");
		}else if(result== "Won"){
			soundManager.play( "win");
		}
		$( "#protein"+ correctIndex).addClass("correct");
        $( "#score_container"+ correctIndex).addClass("correct_bg");
		
	},
    show_correct: function (selected, selectedIndex){
    	var game_instance=App.game_instances_manager.get_game_instance();
    	var scop=_.indexes(game_instance.proteins,function(x){return x.id === game_instance.scop.id;});
    	var correctIndex= scop[0];
    	var scored= selected.id===game_instance.scop.id;
        var result=(scored)? "Won": "Lost";
        App.attempted(scored);

        App.trigger('selection_result_shown',scored);
        Api.get_game_scores_for_user(function(game_scores){
      		App.view.score_panel.update_best_and_avg(game_scores);
      	});
        this.show_correct_interface(result, selectedIndex,correctIndex);

    },
    show_correct2: function (selected, selectedIndex){
        var game_instance=App.game_instances_manager.get_game_instance();
        game_instance.votes[selectedIndex]++;
        var scop=_.indexes(game_instance.proteins,function(x){return x.id === game_instance.scop.id;});
        game_instance.votes[scop[0]]++;
        if(game_instance.cath !== 'none'){
        var cath=_.indexes(game_instance.proteins,function(x){return x.id === game_instance.cath.id;});
        game_instance.votes[cath[0]]++;
        game_instance.votes[game_instance.cath]++;
        }
        var max= _.max(game_instance.votes);
        var indexes= _.indexes(game_instance.votes,function(x){return x === max;});
        if(indexes.length > 1){ // We have a tie
            if(!_.include(indexes,selectedIndex)){
                $( "#protein"+ selectedIndex).addClass("incorrect");
                $( "#score_container"+ selectedIndex).addClass("incorrect_bg");
                App.attempted(indexes[0]==selectedIndex);
            }
            _.each(indexes,function(i){$( "#protein"+ i).addClass("tie");})
            _.each(indexes,function(i){$( "#score_container"+ i).addClass("tie_bg");})
        }else{
            App.attempted(indexes[0]==selectedIndex);
            if(indexes[0]==selectedIndex){
                soundManager.play( "win");
            }else{
                soundManager.play( "lose");
                $( "#protein"+ selectedIndex).addClass("incorrect");
                $( "#score_container"+ selectedIndex).addClass("incorrect_bg");
            }
                $( "#protein"+ indexes[0]).addClass("correct");
        $( "#score_container"+ indexes[0]).addClass("correct_bg");
        }


    }
});
CG=new Controller();


function hide_proteins(){
    App.applets.executor.apply_to_jmol_windows("hide all; set frank off; set echo middle center; font echo 19 sans; color echo [xAA0000]; echo Cargando proteina...; refresh;");
}

function update_game_settings() {
    App.game_settings.spin=$("#spin").is(':checked');
    Api.update_game_settings(App.game_settings);
}

function load_protein_script(p){
    var default_representation="set defaultStructureDSSP true;  zoom 120; set measurementUnits ANGSTROMS;  select all;  spacefill off; wireframe off; backbone off; cartoon on; color cartoon structure; color structure;  select ligand;wireframe 0.16;spacefill 0.5; color cpk ; select all; model 0;set antialiasDisplay true; ;save STATE state_1;set disablePopupMenu true;";
    return " load '"+Config.static_url+"proteins/"+p.name+"';;  "+default_representation
}
function load_proteins_scripts(proteins){
    App.trigger('loading_proteins');
    result=[];
    for (var i = 0; i < 3; i++) {
        result.push(load_protein_script(proteins[i]));
    }
    return result;
}

function update_game_data(){
    Api.get_game_data(function(game_data){
        //  for the first time, and later just in case, update the GUI with data from from the server
        $.extend(App.game_score,game_data.game_score);
        $.extend(App.game_settings,game_data.game_settings);
        App.view.game_panel.update_game_data_gui();
    }
    );
} 

//quick and dirty BFS children traversal, Im sure you could find a better one
function traverseChildren(elem){
    var children = [];
    var q = [];
    q.push(elem);
    while (q.length>0)
    {
        var elem = q.pop();
        children.push(elem);
        pushAll(elem.children);
    }
        function pushAll(elemArray){
            for(var i=0;i<elemArray.length;i++)
            {
                q.push(elemArray[i]);
            }

        }
        return children;
}
