"""
Ollama LLM integration for local inference.
"""
import requests
from typing import Optional, Generator, Dict, Any

import sys
sys.path.append('..')
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaLLM:
    """Interface for Ollama local LLM."""
    
    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL
    ):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: Ollama server URL
            model: Model name to use
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.generate_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"
    
    def check_connection(self) -> bool:
        """Check if Ollama server is accessible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def check_model_available(self) -> bool:
        """Check if the configured model is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "").split(":")[0] for m in models]
                return self.model.split(":")[0] in model_names or self.model in [m.get("name") for m in models]
            return False
        except requests.RequestException:
            return False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            Generated text response
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "")
            
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Ollama: {e}")
    
    def chat(
        self,
        messages: list,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """
        Chat with the LLM using message format.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        # Build messages list
        chat_messages = []
        
        if system_prompt:
            chat_messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        chat_messages.extend(messages)
        
        payload = {
            "model": self.model,
            "messages": chat_messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(
                self.chat_url,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("message", {}).get("content", "")
            
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to Ollama: {e}")
    
    def generate_with_context(
        self,
        query: str,
        context: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a response using retrieved context.
        
        Args:
            query: User query
            context: Retrieved document context
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        # Build the prompt with context
        full_prompt = f"""Context information:
{context}

Based on the above context, please answer the following question:
{query}

Answer:"""
        
        return self.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=temperature
        )
