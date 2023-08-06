define(function(){

    function load_ipython_extension(){
        console.info('serving bokeh javascript in jupyter');
    }

    return {
        load_ipython_extension: load_ipython_extension
    };
});