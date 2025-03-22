"""
Author: Yuqian Lan (Yuqian_Lan_xjtu@stu.xjtu.edu.cn)

File: mind4things_memory.py
Description: Define memory modules that model cognition of things.
"""
import sys
sys.path.append('../../')

import json
import datetime


# <Mind4thingNode> 类，用于 创建和更新 单个 事物的心智建模
class Mind4thingNode:
    def __init__(self, name, state,
                 where, comment, notice,
                 function, material):
        # 基础属性
        self.name = name
        self.state = state
        self.where = where
        self.comment = comment
        self.notice = notice
        self.function = function
        self.material = material



# <Mind4thingsMemory> 类，用于 创建和更新 所有 事物的心智建模
class Mind4thingsMemory:
    def __init__(self, mind_saved):
        #self.mind4things = dict()

        self.mind4thingMemory = json.load(open(mind_saved + "/mind4things_memory.json"))    # 获取所有 事物 的相关信息
        self.nodelist = list(self.mind4thingMemory.keys())                                  # 获取所有 事物 的名字


    # 保存心智记忆
    def save(self, out_json):

        with open(out_json+"/mind4things_memory.json", "w") as outfile:
            json.dump(self.mind4thingMemory, outfile, indent=2)


    # 根据 事物名称 新增并初始化相关信息
    def create_mind4thing_byThingName(self, ThingName):

        if ThingName not in self.nodelist:
            self.mind4thingMemory[ThingName] = dict()
            self.mind4thingMemory[ThingName]["name"] = ThingName
            self.mind4thingMemory[ThingName]["state"] = None
            self.mind4thingMemory[ThingName]["where"] = None
            self.mind4thingMemory[ThingName]["comment"] = None
            self.mind4thingMemory[ThingName]["notice"] = None
            self.mind4thingMemory[ThingName]["function"] = None
            self.mind4thingMemory[ThingName]["material"] = None

            self.nodelist.append(ThingName)
            return True
        else:
            return False    # 如果该事物名称不在已有的节点列表中，则新增该事物的初始化信息，否则返回False以表示该智能体已经存在


    # 根据 事物名称 找到并获取相关信息
    def read_mind4thing_byThingName(self, ThingName):

        if ThingName in self.nodelist:
            thing_details = self.mind4thingMemory[ThingName]

            thing = Mind4thingNode(thing_details["name"], thing_details["state"],
                 thing_details["where"], thing_details["comment"], thing_details["notice"],
                 thing_details["function"], thing_details["material"])
            return thing
        else:
            return False    # 如果找到则返回查找到的 事物的心智，否则返回False以表示按照名字找不到相关心智记忆


    # 根据 事物名称、属性名称、属性值 找到并修改相关属性
    def update_mind4thing_byAttrName(self, ThingName, attrName, attrValue):

        if ThingName in self.nodelist:
            self.mind4thingMemory[ThingName][attrName] = attrValue
            return True
        else:
            return False    # 如果找到对应名字的事物和相关属性，则保存属性值，否则返回False以表示修改失败


    # 根据 事物名称 找到并删除
    def delete_mind4thing_byAttrName(self, ThingName):

        if ThingName in self.nodelist:
            del self.mind4thingMemory[ThingName]
            self.nodelist = [s for s in self.nodelist if s != ThingName]
            return True
        else:
            return False    # 如果找到对应名字的事物并删除，否则返回False以表示未找到该事物




