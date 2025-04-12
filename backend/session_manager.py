import uuid
from datetime import datetime
from backend.advisor import RelocationAdvisor  
from backend.database import SupabaseVectorDB

class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.advisor = RelocationAdvisor()
        self.vector_db = SupabaseVectorDB()
    
    def get_context(self, query):
        # Get embedding of current query
        query_embed = self.advisor.embed_model.embed_content(query)
        
        # Query vector DB
        results = self.advisor.vector_db.query(
            vector=query_embed,
            filter={'user_id': self.user_id},
            top_k=3,
            include_metadata=True
        )
        return [match.metadata for match in results.matches]
    
    def store_interaction(self, query, response, city):
        # Create composite context
        context = {
            'query': query,
            'response': response.text,
            'city': city,
            'timestamp': datetime.now().isoformat(),
            'user_id': self.user_id
        }
        
        # Generate embedding
        embed = self.advisor.embed_model.embed_content(str(context))
        
        # Store in vector DB
        self.advisor.vector_db.upsert([{
            'id': str(uuid.uuid4()),
            'values': embed,
            'metadata': context
        }])