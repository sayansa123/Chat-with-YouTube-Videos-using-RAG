from fastapi import FastAPI, APIRouter, HTTPException
from rag import fetch_transcript, build_vector_store, answer_question
from store_cache import set_store, get_store

app = FastAPI()
router = APIRouter()


@router.get('/load_video')
def load_video(
    video_id:str
):
    if get_store(video_id=video_id):
        raise HTTPException(status_code=404, detail='Already loaded')
    text = fetch_transcript(video_id=video_id)
    vector_store = build_vector_store(video_id=video_id, text=text)
    set_store(video_id=video_id, vector_store=vector_store)
    return{
        'message':'Loaded'
    }


@router.get('/ask')
def ask(
    video_id:str,
    query:str
):
    vector_store = get_store(video_id=video_id)
    if not vector_store:
        raise HTTPException(status_code=400, detail='Item not found')
    answer = answer_question(vector_store= vector_store, query=query)
    return{
        'message':answer
    }


app.include_router(router)
