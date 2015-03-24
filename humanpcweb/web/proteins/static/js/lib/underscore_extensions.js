_.printVariables=JSON.stringify;
_.printMethods= function(obj){
  var result = [];
  for (var id in obj) {
    try {
      if (typeof(obj[id]) == "function") {
        result.push(id + ": " + obj[id].toString());
      }
    } catch (err) {
      result.push(id + ": inaccessible");
    }
  }
  return result;
}
_.indexes=function(array,f){
    var result=[]
    for(var i=0; i < array.length; i++){
        if(f(array[i])){
            result.push(i)
        }
    }
    return result;
}