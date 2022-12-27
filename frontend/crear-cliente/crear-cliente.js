$('document').ready(async function(){
    
    $("#input-crear-cliente-rut2").prop('disabled',true)

    $("#crear-mandar").prop('disabled',true)
    $("#crear-verificar").prop('disabled',true)

    $("#check-ref").click(()=>{
        $("#input-crear-cliente-rut2").prop('disabled',false)
        $("#input-crear-cliente-rut2").prop('required',true)
        $("#crear-verificar").prop('disabled',false)
        $("#crear-mandar").prop('disabled',true)
    });

    $("#check-sin").click(()=>{
        $("#input-crear-cliente-rut2").prop('disabled',true)
        $("#input-crear-cliente-rut2").prop('required',false)
        $("#crear-verificar").prop('disabled',true)
        $("#crear-mandar").prop('disabled',false)
        $('#input-crear-cliente-rut2').val('')
    })

    $("#crear-verificar").click(async ()=>{
        create_loaderjs_tags("#crear-verificar");
        let rut2 = $('#input-crear-cliente-rut2');
        if (rut2.val()=='' || isNaN(rut2.val())){
            borrar_loaderjs_tags();
            mensaje('faltan datos o datos incorrectos',false);
        }else{
            let rut_st2 = rut2.val().toString();
            let data = {'rut': rut_st2};
            let [mens,tipo] = await eel.verificar_cliente(data)();
            console.log(mens);
            if(tipo==true){
                ready_create();
                borrar_loaderjs_tags();
            }else{
                borrar_loaderjs_tags();
                mensaje(mens,false);
            };  
        };
    })

    $("#form-crear-cliente").submit(async (e)=>{
        e.preventDefault();
        create_loaderjs_tags("#crear-mandar");
        let rut = $('#input-crear-cliente-rut');
        let rut2 = $('#input-crear-cliente-rut2');
        if (rut.val()=='' || isNaN(rut.val())){
            borrar_loaderjs_tags();
            mensaje('faltan datos o datos incorrectos',false);
        }else{
            if (rut2.val()==''){
                rut2.val('0')
            }
            let rut_st = rut.val().toString();
            let rut_st2 = rut2.val().toString();
            let data = {'rut': rut_st,'referido':rut_st2};
            console.log(data)
            let [mens,tipo] = await eel.crear_cliente(data)();
            console.log(mens);
            if(tipo==true){
                borrar_loaderjs_tags();
                mensaje('Se ha creado cliente correctamente',true);
                limpiar_nueva();
            }else{
                borrar_loaderjs_tags();
                mensaje(mens,false);
            };  
        };
    });
});

function limpiar_nueva(){
    $('#input-crear-cliente-rut').val("");
    $('#side-crear-cliente').click();
};

function ready_create(){
    $("#input-crear-cliente-rut2").prop('disabled',true)
    $("#input-crear-cliente-rut").prop('disabled',true)
    $("#crear-verificar").prop('disabled',true)
    $("#crear-mandar").prop('disabled',false)
}