AppletLoadedDetector = {
    ids: [],
    callback: function () {
    },
    error_callback: function () {
    },
    executed_callback: false,
    set_ids: function (ids) {
        AppletLoadedDetector.ids = ids;
        AppletLoadedDetectorByJmolScript.applets_to_load = this.ids.length;
    },
    all_loaded: function () {
        return AppletLoadedDetectorByJmolScript.initialized && AppletLoadedDetectorByFunction.all_loaded(this.ids);
    },
    start_detection_by_function: function () {
        Log.info(" check detection");
        if (AppletLoadedDetector.all_loaded()) {
            Log.debug(" start detection by function/all loaded");
            AppletLoadedDetector.callback();
        } else {
            Log.debug(" start detection by function/not all loaded");
            AppletLoadedDetectorByFunction.wait_for_applets_to_load(AppletLoadedDetector.ids, 5, 2000,
                    AppletLoadedDetector.check_both_loaded, AppletLoadedDetector.error_callback
                    );
        }

    },
    start_detection_by_jmol_script: function () {

        AppletLoadedDetectorByJmolScript.set_callback(this.check_both_loaded);

    },
    check_both_loaded: function () {
        if ((AppletLoadedDetector.all_loaded()) && (!AppletLoadedDetector.executed_callback)) {
            AppletLoadedDetector.executed_callback = true;
            AppletLoadedDetector.callback();
        }
    }


};

AppletLoadedDetectorByJmolScript = {
    applets_to_load: 0,
    applets_loaded: 0,
    callback: function () {
    },
    initialized: false,
    set_callback: function (callback) {
        this.callback = callback;
    },
    notice: function (applet_index) {
        AppletLoadedDetectorByJmolScript.applets_loaded++;
        Log.info("Applet " + applet_index + " has loaded (by jmol). (initialized: " + this.initialized + ", applets_loaded: " + AppletLoadedDetectorByJmolScript.applets_loaded + " )");
        if (this.applets_loaded === this.applets_to_load && !this.initialized) {

            Log.info("applets loaded (by jmol)");
            this.initialized = true;
            this.callback();
        }
        Log.info(this.applets_to_load);
    }


};


AppletLoadedDetectorByFunction = {
    initialized: false,
    wait_for_applets_to_load: function (ids, attempts, delay, onSuccessCallback, onFailCallback) {
        Log.info(" check applets loaded by function (attempts left: " + attempts + " ) ");
        if (attempts === 0) {
            onFailCallback();
        } else {
            if (AppletLoadedDetectorByFunction.all_loaded(ids)) {
                Log.info("applets loaded (by function)");
                AppletLoadedDetectorByFunction.initialized = true;
                //        Log.info( "calling success callback ");
                onSuccessCallback();
                //        Log.info( " end calling success callback ");
            } else {
                attempts--;
                setTimeout(function () {
                    AppletLoadedDetectorByFunction.wait_for_applets_to_load(ids, attempts, delay, onSuccessCallback, onFailCallback);
                }, delay);
            }

        }
    },
    all_loaded: function (ids) {
        var all_loaded = true;
        for (var i = 0; i < ids.length; i++) {
            if (!AppletLoadedDetectorByFunction.applet_loaded(ids[i])) {
                all_loaded = false;
                break;
            }
        }
        return all_loaded;
    },
    applet_loaded: function (id) {
        //Test
        var applet = document.getElementById(id);
        var to = (applet) ? typeof (applet.script) : "";
//    Log.debug(  "(check applet loaded by function) id: "+id+ " element "+applet+ " type of applet.script: "+to);
        return to == "function" || to == "unknown";
    }

};


AppletCreator = Base.extend({
    constructor: function () {
        this.codebase = Config.static_url + 'jmol';

    },
    create: function (applet_id, element_id, script) {
        var string = '<object name="' + applet_id + '" id="' + applet_id + '" type="application/x-java-applet" width="220" height="220" align="middle">\n\
                        <param name="codebase" value="' + this.codebase + '"> \n\
                        <param name="java_arguments" value="-Xmx512m"> \n\
                        <param name="mayscript" value="true"> \n\
                        <param name="progresscolor" value="blue">\n\
                        <param name="boxbgcolor" value="black">\n\
                        <param name="boxfgcolor" value="white">\n\
                        <param name="boxmessage" value="Downloading JmolApplet ...">\n\
                        <param name="script" value="' + script + ';">\n\
                        <param name="useCommandThread" value="TRUE">\n\
                        <param name="progressbar" value="true">\n\
                    </object>';
//    switching to using applet instead of object because it works better apparently
        var string = '<applet class= "protein_applet" name="' + applet_id + '" id="' + applet_id + '" code="JmolApplet" archive="JmolAppletSigned.jar"\n\
        codebase= "' + this.codebase + '"\n\
        width="220" height="220"  align="absmiddle"  mayscript="true">\n\
        <param name="script" value="' + script + ';">\n\
        <param name="progressbar" value="true">\n\
        <param name="useCommandThread" value="TRUE">\n\
        <param name="progresscolor" value="blue">\n\
        <param name="boxbgcolor" value="black">\n\
        <param name="boxfgcolor" value="white">\n\
</applet>';

        Log.debug(" creating applet, about to modify dom ...");
        document.getElementById(element_id).innerHTML = document.getElementById(element_id).innerHTML + string;
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
            if (AppletLoadedDetectorByFunction.all_loaded(ids)) {
                this.apply_to_jmol_windows(ids, script);
                Log.debug("script  " + script + "executed for this " + ids + ".");

                //        Log.info( "calling success callback ");

                callback();
                //        Log.info( " end calling success callback ");
            } else {
                attempts--;
                setTimeout(function () {
                    this.execute_script_do(ids, script, callback, error_callback, attempts, delay);
                }, delay);
            }

        }
    },
    execute_scripts_do: function (ids, scripts, callback, error_callback, attempts, delay) {
        if (attempts === 0) {
            Log.error(" could not execute scripts: " + scripts + " for this " + ids + ".");
            error_callback();
        } else {
            if (AppletLoadedDetectorByFunction.all_loaded(ids)) {
                this.apply_scripts_to_jmol_windows(ids, scripts);
                Log.debug("scripts " + scripts + " executed for this " + ids + ".");

                //        Log.info( "calling success callback ");
                callback();
                //        Log.info( " end calling success callback ");
            } else {
                //        Log.debug( "attempts  "+ attempts +" remaining to execute scripts: "+ scripts + " for this "+ids +".");
                attempts--;
                setTimeout(function () {
                    this.execute_scripts_do(ids, scripts, callback, error_callback, attempts, delay);
                }, delay);
            }

        }
    },
    apply_to_jmol_windows: function (ids, script) {
        var showing = App.view.game_panel.showing_proteins;
        App.view.game_panel.show_proteins();
        for (var i = 0; i < ids.length; i++) {
//      jmolScript(script,i);
            Jmol.script(myJmol, script);
        }
        if (!showing) {
            App.view.game_panel.hide_proteins();
        }
    },
    apply_scripts_to_jmol_windows: function (ids, scripts) {
        var showing = App.view.game_panel.showing_proteins;
        App.view.game_panel.show_proteins();
        for (var i = 0; i < ids.length; i++) {
            jmolScript(scripts[i], i);
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
        this.applet_creator.create(applet_id, element_id, "javascript AppletLoadedDetectorByJmolScript.notice(" + applet_id + ");");
    },
    create_applets: function (element_ids) {

        this.ids = _.map(range(element_ids.length), function (i) {
            return 'jmolApplet' + i;
        });

        Log.debug("about to create applet with ids: " + this.ids);
        AppletLoadedDetector.set_ids(this.ids);
        Log.info(" registering for applet loading by jmol script");
        AppletLoadedDetector.start_detection_by_jmol_script();
        _.each(range(element_ids.length), function (i) {
            //    Log.debug(_.printMethods( this ));
            this.create_applet(this.ids[i], element_ids[i]);
//      Log.debug( " applet "+i+ " created. ");
        }, this);
        Log.info("Applets created");
    }

});

Applets = new AppletManager(10, 500);