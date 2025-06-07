from sentence_transformers import SentenceTransformer, util
from authors import authors
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# 작가별 평균 임베딩 계산
author_embeddings = {}

for author, paragraph_list in authors.items():
    embeddings = model.encode(paragraph_list, convert_to_tensor=True) # 입력 문장 벡터로 변환(임베딩)
    avg_embedding = embeddings.mean(dim=0)  # 평균 벡터 계산
    author_embeddings[author] = avg_embedding

# 사용자 문단과의 유사도 비교
def analyze_similarity(user_text):
    results = {}
    user_embedding = model.encode(user_text, convert_to_tensor=True)

    for author, avg_embedding in author_embeddings.items():
        similarity = util.cos_sim(user_embedding, avg_embedding).item() # 코사인 유사도 계산
        results[author] = round(similarity, 3)

    return results
