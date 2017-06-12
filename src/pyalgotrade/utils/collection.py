# coding=utf-8
'''
Created on 2017年6月11日

@author: Administrator
'''

import numpy as np

# 判断v1是否小于v2
def lt(v1, v2):
    if v1 is None:
        return True
    elif v2 is None:
        return False
    else:
        return v1 < v2

# Returns (values, ix1, ix2)
# values1 and values2 are assumed to be sorted
# 参数默认是排好序的，找出values1和values2中相同的元素，并且返回各自在原列表中的位置
def intersect(values1, values2, skipNone=False):
    ix1 = []
    ix2 = []
    values = []
    
    i1 = 0
    i2 = 0
    
    while i1 < len(values1) and i2 < len(values2):
        v1 = values1[i1]
        v2 = values2[i2]
        
        if v1 == v2 and (v1 is not None or skipNone is False):
            ix1.append(i1)
            ix2.append(i2)
            values.append(v1)
            i1 += 1
            i2 += 1
        elif lt(v1, v2):
            i1 += 1
        else:
            i2 += 1
            
    return (values, ix1, ix2)

# Like a collections.deque(双向队列) but using a numpy.array.
# self只有在类的方法中才会有，独立的函数或方法是不必带有self的。self在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数。
# self名称不是必须的，在python中self不是关键词，你可以定义成a或b或其它名字都可以,但是约定成俗统一使用self.
# 等价于C++中的self指针和Java、C#中的this,指的是对象本身
class NumPyDeque(object):
    def __init__(self, maxLen, dtype=float):
        assert maxLen > 0, "Invalid maximum length"
        
        self.__values = np.empty(maxLen, dtype=dtype)  # 创建一个类型为dtype，长度为maxLen的numpy.array
        self.__maxLen = maxLen
        self.__nextPos = 0
        
    # 获得属性__maxLen
    def getMaxLen(self):
        return self.__maxLen
    
    # 在数组后面添加一个值，若已经超出数组范围，则左移之后添加到最右边
    def append(self, value):
        if self.__nextPos < self.__maxLen:
            self.__values[self.__nextPos] = value
            self.__nextPos += 1
        else:
            # Shift items to the left and put the last value.
            # I'm not using np.roll to avoid creating a new array.
            # 负数表示从后数第几个元素，-1即为列表的最后一个元素
            # 列表切片： (注意：切片并不会取到“尾下表”那个数)
            # # 定义列表L
            # L = [1,2,3,4,5,6,7,8,9]
            # L[1:5] = [2, 3, 4, 5]
            self.__values[0:-1] = self.__values[1:]
            self.__values[self.__nextPos - 1] = value
    
    # 返回数组，若数组长度未用完则只返回已经初始化的部分；若数组长度已用完则返回整个数组
    def data(self):
        # If all values are not initialized, return a portion of the array.
        if self.__nextPos < self.__maxLen:
            ret = self.__values[0:self.__nextPos]
        else:
            ret = self.__values
        return ret
    
    def resize(self, maxLen):
        assert maxLen > 0, "Invalid maximum length"
        
        # Create empty, copy last values and swap.
        values = np.empty(maxLen, dtype=self.__values.dtype)
        lastValues = self.__values[0:self.__nextPos]
        values[0:min(maxLen, len(lastValues))] = lastValues[-1 * min(maxLen, len(lastValues)):]
        self.__values = values
        
        self.__maxLen = maxLen
        if self.__nextPos >= self.__maxLen:
            self.__nextPos = self.__maxLen
            
    # 获得当前__nextPos的值        
    def __len__(self):
        return self.__nextPos
    
    # 获得数组中对应key位置的值
    def __getitem__(self, key):
        return self.data()[key]
    
# I'm not using collections.deque because:
# 1: Random access is slower.
# 2: Slicing(切割) is not supported.
class ListDeque(object):
    def __init__(self, maxLen):
        assert maxLen > 0, "Invalid maximum length"
        
        self.__values = []
        self.__maxLen = maxLen
        
    # 得到maxLen的值
    def getMaxLen(self):
        return self.__maxLen
    
    # 向列表中添加一个元素value，添加到末端，再检查list大小是否超出最大值，若超出，则
    # 移除list的第一个元素 
    def append(self, value):
        self.__values.append(value)
        # Check bounds检查边界
        if len(self.__values) > self.__maxLen:
            # pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
            self.__values.pop(0)
    
    # 返回__values的list   
    def data(self):
        return self.__values
    
    # 重新设定__values的list的最大长度，并且
    def resize(self, maxLen):
        assert maxLen > 0 , "Invalid maximum length"
        
        self.__maxLen = maxLen
        self.__values = self.__values[-1 * maxLen:]
    
    # 返回__values的list的长度
    def __len__(self):
        return len(self.__values)
    
    # 返回位置为key的__values__中的值
    def __getitem__(self, key):
        return self.__values[key]
    
if __name__ == "__main__": 
    values1 = [0, 1, 4, 7]
    values2 = [4, 5, 6, 7]
    print intersect(values1, values2)
