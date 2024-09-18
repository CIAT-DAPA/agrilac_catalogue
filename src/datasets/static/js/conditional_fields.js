document.addEventListener('DOMContentLoaded', function() {
    function toggleUrlField() {
        var typeDatasetField = document.querySelector('select[name="type_dataset"]');
        var urlDatasetFieldWrapper = document.querySelector('.w-field.w-field--url_field.w-field--url_input.w-field--commentable');
        var urlDatasetLabelWrapper = document.querySelector('label[id="id_url_dataset-label"]');
        
        if (typeDatasetField) {
            console.log("entré url")
            print("entré url")
            if (typeDatasetField.value === 'public') {
                if (urlDatasetFieldWrapper && urlDatasetLabelWrapper) {
                    urlDatasetFieldWrapper.style.display = 'block';
                    urlDatasetLabelWrapper.style.display = 'block';
                }
            } else {
                if (urlDatasetFieldWrapper && urlDatasetLabelWrapper) {
                    urlDatasetFieldWrapper.style.display = 'none';
                    urlDatasetLabelWrapper.style.display = 'none';
                }
            }
        }
    }

    // Función que muestra u oculta los campos según la selección del tipo de dato geográfico
    function toggleGeoFields() {
        console.log("entré1")
        var geoType = document.querySelector('select[name="geo_type"]').value; // Obtener el valor seleccionado en geo_type
        
        // Selecciona todos los grupos de campos de datos geográficos dinámicos
        var geoFields = document.querySelectorAll('section[id^="panel-child-content-datos_geograficos-section"]');

        geoFields.forEach(function(section, index) {
            console.log(index)
            // Seleccionar los campos y etiquetas de cada grupo
            var latitudeField = section.querySelector(`input[name="geo_data-${index}-latitude"]`)?.closest('.w-field');
            var longitudeField = section.querySelector(`input[name="geo_data-${index}-longitude"]`)?.closest('.w-field');
            var regionField = section.querySelector(`input[name="geo_data-${index}-region_name"]`)?.closest('.w-field');
            var municipalityField = section.querySelector(`input[name="geo_data-${index}-municipality_name"]`)?.closest('.w-field');
            
            // Lógica para mostrar/ocultar campos dependiendo del valor seleccionado
            if (geoType === 'coords') {
                // Mostrar latitud/longitud y ocultar región/municipalidad
                if (latitudeField && longitudeField) {
                    latitudeField.style.display = 'block';
                    longitudeField.style.display = 'block';
                }
                if (regionField && municipalityField) {
                    regionField.style.display = 'none';
                    municipalityField.style.display = 'none';
                }
            } else if (geoType === 'admin_levels') {
                // Mostrar región/municipalidad y ocultar latitud/longitud
                if (latitudeField && longitudeField) {
                    latitudeField.style.display = 'none';
                    longitudeField.style.display = 'none';
                }
                if (regionField && municipalityField) {
                    regionField.style.display = 'block';
                    municipalityField.style.display = 'block';
                }
            }
        });
    }


    function observeDynamicFields() {
        var formContainer = document.querySelector('section[id="panel-child-content-datos_geograficos-section"]');
        console.log("entré0")
        if (formContainer) {
            console.log("entré2")
            var observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes.length > 0) {
                        setTimeout(function() {
                            toggleGeoFields(); // Asegura que los nuevos campos añadidos respeten la selección global
                        }, 500); // Espera a que los campos dinámicos se añadan
                    }
                });
            });

            observer.observe(formContainer, { childList: true, subtree: true });
        }
    }


    function init() {
        // Ejecutar la función para el campo de tipo de dataset al cargar la página
        toggleUrlField();
        toggleGeoFields();

        // Agregar event listener para cambios en el select de tipo de dataset
        document.addEventListener('change', function(e) {
            if (e.target.matches('select[name="type_dataset"]')) {
                toggleUrlField();
            }
        });

        // Escuchar cambios en el select de tipo de geo-dato
        document.querySelector('select[name="geo_type"]').addEventListener('change', toggleGeoFields);

        // Iniciar la observación de campos dinámicos
        observeDynamicFields();


    }

     // Ejecutar init cuando el DOM esté listo
     setTimeout(init, 500);

});
