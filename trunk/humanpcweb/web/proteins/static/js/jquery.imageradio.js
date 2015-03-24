(function($){

  $.fn.extend({

    imageradio: function(method) {
      var methods= {

        init: function(options ){
          //Set the default values, use comma to separate the settings, example:
          var defaults = {
                
          }
         this.options =  $.extend(defaults, options);
          this.css( "padding-top: 18px; ");
          this.css( "display:none;");
          this.imageradio("update");
            
          this.change(function(){
//            this.css( "padding-top: 18px; background: url( "+ this.options.url+") repeat-x 0 0");
  
            $( "input[name='"+ this.options.name +"']:checked").not().imageradio( "update");
          });

          return this;
        },
        update: function(){
          if(this.is(':checked')){
            this.imageradio("check");
          }else{
            this.imageradio("uncheck");
          }
          return this;
        },
        update_image: function(url){
          this.css ( " background:url("+url+")  repeat-x 0 0");
        },
        check: function( ){
          methods.update_image.apply(this,[this.options.checked_url]);
        },
        hover: function( ){
          methods.update_image(this.options.hover_url);
        },
        uncheck: function( ){
          methods.update_image(this.options.uncheck_url);
        }
      };


//      call methods
      if ( methods[method] ) {
        return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
      } else if ( typeof method === 'object' || ! method ) {
        return methods.init.apply( this, arguments );
      } else {
        return $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );
      }

    }
  });

})(jQuery);