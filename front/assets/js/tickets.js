async function obtenerUltimoTicket() {
    try {
        const response = await fetch(`${API_BASE_URL}ticket/ultimo/imprimir`);
        
        if (!response.ok) {
            throw new Error(`Error al obtener ticket: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return {
            error: true,
            message: 'No se pudo cargar el último ticket'
        };
    }
}