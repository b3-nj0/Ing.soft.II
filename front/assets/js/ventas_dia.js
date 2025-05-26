// Configuraci�n del endpoint (ajusta la URL seg�n tu backend)
const endpoint = 'http://127.0.0.1:8000/ventas-del-dia'; 

// Funci�n para obtener datos del endpoint
async function obtenerVentas() {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        const data = await response.json();
        llenarTabla(data);
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

// Funci�n para llenar la tabla con los datos obtenidos
function llenarTabla(ventas) {
    const cuerpoTabla = document.getElementById('cuerpoTabla');
    cuerpoTabla.innerHTML = ''; // Limpiar la tabla antes de llenarla

    if (ventas.length === 0) {
        // Mostrar mensaje si no hay datos
        cuerpoTabla.innerHTML = `
            <tr>
                <td colspan="4" style="text-align: center;">
                    No hay ventas registradas hoy
                </td>
            </tr>
        `;
        return;
    }

    // Crear filas para cada producto vendido
    ventas.forEach(venta => {
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${venta.id_producto}</td>
            <td>${venta.nombre}</td>
            <td>${venta.cantidad}</td>
            <td>${venta.total.toFixed(2)} bs.</td>
        `;
        cuerpoTabla.appendChild(fila);
    });

    // Agregar fila de total general (opcional)
    const totalGeneral = ventas.reduce((sum, venta) => sum + venta.total, 0);
    const filaTotal = document.createElement('tr');
    filaTotal.style.fontWeight = 'bold';
    filaTotal.innerHTML = `
        <td colspan="3">TOTAL GENERAL</td>
        <td>${totalGeneral.toFixed(2)} bs.</td>
    `;
    cuerpoTabla.appendChild(filaTotal);
}

// Llamar a la funci�n para obtener las ventas al cargar la p�gina
document.addEventListener('DOMContentLoaded', obtenerVentas);

// Opcional: Actualizar cada 30 segundos
setInterval(obtenerVentas, 30000);