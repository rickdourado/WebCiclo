# image_service.py
# Serviço para processamento e análise de imagens

import os
from PIL import Image
import io

class ImageService:
    """Serviço para processamento de imagens"""
    
    def __init__(self):
        self.target_size = (1080, 1080)
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.allowed_formats = ['JPEG', 'PNG', 'JPG', 'BMP']
    
    def resize_image(self, image_file, output_path=None):
        """
        Redimensiona imagem para 1080x1080 mantendo proporção
        
        Args:
            image_file: Arquivo de imagem ou caminho
            output_path: Caminho para salvar (opcional)
            
        Returns:
            bytes: Imagem redimensionada em bytes ou salva no caminho especificado
        """
        try:
            # Abrir imagem
            if isinstance(image_file, str):
                img = Image.open(image_file)
            else:
                img = Image.open(image_file)
            
            # Converter para RGB se necessário (para garantir compatibilidade)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Criar fundo branco
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calcular dimensões para cobrir todo o canvas mantendo proporção
            img_ratio = img.width / img.height
            target_ratio = self.target_size[0] / self.target_size[1]
            
            if img_ratio > target_ratio:
                # Imagem mais larga
                new_height = self.target_size[1]
                new_width = int(new_height * img_ratio)
            else:
                # Imagem mais alta
                new_width = self.target_size[0]
                new_height = int(new_width / img_ratio)
            
            # Redimensionar imagem
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Criar canvas 1080x1080
            canvas = Image.new('RGB', self.target_size, (255, 255, 255))
            
            # Calcular posição para centralizar
            x = (self.target_size[0] - new_width) // 2
            y = (self.target_size[1] - new_height) // 2
            
            # Colar imagem no canvas
            canvas.paste(img_resized, (x, y))
            
            # Salvar ou retornar bytes
            if output_path:
                canvas.save(output_path, 'JPEG', quality=92, optimize=True)
                return output_path
            else:
                buffer = io.BytesIO()
                canvas.save(buffer, format='JPEG', quality=92, optimize=True)
                buffer.seek(0)
                return buffer.getvalue()
                
        except Exception as e:
            print(f"Erro ao redimensionar imagem: {str(e)}")
            raise
    
    def validate_image(self, image_file):
        """
        Valida se a imagem atende aos requisitos
        
        Args:
            image_file: Arquivo de imagem
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Verificar tamanho do arquivo
            if hasattr(image_file, 'seek'):
                image_file.seek(0, 2)  # Ir para o final
                file_size = image_file.tell()
                image_file.seek(0)  # Voltar ao início
                
                if file_size > self.max_file_size:
                    return False, "Arquivo muito grande. Tamanho máximo: 5MB"
            
            # Tentar abrir a imagem
            img = Image.open(image_file)
            
            # Resetar posição do arquivo
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            # Verificar formato
            if img.format not in self.allowed_formats:
                return False, f"Formato não suportado. Use: {', '.join(self.allowed_formats)}"
            
            # Validação de dimensões mínimas (opcional)
            min_dimension = 500
            if img.width < min_dimension or img.height < min_dimension:
                return False, f"Imagem muito pequena. Dimensões mínimas: {min_dimension}x{min_dimension}px"
            
            return True, None
            
        except Exception as e:
            return False, f"Erro ao validar imagem: {str(e)}"
    
    def get_image_info(self, image_file):
        """
        Obtém informações da imagem
        
        Args:
            image_file: Arquivo de imagem
            
        Returns:
            dict: Informações da imagem
        """
        try:
            img = Image.open(image_file)
            
            # Resetar posição do arquivo
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            info = {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'size_kb': round(os.path.getsize(image_file.name) / 1024, 2) if hasattr(image_file, 'name') else 0
            }
            
            return info
            
        except Exception as e:
            print(f"Erro ao obter informações da imagem: {str(e)}")
            return None
