# ---------- ddddocr ----------

import ddddocr


def imageOCR(imageFile):
    """ 调用 ddddocr 识别验证码 """
    try:
        ocr = ddddocr.DdddOcr()
        with open(imageFile, 'rb') as f:
            img_bytes = f.read()
        result = ocr.classification(img_bytes)
        return True, result
    except Exception as Exc:
        return False, Exc

# ---------- pytesseract ----------
# import re
# import os
# import pytesseract
# from PIL import Image
#
# def imageOCR(imageFile):
#     """ 调用 Tesseract 识别验证码 """
#     if not os.path.exists(imageFile):
#         return f'不存在图像文件：{imageFile}'
#     try:
#         CodeImage = Image.open(imageFile)  # 读取验证码
#         CodeImage = CodeImage.convert('L')  # 转灰度
#         pixdata = CodeImage.load()  # 加载
#         w, h = CodeImage.size
#         threshold = 160
#         # 遍历所有像素，大于阈值的为黑色
#         for y in range(h):
#             for x in range(w):
#                 if pixdata[x, y] < threshold:
#                     pixdata[x, y] = 0
#                 else:
#                     pixdata[x, y] = 255
#         images = CodeImage
#         data = images.getdata()
#         w, h = images.size
#         black_point = 0
#         for x in range(1, w - 1):
#             for y in range(1, h - 1):
#                 mid_pixel = data[w * y + x]  # 中央像素点像素值
#                 if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
#                     top_pixel = data[w * (y - 1) + x]
#                     left_pixel = data[w * y + (x - 1)]
#                     down_pixel = data[w * (y + 1) + x]
#                     right_pixel = data[w * y + (x + 1)]
#                     # 判断上下左右的黑色像素点总个数
#                     if top_pixel < 10:
#                         black_point += 1
#                     if left_pixel < 10:
#                         black_point += 1
#                     if down_pixel < 10:
#                         black_point += 1
#                     if right_pixel < 10:
#                         black_point += 1
#                     if black_point < 1:
#                         images.putpixel((x, y), 255)
#                     black_point = 0
#         result_raw = pytesseract.image_to_string(images)  # 图片转文字
#         result = re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])', '', result_raw)  # 去除识别出来的特殊字符
#         return True, result
#     except Exception as Exc:
#         return False, Exc
