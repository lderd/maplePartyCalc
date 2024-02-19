from PIL import Image
from pytesseract import *
import cv2


filename = "./smaller/smaller.png"

# 이미지 전처리
# img = cv2.imread(filename)
# grayscale 이미지 생성
img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
# cv2.imshow('원본', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 임계처리 하기(binary image 생성)
ret, thresh1 = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)

# 임계처리한 이미지 2배로 확대하기
zoom3 = cv2.resize(thresh1, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
# 확대, 임계처리 한 사진 띄우기
# cv2.imshow('zoom3', zoom3)

# kernel : Morphological Transformations하는데에 사용하는 형태
# 사각형 모양 (3 * 3)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
# 타원 모양 (5 * 5)
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
# 십자 모양 (3 * 3)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

# kernel에 빈 공간이 있다면 가운데를 비워주기(작은 object 제거)
erosion = cv2.erode(zoom3, kernel, iterations = 1)
# cv2.imshow('erosion', erosion)

# kernel에 채워진 공간이 있다면 가운데를 채워주기(작은 object 확대, 빈 공간 채우기)
dilation = cv2.dilate(zoom3,kernel,iterations = 1)

# opening : erosion 이후에 dilation 하기
opening = cv2.morphologyEx(zoom3, cv2.MORPH_OPEN, kernel)
# cv2.imshow('opening', opening)

# closing : dilation 이후에 erosion 하기
closing = cv2.morphologyEx(zoom3, cv2.MORPH_CLOSE,kernel)


# 키 입력 전까지 화면에 이미지 띄우기
# cv2.waitKey(0)

# # 이미지 파일 생성
cv2.imwrite('./smaller/smaller_sizeup3.png', zoom3)
cv2.imwrite('./smaller/smaller_sizeup3_erosion.png', erosion)
cv2.imwrite('./smaller/smaller_sizeup3_dilation.png', dilation)
cv2.imwrite('./smaller/smaller_sizeup3_opening.png', opening)
cv2.imwrite('./smaller/smaller_sizeup3_closing.png', closing)

# # 화면에 뜬 이미지 창 닫기
# cv2.destroyAllWindows()


# img to txt file

text = image_to_string(zoom3, lang="Hangul")
with open("./smaller/smaller_hangul_sizeup3.txt", "w") as f:
    f.write(text)

text = image_to_string(erosion, lang="Hangul")
with open("./smaller/smaller_hangul_sizeup3_erosion.txt", "w") as f:
    f.write(text)

text = image_to_string(dilation, lang="Hangul")
with open("./smaller/smaller_hangul_sizeup3_dilation.txt", "w") as f:
    f.write(text)

text = image_to_string(opening, lang="Hangul")
with open("./smaller/smaller_hangul_sizeup3_opening.txt", "w") as f:
    f.write(text)

text = image_to_string(closing, lang="Hangul")
with open("./smaller/smaller_hangul_sizeup3_closing.txt", "w") as f:
    f.write(text)
