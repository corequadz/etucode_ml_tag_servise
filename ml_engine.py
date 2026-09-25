import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

logger = logging.getLogger(__name__)

class TagPredictor:
    
    def __init__(self) -> None:
        logger.info("Загрузка модели rubert-tiny2...")
        self.model = SentenceTransformer('cointegrated/rubert-tiny2')
        
        self.candidate_tags: List[str] = [
            "инструменты", "музыка", "электроника", "одежда", "услуги", 
            "гитара", "дрель", "коляска",
            "покупка", "продажа", "помощь", "аренда", "обмен"
        ]
        
        logger.info("Предвычисление векторов тегов...")
        self.tag_embeddings: Dict[str, Any] = {
            tag: self.model.encode(tag) for tag in self.candidate_tags
        }
        logger.info("ML-движок успешно инициализирован.")

    def process_message(self, text: str) -> Dict[str, Any]:
        text_embedding = self.model.encode(text.lower())
        
        scores: Dict[str, float] = {}
        for tag, tag_emb in self.tag_embeddings.items():
            similarity = 1 - cosine(text_embedding, tag_emb)
            scores[tag] = similarity
            
        sorted_tags = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        best_tags = [tag for tag, score in sorted_tags if score > 0.4]
        
        if not best_tags:
            best_tags = ["прочее"]
            
        return {
            "tags": best_tags[:3],
            "vector": text_embedding.tolist()
        }

predictor = TagPredictor()