function copyCitation() {
  // Seleccionar el texto de la cita
  const citationText = document.getElementById("citationText").innerText;

  // Crear un elemento temporal para copiar al portapapeles
  const tempElement = document.createElement("textarea");
  tempElement.value = citationText;
  document.body.appendChild(tempElement);

  // Seleccionar el contenido y copiarlo
  tempElement.select();
  document.execCommand("copy");

  // Remover el elemento temporal
  document.body.removeChild(tempElement);

  // Cambiar el botón a verde con el ícono de check
  const copyButton = document.getElementById("copyButton");
  const copyIcon = document.getElementById("copyIcon");

  copyButton.classList.remove("btn-outline-primary");
  copyButton.classList.add("btn-success");

  // Cambiar el ícono a un check
  copyIcon.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
           stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
           class="icon icon-tabler icon-tabler-check">
          <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
          <path d="M5 12l5 5l10 -10" />
      </svg>
  `;

  // Cambiar el tooltip para indicar que ya se copió
  copyButton.setAttribute("title", "Cita copiada");
  const tooltip = bootstrap.Tooltip.getInstance(copyButton); // Obtener la instancia del tooltip
  tooltip.setContent({ ".tooltip-inner": "Cita copiada" }); // Cambiar el contenido del tooltip
  tooltip.show(); // Mostrar el nuevo tooltip

  // Después de 2 segundos, restaurar el botón a su estado inicial
  setTimeout(() => {
    copyButton.classList.remove("btn-success");
    copyButton.classList.add("btn-outline-primary");

    // Restaurar el ícono original
    copyIcon.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             class="icon icon-tabler icon-tabler-copy">
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path
                d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z" />
            <path
                d="M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1" />
        </svg>
    `;

    // Restaurar el tooltip a su mensaje original
    copyButton.setAttribute("title", "Copiar cita");
    tooltip.setContent({ ".tooltip-inner": "Copiar cita" }); // Cambiar el contenido del tooltip
  }, 2000); // Tiempo de espera en milisegundos (2 segundos)
}

// Inicializa el mapa pero no lo muestres aún
var map = L.map("map").setView([14.305, -90.785], 13);

// Agrega la capa de OpenStreetMap
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Escucha el evento de activación de la pestaña de "Datos geográficos"
document
  .querySelector("a#geograficos-tab")
  .addEventListener("shown.bs.tab", function (e) {
    // Cuando la pestaña de datos geográficos es visible, invalidamos el tamaño del mapa
    map.invalidateSize();

    // Crear un grupo de marcadores para almacenar los puntos
    var markers = L.featureGroup();

    // Iteramos sobre las coordenadas y añadimos marcadores al mapa
    geoCoords.forEach(function (coord) {
      if (coord.lat && coord.lng) {
        var marker = L.marker([coord.lat, coord.lng]).addTo(map);
        markers.addLayer(marker); // Añadir el marcador al grupo
      }
    });

    // Ajustar el mapa para que abarque todos los puntos
    if (markers.getLayers().length > 0) {
      map.fitBounds(markers.getBounds());
    }
  });
