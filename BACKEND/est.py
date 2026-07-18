from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv('openAiApi')
print(db_url)