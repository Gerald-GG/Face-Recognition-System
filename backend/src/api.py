from flask import Flask, request, jsonify
from flask_cors import CORS
from .utils import decode_base64_image
from .recognize_face import recognize_face

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/detect', methods=['POST'])
    def detect():
        data = request.get_json()
        base64_image = data.get('image')
        if not base64_image:
            return jsonify({"error": "Missing image"}), 400

        image = decode_base64_image(base64_image)
        if image is None:
            return jsonify({"error": "Invalid image format"}), 400

        result = recognize_face(image)
        return jsonify({"result": result or "No match"})

    return app
