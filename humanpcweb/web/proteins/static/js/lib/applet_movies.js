AppletManagerMovie = AppletManager.extend({
  reset_applet: function (id) {
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
      allowjavascript: true
    };
    Jmol._destroy(eval(id));
    for (var k in Jmol._applets) {
      if (k.indexOf(id) != -1) {
        Jmol._applets[k] = null;
        delete (Jmol._applets[k]);
      }
    }
    delete (eval(id));
    if (id === "jmolApplet2")
      $("#" + id + "_2dappletdiv").parent().parent().empty();
    else
      $("#" + id + "_canvas2d").remove();
    Jmol.getApplet(id, Info);
  },
  reset_applets: function () {
    _.each(range(this.ids.length), function (i) {
      this.reset_applet(this.ids[i]);
    }, this);
  },
  load_scripts: function () {
    if (App.flags.first) {
      App.flags.first = false;
    } else {
      this.reset_applets();
      App.applets.executor.apply_to_jmol_windows([0, 1, 2], "hide all; set frank off; set echo middle center; font echo 19 sans; color echo [xAAAAAA]; echo Cargando proteina...; refresh;");
    }
    return load_all_proteins_scripts_movies(App.game_instances_manager.game_instances);

  }
});

Applets = new AppletManagerMovie(10, 500);