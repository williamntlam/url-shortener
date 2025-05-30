from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = f"mongodb+srv://{os.getenv("MONGODB_USERNAME")}:{os.getenv("MONGODB_PASSWORD")}@{os.getenv("MONGODB_CLUSTER")}.ixmzem2.mongodb.net/?retryWrites=true&w=majority&appName={os.getenv("MONGODB_CLUSTER")}"

# Create a new client and connect to the server
client = AsyncMongoClient(MONGODB_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)