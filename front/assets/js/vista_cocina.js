// Configuraci�n del endpoint (ajusta la URL seg�n tu backend)
const endpoint = 'http://127.0.0.1:8000/ordenes-cocina'; 

// Funci�n para obtener datos del endpoint
async function obtenerVentas() {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
        const data = await response.json();
        // Cambios ----------------------------------------------------------------------------------
        // llenarTabla(data);
        // Nuevos cambios ----------------------------------------------------------------------------------
        renderizarTarjetas(data);
    } catch (error) {
        console.error('Error al obtener los datos:', error);
        // Mostrar mensaje de error en la tabla
        const cuerpoTabla = document.getElementById('cuerpoTabla');
        cuerpoTabla.innerHTML = `
            <tr>
                <td colspan="4" style="color: red; text-align: center;">
                    Error al cargar los datos: ${error.message}
                </td>
            </tr>
        `;
    }
}

// Cambios ----------------------------------------------------------------------------------
// function llenarTabla(ventas) {
//     const cuerpoTabla = document.getElementById('cuerpoTabla');
//     cuerpoTabla.innerHTML = ''; // Limpiar la tabla antes de llenarla

//     if (ventas.length === 0) {
//         // Mostrar mensaje si no hay datos
//         cuerpoTabla.innerHTML = `
//             <tr>
//                 <td colspan="5" style="text-align: center;">
//                     No hay ventas registradas hoy
//                 </td>
//             </tr>
//         `;
//         return;
//     }

//     // Crear filas para cada producto vendido
//     ventas.forEach(venta => {
//         const fecha = new Date(venta.hora);
//         const horas = String(fecha.getHours()).padStart(2, '0');
//         const minutos = String(fecha.getMinutes()).padStart(2, '0');
        
//         const horaFormateada = `${horas}:${minutos}`;

//         const fila = document.createElement('tr');
//         fila.innerHTML = `
//             <td class="numero_ticket">${venta.numero_ticket}</td>
//             <td>${venta.nombre_plato}</td>
//             <td>${venta.cantidad}</td>
//             <td class="estado">${venta.estado_plato}</td>
//             <td>${horaFormateada}</td>
//             <td class="button_td">
//                 <button class="btn-cambiar-estado" data-id="${venta.numero_ticket}">ENTREGADO</button>
//                 <button class="btn-cambiar-estado" data-id="${venta.numero_ticket}">RECHAZADO</button>
//             </td>
//         `;
//         cuerpoTabla.appendChild(fila);
//     });

//     // Agregar evento a los botones de cambiar estado
//     document.querySelectorAll('.btn-cambiar-estado').forEach(button => {
//         button.addEventListener('click', async function() {
//             const idPedido = this.getAttribute('data-id');
//             await cambiarEstadoPedido(idPedido);
//         });
//     });
// }



// Nuevos cambios ----------------------------------------------------------------------------------
function renderizarTarjetas(ventas) {
    const contenedor = document.getElementById("contenedorTarjetas");
    contenedor.innerHTML = "";

    const hoy = new Date();
    const hoyStr = hoy.toISOString().slice(0, 10); // YYYY-MM-DD

    // Filtrar solo pendientes del día actual
    const ventasFiltradas = ventas.filter(v => {
        const fechaVenta = new Date(v.hora).toISOString().slice(0, 10);
        return v.estado_plato === "Pendiente" && fechaVenta === hoyStr;
    });

    if (ventasFiltradas.length === 0) {
        contenedor.innerHTML = `
            <div style="text-align: center; color: gray;">No hay pedidos pendientes hoy.</div>
        `;
        return;
    }

    // Agrupar por número de ticket
    const tickets = {};
    ventasFiltradas.forEach(v => {
        if (!tickets[v.numero_ticket]) {
            tickets[v.numero_ticket] = {
                hora: v.hora,
                productos: []
            };
        }
        tickets[v.numero_ticket].productos.push(v);
    });

    // Renderizar tarjetas por ticket
    Object.entries(tickets).forEach(([ticket, info]) => {
        const hora = new Date(info.hora);
        const horaFormateada = `${hora.getHours().toString().padStart(2, '0')}:${hora.getMinutes().toString().padStart(2, '0')}`;

        const card = document.createElement("div");
        card.className = "ticket-card_cocina";
        card.innerHTML = `
            <div class="ticket-header_cocina">
                <h3>Ticket #${ticket}</h3>
                <span class="ticket-hora">${horaFormateada}</span>
            </div>
            <ul class="ticket-productos_cocina">
                ${info.productos.map(p => `<li>${p.nombre_plato} (x${p.cantidad})</li>`).join("")}
            </ul>
            <div class="ticket-actions_cocina">
                <button class="btn-cambiar-estado" data-id="${ticket}" data-accion="ENTREGADO">Terminado</button>
                <button class="btn-cambiar-estado" data-id="${ticket}" data-accion="CANCELADO">Cancelado</button>
            </div>
        `;
        contenedor.appendChild(card);
    });

    // Eventos de botón
    document.querySelectorAll('.btn-cambiar-estado').forEach(btn => {
        btn.addEventListener("click", async function () {
            const ticket = this.dataset.id;
            const accion = this.dataset.accion;

            if (accion === "CANCELADO") {
                await cambiarEstadoPedido_cancelado(ticket);
            } else if (accion === "ENTREGADO") {
                await cambiarEstadoPedido(ticket);
            }
        });
    });
}





// Cambios ----------------------------------------------------------------------------------
// Función para cambiar el estado del pedido con Swal.fire y recarga
async function cambiarEstadoPedido(idPedido) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/ordenes-cocina/${idPedido}/cambiar-estado`, {
            method: 'PUT'
        });
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        const data = await response.json();
        
        // Mostrar alerta con SweetAlert2
        Swal.fire({
            title: `Estado actualizado a: ${data.nuevo_estado}`,
            text: 'PEDIDO ENTREGADO',
            icon: 'success',
            draggable: true,
            // colocar el timer: 2000
            timer: 2000,
            willClose: () => {
                // Recargar la página cuando se cierre la alerta
                location.reload();
            }
        });
        
    } catch (error) {
        Swal.fire({
            title: 'Error',
            text: 'No se pudo cambiar el estado: ' + error.message,
            icon: 'error',
            draggable: true
        });
    }
}
async function cambiarEstadoPedido_cancelado(idPedido) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/ordenes-cocina/${idPedido}/cambiar-estado-cancelado`, {
            method: 'PUT'
        });
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        const data = await response.json();
        
        // Mostrar alerta con SweetAlert2
        Swal.fire({
            title: `Estado actualizado a: ${data.nuevo_estado}`,
            text: 'PEDIDO CANCELADO',
            icon: 'success',
            draggable: true,
            // colocar el timer: 2000
            timer: 2000,
            willClose: () => {
                // Recargar la página cuando se cierre la alerta
                location.reload();
            }
        });
        
    } catch (error) {
        Swal.fire({
            title: 'Error',
            text: 'No se pudo cambiar el estado: ' + error.message,
            icon: 'error',
            draggable: true
        });
    }
}

// Nuevos cambios ----------------------------------------------------------------------------------
// async function cambiarEstadoPedido(ticket, nuevoEstado) {
//     try {
//         const response = await fetch(`http://127.0.0.1:8000/ordenes-cocina/${ticket}/cambiar-estado`, {
//             method: 'PUT',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ nuevo_estado: nuevoEstado })
//         });
//         if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
//         const data = await response.json();
//         Swal.fire({
//             title: `Estado actualizado a: ${data.nuevo_estado}`,
//             icon: 'success',
//             timer: 2000,
//             willClose: () => location.reload()
//         });
//     } catch (error) {
//         Swal.fire({
//             title: 'Error',
//             text: `No se pudo actualizar el estado: ${error.message}`,
//             icon: 'error'
//         });
//     }
// }



// Llamar a la funci�n para obtener las ventas al cargar la p�gina
document.addEventListener('DOMContentLoaded', obtenerVentas);

// Opcional: Actualizar cada 30 segundos
setInterval(obtenerVentas, 30000);