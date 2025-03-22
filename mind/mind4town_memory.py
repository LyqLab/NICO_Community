"""
Author: Yuqian Lan (Yuqian_Lan_xjtu@stu.xjtu.edu.cn)

File: mind4Towns_memory.py
Description: Define memory modules that model cognition of location in the Town.
"""
import sys
sys.path.append('../../')

import json
import datetime


# <Mind4TownNode> 类，用于 创建和更新 单个 地点的心智建模
class Mind4TownNode:
    def __init__(self, what, who, notice, related):
        # 基础属性
        self.name = name
        self.what = what
        self.who = who
        self.notice = notice
        self.related = related



# <Mind4TownsMemory> 类，用于 创建和更新 所有 地点的心智建模
class Mind4TownsMemory:
    def __init__(self, mind_saved):
        #self.mind4Towns = dict()

        self.mind4TownMemory = json.load(open(mind_saved + "/mind4Towns_memory.json"))    # 获取所有 地点 的相关信息
        self.nodelist = list(self.mind4TownMemory.keys())                                  # 获取所有 地点 的名字


    # 保存心智记忆
    def save(self, out_json):

        with open(out_json+"/mind4Towns_memory.json", "w") as outfile:
            json.dump(self.mind4TownMemory, outfile, indent=2)


    # 根据 地点名称 新增并初始化相关信息
    def create_mind4Town_byLocationName(self, LocationName):

        if LocationName not in self.nodelist:
            self.mind4TownMemory[LocationName] = dict()
            self.mind4TownMemory[LocationName]["name"] = LocationName
            self.mind4TownMemory[LocationName]["what is main business"] = None
            self.mind4TownMemory[LocationName]["who worked there"] = None
            self.mind4TownMemory[LocationName]["notice"] = None
            self.mind4TownMemory[LocationName]["related information"] = None

            self.nodelist.append(LocationName)
            return True
        else:
            return False    # 如果该地点名称不在已有的节点列表中，则新增该地点的初始化信息，否则返回False以表示该智能体已经存在


    # 根据 地点名称 找到并获取相关信息
    def read_mind4Town_byLocationName(self, LocationName):

        if LocationName in self.nodelist:
            Location_details = self.mind4TownMemory[LocationName]

            Town = Mind4TownNode(Location_details["name"], Location_details["what is main business"],
                 Location_details["who worked there"], Location_details["notice"],
                 Location_details["related information"])
            return Town
        else:
            return False    # 如果找到则返回查找到的 地点的心智，否则返回False以表示按照名字找不到相关心智记忆


    # 根据 地点名称、属性名称、属性值 找到并修改相关属性
    def update_mind4Town_byAttrName(self, LocationName, attrName, attrValue):

        if LocationName in self.nodelist:
            self.mind4TownMemory[LocationName][attrName] = attrValue
            return True
        else:
            return False    # 如果找到对应名字的地点和相关属性，则保存属性值，否则返回False以表示修改失败


    # 根据 地点名称 找到并删除
    def delete_mind4Town_byAttrName(self, LocationName):

        if LocationName in self.nodelist:
            del self.mind4TownMemory[LocationName]
            self.nodelist = [s for s in self.nodelist if s != LocationName]
            return True
        else:
            return False    # 如果找到对应名字的地点并删除，否则返回False以表示未找到该地点




