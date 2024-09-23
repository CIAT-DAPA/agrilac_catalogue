document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const resultsContainer = document.getElementById("resultsContainer");

  searchInput.addEventListener("input", function () {
    const query = searchInput.value;
    console.log(query);
    // Realiza la búsqueda solo si hay algo escrito
    if (query.length >= 0) {
      fetch(`/search/searchDataset/?query=${encodeURIComponent(query)}`)
        .then((response) => response.text())
        .then((data) => {
          resultsContainer.innerHTML = data; // Actualiza el contenedor de resultados
        })
        .catch((error) => console.error("Error:", error));
    } else {
      // Si el campo de búsqueda está vacío, puedes restablecer los resultados
      resultsContainer.innerHTML = "<p>No se encontraron datasets.</p>"; // Opcional: restablece el mensaje
    }
  });
});
