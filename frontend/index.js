$("document").ready(()=>{
    cargar_inicio();;
});

function borrar_null_tags(){
    $(".nulo").each(function() {
        this.parentNode.removeChild(this);
    });
};



async function cargar_inicio(){
    let container = document.querySelector('.main');
    container.innerHTML = await eel.pass_html("frontend/inicio/inicio.html")();
    borrar_null_tags();
    let script = document.createElement('script');
    script.src = 'inicio/inicio.js';
    script.classList.add('nulo');
    document.body.appendChild(script);
};

$('#side-inicio').click(async ()=>{
    await cargar_inicio();
});

$('#side-crear-cliente').click(async ()=>{
    let container = document.querySelector('.main');
    container.innerHTML = await eel.pass_html("frontend/crear-cliente/crear-cliente.html")();
    borrar_null_tags();
    let script = document.createElement('script');
    script.src = 'crear-cliente/crear-cliente.js';
    script.classList.add('nulo');
    document.body.appendChild(script);
    var link = document.createElement('link');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = 'crear-cliente/crear-cliente.css';
    link.classList.add('nulo');
    document.head.appendChild(link);
});

$('#side-cliente').click(async ()=>{
    let container = document.querySelector('.main');
    container.innerHTML = await eel.pass_html("frontend/cliente/cliente.html")();
    borrar_null_tags();
    let script = document.createElement('script');
    script.src = 'cliente/cliente.js';
    script.classList.add('nulo');
    document.body.appendChild(script);
    var link = document.createElement('link');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = 'cliente/cliente.css';
    link.classList.add('nulo');
    document.head.appendChild(link);
});

$('#side-clientes').click(async ()=>{
    let container = document.querySelector('.main');
    container.innerHTML = await eel.pass_html("frontend/clientes/clientes.html")();
    borrar_null_tags();
    let script = document.createElement('script');
    script.src = 'clientes/clientes.js';
    script.classList.add('nulo');
    document.body.appendChild(script);
    var link = document.createElement('link');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = 'clientes/clientes.css';
    link.classList.add('nulo');
    document.head.appendChild(link);
});

$('#side-canjear').click(async ()=>{
    let container = document.querySelector('.main');
    container.innerHTML = await eel.pass_html("frontend/canjear/canjear.html")();
    borrar_null_tags();
    let script = document.createElement('script');
    script.src = 'canjear/canjear.js';
    script.classList.add('nulo');
    document.body.appendChild(script);
    var link = document.createElement('link');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = 'canjear/canjear.css';
    link.classList.add('nulo');
    document.head.appendChild(link);
});

$('#side-registros').click(async ()=>{
    let container = document.querySelector('.main');
    container.innerHTML = await eel.pass_html("frontend/registros/registros.html")();
    borrar_null_tags();
    let script = document.createElement('script');
    script.src = 'registros/registros.js';
    script.classList.add('nulo');
    document.body.appendChild(script);
    var link = document.createElement('link');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = 'registros/registros.css';
    link.classList.add('nulo');
    document.head.appendChild(link);
});


$('#side-editar').click(async ()=>{
    let container = document.querySelector('.main');
    container.innerHTML = await eel.pass_html("frontend/editar/editar.html")();
    borrar_null_tags();
    let script = document.createElement('script');
    script.src = 'editar/editar.js';
    script.classList.add('nulo');
    document.body.appendChild(script);
    var link = document.createElement('link');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    link.href = 'editar/editar.css';
    link.classList.add('nulo');
    document.head.appendChild(link);
});