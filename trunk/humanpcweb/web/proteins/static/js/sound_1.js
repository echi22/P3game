Sound= {

configure_sound_manager: function(){
soundManager.debugMode = false;
soundManager.url = Config.static_url+'sound/swf/'; // directory where SM2 .SWFs live
soundManager.waitForWindowLoad = false;
soundManager.flashVersion = 9;
soundNames=[ "win", "lose", "level_up", "finished_game"];
//soundManager.mute();

/*
 * Note that SoundManager will determine and append the appropriate .SWF file to the URL,
 * eg. /path/to/sm2-flash-files/soundmanager2.swf automatically.
 *
 * Bonus: Read up on HTML5 audio support1, if you're feeling adventurous.
 * iPad/iPhone and devices without flash installed will always attempt to use it.
 *
 * Also, See the flashblock demo2 when you want to start getting fancy.
*/

// disable debug mode after development/testing..


// The basics: onready() callback

soundManager.onready(function(){

  // SM2 has loaded - now you can create and play sounds!
  for (i in soundNames){
   soundManager.createSound({
    id: soundNames[i],
    url: Config.static_url+ 'sounds/'+soundNames[i]+'.mp3'
    // onload: myOnloadHandler,
    // other options here..
  });
  }

});

// Optional: ontimeout() callback for handling start-up failure

soundManager.ontimeout(function(){
  Log.error( "Could not load sound manager ");
  // Hrmm, SM2 could not start. Flash blocker involved? Show an error, etc.?
//  alert( " whoops ");
});

}

}
 Sound.configure_sound_manager();