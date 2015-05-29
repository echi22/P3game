Panel = Base.extend({
});
MessagePanel = Panel.extend({
  constructor: function (element_id) {

  },
  loading: function () {
    $("#message_box2").html($("#loading").html());
  },
  error_message: function () {

  },
  show_message: function (html) {
    $("#message_box2").html(html);
    //$("#message_box2").show('slide',{direction: 'up'},1000);
    //setTimeout('$("#message_box2").hide("slide",{direction: "up"},1000);',3000);
  },
  hide_message: function () {
    $("#message_box2").html('');
    //$("#message_box2").hide('slide',{direction: 'up'},1000);
  },
  show_correct_message: function () {
    $.notification("You picked the correct protein!", {
      duration: 4000,
      freezeOnHover: false,
      hideSpeed: 1000,
      position: "top",
      showSpeed: 1000
    });
  },
  show_error_message: function (pos) {
    $.notification("You picked an incorrect protein. The different one was protein " + (pos + 1) + ".", {
      duration: 5000,
      freezeOnHover: false,
      hideSpeed: 1000,
      position: "top",
      showSpeed: 200
    });
  }


});

GamePanel = Panel.extend({
  constructor: function (application) {
    this.showing_proteins = true;
    this.loading_percentage = 0;
    application.register_observer(new Observer(this.loading_level, this), "initialized");
    application.register_observer(new Observer(this.update_loading, this), "protein_loaded");
    application.register_observer(new Observer(this.loading_message, this), "game_instance_change");
    application.register_observer(new Observer(this.update_game_instance, this), "game_instance_change");
    application.register_observer(new Observer(this.select_feedback, this), "select_protein");


    function make_mouse_enter_function(i) {
      return function () {
        $("#protein" + i).addClass("protein_selected");
      };
    }
    function make_mouse_leave_function(i) {
      return function () {
        $("#protein" + i).removeClass("protein_selected");
      };
    }
    for (var i = 0; i < 3; i++) {
      var buttonId = 'select_button' + i;
      $("#" + buttonId).hover(make_mouse_enter_function(i), make_mouse_leave_function(i));

    }
  },
  loading_level: function () {
    $("#loading_percentage").html(0 + "%");
    $("#progressbar").progressbar({
      value: 0
    });
  },
  update_loading: function () {
    this.loading_percentage++;
    var p = Math.floor((this.loading_percentage * 100) / (App.game_instances_manager.game_instances.length * 3));
    $("#loading_percentage").html(p + "%");
    $("#progressbar").progressbar({
      value: p
    });
    if (p >= 100) {
      $("#loading_level").hide();
    }
  },
  hide_proteins: function () {
    this.showing_proteins = false;
    document.getElementById('game').style.visibility = 'hidden';
  },
  show_proteins: function () {
    this.showing_proteins = true;
    document.getElementById('game').style.visibility = 'visible';
  },
  update_game_instance: function () {
    this.clear_gui();
    this.update_proteins();
  },
  clear_gui: function () {
    $(".protein").removeClass("incorrect correct tie");
    $(".votes").removeClass("incorrect_bg correct_bg tie_bg");
//    $("#send").hide();
//    $("#reload").show();
    $("#send").addClass("flip");
    $("#reload").removeClass("flip");
    $(".selectButton").show();
  },
  update_proteins: function () {
    game_instance = App.game_instances_manager.get_game_instance();
    var scripts;
    scripts = Applets.load_scripts(game_instance);
    var self = this;
    Applets.execute_scripts_all(scripts, function () {
    
//      self.switch_spin();

    });
    _.each(game_instance.proteins, function (protein, i) {
      $("#select_button" + i).unbind("click");
      $("#select_button" + i).click(function () {
        App.select_protein(i);
      });
      var info = '<p style="float:left">';
      info += 'Name:' + protein.code;
      info += ' - Classification:' + protein.classification;
      info += ' - <a href="/browser/protein?id=' + protein.code;
      info += '"target="_blank">More Info</a></p>';
      $("#info" + i).html(info);
    });
  },
  switch_spin: function () {
    var spinCommand = ($("#spin").is(':checked')) ? "spin on" : "spin off";
    App.applets.execute_script_all(spinCommand);
    App.game_settings.spin = $("#spin").is(':checked');
  },
  select_feedback: function () {

    $("#protein" + App.game_instances_manager.get_game_instance().different_index).addClass("correct");
    $("#score_container" + App.game_instances_manager.get_game_instance().different_index).addClass("correct_bg");
//    $("#send").show();
    $("#send").removeClass("flip");
    $("#reload").addClass("flip");
    if (App.game_score.level == (App.game_settings.levels_per_game - 1)) {

      soundManager.play("finished_game");
      $("#send").text("Volver a jugar");
      $("#send").click(this.play_again);
    }

//    $("#reload").hide();
    $(".selectButton").hide();
  },
  play_again: function(){
   $("#game_type").val(App.game_settings.game_type);
   $("#game_type_form").submit();
  },
  
  show_highscores: function(){
   $("#game_type_highscore").val(App.game_settings.game_type);
   $("#highscore_form").submit();
  },
  
  loading_message: function () {
    console.log(App.game_settings.game_type);
    if (App.flags.first)
      App.applets.executor.apply_to_jmol_windows([0, 1, 2], "hide all; set frank off; set echo middle center; font echo 19 sans; color echo [xAAAAAA]; echo Cargando proteina...; refresh;");
}
});

ProteinSelectionPanel = Panel.extend({
  constructor: function (application) {
    $("#send").click(function () {
      App.switch_to_next_game_instance();
    });
  }
});
PlayerPanel = Panel.extend({
  constructor: function (application, id) {

    application.register_observer(new Observer(this.update_votes, this), "select_protein");
    application.register_observer(new Observer(this.update_image, this), "loading_proteins");
    application.register_observer(new Observer(this.clear_votes, this), "loading_proteins");

  },
  update_votes: function () {
    $(".votes").show();
    $(".select_button").hide();
    var game_instance = App.game_instances_manager.get_game_instance();
    for (var i = 0; i < game_instance.proteins.length; i++) {
      var p = 'p' + i;
      //$("#"+p+"_points").text(game_instance.votes[i]);

    }
  },
  update_image: function () {
    var game_instance = App.game_instances_manager.get_game_instance();
    for (var i = 0; i < game_instance.proteins.length; i++) {
      var p = 'p' + i;
      var protein = game_instance.proteins[i];
      $("#" + p + "_image").attr("src", App.rm.protein_thumbnail(protein));
    }
  },
  clear_votes: function () {
    $(".votes").hide();
    $(".select_button").show();
    var game_instance = App.game_instances_manager.get_game_instance();
    for (var i = 0; i < game_instance.proteins.length; i++) {
      var p = 'p' + i;
      $("#" + p + "_points").text('');

    }


  }
});
LevelPanel = Panel.extend({
  constructor: function (application) {
    application.register_observer(new Observer(this.level_up, this), 'level_up');
    application.register_observer(new Observer(this.change_selected, this), 'change_level');
    application.register_observer(new Observer(this.initialize, this), 'initialized');
    this.application = application;
    this.change_selected();

  },
  initialize: function () {
    for (var i = 1; i <= this.application.user.profile.level + 1; i++) {
      $("#level" + i).attr('src', Config.static_url + 'images/buttons/level' + i + '.png');
      $("#level" + i).addClass("level_unlocked");
    }
    for (var j = this.application.user.profile.level + 2; j <= this.application.game_settings.levels_per_game; j++) {
      $("#level" + j).attr('src', Config.static_url + 'images/buttons/level' + j + '_invalid.png');
    }
    this.change_selected();
  },
  change_selected: function () {
    //$("#level").text( "Level:"+this.application.user.profile.level+ "/"+this.application.game_settings.level);
    $('input[name^="level"]').removeClass('level_selected');
    $("#level" + (this.application.game_settings.level + 1)).addClass('level_selected');
  },
  level_up: function () {
    $("#level" + (this.application.user.profile.level + 1)).attr('src', Config.static_url + 'images/buttons/level' + (this.application.user.profile.level + 1) + '.png')
    this.change_selected();
    //soundManager.play( "level_up");
  }
})
ScorePanel = Panel.extend({
  constructor: function (application) {
    application.register_observer(new Observer(this.score_gui, this), "select_protein_result");
    application.register_observer(new Observer(this.mark_as_playing, this), "game_instance_change");
    application.register_observer(new Observer(this.reorder_last_level_points, this), "level_up");
    this.application = application;
  },
  reorder_last_level_points: function (action, previous_game_score) {
    console.log(previous_game_score);
    this.show_level_score(previous_game_score);
  },
  update_level_and_game_instance: function () {
    this.current_level = this.application.user.profile.level;
    this.current_game_instance = this.application.game_score.game_instances_played;
  },
  initialize: function (game_scores) {
    for (var i = 0; i < game_scores.length; i++) {
      this.show_level_score(game_scores[i]);
    }
    $("#score").text(this.application.user.profile.points);
  },
  update_best_and_avg: function (game_scores) {
    $("#best_score").text(game_scores.best_score);
    $("#user_level").text(game_scores.user_level);
    $("#avg_score").text(game_scores.avg_score + "%");
  },
  show_level_score: function (game_score) {
    for (var i = 0; i < game_score.game_instances_correct; i++) {
      $("#instance_" + game_score.level + "_" + i).removeClass("playing_score circle correct_score incorrect_score").addClass("circle correct_score");
    }
    for (var i = game_score.game_instances_correct; i < game_score.game_instances_played; i++) {
      $("#instance_" + game_score.level + "_" + i).removeClass("playing_score circle correct_score incorrect_score").addClass("circle incorrect_score");
    }
  },
  current_id: function () {
    return "#instance_" + this.current_level + "_" + (this.current_game_instance);
  },
  mark_as_playing: function () {
    this.update_level_and_game_instance();
    $(this.current_id()).removeClass("not_played_score").addClass("playing_score");
  },
  score_gui: function (event, scored) {
    $(this.current_id()).removeClass("playing_score");
    if (scored) {
      var klass = "correct_score";
      previous_score = parseInt($("#score").text());
      $("#score").text(previous_score + 1);
    } else {
      var klass = "incorrect_score";
    }
    $(this.current_id()).addClass(klass);
    if (App.user.profile.level > 0)
      $("#score").text(this.application.user.profile.points);
  }
});
RepresentationPanel = Panel.extend({
  constructor: function (application) {
    this.initialize_gui();

  },
  initialize_gui: function () {
    $("input[name='representation']").change(function () {
      CG.update_representation_color();
    });
    $("input[name='color']").change(function () {
      CG.update_representation_color();
    });
    var items = ["backbone", "cartoon"];
    var extensions = ["png", "png"];
    var name = "representation";
    simple_image_radio(items, extensions, name);

    simple_image_radio(["secondary", "amino", "group", "temperature", "monochrome"],
            ["png", "png", "png", "png", "png"], "color");

    simple_image_checkbox(["spin"], ["png"]);

    function simple_image_radio(items, extensions, name) {
      for (i = 0; i < items.length; i++) {
        $('#' + name + '_' + items[i]).simpleImageCheck({
          imageChecked: Config.static_url + 'images/radiobuttons/' + items[i] + "_on." + extensions[i],
          image: Config.static_url + 'images/radiobuttons/' + items[i] + "_off." + extensions[i],
          height: 64,
          width: 64
        });
      }
    }
    function simple_image_checkbox(items, extensions) {
      for (i = 0; i < items.length; i++) {
        $('#' + items[i]).simpleImageCheck({
          image: Config.static_url + 'images/radiobuttons/' + items[i] + "_off." + extensions[i],
          imageChecked: Config.static_url + 'images/radiobuttons/' + items[i] + "_on." + extensions[i],
          afterCheck: function switch_spin(isChecked) {
            var spinCommand = (isChecked) ? "spin on" : "spin off";
            App.applets.execute_script_all(spinCommand)
            App.game_settings.spin = $("#spin").is(':checked');
            //  update_game_settings_gui();
          },
          height: 64,
          width: 64
        });
      }
    }

    //		$( "#colors" ).tabs();
  }



});
TutorialPanel = Panel.extend({
  constructor: function (application) {
    application.register_observer(new Observer(this.ask_for_tutorial, this), "asked_for_tutorial");
    application.register_observer(new Observer(this.show_tutorial_message, this), "game_instance_change");
    application.register_observer(new Observer(this.first_correct_guess, this), "selection_result_shown");
    application.register_observer(new Observer(this.first_wrong_guess, this), "selection_result_shown");
    application.register_observer(new Observer(this.votes_explanation, this), "selection_result_shown");
    application.register_observer(new Observer(this.level_change, this), "user_level_up");
    application.register_observer(new Observer(this.first_guess_after_losing_and_winning, this), "selection_result_shown");
    this.votes_explanation_shown = false;
    this.tutorialMessagesShowed = 0;
    this.askedToShowTutorial = false;
    $("#tutorialImage").click(function () {
      App.trigger("asked_for_tutorial");
    });
  },
  first_time_playing: function () {
    return App.user.profile.game === 0 && App.user.profile.level === 0 && App.game_score.attempts === App.user.proteins_compared;
  },
  is_nth_correct_guess: function (scored, n) {
    return this.first_time_playing() && scored && App.game_score.game_instances_correct == n;
  },
  is_nth_wrong_guess: function (scored, n) {
    return this.first_time_playing() && !scored && App.game_score.game_instances_lost() === n;
  },
  show_message: function (text, layout, callback) {
    $("#customContainer").noty({"text": text, "layout": layout, "type": "tutorial", dismissQueue: false, "textAlign": "left", "easing": "swing", "animateOpen": {"height": "toggle"}, "animateClose": {"height": "toggle"}, "speed": "500", "timeout": "30000", closeWith: ['button'], callback: {afterClose: callback}, buttons: [{addClass: 'btn btn-primary', text: 'Ok', onClick: function ($noty) {
            $noty.close();
          }
        }]});
  },
  ask_for_tutorial: function () {
    this.askedToShowTutorial = true;
    this.show_tutorial_message();
  },
  show_tutorial_message: function () {
    messages = new Array();
    messages[0] = "En los círculos aparecen tres proteínas. Debes seleccionar la que te parece más diferente. Si tu selección coincide con la de expertos, sumas un punto. Cuando logras " + App.game_settings.game_instances_correct_to_level_up + " puntos en un juego, pasas de nivel.";

    if ((this.first_time_playing() || this.askedToShowTutorial) && this.tutorialMessagesShowed < messages.length) {

      $("#tutorialImage").hide();
      _self = this;
      if (App.game_score.game_instances_played == 0) {
        var message = messages[this.tutorialMessagesShowed]
        this.show_message(message, "topCenter", function () {
          _self.show_tutorial_message("hola", "topCenter")
        });

      }

      this.tutorialMessagesShowed++;
    } else {
      this.askedToShowTutorial = false;
      this.tutorialMessagesShowed = 0;
      $("#tutorialImage").show();
    }
  },
  first_wrong_guess: function (event, scored) {
    if (this.is_nth_wrong_guess(scored, 1)) {
      var message = "La proteina que elegiste no era la más diferente de las tres." +
              "<br> No te preocupes, aunque no aciertes, estás ayudando a realizar una mejor clasificación de las proteinas.";
      this.show_message(message, "topLeft");
    }
  },
  first_correct_guess: function (event, scored) {
    if (this.is_nth_correct_guess(scored, 1)) {
      this.show_message("¡Muy bien! La proteina que elegiste es la más diferente de acuerdo a la base de datos de "
              + " SCOP (Structural classification of proteins), una de las clasificaciones de proteinas más populares", "topRight");
    }
  },
  votes_explanation: function (event, scored) {
    if (!this.is_nth_correct_guess(scored, 1)
            && !this.is_nth_wrong_guess(scored, 1)
            && !this.votes_explanation_shown) {
      this.votes_explanation_shown = true;
      var message = "The numbers in the red, green and gray circles tell you how many people voted the corresponding proteins. " +
              "<br> The first two votes are calculated using info from SCOP and CATH, two famous protein classifications.";
      //this.show_message(message, "topLeft");
    }
  },
  first_guess_after_losing_and_winning: function () {
//    	if(this.first_time_playing() && !this.is_nth_correct_guess(scored,1) 
//    			&& !this.is_nth_wrong_guess(scored,1)
//    			&& this.votes_explanation_shown ){
//    		var message = "";
//    			this.show_message(message, "center");
//    	}
  },
  level_change: function () {
    this.show_message("¡Felicitaciones! Pasaste al nivel " + App.user.profile.user_level);
//    	if(App.user.profile.level==1){
//    		//var score=Your score in level "+App.user.profile.level +" was "+App.game_score.game_instances_correct+"/"+App.game_settings.game_instances_per_level;
//    		this.show_message("Congratulations! You have finished level 1. \n From now on, you'll be challenged with increasingly more similar protein trios.\n","topLeft");
//    	}else {
//    		//var score=". \n Your score was "+App.game_score.game_instances_correct+"/"+App.game_settings.game_instances_per_level;
//    		this.show_message("Congratulations! You have finished level "+App.user.profile.level,"topLeft");
//    	}
  }
});

ConfigPanel = Panel.extend({
  constructor: function () {
    $("#mute").click(this.toogle_mute);


  },
  toogle_mute: function () {
    var src = document.getElementById('mute').src;
    if (src.split('/')[(src.split('/').length) - 1] === "sound.png") {
      $("#mute").attr("src", Config.static_url + "images/buttons/mute.png");
      soundManager.mute();
    } else {
      $("#mute").attr("src", Config.static_url + "images/buttons/sound.png");
      soundManager.unmute();
    }
  },
});

View = Base.extend({
  constructor: function (application) {
    //this.message_panel= new MessagePanel();
    this.player_panels = [];
    this.config_panel = new ConfigPanel();
    this.protein_selection_panel = new ProteinSelectionPanel(application);
    this.game_panel = new GamePanel(application);
    this.score_panel = new ScorePanel(application);
    this.level_panel = new LevelPanel(application);
    this.player_panel = new PlayerPanel(application);
    this.tutorial_panel = new TutorialPanel(application);
    this.representation_panel = new RepresentationPanel(application);
  }
});
