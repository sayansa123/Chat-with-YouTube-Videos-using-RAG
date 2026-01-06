from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from youtube_transcript_api import YouTubeTranscriptApi

import os
os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'Your API Key Here'





def fetch_transcript(video_id:str)->str:
    transcript_obj = YouTubeTranscriptApi()
    transcript = transcript_obj.fetch(video_id)
    return ''.join(i['text'] for i in transcript.to_raw_data())





def build_vector_store(video_id:str, text:str)->Chroma:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 0
    )
    splited_documents = splitter.create_documents([text])

    embeddings = HuggingFaceEmbeddings()
    vector_store = Chroma(
        collection_name=f'video_{video_id}',
        embedding_function=embeddings,
        persist_directory='ChromaDB'
    )

    if vector_store._collection.count() == 0:
        vector_store.add_documents(splited_documents)

    return vector_store





def answer_question(vector_store:Chroma, query:str)->str:
    retriver = vector_store.as_retriever(
        search_type='mmr',
        search_kwargs={'k':5}
    )
    retrived_documents = retriver.invoke(query)
    retrived_documents_texts = '\n\n'.join(i.page_content for i in retrived_documents)

    llm = HuggingFaceEndpoint(
        repo_id='mistralai/Mistral-7B-Instruct-v0.2',
        task = 'text-generation'
    )
    model = ChatHuggingFace(llm=llm)

    prompt = ChatPromptTemplate([
        ('system',"You are a highly professional and precise AI assistant."),
        ('user',"Answer ONLY from the provided context."
            "If the context is insufficient, just say you don't know"
            "Query:\n{query}\n\n"
            "Context:\n{context}"
        )
    ])

    chain = prompt | model | StrOutputParser()
    return chain.invoke({
        'query': query,
        'context':retrived_documents_texts
    })