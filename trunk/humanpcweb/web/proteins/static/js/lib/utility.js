Log = log4javascript.getLogger();

function initialize_log(log ){
var popUpAppender = new log4javascript.BrowserConsoleAppender();
popUpAppender.setThreshold(log4javascript.Level.DEBUG);
var popUpLayout = new log4javascript.PatternLayout("%d{HH:mm:ss} %-5p - %m%n");
popUpAppender.setLayout(popUpLayout);
log.addAppender(popUpAppender);
}
initialize_log(Log );
/**
 * Behaves just like the python range() built-in function.
 * Arguments:   [start,] stop[, step]
 *
 * @start   Number  start value
 * @stop    Number  stop value (excluded from result)
 * @step    Number  skip values by this step size
 *
 * Number.range() -> error: needs more arguments
 * Number.range(4) -> [0, 1, 2, 3]
 * Number.range(0) -> []
 * Number.range(0, 4) -> [0, 1, 2, 3]
 * Number.range(0, 4, 1) -> [0, 1, 2, 3]
 * Number.range(0, 4, -1) -> []
 * Number.range(4, 0, -1) -> [4, 3, 2, 1]
 * Number.range(0, 4, 5) -> [0]
 * Number.range(5, 0, 5) -> []
 *   Number.range(5, 4, 1) -> []
 * Number.range(0, 1, 0) -> error: step cannot be zero
 * Number.range(0.2, 4.0) -> [0, 1, 2, 3]
 */
function range() {
  var start, end, step;
  var array = [];

  switch(arguments.length){
    case 0:
      throw new Error('range() expected at least 1 argument, got 0 - must be specified as [start,] stop[, step]');
      return array;
    case 1:
      start = 0;
      end = Math.floor(arguments[0]) - 1;
      step = 1;
      break;
    case 2:
    case 3:
    default:
      start = Math.floor(arguments[0]);
      end = Math.floor(arguments[1]) - 1;
      var s = arguments[2];
      if (typeof s === 'undefined'){
        s = 1;
      }
      step = Math.floor(s) || (function(){
        throw new Error('range() step argument must not be zero');
      })();
      break;
  }

  if (step > 0){
    for (var i = start; i <= end; i += step){
      array.push(i);
    }
  } else if (step < 0) {
    step = -step;
    if (start > end){
      for (var i = start; i > end + 1; i -= step){
        array.push(i);
      }
    }
  }
  return array;
}


function preload(arrayOfImages) {
  $(arrayOfImages).each(function(index){
    $('<img />')
    .attr('src', arrayOfImages[index])
  });
}
Utility= {
  //sequences function invocations
  seq:function(f1, f2){
    f1();
    f2();
  }
};
function defined(e){
  var result=!( typeof e === "undefined");
  return result;
}
get_all_urls= function(urls,callback){
    do_get_all_urls(urls,[],callback);
}
function do_get_all_urls(urls,result,callback){
    if(urls.length === 0){
        callback(result);
    }else{
       var url=urls.pop();
       $.ajax({
            type: "GET",
            url: url,
            data: "",
            success: function(data){
                result.push(data);
                do_get_all_urls(urls,result,callback);
            }
          });
    }
}
/*Log={

  info: function(message){
    if (!defined(window.console)) {
    
    }else{
      if(window.console.info){
        window.console.info(message );
      }
    }
  },
  debug: function(message){
    if (!defined (window.console)) {

    }else{
      if(window.console.debug){
        window.console.debug(message );
      }
    }
  },
  error: function(message){
    if (!defined (window.console)) {

    }else{
      if(window.console.error){
        window.console.error(message );
      }
    }
  },
  warn: function(message){
    if (!defined (window.console)) {

    }else{
      if(window.console.warn){
        window.console.warn(message );
      }
    }
  }
};

function create_log(){
  var Log={
    info: function(a){},
    error: function(a){},
    debug: function(a){},
    warn: function(a){}
  };

  if (defined (window.console)){
    var types=[ "info", "error", "debug", "warn"];
    for (i = 0; i < types.length; i++) {
      if(defined (window.console[types[i]])){
        Log[types[i]]=window.console[types[i]];
      }
    }
  }
  return Log;
}
//Log= create_log();
*/


function delete_item(array,item){
    for(var i=0; i < array.length; i++){
        if(item===array[i]){
            delete array[i];
        i--;
        }
    }
}

function check_date_format(){
  var fecha = $("#birthday").val();
  fecha = fecha.replace(/\//g, '-');
  if(!fecha.match(/^\d{4}-((0\d)|(1[012]))-(([012]\d)|3[01])$/)){
      fecha2 = fecha.substr(fecha.length - 4) + "-" + fecha.substr(3,2) + "-" + fecha.substr(0,2);
      $("#birthday").val(fecha2);
  }
}