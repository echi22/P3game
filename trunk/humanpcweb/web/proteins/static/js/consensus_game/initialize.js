// initialize application
// 
//this has to go before the page loads because the library requires to be configured before that
//        Log.info( " configuring sound manager... ");


Initialize = {
    create_applets: function () {
        jmolSetDocument(false);
        var element_ids = _.map(range(0, 3), function (i) {
            return "protein" + i
        });
        //        Log.debug(  " element IDs: "+element_ids);
        Applets.create_applets(element_ids);
    }, jmol_isReady: function (applet) {
        alert("la puta q te pario");
        //Jmol._getElement(applet, "appletdiv").style.border="1px solid blue"
    },
    create_applets_js: function () {
//        Info = {
////	width: 450,
//            use: "HTML5",
//            j2sPath: "j2s"}
//        $(function () {
//            Jmol.getApplet("jmolApplet0", Info);
//            console.log("holi");
//        });
//        Info = {
//            width: 300,
//            height: 300,
//            addSelectionOptions: true,
//            allowJavaScript: true,
//            color: "0xFFFFFF",
//            coverCommand: "",
//            coverImage: null,
//            coverTitle: "",
//            debug: false,
//            defaultModel: "",
//            deferApplet: false,
//            deferUncover: false,
//            disableInitialConsole: true,
//            disableJ2SLoadMonitor: true,
//            isSigned: true,
//            j2sPath: "j2s",
//            //jarFile: "JmolAppletSigned.jar",
//            //jarPath: "./java",
//            script: "set antialiasDisplay; load /static/proteins/d12asa_.pdb",
//            //serverUrl: "http://127.0.0.1/static/jmol/",
//            serverURL: "http://chemapps.stolaf.edu/jmol/jsmol/php/jsmol.php",
//            readyFunction: this.jmol_isReady,
//            src: null,
//            use: "HTML5"};
//        var script = 'h2oOn=true;set animframecallback "jmolscript:if (!selectionHalos) {select model=_modelNumber}";'
//                + 'set errorCallback "myCallback";'
//                + 'set defaultloadscript "isDssp = false;set defaultVDW babel;if(!h2oOn){display !water}";'
//                + 'set zoomlarge false;set echo top left;echo loading XXXX...;refresh;'
//                + 'load "/static/proteins/d12asa_.pdb";set echo top center;echo XXXX;'
//                + 'spacefill off;wireframe off;cartoons on;color structure;';
//        var Info2 = {
//            width: 450,
//            height: 450,
//            debug: false,
//            color: "white",
//            addSelectionOptions: false,
//            serverURL: "http://chemapps.stolaf.edu/jmol/jsmol/php/jsmol.php",
//            use: "HTML5",
//            j2sPath: "j2see",
//            //readyFunction: jmol_isReady,
//            script: script,
//            //jarPath: "java",
//            //jarFile: (useSignedApplet ? "JmolAppletSigned.jar" : "JmolApplet.jar"),
//            //isSigned: useSignedApplet,
//            //disableJ2SLoadMonitor: true,
//            disableInitialConsole: false
//                    //defaultModel: "$dopamine",
//                    //console: "none", // default will be jmolApplet0_infodiv
//        };
//        var s = document.location.search;
//        Jmol._debugCode = (true);
//        Jmol.setDocument(0);
//        Jmol.getApplet("myJmol", Info2);
//        document.getElementById("protein0").innerHTML = document.getElementById("protein0").innerHTML + Jmol.getAppletHtml(myJmol);
//        this.initialize();
//        var Info = {
//            use: "HTML5",
//            j2sPath: "../static/j2s",
//            script: "set antialiasDisplay;load /static/proteins/movie.pdb; anim mode loop;anim on",
//        };
//        Jmol.setXHTML("protein0");
//        Jmol.getApplet("jmolApplet0", Info);
    },
    initialize0: function () {
        Log.info(" initializing... ");

        Log.info(" initializing full screen API ");
        FullScreen.initialize();
        FullScreen.initialize_handlers();

        AppletLoadedDetector.callback = Initialize.initialize;
        Log.info("creating applets");
        Initialize.create_applets_js();

        Log.info(" registering for applet loading by function");
        AppletLoadedDetector.start_detection_by_function();


        //   check if the browser supports Java applets
        // jmolCheckBrowser("popup", "../../browsercheck", "onClick");
    },
    initialize: function () {

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

/*   <object name="jmolApplet0" id="jmolApplet0" width="400" height="400" type="application/x-java-applet">
 <param name="syncId" value="8411159524694085">
 <param name="progressbar" value="true">
 <param name="progresscolor" value="blue">
 <param name="boxbgcolor" value="black">
 <param name="boxfgcolor" value="white">
 <param name="boxmessage" value="Downloading JmolApplet ...">
 <param name="useCommandThread" value="TRUE">
 <param name="archive" value="JmolApplet0.jar">
 <param name="mayscript" value="true">
 <param name="codebase" value="/static/humanpcweb/jmol">
 <param name="code" value="JmolApplet">
 <param name="java_arguments" value="-Xmx512m">
 <param name="script" value="javascript AppletLoadedDetectorByJmolScript.notice(0);">
 <p style="background-color:yellow; color:black; width:400px;height:400px;text-align:center;vertical-align:middle;">
 You do not have Java applets enabled in your web browser, or your browser is blocking this applet.<br>
 Check the warning message from your browser and/or enable Java applets in<br>
 your web browser preferences, or install the Java Runtime Environment from <a href="http://www.java.com">www.java.com</a><br></p></object>
 */