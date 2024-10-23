document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const resultsContainer = document.getElementById("resultsContainer");

  if (!searchInput || !resultsContainer) {
    console.error("Missing required DOM elements.");
    return;
  }

  // Función para realizar la búsqueda con filtros
  function search(query, page = 1) {
    const params = buildQueryParams(query, page);
    fetch(`/search/search_users/${params}`)
      .then((response) => response.text())
      .then((data) => {
        resultsContainer.innerHTML = data; // Actualiza el contenedor de resultados
        attachPaginationHandlers(); // Volver a adjuntar los handlers de paginación después de actualizar
      })
      .catch((error) => console.error("Error:", error));
  }

  // Función para manejar los clics en la paginación
  function attachPaginationHandlers() {
    const paginationLinks = resultsContainer.querySelectorAll(".pagination a");

    paginationLinks.forEach((link) => {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        const page = new URL(link.href).searchParams.get("page");
        search(searchInput.value, page); // Realiza la búsqueda con el número de página
      });
    });
  }

  // Función para construir los parámetros de la consulta
  function buildQueryParams(query, page) {
    const params = [`query=${encodeURIComponent(query)}`, `page=${page}`];
    return `?${params.join("&")}`;
  }

  // Inicializa la búsqueda y los handlers de paginación
  search(searchInput.value);
  searchInput.addEventListener("input", () => search(searchInput.value));
  attachPaginationHandlers();
});
