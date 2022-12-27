INSERT INTO clients_info(
    rut ,
    name,
    phone,
    mail
) 
VALUES(
    :rut,
    :name,
    :phone,
    :mail
); 


INSERT INTO clients_points(
    id_client,
    points,
    date_creation,
    date_last_update,
    time_grab,
    referido_bool,
    id_referido
) 
VALUES(
    :id_client,
    :points,
    :date_creation,
    :date_last_update,
    :time_grab,
    :referido_bool,
    :id_referido
); 


INSERT INTO records(
    id_client,
    type_trans,
    date_trans,
    monto,
    saldo
) 
VALUES(
    :id_client,
    :type_trans,
    :date_trans,
    :monto,
    :saldo
); 


INSERT INTO vencimientos(
    id_client,
    puntos,
    date_venc
) 
VALUES(
    :id_client,
    :puntos,
    :date_venc
); 