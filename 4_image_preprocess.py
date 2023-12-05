from PIL import Image
import os

def crop_images_in_folder(folder_path, output_folder):
    # 지정된 폴더에서 모든 파일 목록 가져오기
    file_list = os.listdir(folder_path)

    # 출력 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 각 이미지 파일에 대해 작업 수행
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)

        # 파일이 이미지인지 확인
        if file_name.lower().endswith(('.png')):
            # 이미지 열기
            with Image.open(file_path) as img:
                # 이미지 크기 가져오기
                width, height = img.size

                # 상하좌우 각각 10픽셀씩 제거
                left = 10
                top = 10
                right = width - 10
                bottom = height - 10

                # 이미지 자르기
                cropped_img = img.crop((left, top, right, bottom))

                # 출력 폴더에 저장
                output_path = os.path.join(output_folder, file_name)
                cropped_img.save(output_path)

if __name__ == "__main__":
    input_folder_path = "download_image"  # 입력 폴더 경로를 수정하세요
    output_folder_path = "cropped_image"  # 출력 폴더 경로를 수정하세요

    crop_images_in_folder(input_folder_path, output_folder_path)