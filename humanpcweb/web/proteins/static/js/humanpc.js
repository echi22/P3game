FullScreen= {
  initialize: function(){
    var
    fullScreenApi = {
      supportsFullScreen: false,
      isFullScreen: function() {
        return false;
      },
      requestFullScreen: function() {},
      cancelFullScreen: function() {},
      fullScreenEventName: '',
      prefix: ''
    },
    browserPrefixes = 'webkit moz o ms khtml'.split(' ');

    // check for native support
    if (typeof document.cancelFullScreen != 'undefined') {
      fullScreenApi.supportsFullScreen = true;
    } else {
      // check for fullscreen support by vendor prefix
      for (var i = 0, il = browserPrefixes.length; i < il; i++ ) {
        fullScreenApi.prefix = browserPrefixes[i];

        if (typeof document[fullScreenApi.prefix + 'CancelFullScreen' ] != 'undefined' ) {
          fullScreenApi.supportsFullScreen = true;

          break;
        }
      }
    }

    // update methods to do something useful
    if (fullScreenApi.supportsFullScreen) {
      fullScreenApi.fullScreenEventName = fullScreenApi.prefix + 'fullscreenchange';

      fullScreenApi.isFullScreen = function() {
        switch (this.prefix) {
          case '':
            return document.fullScreen;
          case 'webkit':
            return document.webkitIsFullScreen;
          default:
            return document[this.prefix + 'FullScreen'];
        }
      }
      fullScreenApi.removeAllListeners = function(){
    	  var old_element = document.getElementById("fullscreen");
    	  var new_element = old_element.cloneNode(true);
    	  old_element.parentNode.replaceChild(new_element, old_element);
      }
      fullScreenApi.requestFullScreen = function(el) {
    	  fullScreenApi.removeAllListeners();
    	  document.getElementById('fullscreen').addEventListener('click', function() {
    	        fullScreenApi.cancelFullScreen(el);
          }, true);
        return (this.prefix === '') ? el.requestFullScreen() : el[this.prefix + 'RequestFullScreen']();
      }
      fullScreenApi.cancelFullScreen = function(el) {
    	  fullScreenApi.removeAllListeners();
    	  document.getElementById('fullscreen').addEventListener('click', function() {
  	        fullScreenApi.requestFullScreen(el);
        }, true);
        return (this.prefix === '') ? document.cancelFullScreen() : document[this.prefix + 'CancelFullScreen']();
      }
    }
    
    // jQuery plugin
    if (typeof jQuery != 'undefined') {
      jQuery.fn.requestFullScreen = function() {

        return this.each(function() {
          var el = jQuery(this);
          if (fullScreenApi.supportsFullScreen) {
            fullScreenApi.requestFullScreen(el);
          }
        });
      };
    }

    // export api
    FullScreen.fullScreenApi = fullScreenApi;
  },
  initialize_handlers: function(){

    var fsButton = document.getElementById('fullscreen'),
    fsElement = document.getElementById('game-main');


    if (FullScreen.fullScreenApi.supportsFullScreen) {
      // handle button click
      fsButton.addEventListener('click', function() {
        FullScreen.fullScreenApi.requestFullScreen(fsElement);
      }, true);

      fsElement.addEventListener(FullScreen.fullScreenApi.fullScreenEventName, function() {
        if (FullScreen.fullScreenApi.isFullScreen()) {
    
        } else {
      }
      }, true);

    } else {

//      $( "#fullscreen_panel").hide();
      var  message='SORRY: Your browser does not support FullScreen';
//      Log.warn(message);
    //	fsStatus.innerHTML = message;
    }

  }

};

// do something interesting with fullscreen support


function change_image_fullscreen(src){
  if( src.split('/')[(src.split('/').length)-1] === "exit_fullscreen.png"){
    $("#fullscreen").attr("src", Config.static_url+"images/buttons/fullscreen.png");
  }else{
    $("#fullscreen").attr("src", Config.static_url+"images/buttons/exit_fullscreen.png");
  }
}


