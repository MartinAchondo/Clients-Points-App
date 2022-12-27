$(document).ready(function () {
 
    let table = $('#clientes-datatable').DataTable({
        "scrollY": "50vh",
        "scrollCollapse": true,
        "pageLength": 100,
        "order": [[ 0, "desc" ]],
        "bInfo" : false,
        drawCallback: function () {
            $('#clientes-datatable_paginate ul.pagination').addClass("pagination-sm");   
        }
        });
        $('.dataTables_length').addClass('bs-select');
    mydata_table(table);

    $("#excel").click(async ()=>{
        create_loaderjs_tags("#excel");
        let check = $('.check-update').is(":checked");
        if (check){
            mensaje('Actualizando base, se demorará unos minutos',true)
        }
        let data = {
            'check': check
        };
        let [mens,tipo] = await eel.print_data_excel(data)();
        if(tipo==true){
            borrar_loaderjs_tags()
            mensaje('Creado',true)
        }else{
            borrar_loaderjs_tags()
            mensaje(mens,false);
        };  
    })

});

async function mydata_table(tabla){
    data = await eel.pedir_clientes_tabla()();
    let lista = [];
    let lis;
    for (tupla of data){
        lis = [
            tupla[0],
            tupla[1],
            tupla[2],
            tupla[3],
            tupla[4].slice(0,10),
        ];
        lista.push(lis);
    };
    tabla.rows.add(lista).draw(true);
};


$.fn.DataTable.ext.classes.sFilterInput = "form-control form-control-sm";
$.fn.DataTable.ext.classes.pageLength = "form-control form-control-sm"; 
