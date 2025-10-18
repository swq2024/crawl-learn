from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'F:\Tesseract-OCR\tesseract.exe'

# 识别image1.png
# captcha = Image.open('image1.png')
# result = pytesseract.image_to_string(captcha)
# print(result)

# 识别image2.png
captcha = Image.open('image3.png')

# 图像预处理
def preprocess_image2(img):
    # 灰度化
    img = img.convert('L')
    
    # 自适应阈值二值化
    from PIL import ImageFilter
    img = img.filter(ImageFilter.SHARPEN)
    img = img.point(lambda x: 0 if x < 180 else 255)
    
    # 降噪
    img = img.filter(ImageFilter.MedianFilter(size=3))
    return img

captcha = preprocess_image2(captcha)
captcha.show()  # 显示处理后的图片

custom_config = r'--oem 3 --psm 6 outputbase digits'
result = pytesseract.image_to_string(captcha, config=custom_config)
print(result)
