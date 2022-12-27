
// aviso true ,error false

function mensaje(texto,tipo){
    if(tipo){
        alert(texto)
    }else{
        alert('Error: '+texto)
    }
};

function create_loaderjs_tags(element){
    $(element).html('<span class="spinner-border spinner-border-sm loaderjs" role="status" aria-hidden="true"></span> '+$(element).html())
};

function borrar_loaderjs_tags(){
    $(".loaderjs").each(function() {
        this.parentNode.removeChild(this);
    });
};
