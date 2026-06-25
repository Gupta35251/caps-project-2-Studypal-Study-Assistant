import os
from dotenv import load_dotenv
import streamlit as st
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEmbeddings
from chat_title import get_chat_title
from chatbot_utility import get_chapter_list
from get_yt_video import get_yt_search


from mongodb.conversations import(
    create_conversation,
    add_messages,
    get_conversation,
    get_all_conversations
)
load_dotenv()
GROQ_MODEL = os.getenv('GROQ_MODEL')
# DEVICE = os.getenv('DEVICE','cuda')

st.session_state.setdefault('conversation_id',None)
st.session_state.setdefault('conversation_title',None)
working_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = working_directory #Here working_directory is same as parent_directory

subject_list = ["Science","English","Hindi"]

def get_vector_db_path(chapter,subject):
    if chapter == "All Chapters":
        return f"{parent_directory}/DB/Class 9/{subject}/vector_db_of_file"
    return f"{parent_directory}/DB/Class 9/{subject}/vector_db_of_particular_chapter/{chapter}"

def setup_chain(selected_chapter,selected_subject):
    get_db_path = get_vector_db_path(selected_chapter,selected_subject)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vector_store = Chroma(embedding_function = embeddings,persist_directory = get_db_path)
    llm = ChatGroq(model = GROQ_MODEL,temperature = 0)
    memory = ConversationBufferMemory(output_key = "answer",memory_key = "chat_history",return_messages = True)

    chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        memory = memory,
        chain_type = "stuff",
        retriever = vector_store.as_retriever(search_type = "mmr",search_kwargs = {'k':3}),
        return_source_documents = True,
        get_chat_history = lambda h:h,   
        ## def get_chat_history(h):
        ##   return h
        verbose = True
    )
    return chain

st.set_page_config(page_title = "StudyPal",page_icon = "🌀",layout = "centered")
st.title("📚 StudyPal - Your Personal Study Assistant")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "video_history" not in st.session_state:
    st.session_state.video_history = []

with st.sidebar:
    st.header("💬 Chat History")
    conversations = get_all_conversations()
    if st.button("➕ New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []
        st.session_state.video_history = []

    for cid,title in conversations.items():
        is_current = cid == st.session_state.conversation_id
        label = f"**{title}**" if is_current else title
        if st.button(label,key = f"conv_{cid}"):
            doc = get_conversation(cid) or {}
            st.session_state.conversation_id = cid
            st.session_state.conversation_title = doc.get("title","untitled") 
            st.session_state.chat_history = [
                {"role":m["role"],"content":m["content"]} for m in doc.get("messages",[])
            ]
            st.session_state.video_history = []
            # We are not storing the videos in mongo db so we are providing the youtube video for the history that is being selected instead of db
            for m in doc.get("messages",[]):
                if m["role"] == "assistant":
                    videos = m.get("videos",[])
                    reference = [[v["title"],v["link"]] for v in videos]
                    st.session_state.video_history.append(reference)


selected_subject = st.selectbox(label = "Select a subject from class 9",options = subject_list,index = None)

if selected_subject:
    chapter_names = get_chapter_list(selected_subject) + ["All Chapters"]
    selected_chapter = st.selectbox(label = "Select a Chapter from the book",options = chapter_names,index = None)
    if selected_chapter:
        if st.session_state.get('selected_chapter') != selected_chapter:
            st.session_state.chat_chain = setup_chain(selected_chapter,selected_subject)  # it is used to create the coplete chain
            st.session_state.chat_history = []
            st.session_state.video_history = []
        st.session_state.selected_chapter = selected_chapter

# Display Previous messages
# for idx,message in enumerate(st.session_state.chat_history):
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#         if(message["role"] == "assistant" and idx < len(st.session_state.video_history)):
#             video_reference = st.session_state.video_history[idx]
#             if video_reference:
#                 st.subheader("Video References")
#                 for title,link in video_reference:
#                     st.markdown(f"title:{title}\nlink:{link}")

assistant_idx = 0
for idx,message in enumerate(st.session_state.chat_history):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if(message["role"] == "assistant"):
            if(assistant_idx < len(st.session_state.video_history)):
                video_reference = st.session_state.video_history[assistant_idx]
                if video_reference:
                    st.subheader("Video References")
                    for title,link in video_reference:
                        st.markdown(f"title:{title}\nlink:{link}")
            assistant_idx+=1

# User's Message
user_input = st.chat_input("Ask AI")
if user_input:
    st.session_state.chat_history.append({"role":"user","content":user_input})
    # st.session_state.video_history = []

    if st.session_state.conversation_id is None:
        title = get_chat_title(user_input)
        conv_id = create_conversation(title = title,role="user",content=user_input)
        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title
    else:
        add_messages(conv_id=st.session_state.conversation_id,role="user",content = user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if "chat_chain" not in st.session_state:
            st.warning("Please select a subject and chapter first.")
            st.stop()
        response = st.session_state.chat_chain.invoke({"question":user_input})  # it is used to retrieve the answer of the question from th emade chain
        st.markdown(response['answer'])
        


        search_query = ', '.join(item['content'] for item in st.session_state.chat_history if item["role"] == "user")
        video_title,video_link = get_yt_search(search_query)
        video_reference = []
        video_reference_for_mongo = []
        st.subheader("Video References")
        for i in range(3):
            st.markdown(f"title:{video_title[i]}\nlink:{video_link[i]}")
            video_reference.append([video_title[i],video_link[i]])
            video_reference_for_mongo.append({"title":video_title[i],"link":video_link[i]})

        st.session_state.chat_history.append({"role":"assistant","content":response['answer']})
        st.session_state.video_history.append(video_reference)
        if st.session_state.conversation_id:
            add_messages(conv_id = st.session_state.conversation_id,role = "assistant",content = response['answer'],videos = video_reference_for_mongo)



