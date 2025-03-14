function modificarCantidad(tipo) {
    var cantidad = document.getElementById("cantidad");
    if (tipo == "sumar") {
        cantidad.innerHTML = parseInt(cantidad.innerHTML) + 1;
    } else {
        if (parseInt(cantidad.innerHTML) > 1) {
            cantidad.innerHTML = parseInt(cantidad.innerHTML) - 1;
        }
    }
}

  
function modificarCantidadCarrito(idobjeto,tipo) {
    var cantidad = document.getElementById("cantidad"+idobjeto);
    if (tipo == "sumar") {
        cantidad.innerHTML = parseInt(cantidad.innerHTML) + 1;
        actualizarCarritoDict(idobjeto,'actualizar')
        actualizarPrecio(idobjeto,tipo)
    } else {
        if (parseInt(cantidad.innerHTML) > 1) {
            cantidad.innerHTML = parseInt(cantidad.innerHTML) - 1;
            actualizarCarritoDict(idobjeto,'actualizar')
            actualizarPrecio(idobjeto,tipo)
        }
    }
};

function eliminarDireccion(idDireccionUsuario) {


    let informacion = [
        { "idDireccionUsuario": idDireccionUsuario }
    ];

    $.ajax({
        type: "POST",
        url: "/eliminar_direccion",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log("Result:");
            console.log(result);
        }
    });
    document.querySelector('.modal-bg').style.display = 'flex';
}
function actualizarCarritoDictProducto() {

    let idproducto = document.getElementById("idProducto").value;
    let cantidadprod = document.getElementById("cantidad").innerHTML;
    let tipo = "agregar";

    let informacion = [
        { "id_producto": idproducto },
        { "cantidad": cantidadprod },
        //tipo determina si se va actualizar la cantidad o si se borrara el registro
        { "tipo": tipo },
    ];

    $.ajax({
        type: "POST",
        url: "/actualizar_carritodict",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log("Result:");
            console.log(result);
        }
    });
    activarModalconID('agregarproducto');
}
function actualizarCarritoDictProductoPerdon(idproducto,cantidadprod) {


    let tipo = "agregar";

    let informacion = [
        { "id_producto": idproducto },
        { "cantidad": cantidadprod },
        //tipo determina si se va actualizar la cantidad o si se borrara el registro
        { "tipo": tipo },
    ];

    $.ajax({
        type: "POST",
        url: "/actualizar_carritodict",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log("Result:");
            console.log(result);
        }
    });
    activarModalconID('agregarproducto');
}

function agregarFavorito(){
    let idproducto = document.getElementById("idProducto").value;
    let cantidadprod = document.getElementById("cantidad").innerHTML;

    let informacion = [
        { "id_producto": idproducto },
        { "cantidad": cantidadprod },
        {"tipo":"agregar"},

    ];

    $.ajax({
        type: "POST",
        url: "/agregar_favorito",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log("Result:");
            console.log(result);
        }
    });
    activarModalconID('agregarwishlist');
}
function agregarFavoritosACarrito(){
    let informacion = [
        { "id_producto": 1 },
        { "cantidad": 1 },
        {"tipo":"agregarACarrito"},

    ];

    $.ajax({
        type: "POST",
        url: "/agregar_favorito",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log("Result:");
            console.log(result);
        }
    });
    desactivarModalconID('agregarcarrito');
}
function agregarPedidoACarrito(id_pedido,){

    let informacion = [
        { "id_pedido": id_pedido },
    ];

    $.ajax({
        type: "POST",
        url: "/recomprar_pedido",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log("Result:");
            console.log(result);
        }
    });

    activarModalconID('agregarpedido');
}
function eliminarFavorito(id_producto,index){

    let informacion = [
        { "id_producto": id_producto },
        { "cantidad": 1 },
        {"tipo":"eliminarFavorito"},

    ];

    $.ajax({
        type: "POST",
        url: "/agregar_favorito",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log("Result:");
            console.log(result);
        }
    });

    let favorito = document.getElementById("fila"+index);
    favorito.remove();
}
function limpiarFavoritos(){

    let informacion = [
        { "id_producto": 1 },
        { "cantidad": 1 },
        {"tipo":"limpiar"},

    ];

    $.ajax({
        type: "POST",
        url: "/agregar_favorito",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function (result) {
            console.log("Result:");
            console.log(result);
        }
    });

    let favoritos = document.getElementById("carrito");
    
    desactivarModalconID('limpiarwishlist');
    setTimeout(() => {
        document.location.reload();
      }, 100);
}
function desactivarModal() {
    document.querySelector('.modal-bg').style.display = 'none';
}

function desactivarModalconID(id) {
    console.log('modal-bg-'+id);
    document.getElementById('modal-bg-'+id).style.display = 'none';
}

function activarModalconID(id) {
    console.log('modal-bg-'+id);
    document.getElementById('modal-bg-'+id).style.display = 'flex';
}

function actualizarPrecio(idobjeto, tipo) {
    var cantidad = document.getElementById("cantidad" + idobjeto);
    var costo_unitario = parseFloat(document.getElementById("costo_unitario" + idobjeto).value);
    var subtotal_producto = document.getElementById("subtotal_producto" + idobjeto);
    var subtotal = document.getElementById("subtotal");
    var gran_total = document.getElementById("gran_total");
    var nuevoSubtotalProducto = costo_unitario * parseInt(cantidad.innerHTML);
    subtotal_producto.innerHTML = nuevoSubtotalProducto.toFixed(2);
    var subtotal = parseFloat(document.getElementById("subtotal_value").innerHTML.substring(1));
    var nuevoSubtotal;
    if (tipo == "sumar") {
        nuevoSubtotal = subtotal + costo_unitario;
    } else {
        nuevoSubtotal = subtotal - costo_unitario;
    }
    document.getElementById("subtotal_value").innerHTML = "$" + nuevoSubtotal.toFixed(2);
    var granTotal = nuevoSubtotal + 50.00;
    document.getElementById("gran_total").innerHTML = "$" + granTotal.toFixed(2);
    gran_total.innerHTML = "Total: $" + (nuevo_subtotal + 50).toFixed(2);
};
function eliminarProducto(idobjeto) {
    actualizarCarritoDict(idobjeto, "eliminar");
    var subtotal_producto = parseFloat(document.getElementById("subtotal_producto" + idobjeto).innerHTML);
    var subtotal = parseFloat(document.getElementById("subtotal_value").innerHTML.substring(1));
    var nuevoSubtotal = subtotal - subtotal_producto;
    if (nuevoSubtotal != 0) {
        document.getElementById("subtotal_value").innerHTML = "$" + nuevoSubtotal.toFixed(2);
        var granTotal = nuevoSubtotal + 50.00;
        document.getElementById("gran_total").innerHTML = "$" + granTotal.toFixed(2);
    } else {
        document.getElementById("subtotal_value").innerHTML = "$0.00";
        document.getElementById("gran_total").innerHTML = "-";
    }

    var elemento = document.getElementById("fila" + idobjeto);
    elemento.remove();

    let carrito = document.getElementsByClassName("wrapper");
    if (carrito.length <= 1) {
        let boton_pagar = document.getElementById("pagar");
        boton_pagar.disabled = true;
    } 
    console.log(carrito);
};

function actualizarCarritoDict(idobjeto,tipo){
    let idproducto=document.getElementById("idproducto_carrito"+idobjeto).value;
    let cantidadprod=document.getElementById("cantidad"+idobjeto).innerHTML;
    let informacion=[
        {"id_producto":idproducto},
        {"cantidad":cantidadprod},
        {"tipo":tipo},
    ];

    $.ajax({
        type: "POST",
        url: "/actualizar_carritodict",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
        console.log("Result:");
        console.log(result);
        }  
        });
};

function borrarCarrito() {
    let informacion = [
        {"id_producto":1},
        {"cantidad":1},
        {"tipo":"limpiar"},
    ];

    $.ajax({
        type: "POST",
        url: "/actualizar_carritodict",
        data: JSON.stringify(informacion),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
        console.log("Result:");
        console.log(result);
        }  
        });

    let carrito = document.getElementById("carrito");
    carrito.innerHTML = "";

    let subtotal = document.getElementById("subtotal_value");
    let gran_total = document.getElementById("gran_total");
    let boton_pagar = document.getElementById("pagar");

    subtotal.innerHTML = "$0.00";
    gran_total.innerHTML = "-";
    boton_pagar.disabled = true;
};    