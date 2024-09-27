document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const resultsContainer = document.getElementById("resultsContainer");
  const locationSearch = document.getElementById("location-search");

  if (!searchInput || !resultsContainer || !locationSearch) {
    console.error("Missing required DOM elements.");
    return;
  }

  // Función para realizar la búsqueda con filtros
  function search(query, page = 1) {
    const fechaInicio = document.getElementById("floatingStart").value;
    const fechaFin = document.getElementById("floatingEnd").value;
    const ubicaciones = getCheckedValues(
      '#location-filter input[type="checkbox"]'
    );
    const variables = getCheckedValues(
      '#variables-filter input[type="checkbox"]'
    );
    const instituciones = getCheckedValues(
      '#institution-filter input[type="checkbox"]'
    );
    const accesos = getCheckedValues('#acces-filter input[type="checkbox"]');
    const palabrasClaves = getCheckedValues(
      '#key-words-filter input[type="checkbox"]'
    );
    const frecuencias = getCheckedValues(
      '#frequency-filter input[type="checkbox"]'
    );

    const filtrosSeleccionados = {
      fechaInicio,
      fechaFin,
      ubicaciones,
      variables,
      instituciones,
      accesos,
      palabrasClaves,
      frecuencias,
    };

    const params = buildQueryParams(filtrosSeleccionados, query, page);
    fetch(`/search/searchDataset/${params}`)
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

  // Función para obtener los valores seleccionados de los checkboxes
  function getCheckedValues(selector) {
    return Array.from(document.querySelectorAll(`${selector}:checked`)).map(
      (checkbox) => checkbox.value
    );
  }

  // Función para construir los parámetros de la consulta
  function buildQueryParams(filters, query, page) {
    const params = [`query=${encodeURIComponent(query)}`, `page=${page}`];

    if (filters.fechaInicio) params.push(`start_date=${filters.fechaInicio}`);
    if (filters.fechaFin) params.push(`end_date=${filters.fechaFin}`);
    if (filters.ubicaciones.length > 0)
      params.push(`region_name=${filters.ubicaciones.join(",")}`);
    if (filters.variables.length > 0)
      params.push(`variable_name=${filters.variables.join(",")}`);
    if (filters.instituciones.length > 0)
      params.push(`institution=${filters.instituciones.join(",")}`);
    if (filters.accesos.length > 0)
      params.push(`type_dataset=${filters.accesos.join(",")}`);
    if (filters.palabrasClaves.length > 0)
      params.push(`keywords=${filters.palabrasClaves.join(",")}`);
    if (filters.frecuencias.length > 0)
      params.push(`upload_frequency=${filters.frecuencias.join(",")}`);

    return `?${params.join("&")}`;
  }

  // Inicializa la búsqueda y los handlers de paginación
  search(searchInput.value);
  searchInput.addEventListener("input", () => search(searchInput.value));
  attachPaginationHandlers();

  // Captura los cambios en los filtros
  const filters = document.querySelectorAll(
    '.form-check-input, input[type="date"]'
  );
  filters.forEach((filter) =>
    filter.addEventListener("change", () => search(searchInput.value))
  );

  // Filtrado dinámico de ubicaciones
  locationSearch.addEventListener("input", function () {
    var filter = this.value.toLowerCase();
    var listItems = document.querySelectorAll("#location-filter li");

    listItems.forEach(function (item) {
      var text = item.textContent.toLowerCase();
      var checkbox = item.querySelector("input[type='checkbox']");
      if (text.includes(filter) || checkbox.checked) {
        item.style.display = "";
      } else {
        item.style.display = "none";
      }
    });
  });
});
