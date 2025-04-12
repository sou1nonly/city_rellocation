import os
import psycopg2
import time
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
from psycopg2 import OperationalError

load_dotenv()

class SupabaseVectorDB:
    def __init__(self):
        self.conn = None
        self._connect()

    def _connect(self):
        """Establish database connection with retries"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.conn = psycopg2.connect(
                    dbname='postgres',
                    user='postgres',
                    password=os.getenv('DB_PASSWORD'),
                    host='db.' + os.getenv('SUPABASE_URL').split('//')[1].split('.')[0] + '.supabase.co',
                    port='6543',
                    connect_timeout=3
                )
                register_vector(self.conn)
                print("✅ Database connection established")
                return
            except OperationalError as e:
                if attempt == max_retries - 1:
                    raise ConnectionError(
                        f"Failed to connect after {max_retries} attempts. Error: {str(e)}"
                    )
                print(f"⚠️ Retry {attempt + 1}/{max_retries}...")
                time.sleep(2)

    def test_connection(self):
        """Test if the database connection is active"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1")
                return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False

    def store_memory(self, user_id: str, embedding: list, content: str, metadata: dict):
        """Store conversation memory"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO relocation_memories 
                    (user_id, embedding, content, metadata)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, embedding, content, metadata)
                )
                self.conn.commit()
        except Exception as e:
            print(f"Error storing memory: {str(e)}")
            raise

    def retrieve_memories(self, user_id: str, query_embedding: list, top_k: int = 3):
        """Retrieve similar memories"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT content, metadata 
                    FROM relocation_memories
                    WHERE user_id = %s
                    ORDER BY embedding <=> %s
                    LIMIT %s
                    """,
                    (user_id, query_embedding, top_k)
                )
                return cur.fetchall()
        except Exception as e:
            print(f"Error retrieving memories: {str(e)}")
            return []

    def __del__(self):
        """Clean up connection when object is destroyed"""
        if self.conn:
            self.conn.close()