document.addEventListener('DOMContentLoaded', function() {
    function toggleUrlField() {
        var typeDatasetField = document.querySelector('select[name="type_dataset"]');
        var urlDatasetFieldWrapper = document.querySelector('.w-field.w-field--url_field.w-field--url_input.w-field--commentable');
        var urlDatasetLabelWrapper = document.querySelector('label[id="id_url_dataset-label"]');

        if (typeDatasetField) {
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

    function toggleGeoFields(geoTypeField) {
        var fieldIndex = geoTypeField.name.match(/\d+/)[0];

        var latitudeField = document.querySelector(`input[name="geo_data-${fieldIndex}-latitude"]`)?.closest('.w-field');
        var longitudeField = document.querySelector(`input[name="geo_data-${fieldIndex}-longitude"]`)?.closest('.w-field');
        var regionField = document.querySelector(`input[name="geo_data-${fieldIndex}-region_name"]`)?.closest('.w-field');
        var municipalityField = document.querySelector(`input[name="geo_data-${fieldIndex}-municipality_name"]`)?.closest('.w-field');

        var latitudeLabel = document.querySelector(`label[id="id_geo_data-${fieldIndex}-latitude-label"]`);
        var longitudeLabel = document.querySelector(`label[id="id_geo_data-${fieldIndex}-longitude-label"]`);
        var regionLabel = document.querySelector(`label[id="id_geo_data-${fieldIndex}-region_name-label"]`);
        var municipalityLabel = document.querySelector(`label[id="id_geo_data-${fieldIndex}-municipality_name-label"]`);

        // Ocultar todos los campos y labels inicialmente
        if (latitudeField && longitudeField && regionField && municipalityField && latitudeLabel && longitudeLabel && regionLabel && municipalityLabel) {
            latitudeField.style.display = 'none';
            longitudeField.style.display = 'none';
            regionField.style.display = 'none';
            municipalityField.style.display = 'none';
            latitudeLabel.style.display = 'none';
            longitudeLabel.style.display = 'none';
            regionLabel.style.display = 'none';
            municipalityLabel.style.display = 'none';

            if (geoTypeField.value === 'coords') {
                latitudeField.style.display = 'block';
                longitudeField.style.display = 'block';
                latitudeLabel.style.display = 'block';
                longitudeLabel.style.display = 'block';
            } else if (geoTypeField.value === 'admin_level') {
                regionField.style.display = 'block';
                municipalityField.style.display = 'block';
                regionLabel.style.display = 'block';
                municipalityLabel.style.display = 'block';
            }
        }
    }

    function applyGeoFieldToggles() {
        var geoTypeFields = document.querySelectorAll('select[name^="geo_data-"][name$="-geo_type"]');

        geoTypeFields.forEach(function(geoTypeField) {
            toggleGeoFields(geoTypeField);

            geoTypeField.addEventListener('change', function() {
                toggleGeoFields(geoTypeField);
            });
        });
    }

    function observeDynamicFields() {
        var formContainer = document.querySelector('section[id="panel-child-content-datos_geograficos-section"]');
        if (formContainer) {
            var observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes.length > 0) {
                        setTimeout(applyGeoFieldToggles, 500); // Espera a que los campos dinámicos se añadan
                    }
                });
            });

            observer.observe(formContainer, { childList: true, subtree: true });
        }
    }

    function init() {
        // Ejecutar la función para los campos que ya están cargados
        applyGeoFieldToggles();

        // Ejecutar la función para el campo de tipo de dataset al cargar la página
        toggleUrlField();

        // Agregar event listener para cambios en el select de tipo de dataset
        document.addEventListener('change', function(e) {
            if (e.target.matches('select[name="type_dataset"]')) {
                toggleUrlField();
            }
        });

        // Iniciar la observación de campos dinámicos
        observeDynamicFields();
    }

    // Ejecutar init cuando el DOM esté listo
    setTimeout(init, 500); // Asegurar que el DOM esté completamente cargado, incluidos los campos dinámicos
});
