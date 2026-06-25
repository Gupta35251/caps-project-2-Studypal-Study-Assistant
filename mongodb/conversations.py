import uuid
from datetime import datetime,timezone
from typing import Optional,Dict,Any
from pymongo import DESCENDING
from mongodb.mongo import get_collection

conversations = get_collection("conversations")


def get_conversation_id()->str:
    return str(uuid.uuid4())
def now_utc():
    return datetime.now(timezone.utc)

def create_conversation(title:Optional[str]=None,role:Optional[str]=None,content:Optional[str]=None):
    conv_id = get_conversation_id()
    ts = now_utc()
    doc = {
        "_id":conv_id,
        "title" : title or "New Conversation",
        "last_interacted" : ts,
        "messages" : []
    }
    if role and content:
        doc["messages"].append({"role":role,"content":content,"videos":[],"timestamp":ts})
    conversations.insert_one(doc)
    return conv_id

def add_messages(conv_id:str,role:str,content:str,videos:list=None)->bool:
    ts = now_utc()
    res = conversations.update_one(
        {"_id":conv_id},
        {
            "$push":{"messages":{"role":role,"content":content,"videos":videos if videos is not None else []}},
            "$set":{"last_interacted":ts}
        }
    )
    return res.modified_count == 1

def get_conversation(conv_id)->Optional[Dict[str,Any]]:
    ts = now_utc()
    doc = conversations.find_one_and_update(
        {"_id":conv_id},
        {
            "$set":{"last_interacted":ts}
        },
        return_document = True
    )
    return doc

def get_all_conversations()->Dict[str,str]:
    cursor = conversations.find({},{"title":1}).sort("last_interacted",DESCENDING)
    return {doc["_id"]:doc["title"] for doc in cursor}


