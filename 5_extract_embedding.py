import os
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import json

# 사전 훈련된 ResNet 모델 로드
model = models.resnet50(pretrained=True)
model.eval()

# 이미지를 로드하고 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

input_folder = 'cropped_image'  # cropped_image 폴더 경로를 수정하세요.
output_folder = 'output_embedding'  # output 폴더 경로를 수정하세요.

# cropped_image 폴더 내의 모든 파일 처리
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.png'):
        input_path = os.path.join(input_folder, filename)
        image = transform(Image.open(input_path).convert("RGB")).unsqueeze(0)

        # 특징 추출
        with torch.no_grad():
            features = model(image)

        # 텐서를 리스트로 변환
        features_list = features.squeeze().tolist()

        # JSON 파일로 저장
        output_dict = {'image_features': features_list}

        # 결과물을 output 폴더에 저장
        output_filename = os.path.splitext(filename)[0] + '_output.json'
        output_path = os.path.join(output_folder, output_filename)
        
        with open(output_path, 'w') as json_file:
            json.dump(output_dict, json_file)

        print(f"Processed: {input_path} --> {output_path}")
