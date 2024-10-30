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

    function toggleGeoFields() {
        var geoTypeSelect = document.querySelector('select[name="geo_type"]');
        if (!geoTypeSelect) return; // Si no se encuentra el campo geo_type, salir
        
        var geoType = geoTypeSelect.value;
        
        // Selecciona todos los grupos de campos de datos geográficos dinámicos
        var geoGroups = document.querySelectorAll('#id_geo_data-FORMS > div[data-inline-panel-child]');

        geoGroups.forEach(function(group, index) {
            // Seleccionar los campos y etiquetas de cada grupo
            var latitudeField = group.querySelector(`input[name="geo_data-${index}-latitude"]`)?.closest('.w-field');
            var latitudeLabel = group.querySelector(`label[for="id_geo_data-${index}-latitude"]`);
            
            var longitudeField = group.querySelector(`input[name="geo_data-${index}-longitude"]`)?.closest('.w-field');
            var longitudeLabel = group.querySelector(`label[for="id_geo_data-${index}-longitude"]`);
            
            var regionField = group.querySelector(`input[name="geo_data-${index}-region_name"]`)?.closest('.w-field');
            var regionLabel = group.querySelector(`label[for="id_geo_data-${index}-region_name"]`);
            
            var municipalityField = group.querySelector(`input[name="geo_data-${index}-municipality_name"]`)?.closest('.w-field');
            var municipalityLabel = group.querySelector(`label[for="id_geo_data-${index}-municipality_name"]`);
            
            // Lógica para mostrar/ocultar campos y sus labels dependiendo del valor seleccionado
            if (geoType === 'coords') {
                // Mostrar latitud/longitud y ocultar región/municipalidad
                if (latitudeField) latitudeField.style.display = 'block';
                if (latitudeLabel) latitudeLabel.style.display = 'block';
                if (longitudeField) longitudeField.style.display = 'block';
                if (longitudeLabel) longitudeLabel.style.display = 'block';
                
                if (regionField) regionField.style.display = 'none';
                if (regionLabel) regionLabel.style.display = 'none';
                if (municipalityField) municipalityField.style.display = 'none';
                if (municipalityLabel) municipalityLabel.style.display = 'none';
            } else if (geoType === 'admin_level') {
                // Mostrar región/municipalidad y ocultar latitud/longitud
                if (latitudeField) latitudeField.style.display = 'none';
                if (latitudeLabel) latitudeLabel.style.display = 'none';
                if (longitudeField) longitudeField.style.display = 'none';
                if (longitudeLabel) longitudeLabel.style.display = 'none';
                
                if (regionField) regionField.style.display = 'block';
                if (regionLabel) regionLabel.style.display = 'block';
                if (municipalityField) municipalityField.style.display = 'block';
                if (municipalityLabel) municipalityLabel.style.display = 'block';
            } else {
                // Oculta todo si no ha seleccionado nada
                if (regionField) regionField.style.display = 'none';
                if (regionLabel) regionLabel.style.display = 'none';
                if (municipalityField) municipalityField.style.display = 'none';
                if (municipalityLabel) municipalityLabel.style.display = 'none';
                if (latitudeField) latitudeField.style.display = 'none';
                if (latitudeLabel) latitudeLabel.style.display = 'none';
                if (longitudeField) longitudeField.style.display = 'none';
                if (longitudeLabel) longitudeLabel.style.display = 'none';
            }
        });
    }

    function observeDynamicFields() {
        var formContainer = document.querySelector('#id_geo_data-FORMS');

        if (formContainer) {
            var observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes.length > 0) {
                        setTimeout(toggleGeoFields, 500); // Espera a que los campos dinámicos se añadan
                    }
                });
            });

            observer.observe(formContainer, { childList: true, subtree: true });
        }
    }

    function init() {
        toggleUrlField();
        toggleGeoFields();

        // Agregar event listener para cambios en el select de tipo de dataset
        document.addEventListener('change', function(e) {
            if (e.target.matches('select[name="type_dataset"]')) {
                toggleUrlField();
            }
        });

        // Escuchar cambios en el select de tipo de geo-dato
        var geoTypeSelect = document.querySelector('select[name="geo_type"]');
        if (geoTypeSelect) {
            geoTypeSelect.addEventListener('change', toggleGeoFields);
        }

        observeDynamicFields();
    }

    setTimeout(init, 500);
});
