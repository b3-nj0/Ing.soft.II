document.addEventListener("DOMContentLoaded", () => {
  const contenedorPlatos = document.querySelector(".productos");
  const contenedorExtras = document.querySelector(".extras-container");
  const contenedorBebidas = document.querySelector(".productos-bebidas");

  if (!contenedorPlatos || !contenedorExtras || !contenedorBebidas) {
    console.error("Faltan uno o más contenedores: .productos, .extras-container, .productos-bebidas");
    return;
  }

  const modalHTML = `
    <div class="modal-overlay" id="productModal" style="display: none;">
      <div class="modal-container">
        <div class="modal-header">
          <h3 id="modalProductName"></h3>
          <span class="close-modal">&times;</span>
        </div>
        <div class="modal-body">
          <div class="modal-image-container">
            <img id="modalProductImage" src="" alt="" class="modal-product-image">
          </div>
          <div class="modal-details">
            <p class="product-description" id="modalProductDescription"></p>
            <div class="modal-quantity">
              <p>Cantidad</p>
              <div class="quantity-selector">
                <button class="quantity-btn minus">-</button>
                <span class="quantity">2 PROD.</span>
                <button class="quantity-btn plus">+</button>
              </div>
            </div>
            <div class="modal-price">
              <p>Precio</p>
              <p class="temperature" id="modalProductPrice"></p>
            </div>
          </div>
          <div class="modal-cart-summary">
            <h2>Resumen del Pedido</h2>
            <div id="cartItemsContainer"></div>
          </div>
          
          <button id="btnAddToCart" class="btn-confirm">Añadir al carrito</button>

        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML("beforeend", modalHTML);

  const modal = document.getElementById("productModal");
  const closeModal = document.querySelector(".close-modal");
  const modalProductName = document.getElementById("modalProductName");
  const modalProductImage = document.getElementById("modalProductImage");
  const modalProductDescription = document.getElementById("modalProductDescription");
  const modalProductPrice = document.getElementById("modalProductPrice");
  const quantityElement = document.querySelector(".modal-quantity .quantity");
  const minusBtn = document.querySelector(".modal-quantity .minus");
  const plusBtn = document.querySelector(".modal-quantity .plus");
  const btnAddToCart = document.getElementById("btnAddToCart");
  const cartItemsContainer = document.getElementById("cartItemsContainer");
  const cartTotal = document.getElementById("cartTotal");

  let quantity = 2;
  let currentProduct = null;
  let carrito = [];

  closeModal.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });

  minusBtn.addEventListener("click", () => {
    if (quantity > 1) {
      quantity--;
      quantityElement.textContent = `${quantity} PROD.`;
      updateTotalPrice();
    }
  });

  plusBtn.addEventListener("click", () => {
    quantity++;
    quantityElement.textContent = `${quantity} PROD.`;
    updateTotalPrice();
  });

  function updateTotalPrice() {
    const pricePerUnit = currentProduct ? currentProduct.precio_venta : 0;
    const totalPrice = pricePerUnit * quantity;
    modalProductPrice.textContent = `Bs. ${totalPrice.toFixed(2)}`;
  }

  function agregarAlCarrito(producto, cantidad) {
    const index = carrito.findIndex(p => p.id_producto === producto.id_producto);
    if (index !== -1) {
      carrito[index].cantidad += cantidad;
    } else {
      carrito.push({ ...producto, cantidad });
    }
  }

  btnAddToCart.addEventListener("click", () => {
    if (currentProduct) {
      agregarAlCarrito(currentProduct, quantity);
      renderResumenCarrito();
      modal.style.display = "none";
    }
  });

  function renderResumenCarrito() {
    cartItemsContainer.innerHTML = "";
    let totalCompra = 0;
    const categorias = {};

    carrito.forEach(producto => {
      const categoria = producto.categoria || "Platos";
      if (!categorias[categoria]) categorias[categoria] = [];
      categorias[categoria].push(producto);
    });

    for (const [categoria, productos] of Object.entries(categorias)) {
      const catHeader = document.createElement("h3");
      catHeader.textContent = categoria;
      cartItemsContainer.appendChild(catHeader);

      productos.forEach(prod => {
        const subtotal = prod.cantidad * prod.precio_venta;
        totalCompra += subtotal;

        const item = document.createElement("div");
        item.className = "cart-item";
        item.innerHTML = `
          <span class="item-name">${prod.nombre}: ${prod.cantidad} = Bs. ${subtotal.toFixed(2)}</span>
          <div class="item-controls">
            <button class="btn-large" data-id="${prod.id_producto}" data-action="decrease"><i class="ri-subtract-line"></i></button>
            <button class="btn-large" data-id="${prod.id_producto}" data-action="increase"><i class="ri-add-line"></i></button>
          </div>
        `;

        cartItemsContainer.appendChild(item);
      });
    }

    cartTotal.textContent = `Bs. ${totalCompra.toFixed(2)}`;

    cartItemsContainer.querySelectorAll(".btn-large").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = parseInt(btn.dataset.id);
        const action = btn.dataset.action;
        const producto = carrito.find(p => p.id_producto === id);

        if (producto) {
          if (action === "increase") producto.cantidad++;
          else if (action === "decrease" && producto.cantidad > 1) producto.cantidad--;
          else if (action === "decrease" && producto.cantidad === 1) {
            carrito = carrito.filter(p => p.id_producto !== id);
          }
          renderResumenCarrito();
        }
      });
    });
  }

  document.querySelector(".modal-footer .btn-confirm").addEventListener("click", () => {
    if (carrito.length === 0) {
      Swal.fire({
        title: '¡Carrito Vacío!',
        text: 'No puedes confirmar un pedido con el carrito vacío.',
        icon: 'warning',
        confirmButtonText: 'Entendido',
        confirmButtonColor: '#e98305',
        confirmButton: {       
          fontSize: '2em'    
        }

      });
      event.preventDefault(); // Prevent the default link behavior
      return;
    }

    const detalles = carrito.map(producto => ({
      id_producto: producto.id_producto,
      cantidad: producto.cantidad,
      precio_unitario: parseFloat(producto.precio_venta),
      subtotal: parseFloat((producto.precio_venta * producto.cantidad).toFixed(2))
    }));

    const total = detalles.reduce((sum, item) => sum + item.subtotal, 0);

    const payload = {
      descripcion: "Pedido generado desde el frontend",
      pedidos: [
        {
          estado: "Pendiente",
          total,
          detalles
        }
      ]
    };


    fetch("http://127.0.0.1:8000/pedidos", {
    // fetch("https://delish.com/api/pedidos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    })


    .then(res => {
      if (!res.ok) throw new Error("Error al enviar el pedido");
      return res.json();
    })

    .then(data => {
      alert("Pedido registrado con éxito. Nro Ticket: " + data.numero_ticket);
      carrito = [];
      renderResumenCarrito();
      modal.style.display = "none";
    })

    .catch(err => {
      console.error("Error al registrar el pedido:", err);
      alert("Hubo un error al registrar el pedido");
    });
    
  });

  fetch("http://127.0.0.1:8000/productos")
    .then((res) => res.json())
    .then((productos) => {
      productos.forEach((producto) => {
        const card = document.createElement("div");
        card.className = "product-card";

        card.innerHTML = `
          <div class="product-card-inner">
            <div class="product-image-container">
              <img src="${producto.imagen || 'assets/img/default-food.png'}"
                   alt="${producto.nombre}"
                   class="product-image"
                   onerror="this.src='assets/img/default-food.png'">
            </div>

            <div class="product-content">
              <div class="product-header">
                <h3 class="product-title">${producto.nombre}</h3>
                <p class="product-description">${producto.descripcion}</p>
              </div>

              <div class="product-footer">
                <div class="price-container">
                  <span class="price-label">Precio:</span>
                  <span class="price-value">Bs. ${producto.precio_venta}</span>
                </div>

                <button class="add-to-cart-btn" data-id="${producto.id_producto}">
                  <i class="ri-shopping-cart-2-line cart-icon"></i> 
                  <p class="add-to-cart-text">Añadir</p>
                </button>
              </div>
            </div>
          </div>
        `;

        const categoria = producto.categoria?.toLowerCase();
        if (categoria === "platos") {
          contenedorPlatos.appendChild(card);
        } else if (categoria === "extras") {
          contenedorExtras.appendChild(card);
        } else if (categoria === "bebidas") {
          contenedorBebidas.appendChild(card);
        } else {
          console.warn(`Categoría no reconocida: ${producto.categoria}`);
          contenedorPlatos.appendChild(card);
        }

        const addButton = card.querySelector(".add-to-cart-btn");
        addButton.addEventListener("click", () => {
          currentProduct = producto;
          quantity = 1;
          modalProductName.textContent = producto.nombre;
          
          // Mostrar la imagen del producto
          // Si la imagen no está disponible, mostrar una imagen por defecto
          if (producto.imagen && producto.imagen.trim() !== "") {
            modalProductImage.src = producto.imagen.trim();
          } else {
            modalProductImage.src = "assets/img/default-food.png";
          }
          modalProductImage.onerror = () => {
            modalProductImage.src = "assets/img/default-food.png";
          };

          // modalProductImage.src = producto.imagen || 'assets/img/default-food.png';


          modalProductDescription.textContent = producto.descripcion;
          modalProductPrice.textContent = `Bs. ${(producto.precio_venta * quantity).toFixed(2)}`;
          quantityElement.textContent = `${quantity} PROD.`;
          modal.style.display = "flex";
        });
      });
    })
    .catch((error) => {
      console.error("Error al obtener los productos:", error);
    });
});
