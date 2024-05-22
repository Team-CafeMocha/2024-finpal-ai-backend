import os
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.chains.query_constructor.base import AttributeInfo
from langchain_openai import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever


class LangchainModel:
    embeddings = os.environ["EMBEDDINGS"]
    db_directory = os.environ["DB_DIRECTORY"]

    base_pdf_files: [str] = [
        "두들린.pdf",
        "루나써클.pdf",
        "뤼이드.pdf",
        "리디.pdf",
        "마크앤컴퍼니.pdf",
        "메디픽.pdf"
    ]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    prompt = ChatPromptTemplate.from_template("""
        you must not use information in the form of <del><> except when requested
        The metadata being different means the documents are different. 
        I want to obtain information seperately for each document.
        you answer me only using context for question:
        <context>
        {context}
        </context>

        Question: {question}
        i want korean answer and don't print english""")

    prompt_korean = ChatPromptTemplate.from_template("""
        너는 문서를 보고 대답을 하는 전문가야 모르는 답은 모른다고 답을 해줘
        문서를 보면 "말소기록()" 괄호로 묶인 텍스트가 있는데 이거는 말소된 기록이란 뜻이야.
        내가 말소기록을 요청할 경우에만 말소기록()을 사용하고 나머지 경우는 사용하지 마. 
        metadata가 다르면 다른 문서라는 의미야. 나는 메타데이터가 같은 문서에 대해 정보를 얻고 싶어
        <context>
        {context}
        </context>

        Question: {question}""")

    retriever = None
    llm = None
    conv_chain = None

    def __init__(self):
        embeddings_open = OpenAIEmbeddings(model=self.embeddings)
        vector_index = Chroma(persist_directory=self.db_directory, embedding_function=embeddings_open)
        self.repo_id = os.environ["HF_LLM_REPO_ID"]

        # self.retriever = vector_index.as_retriever(
        #     search_type="similarity",
        #     search_kwargs={
        #         "k": 5,
        #     }
        # )

        # --- new ---
        pdfs_info = ",".join(list(map(lambda x: f"\'{x}\'", self.base_pdf_files)))
        metadata_field_info = [
            AttributeInfo(
                name="source",
                description="The company the chunk is from, should be one of " + pdfs_info,
                type="string",
            )
        ]

        document_content_description = "company information"

        llm = ChatOpenAI(temperature=0)

        self.retriever = SelfQueryRetriever.from_llm(
            llm,
            vector_index,
            document_content_description,
            metadata_field_info,
            search_kwargs={
                "k": 5,  # Select top k search results
            }
        )

        # ---  ---

        # open_llm = ChatOpenAI(
        #     temperature=0.5,  # 창의성 (0.0 ~ 2.0)
        #     max_tokens=2048,  # 최대 토큰수
        #     model_name="gpt-3.5-turbo",  # 모델명
        # )

        self.llm = HuggingFaceEndpoint(
            repo_id=self.repo_id,
            max_new_tokens=2048,
            temperature=0.1,
            callbacks=[StreamingStdOutCallbackHandler()],
            streaming=True,
        )

        self.conv_chain = ConversationalRetrievalChain.from_llm(
            self.llm,
            retriever=self.retriever,
            # chain_type="stuff",
            combine_docs_chain_kwargs={"prompt": self.prompt},
            memory=self.memory
        )

    def query(self, query: str, chat_history: [(str, str)]):
        return self.conv_chain.invoke({"question": query, "chat_history": chat_history})


