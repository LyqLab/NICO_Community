"""
Author: Yuqian Lan (Yuqian_Lan_xjtu@stu.xjtu.edu.cn)

File: mind4others_memory.py
Description: Define memory modules that model other people's minds.
"""
import sys
sys.path.append('../../')

import json
import datetime


# <Mind4otherNode> 类，用于 创建和更新 单个 其他智能体的心智建模
class Mind4otherNode:
    def __init__(self, name, nickname,
                 learned, skills, education,
                 innate, likes, hates,
                 interpersonal, family,
                 currently, lifestyle,
                 needs, belongings, financial,
                 position):
        # 基础一阶心智理解（我 认为 其他智能体 ...）
        self.name = name
        self.nickname = nickname
        self.learned = learned
        self.skills = skills
        self.education = education
        self.innate = innate
        self.likes = likes
        self.hates = hates
        self.interpersonal = interpersonal
        self.family = family
        self.currently = currently
        self.lifestyle = lifestyle
        self.needs = needs
        self.belongings = belongings
        self.financial = financial
        self.position = position




# <Mind4othersMemory> 类，用于 创建和更新 所有 其他智能体的心智建模
class Mind4othersMemory:
    def __init__(self, mind_saved):
        #self.mind4others = dict()

        self.mind4otherMemory = json.load(open(mind_saved + "/mind4others_memory.json"))    # 获取所有 其他智能体 的相关信息
        self.nodelist = list(self.mind4otherMemory.keys())                                  # 获取所有 其他智能体 的名字


    # 保存心智记忆
    def save(self, out_json):

        with open(out_json+"/mind4others_memory.json", "w") as outfile:
            json.dump(self.mind4otherMemory, outfile, indent=2)


    # 根据 智能体名称 新增并初始化相关信息
    def create_mind4other_byPersonaName(self, personaName):

        if personaName not in self.nodelist:
            self.mind4otherMemory[personaName] = dict()
            self.mind4otherMemory[personaName]["name"] = personaName
            self.mind4otherMemory[personaName]["nickname"] = None
            self.mind4otherMemory[personaName]["learned"] = None
            self.mind4otherMemory[personaName]["skills"] = None
            self.mind4otherMemory[personaName]["education"] = None
            self.mind4otherMemory[personaName]["innate"] = None
            self.mind4otherMemory[personaName]["likes"] = None
            self.mind4otherMemory[personaName]["hates"] = None
            self.mind4otherMemory[personaName]["interpersonal"] = None
            self.mind4otherMemory[personaName]["family"] = None
            self.mind4otherMemory[personaName]["currently"] = None
            self.mind4otherMemory[personaName]["lifestyle"] = None
            self.mind4otherMemory[personaName]["needs"] = None
            self.mind4otherMemory[personaName]["belongings"] = None
            self.mind4otherMemory[personaName]["financial"] = None
            self.mind4otherMemory[personaName]["position"] = None

            self.nodelist.append(personaName)
            return True
        else:
            return False    # 如果该智能体名称不在已有的节点列表中，则新增该智能体的初始化信息，否则返回False以表示该智能体已经存在


    # 根据 智能体名称 找到并获取相关信息
    def read_mind4other_byPersonaName(self, personaName):

        if personaName in self.nodelist:
            agent_details = self.mind4otherMemory[personaName]

            agent = Mind4otherNode(agent_details["name"], agent_details["nickname"],
                 agent_details["learned"], agent_details["skills"], agent_details["education"],
                 agent_details["innate"], agent_details["likes"], agent_details["hates"],
                 agent_details["interpersonal"], agent_details["family"],
                 agent_details["currently"], agent_details["lifestyle"],
                 agent_details["needs"], agent_details["belongings"], agent_details["financial"],
                 agent_details["position"])
            return agent
        else:
            return False    # 如果找到则返回查找到的 智能体心智，否则返回False以表示按照名字找不到相关心智记忆


    # 根据 智能体名称、属性名称、属性值 找到并修改相关属性
    def update_mind4other_byAttrName(self, personaName, attrName, attrValue):

        if personaName in self.nodelist:
            self.mind4otherMemory[personaName][attrName] = attrValue
            return True
        else:
            return False    # 如果找到对应名字的智能体和相关属性，则保存属性值，否则返回False以表示修改失败


    # 根据 智能体名称 找到并删除
    def delete_mind4other_byAttrName(self, personaName):

        if personaName in self.nodelist:
            del self.mind4otherMemory[personaName]
            self.nodelist = [s for s in self.nodelist if s != personaName]
            return True
        else:
            return False    # 如果找到对应名字的智能体并删除，否则返回False以表示未找到该智能体




if __name__ == "__main__":
    # 进行测试，读取文件
    path = "..."
    memory = Mind4othersMemory(path)
    print('the primary list of nodes is: ', memory.nodelist)
    #agent = memory.mind4otherMemory["Maria Lopez"]
    #print(list(agent.keys()))


    # 新增实验
    flag_create = memory.create_mind4other_byPersonaName("Anne Hathaway")
    if flag_create == True:
        print('\nthe create is done...')
        print('the new list of nodes is: ', memory.nodelist)
    else:
        print('\nthe create can not finish for the name is exist...')

    # 删除实验
    flag_delete = memory.delete_mind4other_byAttrName("Isabella Rodriguez")
    if flag_delete == True:
        print('\nthe delete is done...')
        print('the new list of nodes is: ', memory.nodelist)
    else:
        print('\nthe delete can not finish for the name is not exist...')

    # 修改实验
    flag_update = memory.update_mind4other_byAttrName("Anne Hathaway", "likes", "sports, movie")
    if flag_update == True:
        print('\nthe update is done...')
    else:
        print('\nthe update can not finish for the name is not exist...')

    # 查找实验
    agent = memory.read_mind4other_byPersonaName("Anne Hathaway")
    name = "Anne Hathaway"
    if agent != False:
        print('\nthe read is done...')
        print(f'\nthe attr #likes# of {name} is: ', agent.likes)
    else:
        print('\nthe update can not finish for the name is not exist...')

    # 保存记忆
    #memory.save(path)
