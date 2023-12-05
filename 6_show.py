import os
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import webbrowser
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

def show_result(file_path):
    def embed(file):
        # 사전 훈련된 ResNet 모델 로드
        model = models.resnet50(pretrained=True)
        model.eval()

        # 이미지를 로드하고 전처리
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        image = transform(Image.open(file).convert("RGB")).unsqueeze(0)

        # 특징 추출
        with torch.no_grad():
            features = model(image)

        # 텐서를 리스트로 변환
        features_list = features.squeeze().tolist()

        return features_list

    # 새로운 벡터 계산
    new_vector = embed('uploads/' + file_path)
    new_vector_arr = np.array([new_vector])

    # 폴더 경로
    folder_path = 'output_embedding/'

    # 최대 유사도와 파일 이름 초기화
    max_similarity = -1
    max_similarity_file = ""

    # 폴더 내의 모든 파일에 대해 반복
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            # 파일 읽기
            with open(os.path.join(folder_path, filename), 'r') as file:
                # JSON 데이터 로드
                data_dict = json.load(file)
            
            # 이전 벡터 가져오기
            old_vector = data_dict.get("image_features", [])
            old_vector_arr = np.array([old_vector])

            # 코사인 유사도 계산
            similarity = cosine_similarity(new_vector_arr, old_vector_arr)[0][0]

            # 최대 유사도 업데이트
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_file = filename

    # 결과 출력
    print(f"가장 높은 코사인 유사도를 갖는 파일: {max_similarity_file}")
    print(f"코사인 유사도: {max_similarity}")

    def extract_lat_lng_from_filename(filename):
        # 정규표현식을 사용하여 숫자를 추출
        match = re.search(r'lat_([-+]?\d*\.\d+|\d+)_lng_([-+]?\d*\.\d+|\d+)', filename)
        
        if match:
            # 추출된 숫자를 튜플로 반환
            lat = float(match.group(1))
            lng = float(match.group(2))
            return (lat, lng)
        else:
            # 일치하는 패턴이 없을 경우 None 반환
            return None

    def generate_google_maps_url(coordinates):
        lat, lng = coordinates

        # 위도 및 경도를 Google Maps의 URL 형식에 맞게 변환
        lat_str = f"{lat:.7f}"
        lng_str = f"{lng:.7f}"

        # URL 생성
        url = f"https://www.google.co.kr/maps/place/{lat_str}N%20{lng_str}E"
        return url

    def open_url_in_default_browser(url):
        # 기본 브라우저로 URL 열기
        webbrowser.open(url)

    def open_png_file(file_path):
        try:
            # PNG 파일 열기
            img = Image.open(file_path)
            img.show()  # 이미지를 기본 이미지 뷰어로 열기

        except Exception as e:
            print(f"Error: {e}")


    result = extract_lat_lng_from_filename(max_similarity_file)

    google_maps_url = generate_google_maps_url(result)

    urls = google_maps_url

    open_url_in_default_browser(urls)


    file_path = "cropped_image/" + max_similarity_file[:-12] + ".png"
    print(file_path)

            

    open_png_file(file_path)

if __name__ == "__main__":
    show_result("../hakgwan.jpg")