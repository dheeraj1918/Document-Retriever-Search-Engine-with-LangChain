from flask import request,jsonify
from generateEmbeddings import generate_embedding
import os 
import tempfile
from pdfLoader import pdf_loader
import traceback
from vectorSearch import get_query_results
def upload(app):
    @app.route("/uploadFiles",methods=["GET","POST"])
    def processFile():
        files=request.files.getlist()
        if not files:
            return jsonify({
                "error":"Files didnt recieve"
            }),404
        numberOfFiles=len(files)
        all_documents=[]
        for file in files:
            mime_type=file.content_type
            with tempfile.NamedTemporaryFile(delete=False,suffix=mime_type) as t:
                file.save(t.name)
                document=pdf_loader(t.name)
                all_documents.extend(document)
            os.remove(t.name)
        collection_name=generate_embedding(all_documents)
        return jsonify({
            "status":"Files uploaded Successfully",
            "numberOfFiles":numberOfFiles,
            "collection":collection_name
        }),200
    
    def user_query():
        try:
            data=request.json
            if not data:
                return jsonify({
                    "error":"No Query found"
                }),404
            user_text=data.get("text","")
            collection_name = data.get("file_id")
            if not user_text.strip():
                return jsonify({
                    "status": "error",
                    "documents": "Text is empty"
                }), 400
            print(data)
            print(collection_name)
            docs=get_query_results(user_text,collection_name)
            return jsonify({
                "status": "success",
                "documents": docs
            }), 200
        except Exception as e:
            traceback.print_exc()
            print(e)

            return jsonify({
                "status": "error",
                "documents": str(e)
            }), 500