document.addEventListener("DOMContentLoaded", function() {
    // Verificar si el usuario es superusuario
    const isSuperuser = document.body.classList.contains('user-is-superuser');
    console.log(isSuperuser)

    if (!isSuperuser) {
        // Ocultar el campo `verified` si no es superusuario
        const verifiedField = document.querySelector('[id^="panel-child-contenido-verified-section"]'); // Seleccionar el campo `verified`
        if (verifiedField) {
            verifiedField.closest('.field').style.display = 'none';
        }
    }
});
