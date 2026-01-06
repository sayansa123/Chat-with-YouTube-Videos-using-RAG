from typing import Dict
from langchain_chroma import Chroma

cache : Dict[str , Chroma] = {}  # {'video_id':'vector_store'}

def set_store(video_id:str, vector_store:Chroma):
    cache[video_id]=vector_store

def get_store(video_id:str):
    return cache.get(video_id)