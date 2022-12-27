$('document').ready(async function(){

    $("#input-canjear-cliente-rut").prop('disabled',true)
    $("#canjear-mandar").prop('disabled',true);

    $("#form-verificar-cliente").submit(async (e)=>{
        e.preventDefault();
        create_loaderjs_tags("#verificar-mandar");
        let rut = $('#input-verificar-cliente-rut');
        if (rut.val()==''){
            mensaje('faltan datos',false);
        }else{
            let rut_st = rut.val().toString();
            let data = {'rut': rut_st};
            let [mens,tipo] = await eel.verificar_cliente(data)();
            console.log(mens);
            if(tipo==true){
                modificar_canjear(data);
                borrar_loaderjs_tags();
            }else{
                mensaje(mens,false);
                borrar_loaderjs_tags();
            };  
        };
    });

    $("#form-canjear-cliente").submit(async (e)=>{
        e.preventDefault();
        create_loaderjs_tags("#canjear-mandar");
        let points = $('#input-canjear-cliente-rut');
        let rut = $('#input-verificar-cliente-rut');
        $("#canjear-mandar").prop('disabled',true);
        if (points.val()==''){
            mensaje('faltan datos',false);
            $("#canjear-mandar").prop('disabled',false);
        }else{
            let rut_st = rut.val().toString();
            if (rut_st.length<8){
                rut_st = '0' + rut_st;
            }
            let data = {'rut': rut_st,'points':points.val()};
            let [mens,tipo] = await eel.canjear_cliente(data)();
            console.log(mens);
            if(tipo==true){
                mensaje(mens,tipo);
                limpiar_nueva();
                borrar_loaderjs_tags();
            }else{
                mensaje(mens,tipo);
                $("#canjear-mandar").prop('disabled',false);
                borrar_loaderjs_tags();
            };  
        };
    });
});

async function modificar_canjear(data){

    let points = await eel.get_points_client(data)();

    $("#input-verificar-cliente-rut").prop('disabled',true);
    $("#verificar-mandar").prop('disabled',true);
    $("#label-canjear").html(data['rut']);
    $("#input-canjear-cliente-rut").prop('disabled',false);
    $("#input-canjear-cliente-rut").attr({
        "min": 1,
        "max": points[0]
    });
    if (points[0]<1){
        $("#canjear-mandar").prop('disabled',true);
    }else{
        $("#canjear-mandar").prop('disabled',false);
    }
    $("#label-canjear-puntos").html(points[0]);
};



function limpiar_nueva(){
    $("#side-canjear").click()
};
 