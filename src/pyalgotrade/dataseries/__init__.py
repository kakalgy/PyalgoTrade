# coding=utf-8
'''
DataSeries：是用于管理时间序列的抽象类
'''

import abc

from pyalgotrade import observer
from pyalgotrade.utils import collection

DEFAULT_MAX_LEN = 1024

# 检测参数maxLen是否为空或者小于等于0
def get_checked_max_len(maxLen):
    if maxLen is None:
        maxLen = DEFAULT_MAX_LEN
    if not maxLen > 0:
        raise Exception("Invalid maximum length")
    return maxLen

# It is important to inherit object to get __getitem__ to work properly.
# Check http://code.activestate.com/lists/python-list/621258/
# 数据序列
class DataSeries(object):
    """Base class for data series.

    .. note::
        This is a base class and should not be used directly.
    """
    
    __metaclass__ = abc.ABCMeta
    
    # 返回data series中的元素数量
    @abc.abstractmethod
    def __len__(self):
        """Returns the number of elements in the data series."""
        raise NotImplementedError()
        
    def __getitem__(self, key):
        """Returns the value at a given position/slice. It raises IndexError if the position is invalid,
        or TypeError if the key type is invalid."""
        # 判断key是否是slice类或者key是否是slice类型(tuple,dict,int,float)变量
        if isinstance(key, slice):
            return [self[i] for i in xrange(*key.indices(len(self)))]
        elif isinstance(key, int):
            if key < 0:
                key += len(self)
            if key >= len(self) or key < 0:
                raise IndexError("Index out of range")
            return self.getValueAbsolute(key)
        else:
            raise TypeError("Invalid argument type")
            
    # This is similar to __getitem__ for ints, but it shouldn't raise for invalid positions.
    @abc.abstractmethod
    def getValueAbsolute(self, pos):
        raise NotImplementedError()
        
    @abc.abstractmethod
    def getDateTimes(self):
        """Returns a list of :class:`datetime.datetime` associated with each value."""
        raise NotImplementedError()

        
class SequenceDataSeries(DataSeries):
    """A DataSeries that holds values in a sequence in memory.

    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding 
        number of items are discarded(丢弃) from the opposite end. If None then 
        dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """
    def __init__(self, maxLen=None):
        super(SequenceDataSeries, self).__init__()
        maxLen = get_checked_max_len(maxLen)
        
        self.__newValueEvent = observer.Event()
        self.__values = collection.ListDeque(maxLen)
        self.__dateTimes = collection.ListDeque(maxLen)
        
    # 得到__values的长度
    def __len__(self):
        return len(self.__values)
    
    # 得到__values中第key位的值
    def __getitem__(self, key):
        return self.__values[key]
    
    # 重新设置__values和__dateTimes的长度
    def setMaxLen(self, maxLen):
        """Sets the maximum number of values to hold and resizes accordingly if necessary."""
        self.__values.resize(maxLen)
        self.__dateTimes.resize(maxLen)
        
    # 得到__values的manLen参数
    def getMaxLen(self):
        """Returns the maximum number of values to hold."""
        return self.__values.getMaxLen()
    
    # Event handler receives:
    # 1: Dataseries generating the event
    # 2: The datetime for the new value
    # 3: The new value
    def getNewValueEvent(self):
        return self.__newValueEvent
    
    # 返回__values中pos位置的值
    def getValueAbsolute(self, pos):
        ret = None
        if pos >= 0 and pos < len(self.__values):
            ret = self.__values[pos]
        return ret
    
    #
    def append(self, value):
        """Appends a value."""
        self.appendWithDateTime(None, value)
        
    #
    def appendWithDateTime(self, dateTime, value):
        """
        Appends a value with an associated datetime.

        .. note::
            If dateTime is not None, it must be greater than the last one.
        """
        if dateTime is not None and len(self.__dateTimes) != 0 and self.__dateTimes[-1] >= dateTime:
            raise Exception("Invalid datetime. It must be bigger than that last one")
        assert(len(self.__values) == len(self.__dateTimes))
        self.__dateTimes.append(dateTime)
        self.__values.append(value)
        
        self.getNewValueEvent().emit(self, dateTime, value)
        
    # 获得__dateTimes中的数组
    def getDateTimes(self):
        return self.__dateTimes.data()
