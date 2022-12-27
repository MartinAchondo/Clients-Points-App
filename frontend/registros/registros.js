$(document).ready(function () {
 
    let table = $('#registros-datatable').DataTable({
        "scrollY": "50vh",
        "scrollCollapse": true,
        "pageLength": 100,
        "order": [[ 0, "desc" ]],
        "bInfo" : false,
        drawCallback: function () {
            $('#registros-datatable_paginate ul.pagination').addClass("pagination-sm");   
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
            mensaje('Creado',true)
            borrar_loaderjs_tags()
        }else{
            mensaje(mens,false);
            borrar_loaderjs_tags()
        };  
    })

}); 

async function mydata_table(tabla){
    data = await eel.pedir_registros_all()();
    let lista = [];
    let lis;
    for (tupla of data){
        lis = [
            tupla[1],
            tupla[0],
            tupla[2],
            tupla[3].slice(0,10),
            tupla[4],
            tupla[5]
        ];
        lista.push(lis);
    };
    tabla.rows.add(lista).draw(true);
};


$.fn.DataTable.ext.classes.sFilterInput = "form-control form-control-sm";
$.fn.DataTable.ext.classes.pageLength = "form-control form-control-sm"; 
