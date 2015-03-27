GameScore = Base.extend({
  constructor: function (game, level, game_instances_played, game_instances_correct) {
    this.game_instances_played = game_instances_played;
    this.game_instances_correct = game_instances_correct;
    this.game = game;
    this.level = level;
    this.extend(new Observable());
    this.last_guess_scored = false;
  },
  game_instances_lost: function () {
    return  this.game_instances_played - this.game_instances_correct;
  }
});

Protein = Base.extend({
  constructor: function (id, code, name, scop, cath) {
    this.id = id;
    this.code = code;
    this.name = name;
    this.scop = scop;
    this.cath = cath;
  }
});
Vote = Base.extend({
  constructor: function (player, different_index) {
    this.player = player;
    this.different_index = different_index;
  }
})
GameInstance = Base.extend({
  constructor: function (id, proteins, game, level, votes, scop, cath) {
    this.id = id;
    this.proteins = proteins;
    this.level = level;
    this.game = game;
    this.scop = scop;
    this.cath = cath;
    this.votes = votes;
    this.original_order = this.proteins;
  },
  different: function () {
    return this.proteins[this.different_index];
  },
  votes: function () {
    return this.votes;
  }
});

GameSettings = Base.extend({
  constructor: function (levels_per_game, game_instances_per_level, game_instances_correct_to_level_up) {
    this.levels_per_game = levels_per_game;
    this.game_instances_per_level = game_instances_per_level;
    this.proteins = 3;
    this.game_instances_correct_to_level_up = game_instances_correct_to_level_up;
  }
});

GameInstancesManager = Base.extend({
  constructor: function () {
    this.clear_game_instances();
  },
  add_game_instance: function (game_instance) {
    this.game_instances.push(game_instance);
  },
  add_game_instances: function (game_instances) {
    for (var i = 0; i < game_instances.length; i++) {
      this.add_game_instance(game_instances[i]);
    }
  },
  switch_to_next_game_instance: function () {
    var game_instance = this.game_instances.shift();
    this.old_game_instances.push(game_instance);
  },
  get_game_instance: function () {
    return this.game_instances[0];
  },
  is_empty: function () {
    return this.game_instances.length === 0;
  },
  clear_game_instances: function () {

    this.game_instances = [];
    this.old_game_instances = [];
  },
  get_proteins_order: function () {
    game_instace = this.game_instances[0];
    var result = "";
    for (var i = 0; i < game_instance.original_order.length; i++) {
      result += "p" + (game_instance.proteins.indexOf(game_instance.original_order[i]) + 1) + "-"
    }
    return result.slice(0, -1);
  }

});
Player = Base.extend({
  constructor: function (name, points) {
    this.name = name;
    this.points = points;
  }
});
Application = Base.extend({
  constructor: function (game_score, game_settings, user, view) {
    this.flags = {level_up: false, finished_game: false, first: true};
    this.game_score = game_score;
    this.game_settings = game_settings;
    this.game_instances_manager = new GameInstancesManager();
    this.user = user;
    this.rm = new ResourceManager(Config.static_url);
    this.extend(new Observable());
    this.view = new View(this);
    // TODO make applets a parameter
    this.applets = Applets;

  },
  initialize: function () {
    Api.get_game_instances(function (
            game_instances) {
      App.game_instances_manager.add_game_instances(game_instances);
      App.trigger('game_instance_change');
    });
  },
  select_protein: function (selected_index) {
    this.trigger("select_protein");
    var selected = App.game_instances_manager.get_game_instance().proteins[ selected_index];
    Api.choose_protein(selected.id, function (profile, game_score) {
      old_profile = App.user.profile;
      App.user.profile = profile;

      if (profile.user_level > old_profile.user_level) {
        App.trigger("user_level_up");
      }
      if (profile.level > old_profile.level) {
        App.flags.level_up = true;
      }
      if (profile.game > old_profile.game) {
        App.flags.finished_game = true;
        App.flags.first = true;
      } else {
        App.game_score = new GameScore().extend(game_score);
      }
      CG.show_correct(selected, selected_index);

    });


  },
  switch_to_next_game_instance: function () {
    if (this.flags.finished_game) {
      this.flags.finished_game = false;
      this.flags.first = true;
      this.finished_game();
      return;
    }
    if (this.flags.level_up) {
      this.flags.level_up = false;
      this.level_up(this.user.profile.level)
    }
    App.game_instances_manager.switch_to_next_game_instance();
    if (App.game_instances_manager.is_empty()) {
      Api.get_game_instances(function (
              game_instances) {
        App.game_instances_manager.add_game_instances(game_instances);
        App.trigger('game_instance_change');
      });
    } else {
      this.trigger('game_instance_change');
    }
  },
  add_game_instance: function (game_instance) {
    this.game_instance = game_instance;
    this.game_instances_manager.add_game_instance(game_instance);
  },
  attempted: function (scored) {

    this.trigger("select_protein_result", [scored]);
  },
  level_up: function (level) {
    Api.get_game_score_for_game_and_level(this.user.profile.game, this.user.profile.level - 1, function (previous_game_score) {
      console.log(previous_game_score);
      App.trigger("level_up", [new GameScore().extend(previous_game_score)]);
      App.change_level(level);
    });


  },
  finished_game: function () {
    setTimeout(function () {
      window.location.href = "/game/play";
    }, 4000);
  },
  change_level: function (level) {
    this.game_settings.level = level;
    this.view.score_panel.show_level_score(this.game_score);
    Api.get_game_score(this.user.profile.level, this.user.profile.game, function (game_score) {
      App.game_score = new GameScore().extend(game_score);
//      App.game_instances_manager.clear_game_instances();
//      App.initialize();
      App.trigger('change_level');
    });
  }
});

ResourceManager = Base.extend({
  constructor: function (baseurl) {
    this.baseurl = baseurl;
  },
  path: function (id) {
    return this.baseurl + id;
  },
  protein_thumbnail: function (protein) {
    return this.path("proteins/images/thumbnails/" + protein.name + ".gif");
  },
  protein_image: function (protein) {
    return this.path("proteins/images/" + protein.name + ".gif")
  }

});
