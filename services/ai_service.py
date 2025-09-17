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
