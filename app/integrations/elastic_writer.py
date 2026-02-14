from elasticsearch import Elasticsearch
from datetime import datetime
import os

# =============================
# Elasticsearch Configuration
# =============================
ES_URL = os.getenv("ES_URL", "http://localhost:9200")
ES_INDEX = os.getenv("ES_INDEX", "triagepp-results")

es = Elasticsearch(ES_URL)

# =============================
# Index Triage Result
# =============================
def index_triage_result(result: dict):
    """
    Index Triage++ decision result into Elasticsearch
    """
    try:
        document = {
            **result,
            "@timestamp": datetime.utcnow().isoformat()
        }

        es.index(
            index=ES_INDEX,
            document=document
        )

    except Exception as e:
        print(f"[ElasticWriter] Failed to index result: {e}")
