# coding=utf-8
'''
Created on 2017年6月8日

@author: liguangyao
'''
# Python本身不提供抽象类和接口机制，要想实现抽象类，可以借助abc模块
import abc

from pyalgotrade import dispatchprio

class Event(object):
    # 初始化
    def __init__(self):
        self.__handlers = []
        # 订阅
        self.__toSubscribe = []
        # 退订
        self.__toUnsubscribe = []
        # 是否发布
        self.__emitting = False
    
    # 函数作用： 1.将__toSubscribe中的值进行遍历，若不在__handlers中，则添加到__handlers中，最后将__toSubscribe清空
    #         2.将__toUnsubscribe中的值进行遍历，若在__handlers中，则将__handlers的值删除，最后将__toUnsubscribe清空
    def __applyChanges(self):
        # 将__toSubscribe中的元素添加到__handlers中(去重)
        if len(self.__toSubscribe):
            for handler in self.__toSubscribe:
                if handler not in self.__handlers:
                    self.__handlers.append(handler)
            self.__toSubscribe = []

        # 将__toUnsubscribe中的元素从__handlers中移除
        if len(self.__toUnsubscribe):
            for handler in self.__toUnsubscribe:
                self.__handlers.remove(handler)
            self.__toUnsubscribe = []
    
    # 订阅的过程
    def subscribe(self, handler):
        if self.__emitting:
            self.__toSubscribe.append(handler)
        elif handler not in self.__handlers:
            self.__handlers.append(handler)
        
    # 退订的过程
    def unsubscribe(self, handler):
        if self.__emitting:
            self.__toUnsubscribe.append(handler)
        else:
            self.__handlers.remove(handler)
    
    #  发布
    #  *用来传递任意个无名字参数，这些参数会一个Tuple(数组)的形式访问。
    #  **用来处理传递任意个有名字的参数，这些参数用dict(Map)来访问        
    def emit(self, *args, **kwargs):
        try:
            self.__emitting = True
            for handler in self.__handlers:
                handler(*args, **kwargs)
        finally:
            self.__emitting = False
            self.__applyChanges()
            
            
class Subject(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        # 调度队列中的subject的优先级
        self.__dispatchPrio = dispatchprio.LAST
    
    # This may raise.  抛出异常  
    @abc.abstractmethod
    def start(self):
        # 空语句，为了保持程序结构的完整性
        pass
    
    # This should not raise.
    @abc.abstractmethod
    def stop(self):
        # python允许程序员自定义异常，用于描述python中没有涉及的异常情况，
        # 自定义异常必须继承Exception类，自定义异常按照命名规范以"Error"结尾，
        # 显示地告诉程序员这是异常。自定义异常使用raise语句引发，而且只能通过人工方式触发。
        raise NotImplementedError()
    
    # This should not raise.
    @abc.abstractmethod
    def join(self):
        raise NotImplementedError()
    
    # Return true if there are not more events to dispatch(调度) 
    # 如果没有其他的event需要调度，则返回ture
    @abc.abstractmethod
    def eof(self):
        raise NotImplementedError()

    # Dispatch events. If True is returned, it means that at least one event was dispatched.
    # 返回true，说明至少有一个event被调度
    @abc.abstractmethod
    def dispatch(self):
        raise NotImplementedError()

    # 返回时间给下一个event，只适用于用来同步非实时subject，实时subject则返回None
    @abc.abstractmethod
    def peekDateTime(self):
        # Return the datetime for the next event.
        # This is needed to properly synchronize non-realtime subjects.
        # Return None since this is a realtime subject.
        raise NotImplementedError()

    # 返回调度队列中的subject的优先级
    def getDispatchPriority(self):
        # Returns a priority used to sort subjects within the dispatch queue.
        # The return value should never change once this subject is added to the dispatcher.
        return self.__dispatchPrio

    # 设置调度队列中的subject的优先级
    def setDispatchPriority(self, dispatchPrio):
        self.__dispatchPrio = dispatchPrio
    
    # 当subject被调度器注册时调用
    def onDispatcherRegistered(self, dispatcher):
        # Called when the subject is registered with a dispatcher.
        pass
    
