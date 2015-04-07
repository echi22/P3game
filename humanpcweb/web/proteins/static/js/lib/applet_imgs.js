AppletCreator = Base.extend({
  constructor: function () {
    this.codebase = Config.static_url + 'jmol';

  },
  create: function (applet_id, element_id) {
    $("#" + element_id).html('<img id="' + applet_id + '" src=""></div>');
    Log.debug(" creating applet, about to modify dom ...");
  }
});

AppletScriptExecutor = Base.extend({
  constructor: function () {
  },
  execute_script_do: function (ids, script, callback, error_callback, attempts, delay) {
    if (attempts === 0) {
      Log.error(" could not execute script: " + script + " for this " + ids + ".");
      error_callback();
    } else {
      this.apply_to_jmol_windows(ids, script);
      Log.debug("script  " + script + "executed for this " + ids + ".");
      callback();
    }
  },
  execute_scripts_do: function (ids, scripts, callback, error_callback, attempts, delay) {
    if (attempts === 0) {
      Log.error(" could not execute scripts: " + scripts + " for this " + ids + ".");
      error_callback();
    } else {
      this.apply_scripts_to_jmol_windows(ids, scripts);
      Log.debug("scripts " + scripts + " executed for this " + ids + ".");
      callback();
    }
  },
  apply_to_jmol_windows: function (ids, script) {
    var showing = App.view.game_panel.showing_proteins;
    App.view.game_panel.show_proteins();
    for (var i = 0; i < ids.length; i++) {
//      $("#jmolApplet" + i).attr("src", "/static/images/tutorial.png");
      $("#jmolApplet" + i).attr("src", script);
    }
    if (!showing) {
      App.view.game_panel.hide_proteins();
    }
  },
  apply_scripts_to_jmol_windows: function (ids, scripts) {
    var showing = App.view.game_panel.showing_proteins;
    App.view.game_panel.show_proteins();
    for (var i = 0; i < ids.length; i++) {
//      $("#jmolApplet" + i).attr("src", "/static/images/tutorial.png");
      $("#jmolApplet" + i).attr("src", scripts[i]);
    }
    if (!showing) {
      App.view.game_panel.hide_proteins();
    }
  }
});


AppletManager = Base.extend({
  constructor: function (max_attempts, delay) {
    this.max_attempts = max_attempts;
    this.delay = delay;
    this.ids = [];
    this.applet_creator = new AppletCreator();
    this.executor = new AppletScriptExecutor();
  },
  execute_scripts_all: function (scripts, callback, error_callback) {
    this.execute_scripts(this.ids, scripts, callback, error_callback);
  },
  execute_script_all: function (script, callback, error_callback) {
    this.execute_script(this.ids, script, callback, error_callback);
  },
  execute_scripts: function (ids, scripts, callback, error_callback) {
    Log.debug(" executing for applets:  " + ids + " scripts: " + scripts);
    if (!defined(callback)) {
      callback = function () {
      };
    }
    if (!defined(error_callback)) {
      error_callback = View.error_message;
    }
    this.executor.execute_scripts_do(ids, scripts, callback, error_callback, this.max_attempts, this.delay);
  },
  execute_script: function (ids, script, callback, error_callback) {
    if (!defined(callback)) {
      callback = function () {
      };
    }
    if (!defined(error_callback)) {
      error_callback = App.error_callback;
    }
    this.executor.execute_script_do(ids, script, callback, error_callback, this.max_attempts, this.delay);
  },
  create_applet: function (applet_id, element_id) {
//    Log.debug( " creating applet... "+ element_id);
    this.applet_creator.create(applet_id, element_id);
  },
  create_applets: function (element_ids) {

    this.ids = _.map(range(element_ids.length), function (i) {
      return 'jmolApplet' + i;
    });

    Log.debug("about to create applet with ids: " + this.ids);
    Log.info(" registering for applet loading by jmol script");
    _.each(range(element_ids.length), function (i) {
      //    Log.debug(_.printMethods( this ));
      this.create_applet(this.ids[i], element_ids[i]);
//      Log.debug( " applet "+i+ " created. ");
    }, this);
    Log.info("Applets created");
  },
  load_scripts: function (game_instance) {
    game_instance.proteins = _.shuffle(game_instance.proteins);
    return load_img_scripts(game_instance.proteins);
  }
});

Applets = new AppletManager(10, 500);