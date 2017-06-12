# coding=utf-8
'''
Created on 2017年6月12日

@author: Administrator
'''

'''
          用来比较两个数组，在具有相同数量元素的情况下，values1-values2每个元素的差，组成一个新的数组

    :param values1: 数组.
    :type values1: 数组.
    :param values2: 数组.
    :type values2: 数组.
'''
def compute_diff(values1, values2):
    assert(len(values1) == len(values2))
    ret = []
    for i in range(len(values1)):
        v1 = values1[i]
        v2 = values2[i]
        if v1 is not None and v2 is not None:
            diff = v1 - v2
        else:
            diff = None
        ret.append(diff)
    return ret

'''
          用来比较两个数组，在具有相同数量元素的情况下，values1-values2每个元素的差，组成一个新的数组

    :param values1: 数组.
    :type values1: 数组.
    :param values2: 数组.
    :type values2: 数组.
    :param alignLeft: 是否左对齐
    :type alignLeft: Boolean
'''
def _get_stripped(values1, values2, alignLeft):
    if len(values1) > len(values2):
        if alignLeft:
            values1 = values1[0:len(values2)]
        else:
            values1 = values1[len(values1) - len(values2):]
    elif len(values2) > len(values1):
        if alignLeft:
            values2 = values2[0:len(values1)]
        else:
            values2 = values2[len(values2) - len(values1):]
    return values1, values2

# 方法测试类
if __name__ == "__main__": 
    
    print compute_diff([1, 1, 1], [0, 1, 2])
    print compute_diff([0, 1, 2], [1, 1, 1])
    print compute_diff([0, 1, 2], [1, 1, 4])
    print compute_diff([0, 1, 2], [1, 1, None])
    
    print _get_stripped([1, 2, 3], [1], True)
    print _get_stripped([1, 2, 3], [1], False)
    print _get_stripped([1, 2, 3], [1, 2, 3, 4, 5, 6, 7], True)
    print _get_stripped([1, 2, 3, 4, 5, 6, 7], [1], False)
    
    
