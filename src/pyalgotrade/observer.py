# coding=utf-8
'''
Created on 2017��6��8��

@author: liguangyao
'''

import abc

from pyalgotrade import dispatchprio

class Event(object):
    # 初始化
    def __init__(self):
        self.__handlers = []
        self.__toSubscribe = []
        self.__toUnsubscribe = []
        self.__emitting = False
    
    # 函数作用： 1.将__toSubscribe中的值进行遍历，若不在__handlers中，则添加到__handlers中，最后将__toSubscribe清空
    #         2.将__toUnsubscribe中的值进行遍历，若在__handlers中，则将__handlers的值删除，最后将__toUnsubscribe清空
    def __applyChanges(self):
        if len(self.__toSubscribe):
            for handler in self.__toSubscribe:
                if handler not in self.__handlers:
                    self.__handlers.append(handler)
            self.__toSubscribe = []

        if len(self.__toUnsubscribe):
            for handler in self.__toUnsubscribe:
                self.__handlers.remove(handler)
            self.__toUnsubscribe = []
    
    
    