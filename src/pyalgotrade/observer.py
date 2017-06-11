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
    
    #订阅的过程
    def subscribe(self, handler):
        if self.__emitting:
            self.__toSubscribe.append(handler)
        elif handler not in self.__handlers:
            self.__handlers.append(handler)
        
    
