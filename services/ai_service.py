# services/ai_service.py
# Serviço de integração com IA (Gemini)

import os
import google.generativeai as genai
from config import Config

class AIService:
    """Serviço para integração com IA"""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = Config.GEMINI_MODEL
        self._configure_gemini()
    
    def _configure_gemini(self):
        """Configura a API do Gemini"""
        if self.api_key:
            genai.configure(api_key=self.api_key)
            print(f"GEMINI_API_KEY configurada: Sim")
            print(f"GEMINI_API_KEY (primeiros 10 chars): {self.api_key[:10]}...")
        else:
            print("AVISO: GEMINI_API_KEY não configurada. A função de melhoria de descrição não estará disponível.")
    
    def enhance_description(self, description: str) -> str:
        """
        Melhora a descrição usando Gemini
        
        Args:
            description: Descrição original
            
        Returns:
            str: Descrição melhorada ou original se houver erro
        """
        print(f"\nTentando melhorar descrição com Gemini...")
        print(f"Descrição original: {description}")
        
        # Verificar se a API key está configurada
        if not self.api_key:
            print("API key do Gemini não configurada. Retornando descrição original.")
            return description
        
        try:
            print("Configurando modelo Gemini...")
            model = genai.GenerativeModel(model_name=self.model_name)
            
            prompt = f"""Explique de forma simples o que o curso ensina em no máximo 3 linhas. Mantenha em português, seja direto e objetivo:

{description}"""
            print("Enviando prompt para o Gemini...")
            
            response = model.generate_content(prompt)
            enhanced = response.text.strip()
            
            print(f"Descrição melhorada: {enhanced}")
            return enhanced
            
        except Exception as e:
            print(f"\nERRO ao melhorar descrição com Gemini: {str(e)}")
            print(f"Tipo do erro: {type(e).__name__}")
            import traceback
            print(f"Traceback completo:\n{traceback.format_exc()}")
            return description
    
    def is_available(self) -> bool:
        """Verifica se o serviço de IA está disponível"""
        return bool(self.api_key)
    
    def analyze_course_image(self, image_path: str, course_title: str = None) -> dict:
        """
        Analisa se a imagem é adequada para uso como capa de curso
        
        Args:
            image_path: Caminho para a imagem
            course_title: Título do curso (opcional)
            
        Returns:
            dict: Resultado da análise com recomendações
        """
        print(f"\nAnalisando imagem do curso com Gemini...")
        print(f"Imagem: {image_path}")
        print(f"Curso: {course_title}")
        
        # Verificar se a API key está configurada
        if not self.api_key:
            print("API key do Gemini não configurada. Pulando análise de imagem.")
            return {
                'is_suitable': True,
                'confidence': 0,
                'issues': [],
                'suggestions': [],
                'message': 'Análise não disponível (API key não configurada)'
            }
        
        try:
            # Upload da imagem para o Gemini
            print("Fazendo upload da imagem para o Gemini...")
            import PIL.Image
            img = PIL.Image.open(image_path)
            
            model = genai.GenerativeModel(model_name='gemini-2.0-flash-exp')
            
            # Prompt para análise
            context = f" para o curso '{course_title}'" if course_title else ""
            prompt = f"""Analise esta imagem que será usada como capa{context}.

Avalie se a imagem é adequada considerando:
1. Contém textos, logotipos ou grafismos excessivos?
2. É visualmente limpa e de fácil leitura?
3. Os elementos visuais são poucos e simples?
4. A imagem é representativa de conteúdo educacional?
5. A qualidade visual é adequada?

Responda em formato JSON com:
{{
    "is_suitable": true/false,
    "confidence": 0-100,
    "issues": ["lista de problemas encontrados"],
    "suggestions": ["lista de sugestões de melhoria"],
    "summary": "resumo da análise em 1-2 linhas"
}}"""

            print("Enviando imagem e prompt para análise...")
            response = model.generate_content([prompt, img])
            
            print(f"Resposta recebida do Gemini")
            
            # Processar resposta
            response_text = response.text.strip()
            
            # Remover marcadores de código se existirem
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Tentar parsear JSON
            import json
            try:
                result = json.loads(response_text)
                print(f"Análise completa: {result.get('summary', 'Sem resumo')}")
                return result
            except json.JSONDecodeError:
                # Se não for JSON válido, criar resposta padrão
                print("Resposta não está em formato JSON, usando análise básica")
                return {
                    'is_suitable': True,
                    'confidence': 50,
                    'issues': [],
                    'suggestions': [],
                    'summary': response_text[:200],
                    'message': 'Análise concluída'
                }
                
        except Exception as e:
            print(f"Erro ao analisar imagem com Gemini: {str(e)}")
            print(f"Detalhes do erro: {type(e).__name__}")
            return {
                'is_suitable': True,
                'confidence': 0,
                'issues': [],
                'suggestions': [],
                'message': f'Erro na análise: {str(e)}'
            }