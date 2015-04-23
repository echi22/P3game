AppletCreator = Base.extend({
  constructor: function () {
    this.codebase = Config.static_url + 'jmol';

  },
  
  create: function (applet_id, element_id) {
    function readyfc() {
//      AppletLoadedDetectorByJmolScript.notice(applet_id);
      console.log("cargado " + applet_id);
      $("#" + applet_id + "_canvas2d").attr("ready", "true");
    }
//    var script = "set antialiasDisplay;load /static/proteins/movie.pdb; anim mode PALINDROME;anim on";
    Jmol.setXHTML(element_id);
    Jmol.setDocument(document.getElementById(element_id));
    var Info = {
      progresscolor: "blue",
      boxbgcolor: "black",
      boxfgcolor: "white",
      progressbar: "true",
      use: "HTML5",
      color: "black",
      debug: false,
      width: "220",
      height: "220",
      loadstructcallback: "animate",
      j2sPath: "../static/j2s",
      //script: script,
      isSigned: false,
      disableJ2SLoadMonitor: true,
      disableInitialConsole: true,
      allowjavascript: true,
      readyFunction: readyfc
    };
    
    Jmol.setAppletCss(null, "style='margin-top:45px'");
    Jmol.getApplet(applet_id, Info);
    Log.debug(" creating applet, about to modify dom ...");
  },
  
});
function animate(){
     Applets.execute_scripts_all(["anim on","anim on","anim on"], function () {
      //self.switch_spin();
    });
  }
  
AppletScriptExecutor = Base.extend({
  constructor: function () {
  },
  execute_script_do: function (ids, script, callback, error_callback, attempts, delay) {
        console.log("ejecuta uno", script);

    if (attempts === 0) {
      Log.error(" could not execute script: " + script + " for this " + ids + ".");
      error_callback();
    } else {
//      if (AppletLoadedDetectorByFunction.all_loaded(ids)) {
      this.apply_to_jmol_windows(ids, script);
      Log.debug("script  " + script + "executed for this " + ids + ".");

      //        Log.info( "calling success callback ");

      callback();
      //        Log.info( " end calling success callback ");
//      } else {
//        attempts--;
//        setTimeout(function () {
//          this.execute_script_do(ids, script, callback, error_callback, attempts, delay);
//        }, delay);
//      }

    }
  },
  execute_scripts_do: function (ids, scripts, callback, error_callback, attempts, delay) {
        console.log("ejecuta todos", scripts);

    if (attempts === 0) {
      Log.error(" could not execute scripts: " + scripts + " for this " + ids + ".");
      error_callback();
    } else {
//      if (AppletLoadedDetectorByFunction.all_loaded(ids)) {
      this.apply_scripts_to_jmol_windows(ids, scripts);
      Log.debug("scripts " + scripts + " executed for this " + ids + ".");

      //        Log.info( "calling success callback ");
      callback();
      //        Log.info( " end calling success callback ");
//      } else {
//        //        Log.debug( "attempts  "+ attempts +" remaining to execute scripts: "+ scripts + " for this "+ids +".");
//        attempts--;
//        setTimeout(function () {
//          this.execute_scripts_do(ids, scripts, callback, error_callback, attempts, delay);
//        }, delay);
//      }

    }
  },
  apply_to_jmol_windows: function (ids, script) {
    var showing = App.view.game_panel.showing_proteins;
    App.view.game_panel.show_proteins();
    for (var i = 0; i < ids.length; i++) {
//      jmolScript(script,i);
//      Jmol.script(myJmol, script);
      Jmol.script(eval("jmolApplet" + i), script);
    }
    if (!showing) {
      App.view.game_panel.hide_proteins();
    }
  },
  apply_scripts_to_jmol_windows: function (ids, scripts) {
    var showing = App.view.game_panel.showing_proteins;
    App.view.game_panel.show_proteins();
    for (var i = 0; i < ids.length; i++) {
      Jmol.script(eval("jmolApplet" + i), scripts[i]);
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
    //  ids:[ "jmolApplet0","jmolApplet1","jmolApplet2"],
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
  load_scripts: function () {
//    if (App.flags.first) {
//      App.flags.first = false;
//      return load_all_proteins_scripts(App.game_instances_manager.game_instances);
//    } else {
//      return load_next_level_scripts(App.game_instances_manager.game_instances);
//    }
  }
});

//Applets = new AppletManager(10, 500);