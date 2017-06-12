# coding=utf-8


# 返回当前值相对于前值的百分比变化
def get_change_percentage(actual, prev):
    if actual is None or prev is None or prev == 0:
        raise Exception("Invalid values")
    diff = actual - prev
    # abs() 返回绝对值ֵ
    ret = diff / float(abs(prev))
    return ret

# 返回两个值中的较小值ֵ
def safe_min(left, right):
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return min(left, right)
    
# 返回两个值中的较大值ֵ
def safe_max(left, right):
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return max(left, right)
    
    
if __name__ == "__main__": 
    print get_change_percentage(10, 5)
    
    print safe_min(5, 10)
    
    print safe_max(5, 10)
    
    
