// initialize application
// 
//this has to go before the page loads because the library requires to be configured before that
//        Log.info( " configuring sound manager... ");


Initialize = {
  create_applets: function () {
//    jmolSetDocument(false);
    var element_ids = _.map(range(0, 3), function (i) {
      return "protein" + i
    });
    //        Log.debug(  " element IDs: "+element_ids);
    Applets.create_applets(element_ids);
    this.initialize();
  },
  initialize0: function () {
    Log.info(" initializing... ");

    Log.info(" initializing full screen API ");
    FullScreen.initialize();
    FullScreen.initialize_handlers();

    Log.info("creating applets");
    Initialize.create_applets();

  },
  initialize: function () {
    soundManager.load_all_audios();
    Log.info("Initializing... ");
    Log.info("getting user... ");
    Api.get_user(function (user) {
      Api.get_game_settings(function (settings) {
        Initialize.initialize2((new User()).extend(user), new GameSettings().extend(settings));
      });
    });

  },
  initialize2: function (user, game_settings) {
    Log.info(" getting game configuration");

    Log.info(" updating game data for the first time ");

    Api.get_game_score(user.profile.level, user.profile.game, function (game_score) {
      //  for the first time, and later just in case, update the GUI with data from from the server
      App = new Application(new GameScore().extend(game_score), game_settings, user);
      App.initialize();
      Api.get_game_score_for_game(user.profile.game, function (game_scores) {
        App.view.score_panel.initialize(game_scores);
        Api.get_game_scores_for_user(function (game_scores) {
          App.view.score_panel.update_best_and_avg(game_scores);
        });
      });
      App.trigger('initialized');
      $("#username").text(user.username);
    });


//    hide_proteins();
    Log.info(" updating games instance for the first time");

//    Log.info( "removing loading message.");
//    $( "#message_box2").html( "");
    Log.info("Initialized correctly.");

  }

}