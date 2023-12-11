from flask import Flask, request, jsonify, render_template
import os
import vertexai
from vertexai import language_models
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/webapp1/mlproj1-403203-c24f2a45ebd5.json'
vertexai.init(project="mlproj1-403203", location="us-central1")
chat_model = language_models.CodeChatModel.from_pretrained("codechat-bison")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/process_sql", methods=["POST"])
def process_sql_request():
    action = request.form.get('action', 'correct')
    sql_query = ''  # Initialize sql_query to ensure it has a value
    timestamp = datetime.now().isoformat()

    # Check for file upload
    file = request.files.get('sql_file')
    if file and file.filename:
        sql_query = file.read().decode('utf-8')
    else:
        sql_query = request.form.get('sql_query')

    if not sql_query:
        return jsonify({"error": "No SQL content provided", "timestamp": timestamp}), 400

    try:
        chat = chat_model.start_chat()
        response = chat.send_message(f"{action.capitalize()} this SQL: {sql_query}")
        result = highlight(response.text, SqlLexer(), HtmlFormatter())
    except Exception as e:
        return jsonify({"error": f"Error processing SQL: {str(e)}", "timestamp": timestamp}), 500

    return jsonify({"result": result, "timestamp": timestamp}), 200

if __name__ == "__main__":
    app.run(debug=True)
