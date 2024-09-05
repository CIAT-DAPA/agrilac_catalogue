document.addEventListener("DOMContentLoaded", function () {
  const words = ["Meteorológicos", "Climáticos", "Atmosféricos", "Ambientales"];
  let index = 0;
  const wordElement = document.getElementById("changing-word");
  let currentWord = "";
  let letterIndex = 0;
  let isDeleting = false;

  function typeWord() {
    const fullWord = words[index];

    if (!isDeleting && letterIndex < fullWord.length) {
      // Añadir letras una por una
      currentWord += fullWord.charAt(letterIndex);
      wordElement.textContent = currentWord;
      letterIndex++;
      setTimeout(typeWord, 100); // Controla la velocidad de escritura
    } else if (isDeleting && letterIndex > 0) {
      // Borrar letras una por una
      currentWord = fullWord.substring(0, letterIndex - 1);
      wordElement.textContent = currentWord;
      letterIndex--;
      setTimeout(typeWord, 50); // Controla la velocidad de borrado
    } else {
      // Si la palabra está completamente escrita o borrada, cambia de estado
      isDeleting = !isDeleting;
      if (!isDeleting) {
        index = (index + 1) % words.length; // Cambia a la siguiente palabra
      }
      setTimeout(typeWord, isDeleting ? 1000 : 500); // Pausa antes de escribir o borrar
    }
  }

  typeWord(); // Inicia la animación
});
