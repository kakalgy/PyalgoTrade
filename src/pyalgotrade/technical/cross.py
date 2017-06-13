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
          两个数组values1和values2，较长的数组按照较短的数组的长度进行截断，alignleft是截断的方向

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

'''
          上穿和下穿的具体实现
    :param values1: 数组.
    :type values1: 数组.
    :param values2: 数组.
    :type values2: 数组.
    :param start: 数组开始位置
    :type start: int
    :param end: 数组结束位置
    :type end: int
    :param signCheck: lamdba表达式
    :type signCheck: lamdba表达式
'''
def _cross_impl(values1, values2, start, end, signCheck):
    # Get both set of values.
    values1, values2 = _get_stripped(values1[start, end], values2[start, end], start > 0)
    
    # Compute differences and check sign changes.
    ret = 0
    diffs = compute_diff(values1, values2)
    # lamdba表达式 可以对简单函数的简洁表示
    '''lambda x:x != 0 相当于
       # ###################### 普通函数 ######################
       # 定义函数（普通方式）
        def func(arg):
            return arg != 0
  
       # 执行函数
        result = func(123)
  
       # ###################### lambda ######################
  
       # 定义函数（lambda表达式）
       my_lambda = lambda arg : arg != 0
  
       # 执行函数
       result = my_lambda(123)
       
                即 返回x是否不为0
    '''
    '''
       filter（）函数包括两个参数，分别是function和list。该函数根据function参数返回的结果是否为真来过滤list参数中的项，最后返回一个新列表，如下例所示：
       >>>a=[1,2,3,4,5,6,7]
       >>>b=filter(lambda x:x>5, a)
       >>>print b
       >>>[6,7]
                 如果filter参数值为None，就使用identity（）函数，list参数中所有为假的元素都将被删除。如下所示：
       >>>a=[0,1,2,3,4,5,6,7]
       b=filter(None, a)
       >>>print b
       >>>[1,2,3,4,5,6,7]
    '''
    diffs = filter(lambda x:x != 0, diffs)
    prevDiff = None
    for diff in diffs:
        if prevDiff is not None and not signCheck(prevDiff) and signCheck(diff):
            ret += 1
        prevDiff = diff
    return ret

# Note:
# Up to version 0.12 CrossAbove and CrossBelow were DataSeries.
# In version 0.13 SequenceDataSeries was refactored to support specifying a limit to the amount
# of values to hold. This was introduced mainly to reduce memory footprint(占用的空间).
# This change had a huge impact on the way DataSeries filters were implemented since they were
# mosly views and didn't hold any actual values. For example, a SMA(200) didn't hold any values at all
# but rather calculate those on demand by requesting 200 values from the DataSeries being wrapped.
# Now that the DataSeries being wrapped may not hold so many values, DataSeries filters were refactored
# to an event based model and they will calculate and hold resulting values as new values get added to
# the underlying DataSeries (the one being wrapped).
# Since it was too complicated to make CrossAbove and CrossBelow filters work with this new model (
# mainly because the underlying DataSeries may not get new values added at the same time, or one after
# another) I decided to turn those into functions, cross_above and cross_below.

"""Checks for a cross above conditions over the specified period between two DataSeries objects.

    It returns the number of times values1 crossed above values2 during the given period.

    :param values1: The DataSeries that crosses.
    :type values1: :class:`pyalgotrade.dataseries.DataSeries`.
    :param values2: The DataSeries being crossed.
    :type values2: :class:`pyalgotrade.dataseries.DataSeries`.
    :param start: The start of the range.
    :type start: int.
    :param end: The end of the range.
    :type end: int.

    .. note::
        The default start and end values check for cross above conditions over the last 2 values.
"""
def cross_above(values1, values2, start=-2, end=None):
    return _cross_impl(values1, values2, start, end, lambda x:x > 0)

"""Checks for a cross below conditions over the specified period between two DataSeries objects.

    It returns the number of times values1 crossed below values2 during the given period.

    :param values1: The DataSeries that crosses.
    :type values1: :class:`pyalgotrade.dataseries.DataSeries`.
    :param values2: The DataSeries being crossed.
    :type values2: :class:`pyalgotrade.dataseries.DataSeries`.
    :param start: The start of the range.
    :type start: int.
    :param end: The end of the range.
    :type end: int.

    .. note::
        The default start and end values check for cross below conditions over the last 2 values.
"""
def cross_below(values1, values2, start=-2, end=None):
    return _cross_impl(values1, values2, start, end, lambda x:x < 0)

# 方法测试类
if __name__ == "__main__": 
    
    print compute_diff([1, 1, 1], [0, 1, 2])
    print compute_diff([0, 1, 2], [1, 1, 1])
    print compute_diff([0, 1, 2], [1, 1, 4])
    print compute_diff([0, 1, 2], [1, 1, None])
    
    print _get_stripped([1, 2, 3], [1], True)
    print _get_stripped([1, 2, 3], [1], False)
    print _get_stripped([1, 2, 3], [1, 2, 3, 4, 5, 6, 7], True)
    print _get_stripped([1, 2, 3, 4, 5, 6, 7], [1, 2, 3], False)
    
    
