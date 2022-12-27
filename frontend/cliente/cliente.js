$(document).ready(function () {
 
    let table = $('#analisis-datatable').DataTable({
        "scrollY": "50vh",
        "scrollCollapse": true,
        "pageLength": 100,
        "order": [[ 0, "desc" ]],
        "bInfo" : false,
        drawCallback: function () {
            $('#analisis-datatable_paginate ul.pagination').addClass("pagination-sm");   
        }
        });
        $('.dataTables_length').addClass('bs-select');

        let table2 = $('#venc-datatable').DataTable({
            "scrollY": "50vh",
            "scrollCollapse": true,
            "pageLength": 100,
            "order": [[ 1, "asc" ]],
            "bInfo" : false,
            drawCallback: function () {
                $('#venc-datatable_paginate ul.pagination').addClass("pagination-sm");   
            }
            });
            $('.dataTables_length').addClass('bs-select');

        $("#form-verificar-cliente").submit(async (e)=>{
            e.preventDefault();
            create_loaderjs_tags("#verificar-mandar");
            let rut = $('#input-verificar-cliente-rut');
            if (rut.val()==''){
                borrar_loaderjs_tags();
                mensaje('faltan datos',false);
            }else{
                let rut_st = rut.val().toString();
                let data = {'rut': rut_st};
                console.log(data)
                let [mens,tipo] = await eel.verificar_cliente(data)();
                console.log(mens);
                if(tipo==true){
                    await pedir_cliente(data);
                    mydata_table(table,data)
                    mydata_table2(table2,data)
                    borrar_loaderjs_tags();
                }else{
                    mensaje(mens,false);
                    borrar_loaderjs_tags();
                };  
            };
        });

});

async function pedir_cliente(data){
    $("#input-verificar-cliente-rut").prop('disabled',true);
    $("#verificar-mandar").prop('disabled',true);
    let ans = await eel.pedir_cliente(data)();
    let ans1 = ans[1][0][0];
    let ans2 = ans[1][1][0];
    $("#analisis-rut").html(ans1['rut']);
    $("#analisis-nombre").html(ans1['name'])
    $("#analisis-numero").html(ans1['phone'])
    $("#analisis-mail").html(ans1['mail'])
    $("#analisis-puntos").html(ans2['points'])
    $("#analisis-fecha").html(ans2['date_creation'].slice(0,10))
}

async function mydata_table(tabla,filter){
    let data = await eel.get_records_client(filter)();
    let lista = [];
    let lis;
    for (tupla of data){
        lis = [
            tupla['id'],
            tupla['type_trans'],
            tupla['date_trans'].slice(0,10),
            tupla['monto'],
            tupla['saldo']
        ];
        lista.push(lis);
    };
    tabla.rows.add(lista).draw(true);
};

async function mydata_table2(tabla,filter){
    let data = await eel.get_last_venc(filter)();
    console.log(data)
    let lista = [];
    let lis;
    for (tupla of data){
        lis = [
            tupla[0],
            tupla[1],
        ];
        lista.push(lis);
    };
    tabla.rows.add(lista).draw(true);
};

$.fn.DataTable.ext.classes.sFilterInput = "form-control form-control-sm";
$.fn.DataTable.ext.classes.pageLength = "form-control form-control-sm"; 
