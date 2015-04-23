AppletManagerMovie = AppletManager.extend({
  
  load_scripts: function () {
    if (App.flags.first) {
      App.flags.first = false;
      return load_all_proteins_scripts(App.game_instances_manager.game_instances);
    } else {
      return load_next_level_scripts(App.game_instances_manager.game_instances);
    }
  }
});

Applets = new AppletManagerMovie(10, 500);