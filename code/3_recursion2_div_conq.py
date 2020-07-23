"""
    有一块1680x640米的田地，
    如何把它均分成正方形，面积最大？
    使用递归和Divide & Conquer
"""

def get_max_square(length: int, width: int) -> int:
    """
        把输入矩形均分成正方形，返回最大正方形边长
    : param length : 矩形长度
    : param width : 矩形宽度
    """
    if length < width:
        length, width = width, length
    
    if length % width == 0:
        return width
    else:
        return get_max_square(length = width, width = length % width)

print(get_max_square(length = 1680, width = 640))