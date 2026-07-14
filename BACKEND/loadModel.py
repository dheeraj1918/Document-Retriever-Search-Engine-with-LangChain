import numpy as np
from sentence_transformers import SentenceTransformer
class EmbeddingManager:
    def __init__(self,model_name:str="all-MiniLM-L6-V2")->np.ndarray:
        self.model_name=model_name
        self.model=None
        self._load_model()
    def _load_model(self):
        try:
            print(f"loading embedding model {self.model_name}")
            self.model=SentenceTransformer(self.model_name)
            print(f"embedding model {self.model}")
            print(f"model loaded successfully. embedding dimensions {self.model.get_embedding_dimension()}")
        except Exception as e:
            print(f"Error {e}")
    def generate_embedding(self,text):
        if not self.model:
            raise ValueError("model not found")
        response=self.model.encode(text)
        print(f"Generating embedding with shape: {response.shape}")
        return response