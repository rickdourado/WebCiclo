# services/file_service.py
# Serviço para gerenciamento de arquivos

import os
from config import Config

class FileService:
    """Serviço para operações com arquivos"""
    
    def __init__(self):
        self.upload_folder = Config.UPLOAD_FOLDER
        self.logo_partners_folder = Config.LOGO_PARCEIROS_FOLDER
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
        self.max_file_size = Config.MAX_FILE_SIZE
    
    def save_partner_logo(self, file, partner_name: str) -> str:
        """
        Salva a logo do parceiro
        
        Args:
            file: Arquivo enviado
            partner_name: Nome do parceiro
            
        Returns:
            str: Nome do arquivo salvo ou None se houver erro
        """
        print(f"\n=== SALVANDO LOGO DO PARCEIRO ===")
        print(f"File: {file}")
        print(f"Partner name: {partner_name}")
        print(f"File filename: {file.filename if file else 'None'}")
        
        if file and file.filename and file.filename != '' and self._allowed_file(file.filename):
            try:
                # Criar diretório se não existir
                logo_dir = self.logo_partners_folder
                print(f"Logo directory: {logo_dir}")
                
                if not os.path.exists(logo_dir):
                    print(f"Criando diretório: {logo_dir}")
                    os.makedirs(logo_dir)
                else:
                    print(f"Diretório já existe: {logo_dir}")
                
                # Obter extensão do arquivo
                extension = file.filename.rsplit('.', 1)[1].lower()
                print(f"Extension: {extension}")
                
                # Criar nome do arquivo: nome_do_parceiro.extensão
                # Limpar caracteres especiais do nome do parceiro
                clean_name = "".join(c for c in partner_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                clean_name = clean_name.replace(' ', '_')
                filename = f"{clean_name}.{extension}"
                print(f"Clean name: {clean_name}")
                print(f"Final filename: {filename}")
                
                # Caminho completo do arquivo
                file_path = os.path.join(logo_dir, filename)
                print(f"Full file path: {file_path}")
                
                # Verificar se arquivo já existe
                if os.path.exists(file_path):
                    print(f"AVISO: Arquivo já existe e será sobrescrito: {file_path}")
                else:
                    print(f"Arquivo novo será criado: {file_path}")
                
                # Salvar arquivo (sobrescreve se já existir)
                file.save(file_path)
                print(f"Arquivo salvo com sucesso: {file_path}")
                
                # Verificar se arquivo foi salvo
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"Confirmação: Arquivo existe com {file_size} bytes")
                else:
                    print(f"ERRO: Arquivo não foi salvo corretamente")
                
                return filename
                
            except Exception as e:
                print(f"ERRO ao salvar logo do parceiro: {str(e)}")
                import traceback
                print(f"Traceback:\n{traceback.format_exc()}")
                return None
        else:
            print(f"Arquivo inválido ou não permitido")
            if file:
                print(f"File filename: {file.filename}")
                print(f"Allowed file: {self._allowed_file(file.filename)}")
            return None
    
    def _allowed_file(self, filename: str) -> bool:
        """Verifica se a extensão do arquivo é permitida"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def delete_file(self, file_path: str) -> bool:
        """
        Exclui um arquivo
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            bool: True se excluído com sucesso
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Erro ao excluir arquivo {file_path}: {str(e)}")
            return False
    
    def get_file_size(self, file_path: str) -> int:
        """
        Obtém o tamanho de um arquivo
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            int: Tamanho em bytes ou 0 se não existir
        """
        try:
            if os.path.exists(file_path):
                return os.path.getsize(file_path)
            return 0
        except Exception as e:
            print(f"Erro ao obter tamanho do arquivo {file_path}: {str(e)}")
            return 0
    
    def ensure_directory(self, directory_path: str) -> bool:
        """
        Garante que um diretório existe
        
        Args:
            directory_path: Caminho do diretório
            
        Returns:
            bool: True se diretório existe ou foi criado
        """
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            return True
        except Exception as e:
            print(f"Erro ao criar diretório {directory_path}: {str(e)}")
            return False
    
    def save_course_cover(self, file, course_title: str) -> str:
        """
        Salva a capa do curso
        
        Args:
            file: Arquivo de imagem enviado
            course_title: Tome do curso para renomear o arquivo
            
        Returns:
            str: Nome do arquivo salvo ou None se houver erro
        """
        print(f"\n=== SALVANDO CAPA DO CURSO ===")
        print(f"File: {file}")
        print(f"Course title: {course_title}")
        print(f"File filename: {file.filename if file else 'None'}")
        
        if not file or not file.filename:
            print("Nenhum arquivo de capa fornecido")
            return None
        
        try:
            # Criar pasta IMAGENSCURSOS se não existir
            images_folder = os.path.join(os.getcwd(), 'IMAGENSCURSOS')
            if not self.ensure_directory(images_folder):
                print(f"Erro ao criar diretório {images_folder}")
                return None
            
            # Validar extensão do arquivo
            if not self._is_allowed_file(file.filename):
                print(f"Extensão não permitida: {file.filename}")
                return None
            
            # Obter extensão do arquivo original
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            # Criar nome do arquivo baseado no título do curso
            safe_title = self._sanitize_filename(course_title)
            new_filename = f"{safe_title}{file_extension}"
            
            # Caminho completo do arquivo
            file_path = os.path.join(images_folder, new_filename)
            
            # Verificar se arquivo já existe e adicionar sufixo se necessário
            counter = 1
            original_path = file_path
            while os.path.exists(file_path):
                name, ext = os.path.splitext(original_path)
                file_path = f"{name}_{counter}{ext}"
                counter += 1
            
            # Salvar arquivo
            file.save(file_path)
            
            print(f"Capa do curso salva: {file_path}")
            print(f"Nome do arquivo: {os.path.basename(file_path)}")
            
            return os.path.basename(file_path)
            
        except Exception as e:
            print(f"Erro ao salvar capa do curso: {str(e)}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitiza nome do arquivo removendo caracteres inválidos
        
        Args:
            filename: Nome original do arquivo
            
        Returns:
            str: Nome sanitizado
        """
        import re
        # Remover caracteres especiais e substituir espaços por underscores
        sanitized = re.sub(r'[^\w\s-]', '', filename)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.strip('_')