var app = {
    initialize: function() {
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
    },
    onDeviceReady: function() {
        this.receivedEvent('deviceready');
    },
    receivedEvent: function(id) {
        var request = window.sessionStorage.getItem("request");
        if(request){
            window.request = JSON.parse(request);
            $('#usuario').text(window.request.usuario)
            $('#usuario_id').text(window.request.usuario_id)
            $('#usuario_name').text(window.request.usuario_name)
            $('.corte_actual').text(window.request.corte)
        }
        else{
            window.location.href = "index.html";   
        }
    }
};
app.initialize();

$( "#btn-logout" ).click(function(event) {
    event.preventDefault();
    window.sessionStorage.clear();
    window.location.href = "index.html";  
});
