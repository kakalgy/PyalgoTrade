# coding=utf-8

'''
Technical：用来对DataSeries进行计算的过滤（指标）器，例如 简单移动平均线（SMA）、相对强弱指标（RSI）等，这些过滤（指标）器被建模为DataSeries的装饰器
'''

from pyalgotrade.utils import collection
from pyalgotrade import dataseries

class EventWindow(object):
    """An EventWindow class is responsible for making calculation over a moving window of values.

    :param windowSize: The size of the window. Must be greater than 0.
    :type windowSize: int.
    :param dtype: The desired data-type for the array.
    :type dtype: data-type.
    :param skipNone: True if None values should not be included in the window.
    :type skipNone: boolean.

    .. note::
        This is a base class and should not be used directly.
    """
    def __init__(self, windowSize, dtype=float, skipNone=True):
        assert(windowSize > 0)
        assert(isinstance(windowSize, int))
        
        self.__values = collection.NumPyDeque(windowSize, dtype)
        self.__windowSize = windowSize
        self.__skipNone = skipNone
        
    # 向__values中添加值value
    def onNewValue(self, dateTime, value):
        if value is not None or not self.__skipNone:
            self.__values.append(value)
    
    # 返回__values中的numpy.array
    def getValues(self):
        """Returns a numpy.array with the values in the window."""
        return self.__values.data()
    
    # 返回__windowSize
    def getWindowSize(self):
        """Returns the window size."""
        return self.__windowSize
    
    # 判断__values的长度是否等于__windowSize，即判断窗口大小是否已经塞满
    def windowFull(self):
        return len(self.__values) == self.__windowSize
    
    # 继承的类重写这个方法用来使用__values中的值来计算
    def getValue(self):
        """Override to calculate a value using the values in the window."""
        raise NotImplementedError()
        
class EventBasedFilter(dataseries.SequenceDataSeries):
    """An EventBasedFilter class is responsible for capturing new values in a :class:`pyalgotrade.dataseries.DataSeries`
    and using an :class:`EventWindow` to calculate new values.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param eventWindow: The EventWindow instance to use to calculate new values.
    :type eventWindow: :class:`EventWindow`.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """
    def __init__(self, dataSeries, eventWindow, maxLen=None):
        super(EventBasedFilter, self).__init__(maxLen)
        self.__dataSeries = dataSeries
        self.__dataSeries.getNewValueEvent().subscribe(self.__onNewValue)
        self.__eventWindow = eventWindow
        
    #
    def __onNewValue(self, dataSeries, dateTime, value):
        # Let the event window perform calculations.
        self.__eventWindow.onNewValue(dateTime, value)
        # Get the resulting value
        newValue = self.__eventWindow.getValue()
        # Add the new value.
        self.appendWithDateTime(dateTime, newValue)
        
    #
    def getDataSeries(self):
        return self.__dataSeries

    #
    def getEventWindow(self):
        return self.__eventWindow
