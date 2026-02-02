from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from app import run   # your RAG pipeline

def create_app():
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )
    CORS(app)

    # 🔹 Frontend route
    @app.route("/", methods=["GET"])
    def home():
        return render_template("index.html")

    # 🔹 API route
    @app.route("/ask", methods=["POST"])
    def ask():
        data = request.get_json()

        video_id = data.get("video_id")
        question = data.get("question")

        if not video_id or not question:
            return jsonify({
                "error": "video_id and question are required"
            }), 400

        try:
            answer = run(video_id, question)
            return jsonify({
                "video_id": video_id,
                "question": question,
                "answer": answer
            })
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


