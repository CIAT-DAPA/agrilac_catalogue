document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const resultsContainer = document.getElementById("resultsContainer");

  // Función para realizar la búsqueda
  function search(query, page = 1) {
    console.log(query, page);
    fetch(
      `/search/searchDataset/?query=${encodeURIComponent(query)}&page=${page}`
    )
      .then((response) => response.text())
      .then((data) => {
        resultsContainer.innerHTML = data; // Actualiza el contenedor de resultados
        attachPaginationHandlers(); // Volver a adjuntar los handlers de paginación después de actualizar
      })
      .catch((error) => console.error("Error:", error));
  }

  // Realiza la búsqueda cuando la página se cargue
  search(searchInput.value);

  // También realiza la búsqueda cuando se ingresa texto en el input
  searchInput.addEventListener("input", function () {
    search(searchInput.value);
  });

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

  // Llamar la función inicialmente para configurar los handlers de paginación
  attachPaginationHandlers();
});
