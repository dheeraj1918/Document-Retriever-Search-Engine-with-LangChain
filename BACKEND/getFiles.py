from flask import request,jsonify
from fileLoader import file_loader
from generatingEmbedding import generate_Embedding
from vectorSearch import get_query_results
import tempfile
import os
import traceback
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
openAiApi = os.getenv('openAiApi')
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=openAiApi
)
def upload(app):
    @app.route("/uploadFiles",methods=["GET","POST"])
    def uploadFiles():
        files=request.files.getlist("files")
        if not files:
            return jsonify({
                "error":"Files didn't recieve"
            }),404
        numberOfFiles=len(files)
        allDocuments=[]
        for file in files:
            extension = os.path.splitext(file.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False,suffix=extension) as temp:
                file.save(temp.name)
                documents=file_loader(temp.name)
                allDocuments.extend(documents)
            os.remove(temp.name)
        file_id=generate_Embedding(allDocuments)
        return jsonify({
            "status":"success",
            "lengthOfFile":numberOfFiles,
            "file_id":file_id
            
        }),200
    @app.route("/uploadQuery",methods=["GET","POST"])
    def uploadQuery():
        try:
            data=request.json
            if not data:
                return jsonify({
                    "error":"Query didn't recived."
                }),400
            user_text=data.get("text","")
            file_id=data.get("file_id")
            if not user_text.strip():
                return jsonify({
                    "error":"Query found empty"
                })
            print(f"file id : {file_id}")
            #get query results
            results=get_query_results(user_text,file_id)
            context = "\n\n".join(
                doc["text"] if isinstance(doc, dict)
                else doc.text
                for doc in results
            )

            prompt = f"""
            Answer the question using the provided context.

            Context:
            {context}

            Question:
            {user_text}

            Answer:
            """

            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b:cerebras",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            ai_response=completion.choices[0].message.content
            print(completion.choices[0].message.content)
            return jsonify({
                "status":"success",
                "documents":results,
                "ai_response":ai_response
            }),200
        except Exception as e:
            traceback.print_exc()
            print(e)
            return jsonify({
                "error":str(e),
            }),500