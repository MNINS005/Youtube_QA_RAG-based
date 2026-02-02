from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

def format_docs(docs):
    """Format retrieved documents into a string."""
    return "\n\n".join([doc.page_content for doc in docs])

def build_qa_chain(retriever, llm):
    prompt = ChatPromptTemplate.from_template("""
    Answer the question using ONLY the context below.
    If the answer is not present, say "I don't know".

    Context:
    {context}

    Question:
    {question}
    """)

    qa_chain = (
        {
            "context": RunnableLambda(lambda x: x["question"]) | retriever | format_docs,
            "question": RunnableLambda(lambda x: x["question"])
        }
        | prompt
        | llm
    )
    return qa_chain