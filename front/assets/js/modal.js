document.addEventListener("DOMContentLoaded", function() {
    // Esperar 3 segundos antes de ejecutar el código
    setTimeout(function() {
        // Obtener el modal
        var modal = document.getElementById("modal");

        // Obtener todos los divs que actúan como botones para abrir el modal
        var cards = document.querySelectorAll(".product-card"); // Cambiado a clase

        // Asegúrate de que 'cards' no esté vacío antes de asignar los eventos
        if (cards.length > 0) {
            // Asignar el evento a cada tarjeta
            cards.forEach(function(card) {
                card.onclick = function() {
                    modal.style.display = "block"; // Mostrar el modal
                };
            });
        } else {
            console.error("No se encontraron elementos con la clase 'card'.");
        }

        // Cuando el usuario hace clic en <span> (x), se cierra el modal
        var closeButton = modal.querySelector(".close"); // Asegúrate de que el modal tenga un botón de cerrar
        if (closeButton) {
            closeButton.onclick = function() {
                modal.style.display = "none"; // Ocultar el modal
            };
        }

        // Cuando el usuario hace clic en cualquier parte fuera del modal, se cierra
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none"; // Ocultar el modal
            }
        };
    }, 3000); // Espera 3 segundos antes de ejecutar el código
});