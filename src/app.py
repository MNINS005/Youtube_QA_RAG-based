from loaders.transcript import get_transcript
from embeddings.embedder import split_text
from vectorstore.store import create_vectorstore
from retriever.retriever import get_retriever
from chains.qa_chain import build_qa_chain
from config import llm, embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_for_translation(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,     # SAFE for Groq TPM
        chunk_overlap=100
    )
    return splitter.split_text(text)


def translate_to_english(text: str, llm) -> str:
    prompt = f"""
Translate the following YouTube transcript into clear English.
Preserve technical meaning.
Do NOT summarize or omit information.

Transcript:
{text}
"""
    return llm.invoke(prompt).content
def translate_chunks(chunks: list[str], llm) -> str:
    translated_chunks = []

    for chunk in chunks:
        prompt = f"""
Translate the following YouTube transcript chunk into clear English.
Preserve technical meaning.
Do NOT summarize or omit information.

Text:
{chunk}
"""
        translated = llm.invoke(prompt).content
        translated_chunks.append(translated)

    return "\n".join(translated_chunks)


def run(video_id: str, question: str):
    # Get transcript + language
    transcript, lang = get_transcript(video_id)

    # Translate ONCE if needed
    if lang != "en":
        chunks = split_for_translation(transcript)
        transcript = translate_chunks(chunks, llm)

    
    docs = split_text(transcript)
    vectorstore = create_vectorstore(docs, embeddings)
    retriever = get_retriever(vectorstore)
    qa_chain = build_qa_chain(retriever, llm)

    result = qa_chain.invoke({"question": question})
    return result.content


# if __name__ == "__main__":
#     video_id = "VIDEO_ID_HERE"
#     question = "What is this video about?"
#     print(run(video_id, question))
