from flask import Flask, render_template, request, redirect, jsonify
from PIL import Image
import os
from io import BytesIO
import show

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 루트 URL에 접속하면 이미지 업로드 폼을 보여줌
@app.route('/')
def index():
    return render_template('index.html')

# 이미지를 업로드하면 호출되는 엔드포인트
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"})

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected image"})

    # 업로드된 이미지를 변수에 저장
    uploaded_image = Image.open(file)


    # 이미지를 로컬 파일로 저장 (JPEG 형식)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
    uploaded_image.save(file_path, 'JPEG')
    #khuda.hellos()
    show.show_result('uploaded_image.jpg')

    return jsonify({"success": True, "file_path": file_path})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)