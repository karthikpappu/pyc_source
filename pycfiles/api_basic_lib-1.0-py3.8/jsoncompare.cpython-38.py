# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\atapibasiclib\jsoncompare.py
# Compiled at: 2019-12-24 22:13:18
# Size of source mod 2**32: 10627 bytes
import copy, json, re
from collections import Counter

def json_comp(dictobj1, dictobj2={}):
    """
    【功能】比较两个字典类型是否是包含关系
    【参数】dictobj1:字典类型
            dictobj2:字典类型
    【结果】如果dictobj2中的键值对在dictobj1中都存在，且路径一致，则认为存在包含关系，否则不存在包含关系
    """
    if dictobj2 is {}:
        return True
    else:
        if not isinstance(dictobj1, dict):
            dictobj1 = json.loads(dictobj1)
        dictobj2 = isinstance(dictobj2, dict) or json.loads(dictobj2)
    values_dictobj2 = list(all_list(getvalues(dictobj2, result=[])).keys())
    fp_dictobj1 = find_path(dictobj1)
    fp_dictobj2 = find_path(dictobj2)
    result = True
    for value in values_dictobj2:
        the_value_path_dictobj1 = list(set(fp_dictobj1.the_value_path(value)))
        the_value_path_dictobj2 = list(set(fp_dictobj2.the_value_path(value)))
        the_value_path_dictobj1 = resetpathindex(the_value_path_dictobj1)
        the_value_path_dictobj2 = resetpathindex(the_value_path_dictobj2)
        print('the_value_path_dictobj1=%s' % the_value_path_dictobj1)
        print('the_value_path_dictobj2=%s' % the_value_path_dictobj2)
        if set(the_value_path_dictobj2) <= set(the_value_path_dictobj1):
            pass
        else:
            result = False
    else:
        return result


class find_path:

    def __init__(self, target):
        self.target = target

    def find_the_value(self, target, value, path='', path_list=None):
        """完全匹配，每经过一层(list、dict)都会记录path，到了最后一层且当前target就是要找的目标，才把对应的path记录下来
        :param target: 被搜索的目标
        :param value: 要搜索的关键字
        :param path: 当前所在的路径
        :param path_list: 存放所有path的列表
        判断当前target类型：···是字典，循环内容，每个键值都记录下路径path，然后以当前值v为判断target，调用自身传入添加了的path判断
                             ···是列表，循环内容，每个元素都记录下路径path，然后以当前元素为判断target，调用自身传入添加了的path判断
                             ···是str或者int，那么就判断当前target是否就是要搜索的value，如果是，那就把路径path放进list里面"""
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1 = path1 + str([k])
                self.find_the_value(v, value, path1, path_list)

        else:
            if isinstance(target, (list, tuple)):
                for i in target:
                    path1 = copy.deepcopy(path)
                    posi = target.index(i)
                    path1 = path1 + '[%s]' % posi
                    self.find_the_value(i, value, path1, path_list)

            else:
                if isinstance(target, (str, int)) and str(value) == str(target):
                    path_list.append(path)

    def find_in_value(self, target, value, path='', path_list=None):
        """包含匹配，内容跟上面一样，只是最后判断时不同"""
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1 = path1 + str([k])
                self.find_in_value(v, value, path1, path_list)

        else:
            if isinstance(target, (list, tuple)):
                for i in target:
                    path1 = copy.deepcopy(path)
                    posi = target.index(i)
                    path1 = path1 + '[%s]' % posi
                    self.find_in_value(i, value, path1, path_list)

            else:
                if isinstance(target, (str, int)) and str(value) in str(target):
                    path_list.append(path)

    def find_the_key(self, target, key, path='', path_list=None):
        """查找key，每经过一层(list、dict)都会记录path，在字典时，若当前的k就是要找的key，那就把对应的path记录下来
                :param target: 被搜索的目标
                :param key: 要搜的键
                :param path: 当前所在的路径
                :param path_list: 存放所有path的列表
                判断当前target类型：···是字典，循环内容，每个键值都记录下路径path，判断当前k是否要查找的：~~~是，那就把路径path放进list里面
                                                                                                 ~~~不是，以当前值v为判断target，调用自身传入添加了的path判断
                                  ···是列表，循环内容，每个元素都记录下路径path，然后以当前元素为判断target，调用自身传入添加了的path判断
                                     """
        if isinstance(target, dict):
            for k, v in target.items():
                path1 = copy.deepcopy(path)
                path1 = path1 + str([k])
                if str(key) == str(k):
                    path_list.append(path1)
                else:
                    self.find_the_key(v, key, path1, path_list)

        else:
            if isinstance(target, (list, tuple)):
                for i in target:
                    path1 = copy.deepcopy(path)
                    posi = target.index(i)
                    path1 = path1 + '[%s]' % posi
                    self.find_the_key(i, key, path1, path_list)

    def in_value_path(self, value):
        """包含匹配value"""
        path_list = []
        self.find_in_value((self.target), value, path_list=path_list)
        return path_list

    def the_value_path(self, value):
        """完全匹配value"""
        path_list = []
        self.find_the_value((self.target), value, path_list=path_list)
        return path_list

    def the_key_path(self, value):
        """只查找key"""
        path_list = []
        self.find_the_key((self.target), value, path_list=path_list)
        return path_list


def getvalues(dic, result):
    """
    【功能】根据传入的字典类型参数，获取其每个键值对的值
    【参数】dic:传入的字典类型参数
            result:列表类型，存在dic中的每个键值对的值
    """
    count = 0
    keys = dic.keys()
    for key in keys:
        value = dic.get(key)
        if isinstance(value, dict):
            getvalues(value, result)
        elif isinstance(value, list):
            for ls in value:
                if isinstance(ls, dict):
                    getvalues(ls, result)
                else:
                    result.append(value)

        else:
            result.append(value)
    else:
        return result


def all_list(arr):
    """
    【功能】去除列表中的重复值
    【参数】arr:列表类型
    【结果】返回不含重复值的列表
    """
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    else:
        return result


def resetpathindex(lst):
    """
    【功能】将一个字典路径中包含的数组下标进行重置
    【参数】lst:期望被重置的字典路径数组
    【结果】被重置后的字典路径  例如：["['result'][2]['orgCodeList'][3]", "['result'][2]['orgCodeList'][3]","['result']['companies'][3]['orgCode']", "['result']['ownOrgCode']"]
            重置后为：["['result'][0]['orgCodeList'][0]", "['result'][1]['orgCodeList'][1]", "['result']['companies'][0]['orgCode']", "['result']['ownOrgCode']"]
    """
    for i in range(len(lst)):
        ls = re.findall('\\[+\\d+\\]+', str(lst[i]))
        for j in range(len(ls)):
            lst[i] = lst[i].replace(ls[j], '[]')
        else:
            list_count = Counter(lst)
            for key in list_count:
                index = 0

        if list_count[key] > 1:
            for k in range(len(lst)):
                if lst[k] == key:
                    lst[k] = lst[k].replace('[]', '[' + str(index) + ']')
                    index += 1
            else:
                index = 0

        else:
            if list_count[key] == 1:
                for k in range(len(lst)):
                    lst[k] = lst[k].replace('[]', '[' + str(index) + ']')
                else:
                    index = 0

            return lst