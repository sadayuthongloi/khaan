import os
import sys
from bson import json_util
from bson.objectid import ObjectId

json_str = """
{
    "_id": {"$oid": "643e5a4db81f338a5c0cf3aa"},
    "name": "Test"
}
"""

try:
    data = json_util.loads(json_str)
    print("Loads ok:", data)
except Exception as e:
    print("Exception", e)
