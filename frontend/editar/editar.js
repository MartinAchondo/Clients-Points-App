$('document').ready(async function(){
    
    $("#input-puntos").prop('disabled',true)
    $("#input-editar-cliente-rut2").prop('disabled',true)
    $("#editar-mandar").prop('disabled',true)
    $("#editar-verificar").prop('disabled',true)

    $("#editar-clave").click(()=>{
        if ($("#input-clave").val()=='club'){
            $("#editar-verificar").prop('disabled',false)
            $("#input-editar-cliente-rut2").prop('disabled',false)
            $("#editar-clave").prop('disabled',true)
        }
         })

    $("#editar-verificar").click(async ()=>{
        create_loaderjs_tags("#editar-verificar");
        let rut2 = $('#input-editar-cliente-rut2');
        if (rut2.val()==''){
            mensaje('faltan datos',false);
        }else{
            let rut_st2 = rut2.val().toString();
            let data = {'rut': rut_st2};
            let [mens,tipo] = await eel.verificar_cliente(data)();
            console.log(mens);
            if(tipo==true){
                ready_editar()
                borrar_loaderjs_tags();
            }else{
                mensaje(mens,false);
                borrar_loaderjs_tags();
            };  
        };
    })

    $("#form-editar-cliente").submit(async (e)=>{
        e.preventDefault();
        create_loaderjs_tags("#editar-mandar");
        let rut2 = $('#input-editar-cliente-rut2');
        let puntos = $('#input-puntos');
        if (rut2.val()=='' || puntos.val()=='' || puntos.val()==0){
            mensaje('faltan datos',false);
            borrar_loaderjs_tags();
        }else{
            let rut_st2 = rut2.val().toString();
            let data = {'rut': rut_st2,'puntos':puntos.val()};
            console.log(data)
            let [mens,tipo] = await eel.modificar_cliente(data)();
            console.log(mens);
            if(tipo==true){
                mensaje('Se ha modificado cliente correctamente',true);
                limpiar_nueva();
                borrar_loaderjs_tags();
            }else{
                mensaje(mens,false);
                borrar_loaderjs_tags();
            };
            $('#side-editar').click();
        };
    });
});

function limpiar_nueva(){
    $('#input-crear-cliente-rut').val("");
};

function ready_editar(){
    $("#input-editar-cliente-rut2").prop('disabled',true)
    $("#input-puntos").prop('disabled',false)
    $("#editar-verificar").prop('disabled',true)
    $("#editar-mandar").prop('disabled',false)
}