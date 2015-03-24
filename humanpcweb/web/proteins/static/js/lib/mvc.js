
Observer= Base.extend({
    constructor: function(callback,obj){
        this.obj=obj;
        this.callback=callback;
    },
    call: function(event,parameters){
        this.callback.apply(this.obj,[event].concat(parameters));
    }
});
Observable= Base.extend({
    constructor: function(){
        this.observers={};
    },
    register_observer: function(observer,event){

        if(this.observers[event] === undefined){
            this.observers[event]=[observer];
        }else{
            this.observers[event].push(observer);
        }
    },
    unregister_observer: function(event,observer){
        if(this.observers[event] !== undefined){
           delete_item(this.observers[event],observer);
        }

    },
    trigger: function(event,parameters){
    	parameters= parameters || [];
        if(this.observers[event] !== undefined){
        for(var i=0; i < this.observers[event].length; i++){
            this.observers[event][i].call(event,parameters);
        }
    }}
});