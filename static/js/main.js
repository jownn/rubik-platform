var app = null
$(function(){
    $('#inputGroupFile01').on('change',function(){
        var fileName = $(this).val();
        $(this).next('.custom-file-label').html(fileName);
    })

    app = new Vue({
        el: '#filaexec',
        data: {
            filaExecucao: []
        },
        methods : {
            load : function(evt) {
                let url = '/getEnvios';
                this.$http.get(url).then(function(request) {
                    this.filaExecucao = request.body;
                });
            },
        },
        delimiters:['({','})']
    });
    var counter = 10;
    setInterval(function(){
        $('#counterShow').html(counter);
        counter--;
        if(counter == 0){
            counter = 10;
            app.load();
        }
    }, 1000);
    app.load();
    
});
