from flask import Flask, request, jsonify, render_template
from gradio_client import Client, handle_file
from pymongo import MongoClient
from datetime import datetime
import shutil
import os

app = Flask(__name__)

# --- CONFIGURATION ---
COLAB_API_URL = "https://1901bf67534673d63a.gradio.live"  # <-- Paste here
MONGO_URI = "mongodb+srv://mohankalimuthu2004_db_user:2IyrWggMKRoOtLFb@habitiqrag.jplmfdn.mongodb.net/?appName=HabitIQRag"  # <-- Paste here

# Database Setup
client = MongoClient(MONGO_URI)
db = client['img2360_db']
history_collection = db['generations']

# Ensure local folders exist for temporary storage
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/models", exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_3d_model():
    if 'car_image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['car_image']
    upload_path = os.path.join("static/uploads", file.filename)
    file.save(upload_path)

    try:
        # Send image to your private Colab GPU
        gradio_client = Client(COLAB_API_URL)

        print("🚀 Sending image to Colab GPU...")

        # THE FIX: Pass arguments positionally (no keywords) to bypass name mismatches
        result = gradio_client.predict(
            handle_file(upload_path),  # 1st argument: The Image File
            True,  # 2nd argument: Remove Background (Boolean)
            0.85,  # 3rd argument: Foreground Ratio (Float)
            api_name="/generate"
        )

        print("✅ 3D Model received!")

        # TripoSR returns an .obj file
        generated_model_path = result[1] if isinstance(result, (list, tuple)) else result
        final_model_name = f"car_{int(datetime.now().timestamp())}.obj"
        final_model_path = os.path.join("static/models", final_model_name)

        shutil.copy(generated_model_path, final_model_path)

        # Log it in MongoDB
        history_collection.insert_one({
            "original_image": file.filename,
            "model_path": final_model_path,
            "created_at": datetime.now()
        })

        return jsonify({"message": "Success", "model_url": f"/{final_model_path}"})

    except Exception as e:
        print("\n--- 🚨 API SCHEMA MISMATCH ---")
        print("Printing the exact expected variables from the Colab server:")
        # If it fails again, this will print the exact expected inputs in your terminal!
        gradio_client.view_api()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)