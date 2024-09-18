document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("li").forEach(function (listItem) {
    const description = listItem.querySelector(".description");
    const button = listItem.querySelector(".toggle-description");

    // Asegurarse de que la descripción y el botón existen antes de continuar
    if (description && button) {
      // Crear un clon invisible para medir la altura real del contenido sin truncamiento
      const clonedDescription = description.cloneNode(true);
      clonedDescription.style.display = "block";
      clonedDescription.style.visibility = "hidden";
      clonedDescription.style.position = "absolute";
      clonedDescription.style.maxHeight = "none"; // Sin límite de altura para obtener la altura real
      clonedDescription.style.webkitLineClamp = "unset"; // Sin límite de líneas

      // Añadimos el clon temporal al DOM para medirlo
      listItem.appendChild(clonedDescription);

      // Comprobar si el contenido está truncado
      const isTruncated =
        clonedDescription.scrollHeight > description.clientHeight;

      if (isTruncated) {
        button.style.display = "inline"; // Mostrar el botón solo si el contenido está truncado
        description.classList.add("mb-0");
        button.classList.add("mb-3");
        button.addEventListener("click", function () {
          if (description.classList.contains("truncate-description")) {
            // Expandir el texto
            description.classList.remove("truncate-description");
            button.textContent = "Ver menos";
          } else {
            // Volver a truncar el texto
            description.classList.add("truncate-description");
            button.textContent = "Ver más";
          }
        });
      } else {
        description.classList.add("mb-3");
        button.classList.add("mb-0");
        button.style.display = "none"; // Ocultar el botón si no está truncado
      }

      // Eliminar el clon después de medir
      listItem.removeChild(clonedDescription);
    }
  });
});
