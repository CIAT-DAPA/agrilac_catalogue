import os

class FileManager:
    def __init__(self, filename, path=''):
        """
        Inicializa el administrador de archivos.
        - filename: Nombre del archivo.
        - path: Ruta relativa al directorio del proyecto (opcional).
        """
        # Obtener la ruta del directorio base del proyecto
        project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Si se proporciona un path, combínalo con el directorio del proyecto
        if path:
            self.path = os.path.join(project_dir, path)
        else:
            self.path = project_dir
        
        self.filename = filename
        self.full_path = os.path.join(self.path, self.filename)

    def create_file(self, content):
        """Crea un archivo (sobrescribe si ya existe) y escribe el contenido."""
        # Asegurarse de que el directorio existe
        os.makedirs(self.path, exist_ok=True)
        
        with open(self.full_path, 'w') as f:
            f.write(content)
        return f"Archivo '{self.full_path}' creado con éxito."

    def update_file(self, content):
        """Actualiza el archivo agregando contenido al final."""
        with open(self.full_path, 'a') as f:
            f.write(content)
        return f"Archivo '{self.full_path}' actualizado con éxito."

    def read_file(self):
        """Lee el contenido del archivo."""
        try:
            with open(self.full_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"Error: El archivo '{self.full_path}' no existe."

