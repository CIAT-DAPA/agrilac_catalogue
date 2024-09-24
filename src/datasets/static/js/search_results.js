document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const resultsContainer = document.getElementById("resultsContainer");

  // Función para realizar la búsqueda
  function search(query, page = 1) {
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

document.addEventListener("DOMContentLoaded", function () {
  // Captura los cambios en los filtros
  const filters = document.querySelectorAll(
    '.form-check-input, input[type="date"]'
  );

  filters.forEach((filter) => {
    filter.addEventListener("change", applyFilters);
  });

  function applyFilters() {
    // Recoge los valores de las fechas
    const fechaInicio = document.getElementById("floatingStart").value;
    const fechaFin = document.getElementById("floatingEnd").value;

    // Filtros de ubicación (paises)
    const ubicaciones = Array.from(
      document.querySelectorAll(
        '#location-filter input[type="checkbox"]:checked'
      )
    ).map((checkbox) => checkbox.value);

    // Filtros de variables
    const variables = Array.from(
      document.querySelectorAll(
        '#variables-filter input[type="checkbox"]:checked'
      )
    ).map((checkbox) => checkbox.value);

    // Filtros de instituciones
    const instituciones = Array.from(
      document.querySelectorAll(
        '#institution-filter input[type="checkbox"]:checked'
      )
    ).map((checkbox) => checkbox.value);

    // Filtros de acceso
    const accesos = Array.from(
      document.querySelectorAll('#acces-filter input[type="checkbox"]:checked')
    ).map((checkbox) => checkbox.value);

    // Filtros de palabras claves
    const palabrasClaves = Array.from(
      document.querySelectorAll(
        '#key-words-filter input[type="checkbox"]:checked'
      )
    ).map((checkbox) => checkbox.value);

    // Filtros de frecuencia de subida
    const frecuencias = Array.from(
      document.querySelectorAll(
        '#frequency-filter input[type="checkbox"]:checked'
      )
    ).map((checkbox) => checkbox.value);

    // Crea el objeto con los filtros seleccionados
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
    console.log(filtrosSeleccionados);

    function search(filtrosSeleccionados) {
      const params = [];

      if (filtrosSeleccionados.fechaInicio) {
        params.push(`start_date=${filtrosSeleccionados.fechaInicio}`);
      }
      if (filtrosSeleccionados.fechaFin) {
        params.push(`end_date=${filtrosSeleccionados.fechaFin}`);
      }
      if (filtrosSeleccionados.ubicaciones.length > 0) {
        params.push(
          `region_name=${filtrosSeleccionados.ubicaciones.join(",")}`
        );
      }
      if (filtrosSeleccionados.variables.length > 0) {
        params.push(
          `variable_name=${filtrosSeleccionados.variables.join(",")}`
        );
      }
      if (filtrosSeleccionados.instituciones.length > 0) {
        params.push(
          `institution=${filtrosSeleccionados.instituciones.join(",")}`
        );
      }
      if (filtrosSeleccionados.accesos.length > 0) {
        params.push(`type_dataset=${filtrosSeleccionados.accesos.join(",")}`);
      }
      if (filtrosSeleccionados.palabrasClaves.length > 0) {
        params.push(
          `keywords=${filtrosSeleccionados.palabrasClaves.join(",")}`
        );
      }
      if (filtrosSeleccionados.frecuencias.length > 0) {
        params.push(
          `upload_frequency=${filtrosSeleccionados.frecuencias.join(",")}`
        );
      }

      const queryString = params.length > 0 ? `?${params.join("&")}` : "";

      fetch(`/search/searchDataset/${queryString}`)
        .then((response) => response.text())
        .then((data) => {
          resultsContainer.innerHTML = data;
        })
        .catch((error) => console.error("Error:", error));
    }

    search(filtrosSeleccionados);
  }
});
