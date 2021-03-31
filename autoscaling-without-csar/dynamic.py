
import copy
import sys
from ruamel.yaml import YAML
import os
import json
from pathlib import Path
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.compat import ordereddict
from collections import OrderedDict

def run(c):
    if c:
        next_node = check_host(c)
        nodesToChange[c]= ''

        if next_node not in nodesToChange:
           run(next_node)
        findNodesToChange(c)


def findNodesToChange(c):
      for node in yamlToDict["topology_template"]["node_templates"]:
        i = check_host(node)
        if i == c:
          if node not in nodesToChange:
            run(node)

def update_dy2(v,var):
    var = str(var)
    node_to_change = v.replace("xx",var)
    original_node = v


    newNode = copy.deepcopy(yamlToDict["topology_template"]["node_templates"][original_node])

    if 'requirements' in newNode.keys():
        for i in newNode['requirements']:
            if 'host' in i.keys():
                i['host'] = i['host'].replace("xx",var)
    if 'properties' in newNode.keys():
        if 'name' in newNode['properties'].keys():
            newNode['properties']['name']=newNode['properties']['name'].replace("xx",var)

#    cntnt["topology_template"]["node_templates"][node_to_change] = newNode
#    print(newNode)
    return node_to_change, newNode

   # print(cntnt["topology_template"]["node_templates"])
   # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")



def update_dy(v,var):
    var = str(var)
    node_to_change = v.replace("xx",var)
    original_node = v
    yamlToDict["topology_template"]["node_templates"][node_to_change] = copy.deepcopy(yamlToDict["topology_template"]["node_templates"][original_node])
    if 'requirements' in yamlToDict["topology_template"]["node_templates"][node_to_change].keys():
        for i in yamlToDict["topology_template"]["node_templates"][node_to_change]['requirements']:
            if 'host' in i.keys():
                i['host'] = i['host'].replace("xx",var)
    if 'properties' in yamlToDict["topology_template"]["node_templates"][node_to_change].keys():
        if 'name' in yamlToDict["topology_template"]["node_templates"][node_to_change]['properties'].keys():
            yamlToDict["topology_template"]["node_templates"][node_to_change]['properties']['name']=yamlToDict["topology_template"]["node_templates"][node_to_change]['properties']['name'].replace("xx", var)
    print(yamlToDict["topology_template"]["node_templates"])
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")






def check_host(k):
    node = k
    nodes = yamlToDict["topology_template"]["node_templates"][node]
    if 'requirements' in nodes.keys():
        for requirement in nodes['requirements']:
            if 'host' in requirement.keys():
                host_i = requirement['host']
                return host_i



if __name__ == "__main__":

    serviceFile = open(sys.argv[1], 'r')
    nodeToScale = sys.argv[2] + '_xx'

    yaml = YAML(typ='safe')
    yaml.default_flow_style = False
    yaml.sort_base_mapping_type_on_output = False


    yamlToDict = yaml.load(serviceFile)
    checkPoint = yamlToDict

# Check the latest number of scalable instance and get  the num from the json file
    dataFile = Path("data.json")
    if dataFile.is_file():
        data_file = open('data.json','r+')
        data =json.load(data_file)
        var = data['scale_index']+1
    else:
        nodeToWrite = {'scale_index' : 0}
        with open('data.json','w') as writeFile:
            json.dump(nodeToWrite, writeFile)
        data = nodeToWrite
        var = data['scale_index'] + 1


    list_node = []
    list_prop = []
    nodesToChange = {}
    run(nodeToScale)
    dict_res = {}

    for scalable_nodes in nodesToChange.keys():
        newNode, newNode_properties = update_dy2(scalable_nodes,var)
        list_prop.append(newNode_properties)
        list_node.append(newNode)
    dict_res = dict(zip(list_node,list_prop))

    tmp = yamlToDict["topology_template"]["node_templates"]


    yamlToDict["topology_template"]["node_templates"] = {}
    checkPoint["topology_template"]["node_templates"] = {}


    checkPoint["topology_template"]["node_templates"].update(dict_res)
    with open('checkPoint_'+str(var) +'.yaml','w') as yamlfile:
        yaml.dump(checkPoint, yamlfile)



    dict_res.update(tmp)
    yamlToDict["topology_template"]["node_templates"].update(dict_res)

    #Save the num to a json file.

    data['scale_index'] = var
    with open('data.json','w') as writeFile:
        json.dump(data, writeFile)

    with open('service.yaml','w') as yamlfile:
        yaml.dump(yamlToDict, yamlfile)

    serviceFile.close()



