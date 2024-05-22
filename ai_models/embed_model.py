import os
import sys
import re
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


class EmbedModel:
    # MARK: - base setting
    base_pdf_directory = os.environ["PDF_BASE_DIRECTORY"]
    base_pdf_files: [str] = [
        "두들린.pdf",
        "루나써클.pdf",
        "뤼이드.pdf",
        "리디.pdf",
        "마크앤컴퍼니.pdf",
        "메디픽.pdf"
    ]
    embedding_model = os.environ["EMBEDDINGS"]
    db_directory = os.environ["DB_DIRECTORY"]
    vector_index = None

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
    )

    def __init__(self):
        if not os.path.isdir(self.db_directory):
            base_pdf_directory_path = f"{sys.path[1]}/{self.base_pdf_directory}"
            base_pdf_file_paths = list(map(lambda x: f"{base_pdf_directory_path}/{x}", self.base_pdf_files))
            self.__setup(base_pdf_file_paths)

    def embed(self, pdf_file_path):
        try:
            texts = self.__data_preprocessing(pdf_file_path)
            pages = self.__make_chunk_data(pdf_file_path, texts)
            self.__store_pages(pages)
            return True
        except Exception as e:
            print(e)
            return e

    def clear(self):
        # # # 정보 삭제
        # ids = vector_index.get(0)['ids']

        # print('before: ', vector_index._collection.count())
        # for i in ids:
        #     vector_index._collection.delete(ids=i)
        # print('after :', vector_index._collection.count())
        pass

    def count(self):
        embeddings_open = OpenAIEmbeddings(model=self.embedding_model)
        vector_index = Chroma(persist_directory=self.db_directory, embedding_function=embeddings_open)
        return vector_index._collection.count()

    '''private functions --------------------------------'''

    def __setup(self, base_pdf_file_paths):
        for pdf_file_path in base_pdf_file_paths:
            try:
                self.embed(pdf_file_path)
            except FileNotFoundError:
                continue

    def __data_preprocessing(self, file_path):
        """
        # Data preprocessing

        * pdf에서 텍스트 추출
        * 취소선과 겹치는 문장의 경우 < del>  <> 이런식으로 처리
        * '. .' 과 같은 불필요한 단어 삭제
        """
        valid_texts, invalid_texts, full_texts = ([], [], [])
        with fitz.open(file_path) as document:
            for (page_number, page) in enumerate(document):
                paths = page.get_drawings()
                words = page.get_text("words")
                strikethrough_lines = self.__find_strikethrough_lines(paths)
                full = self.__mark_invalid_texts(words, strikethrough_lines)
                full_texts += full
        texts = self.__remove_stopword(full_texts)
        return texts

    @staticmethod
    def __find_strikethrough_lines(paths):
        strikethrough_lines = []
        for path in paths:
            if path["color"] != (1, 0, 0): continue
            for item in path["items"]:
                if (item[0] == "l"  # 선인 경우
                        and item[1].y == item[2].y):
                    p1, p2 = item[1:]
                    rect = fitz.Rect(p1.x, p1.y - 1, p2.x, p2.y + 1)
                    strikethrough_lines.append(rect)
                elif (item[0] == "re"  # 사각형인 경우
                      and item[1].width > item[1].height and item[1].height < 3):
                    strikethrough_lines.append(item[1])
        return strikethrough_lines

    @staticmethod
    def __mark_invalid_texts(words, strikethrough_lines):
        non_strikethrough_texts = []
        strikethrough_texts = []
        full_texts = []

        same_line = words[0][5]
        previous_strike = False
        strike_line, line = ('', '')
        for word in words:
            word_rect = fitz.Rect(word[:4])  # 단어의 위치
            strikethrough_found = False

            for line_rect in strikethrough_lines:
                if word_rect.intersects(line_rect):  # 겹치면
                    strikethrough_found = True
                    break

            if not strikethrough_found:  # 취소선이 없으면
                non_strikethrough_texts.append(word[4:6])  # 취소선이 적용되지 않은 단어 추가
                if same_line != word[5]:
                    same_line = word[5]
                    line += '\n'
                line = line + ' ' + word[4]
                if strikethrough_found != previous_strike:
                    full_texts.append('<del>' + strike_line + '<>')
                    strike_line = ''
                previous_strike = False
            else:
                strikethrough_texts.append(word[4:6])  # 취소선이 적용된 단어 추가
                strike_line = strike_line + ' ' + word[4]
                if strikethrough_found != previous_strike:
                    full_texts.append(line + '\n')
                    line = ''
                previous_strike = True
        return full_texts

    @staticmethod
    def __remove_stopword(full_texts: [str]):
        return ''.join([re.sub(r'\.\s*\.', '', text) for text in full_texts])

    def __make_chunk_data(self, pdf, texts):
        """
        # Make chunk data - vector db에 저장하기 전 데이터 만들기

        * 앞서 pdf에서 추출한 데이터 활용
        * vector DB에 저장하기 위해 pdf를 chunk 단위로 잘라 저장할 필요가 있음
        * RecursiveCharacterTextSplitter를 이용하여 2000개씩 자르고, 200개씩 겹쳐서 문서가 연결되게끔 split
        * ex) "나는 ai 파트를 맡고", "ai 파트를 맡고 있어요" -> 이런식으로 겹쳐서 저장

        * 메타데이터로 pdf 문서 이름을 같이 저장
        * create_document를 이용해서 2000개로 자른 텍스트와 메타데이터 저장
        * Document(page_content='< del>  <> 1 주의 금액 400원  , metadata={'source': 'real_data_ex.pdf'}) 형식
        """
        split_texts = self.text_splitter.split_text(texts)
        filename = pdf.split("/")[-1]
        metadata = [{'source': filename}] * len(split_texts)
        print("metadata", metadata)
        pages = self.text_splitter.create_documents(split_texts, metadatas=metadata)
        return pages

    def __store_pages(self, pages):
        """
        # Store data to vector DB
        * vector db에 저장하기 위한 임베딩은 openai의 임베딩을 사용
        * 앞서 Document(page_content, metadata) 형식의 데이터를 db에 저장
        * persist_directory는 로컬에 저장할 폴더 이름
        * vector_index._collection.count()로 현재 DB에 몇 개의 Document가 저장되어 있는지 알 수 있다.
        """

        embeddings_open = OpenAIEmbeddings(model=self.embedding_model)
        # embeddings = HuggingFaceEmbeddings()
        # embeddings_model = HuggingFaceEmbeddings(
        #     model_name='jhgan/ko-sbert-nli',
        #     model_kwargs={'device':'cpu'},
        #     encode_kwargs={'normalize_embeddings':True},
        # )

        vector_index = Chroma.from_documents(
            pages,  # Documents
            embedding=embeddings_open,  # Text embedding model
            persist_directory=self.db_directory  # persists the vectors to the file system
        )
        return vector_index
