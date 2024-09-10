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
    geoData.forEach(function (geo) {
      if (geo.type === "coords" && geo.latitude && geo.longitude) {
        var marker = L.marker([geo.latitude, geo.longitude]).addTo(map);
        markers.addLayer(marker); // Añadir el marcador al grupo
      }
    });

    // Ajustar el mapa para que abarque todos los puntos
    if (markers.getLayers().length > 0) {
      map.fitBounds(markers.getBounds());
    }
  });

document
  .getElementById("download-locations")
  .addEventListener("click", function () {
    let csvContent = "data:text/csv;charset=utf-8,";

    // Crear el encabezado del CSV de manera condicional
    csvContent += "Tipo";

    // Revisa si existen datos del tipo "coords"
    const hasCoords = geoData.some((geo) => geo.type === "coords");
    if (hasCoords) {
      csvContent += ",Latitud,Longitud";
    }
    // Revisa si existen datos del tipo distinto a "coords"
    const hasRegions = geoData.some((geo) => geo.type !== "coords");
    if (hasRegions) {
      csvContent += ",Región,Municipalidad";
    }
    csvContent += "\n"; // Finaliza el encabezado
    // Llenar el CSV con los datos
    geoData.forEach(function (geo) {
      if (geo.type === "coords") {
        // Para coordenadas, llenamos latitud y longitud
        csvContent += `Coordenadas,${geo.latitude},${geo.longitude}`;
        // Si también hay columnas de región, añadimos columnas vacías para esas
        if (hasRegions) {
          csvContent += ",,";
        }
        csvContent += "\n"; // Nueva línea
      } else {
        // Para región y municipalidad
        csvContent += `Región`;
        csvContent += `,"${geo.region_name}","${geo.municipality_name}"\n`;
      }
    });

    // Crear un enlace de descarga
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "ubicaciones.csv");

    // Simular el clic para descargar el archivo
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

document.addEventListener("DOMContentLoaded", function () {
  // Seleccionamos todas las pestañas
  const tabs = [
    {
      id: "complementaria-tab",
      content: document.querySelector("#complementaria"),
    },
    { id: "acceso-tab", content: document.querySelector("#acceso") },
    { id: "descripcion-tab", content: document.querySelector("#descripcion") },
    { id: "geograficos-tab", content: document.querySelector("#geograficos") },
    { id: "contacto-tab", content: document.querySelector("#contacto") },
  ];

  // Iteramos sobre cada pestaña
  tabs.forEach(function (tab) {
    // Verificamos si el contenido de la pestaña está vacío
    if (tab.content && tab.content.innerHTML.trim() === "") {
      // Si está vacío, deshabilitamos la pestaña
      document.getElementById(tab.id).classList.add("disabled");
      document.getElementById(tab.id).setAttribute("aria-disabled", "true");
      document.getElementById(tab.id).removeAttribute("data-bs-toggle"); // Quitamos la funcionalidad de activación
    }
  });
});
