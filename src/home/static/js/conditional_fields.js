document.addEventListener('DOMContentLoaded', function() {
    var typeDatasetField = document.querySelector('select[name="type_dataset"]');
    var urlDatasetFieldWrapper = document.querySelector('.w-field.w-field--url_field.w-field--url_input.w-field--commentable');
    var urlDatasetLabelWrapper = document.querySelector('label[id="id_url_dataset-label"]');

    function toggleUrlField() {
        if (typeDatasetField && typeDatasetField.value === 'public') {
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

    if (typeDatasetField) {
        toggleUrlField();  // Ejecuta la función al cargar la página
        typeDatasetField.addEventListener('change', toggleUrlField);  // Agrega el evento para cambios
    }
});
