from PIL import Image
from pytesseract import *
import cv2


filename = "./smaller/smaller.png"

# 이미지 전처리
# img = cv2.imread(filename)
# grayscale 이미지 생성
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
cv2.imshow('원본', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

ret, thresh1 = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)
cv2.imshow('임계처리', thresh1)

# 키 입력 전까지 화면에 이미지 띄우기
cv2.waitKey(0)

# 이미지 파일 생성
cv2.imwrite('./smaller/greyScaleSmaller.png', thresh1)


# 화면에 뜬 이미지 창 닫기
cv2.destroyAllWindows()

# img to txt file
image = Image.open('./smaller/greyScaleSmaller.png')

text = image_to_string(image, lang="kor")

with open("./smaller/after_smaller.txt", "w") as f:
    f.write(text)
# img to txt file
