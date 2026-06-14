from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

_sessions: dict[str, ConversationBufferWindowMemory] = {}


def get_llm():
    return AzureChatOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        azure_deployment=settings.azure_openai_chat_deployment,
        openai_api_version=settings.azure_openai_api_version,
        api_key=settings.azure_openai_api_key,
        temperature=0.1,
        max_tokens=2000,
        streaming=True,
    )


def get_embeddings():
    return AzureOpenAIEmbeddings(
        azure_endpoint=settings.azure_openai_endpoint,
        azure_deployment=settings.azure_openai_embedding_deployment,
        openai_api_version=settings.azure_openai_api_version,
        api_key=settings.azure_openai_api_key,
    )


def get_vector_store():
    return AzureSearch(
        azure_search_endpoint=settings.azure_search_endpoint,
        azure_search_key=settings.azure_search_api_key,
        index_name=settings.azure_search_index_name,
        embedding_function=get_embeddings().embed_query,
        search_type="hybrid",
        semantic_configuration_name="trading-semantic",
    )


SYSTEM_PROMPT = """You are a trading domain knowledge assistant for a regulated investment firm.
You answer questions about trading strategies, market structure, regulations, and risk management.

Use the provided context to answer. Always cite your sources by mentioning the document name.
If the context does not contain the answer, say so clearly — do not hallucinate.

Context:
{context}

Chat History:
{chat_history}

Question: {question}

Answer:"""


def get_session_memory(session_id: str) -> ConversationBufferWindowMemory:
    if session_id not in _sessions:
        _sessions[session_id] = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10,
        )
    return _sessions[session_id]


async def run_rag_query(question: str, session_id: str) -> dict:
    llm = get_llm()
    vector_store = get_vector_store()
    memory = get_session_memory(session_id)

    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=SYSTEM_PROMPT
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": settings.search_top_k}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        verbose=False,
    )

    result = await chain.ainvoke({"question": question})

    sources = [
        {
            "document_name": doc.metadata.get("document_name", "Unknown"),
            "page_number": doc.metadata.get("page_number", 0),
            "excerpt": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        }
        for doc in result.get("source_documents", [])
    ]

    return {
        "answer": result["answer"],
        "sources": sources,
        "session_id": session_id,
    }
