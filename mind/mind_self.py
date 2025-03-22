"""
Author:  Yuqian Lan (Yuqian_Lan_xjtu@stu.xjtu.edu.cn)

File: mind.py
Description: Functions and resources associated with the agent's mind.
1 def mind(persona, retrieved)
"""

#from persona.cognitive_modules.mind import *
from persona.cognitive_modules.mind4others_memory import *
from persona.cognitive_modules.mind4things_memory import *
from persona.cognitive_modules.mind4town_memory import *
from persona.prompt_template.run_gpt_prompt import *



def _filter_retrieved(persona, retrieved):


    copy_retrieved = retrieved.copy()
    for event_desc, eventItem in copy_retrieved.items():
        # 彻底删除原检索记忆中含有idle的项目，也可以理解为["curr_event"]中如果包含idle的项目（等价于event_desc中含有idle的项目）
        if "is idle" in event_desc or "sleeping" in event_desc or eventItem["curr_event"].poignancy < 7:
            del retrieved[event_desc]
            continue                                    # 由于彻底删除了这个字典，所以下面的过滤无法进行，跳过当前这一次的for循环

        # 删除["events"]中包含idle的项目
        for index, node in enumerate(eventItem["events"]):
            if "is idle" in node.description or "sleeping" in node.description or node.poignancy < 7:
                del retrieved[event_desc]["events"][index]

        # 删除["thoughts"]中包含idle的项目
        for index, node in enumerate(eventItem["thoughts"]):
            if "is idle" in node.description or "sleeping" in node.description or node.poignancy < 7:
                del retrieved[event_desc]["thoughts"][index]
    return retrieved


# 根据输入的 角色 和 事件列表，更新角色属性。
def mind(persona, retrieved):

    # 如果角色当前是系统初始化无动作，或有动作是在睡觉，则不进行心智更新
    if persona.scratch.act_description == None:
        return
    elif "sleeping" in persona.scratch.act_description:
        return


    # 第一步，获取角色的心智属性名称和值，每一个角色要进行更新的属性存在差异（即每个角色的 跟新列表updateList 不一定相同）。
    attrName_self = persona.scratch.updateList_mind4self_Event.copy()  # 对 自我心智 的建模属性
    attrValue_self = []
    for aN in persona.scratch.updateList_mind4self_Event: # 遍历每一个预定要更新的属性，如果按照这个属性名称存在，则加入到属性值列表中（顺序对应于属性名），否则删除该属性名
        if hasattr(persona.scratch, aN):
            attrValue_self.append(getattr(persona.scratch, aN))
        else:
            del attrName_self[aN]

    # 第二部，Retrieved 中可能包含多个事件。这里需要过滤掉一些事件。
    #         <focused_event> takes the form of a dictionary like this:
    #         dictionary {["curr_event"] = <ConceptNode>,
    #                     ["events"] = [<ConceptNode>, ...],
    #                     ["thoughts"] = [<ConceptNode>, ...]}
    if retrieved.keys():
        retrieved = _filter_retrieved(persona, retrieved)

    # 第三步，遍历每一个被检索的感知事件，基于 角色的心智属性，进行自我更新
    nodelist = []
    if retrieved is not None:
        for event_desc, eventItem in retrieved.items():     # 遍历感知事件
            nodelist.clear()
            nodelist.append(eventItem["curr_event"])
            nodelist.extend(eventItem["events"])
            nodelist.extend(eventItem["thoughts"])

            print('\n\n\n\n\n>>>>>>>>>  即将进行心智更新时，基于的内容节点个数是：', len(nodelist))
            print('\n\n')
            for node in nodelist:

                #for node in eventItem.items():
                type_target = "unknow"
                target = None
                # 如果感知事件类型是"event"
                if node.type == "event":
                    description = node.description + ' at ' + node.created.strftime("%B %d, %Y, %H:%M:%S")
                    attrName_thing = persona.scratch.updateList_mind4things_Event.copy()
                    attrName_town = persona.scratch.updateList_mind4maze_Event.copy()
                    target = node.object
                    thing = run_gpt_update_match_thing(description)
                    location = run_gpt_update_match_location(description)
                    type_target = "event"

                # 如果感知事件类型是"chat"
                elif node.type == "chat":
                    sessionContent = []
                    for utterance in node.filling:    # 将对话内容拼接，作为心智更新的基础
                        sessionContent.append(utterance[0] + ': ' + utterance[1])
                    description = node.created.strftime("%B %d, %Y, %H:%M:%S") + ':\n' + '\n'.join(sessionContent)

                    name_other = node.object          # 提取对话目标智能体的名字
                    attrName_other = persona.scratch.updateList_mind4others_Event.copy()  # 对 其他智能体心智 的建模属性
                    attrName_thing = persona.scratch.updateList_mind4things_Event.copy()
                    attrName_town = persona.scratch.updateList_mind4maze_Event.copy()
                    attrValue_other = []
                    #mindTarget = persona.mind_others.mind4otherMemory[name_other]
                    mindTarget = persona.mind_others.read_mind4other_byPersonaName(name_other)  # 获得目标智能体的心智
                    if mindTarget == False:                                                     # 如果是从来没有建立过的智能体的名字的心智，这里需要建立再获得
                        persona.mind_others.create_mind4other_byPersonaName(name_other)
                        mindTarget = persona.mind_others.read_mind4other_byPersonaName(name_other)

                    for aN in persona.scratch.updateList_mind4others_Event:  # 遍历每一个预定要更新的属性，如果按照这个属性名称存在，则加入到属性值列表中（顺序对应于属性名），否则删除该属性名
                        if hasattr(mindTarget, aN):
                            attrValue_other.append(getattr(mindTarget, aN))
                        else:
                            del attrName_other[aN]
                    
                    thing = run_gpt_update_match_thing(description)
                    location = run_gpt_update_match_location(description)
                    target = mindTarget
                    type_target = "other"

                # 如果感知事件类型是"thought"
                elif node.type == "thought":
                    description = node.description + ' at ' + node.created.strftime("%B %d, %Y, %H:%M:%S")
                    attrName_thing = persona.scratch.updateList_mind4things_Event.copy()
                    attrName_town = persona.scratch.updateList_mind4maze_Event.copy()
                    thing = run_gpt_update_match_thing(description)
                    location = run_gpt_update_match_location(description)
                    target = node.object
                    type_target = "thought"

                else:
                    break

                #************************************ 针对 自我 心智更新 ************************************#

                print('\n\n\n\n\n>>>>>>>>>  进行 自我 心智更新时，基于的内容是：\n', description)
                print('the type of target is: ', type_target)
                print('\n\n')

                # 对自我的心智更新
                flag_update_needs4self = False
                for i in range(len(attrName_self)):                  # 遍历心智属性
                    answear = run_gpt_update_mind4self_event(persona, node.object, description,
                                                                attrName_self[i], attrValue_self[i])
                    if answear != False:                                # 如果更新内容成功存在，则更新属性值。否则跨过当前属性并继续
                        new_attValue = answear[0]
                        print('\n\n...... attrName of self: ', attrName_self[i])
                        print('\n\n...old_attValue of self: ', attrValue_self[i])
                        print('\n\n...new_attValue of self: ', new_attValue)
                        setattr(persona.scratch, attrName_self[i], new_attValue)
                        flag_update_needs4self = True
                    else:
                        continue

                # 对自我的需求更新
                if flag_update_needs4self == True:
                    answear = run_gpt_update_needs4self_event(persona, node.object, description)

                    if answear != False:                            # 如果更新内容成功存在，则更新需求。否则不做任何处理
                        new_needs = answear[0]
                        print('\n\n......old_needs of self: ', persona.scratch.needs)
                        print('\n\n......new_needs of self: ', new_needs)
                        setattr(persona.scratch, "needs", new_needs)

                # ************************************ 针对 他人 心智更新 ************************************#

                if target != False:
                
                    print('\n\n\n\n\n>>>>>>>>>  进行 他人 心智更新时，基于的内容是：\n', description)
                    print('\n\n')

                    # 对他人的心智更新
                    flag_update_needs4other = False
                    for i in range(len(attrName_other)):  # 遍历心智属性
                        answear = run_gpt_update_mind4other_event(persona, target, description,
                                                                  attrName_other[i], attrValue_other[i])
                        if answear != False:  # 如果更新内容成功存在，则更新属性值。否则跨过当前属性并继续
                            new_attValue = answear[0]
                            print('\n\n++++++ attrName of other: ', attrName_other[i])
                            print('\n\n+++old_attValue of other: ', attrValue_other[i])
                            print('\n\n+++new_attValue of other: ', new_attValue)
                            setattr(persona.mind_others.mind4otherMemory[target], attrName_other[i], new_attValue)
                            flag_update_needs4other = True
                        else:
                            continue


                    # 对他人的需求更新
                    if flag_update_needs4other == True:
                        answear = run_gpt_update_needs4other_event(persona, target, description)

                        if answear != False:  # 如果更新内容成功存在，则更新需求。否则不做任何处理
                            new_needs = answear[0]
                            print('\n\n++++++old_needs of other: ', persona.scratch.needs)
                            print('\n\n++++++new_needs of other: ', new_needs)
                            setattr(persona.scratch, "needs", new_needs)



                # ************************************ 针对 事物 心智更新 ************************************#
                
                if thing != False:
                
                    print('\n\n\n\n\n>>>>>>>>>  进行 事物 心智更新时，基于的内容是：\n', description)
                    print('\n\n')
                    
                    # 对事物的心智更新
                    for i in range(len(attrName_thing)):  # 遍历心智属性
                        answear = run_gpt_update_mind4thing_event(persona, thing, description, attrName_thing[i])
                        if answear != False:  # 如果更新内容成功存在，则更新属性值。否则跨过当前属性并继续
                            new_attValue = answear[0]
                            print('\n\n++++++ attrName of thing: ', attrName_other[i])
                            print('\n\n+++new_attValue of thing: ', new_attValue)
                            setattr(persona.mind_things.mind4thingMemory[thing], attrName_other[i], new_attValue)
                        else:
                            continue

                # ************************************ 针对 地图 心智更新 ************************************#
                
                if location != False:
                
                    print('\n\n\n\n\n>>>>>>>>>  进行 地点 心智更新时，基于的内容是：\n', description)
                    print('\n\n')
                    
                    # 对地点的心智更新
                    for i in range(len(attrName_town)):  # 遍历心智属性
                        answear = run_gpt_update_mind4town_event(persona, location, description, attrName_town[i])
                        if answear != False:  # 如果更新内容成功存在，则更新属性值。否则跨过当前属性并继续
                            new_attValue = answear[0]
                            print('\n\n++++++ attrName of town: ', attrName_other[i])
                            print('\n\n+++new_attValue of town: ', new_attValue)
                            setattr(persona.mind_town.mind4townMemory[location], attrName_other[i], new_attValue)
                        else:
                            continue
                
                
                
                
