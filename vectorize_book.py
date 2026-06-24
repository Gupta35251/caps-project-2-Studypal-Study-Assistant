import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader,DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


load_dotenv()
embeddings = HuggingFaceEmbeddings()
text_splitter  = CharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 200
)

working_dir_path = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(working_dir_path)
parent_dir = working_dir_path
db_path = f"{parent_dir}/DB"


def vectorize_book_and_store_to_db(book_name):
    print(parent_dir)
    data = f"{parent_dir}/Data/{book_name}"
    vector_db_path = f"{db_path}/{book_name}/vector_db_of_file"
    loader = DirectoryLoader(data,glob = "**/*.pdf",loader_cls = UnstructuredFileLoader)
    documents = loader.load()
    chunks = text_splitter.split_documents(documents) 
    vector_db = Chroma.from_documents(embedding = embeddings,documents = chunks,persist_directory = vector_db_path)
    print(f"Data {book_name} stored to vector_db_of_file successfully!")
    return 0


def vectorize_individually(book_name):
    for file in os.listdir(path = f"{parent_dir}/Data_ind/{book_name}"):
        # file = file[:-4]
        if file.endswith(".pdf"):
            chapter_name = os.path.splitext(file)[0]
            vector_db_path = f"{db_path}/{book_name}/vector_db_of_particular_chapter/{chapter_name}"
            loader = UnstructuredFileLoader(f"{parent_dir}/Data_ind/{book_name}/{file}")
            documents = loader.load()
            chunks = text_splitter.split_documents(documents) 
            vector_db = Chroma.from_documents(embedding = embeddings,documents = chunks,persist_directory = vector_db_path)
            print(f"Data {book_name} stored to vector_db_of_particular_chapter successfully!")
    return 0

