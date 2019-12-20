# @author: 1173710217_侯鹏钰, 1173710132_牟虹霖 , 1173300919_史纪元
# @time:2019/12/19

from copy import copy

class Node(object):
    def __init__(self, name):
        '''
        初始化函数
            name: 节点名称
            fathers：父节点列表
            CPT：该节点的CPT表
                CPT表存储格式为:{
                    ((self.name, 'true/false'), (farher1, 'true/false'), ...): probality,
                    ...
                }
        '''
        self.name = name
        self.fathers = []
        self.CPT = {}

    def add_father(self, father):
        '''
        添加父节点
            注：这里添加的父节点是有顺序的，在之后计算 P((self.name, 'true/false)|(father1.name, 'true/false)...)概率的时候
            父节点的顺序是按照这里父节点列表的顺序的，否则在CPT表中索引不到
        '''
        self.fathers.append(father)
    
    # 将所有（可以不包含在这个节点父节点列表中的节点）而且可以无序的(node.name ,val)节点作为输入
    def self_parents_multi(self, node_val_tuple_list):
        '''
        计算 P((self.name, 'true/false)|parent(self.name))
            node_val_tuple_list: 是 **所有节点** 的 (节点,值) 列表
            注：参数的节点——值对列表是可无固定顺序的，因为会按照父节点列表的顺序取父节点，查找得到对应值，组成((节点，值),...)作为CPT的键进行索引
        '''
        _ , self_val = Node.search_node(node_val_tuple_list, self.name)
        # 如果父节点数量为0。可直接返回对应True or False的概率
        if len(self.fathers) == 0:
            # 注意这里必须为tuple([(self.name, self_val)])因为这样才会把单独的元组转换为列表再转换为元组
            # 如果不采取这种方式，那么索引的键会是((self.name, self_val))，但是索引的键应当是((self.name. self_val),)
            return self.CPT[tuple([(self.name, self_val)])]

        # 节点数量不为0，先按名称的字典序过滤出
        temp_lst = [(self.name, self_val)]
        for father in self.fathers:
            father, val = Node.search_node(node_val_tuple_list, father)
            temp_lst.append((father, val))
        return self.CPT[tuple(temp_lst)]

    @staticmethod
    def search_node(node_val_tuple_list, name):
        '''
        从节点——值对来索引name节点对应的值("true/false")
        参数是
            node_val_tuple_list:[(node, val(ture or false)), ...]
            name:要查找的节点名字
        '''
        for (node, val) in node_val_tuple_list:
            if node == name:
                return (node, val)


class Bayes_Net(object):
    '''
    贝叶斯网络
    '''
    def __init__(self, file):
        '''
        初始化，构建贝叶斯网络
        '''
        with open(file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            lines = [line for line in lines if line != '']
        
        # 解析节点个数
        self.num_nodes = int(lines[0])

        # 解析各个节点名称并添加至节点列表
        self.nodes = []
        names = lines[1].split()
        assert len(names) == self.num_nodes
        for name in names:
            self.nodes.append(Node(name))
        del names

        # 解析节点网络
        line_index = 2
        for i in range(self.num_nodes):
            for j, val in enumerate(lines[line_index].split()):
                if val == '1':
                    self.nodes[j].add_father(self.nodes[i].name)
            line_index += 1

        # 解析CPT表
        for node in self.nodes:
            # print(node.name)
            father_num = len(node.fathers)
            # print(father_num)
            line_num = 2 ** father_num
            # print(line_num)
            for i in range(0, line_num):
                # print(line_index + i)
                b_str = bin(i).replace('0b','')
                tmp_b_lst = list(b_str)
                while len(tmp_b_lst) < father_num:
                    tmp_b_lst.insert(0, '0')
                b_str = ''.join(tmp_b_lst)
                tmp_lst = []
                for j, father in enumerate(node.fathers):
                    if b_str[j] == '0':
                        tmp_lst.append((father, 'false'))
                    else:
                        tmp_lst.append((father, 'true'))
                f_tmp_lst = copy(tmp_lst)
                tmp_lst.insert(0, (node.name, 'true'))
                f_tmp_lst.insert(0, (node.name, 'false'))
                node.CPT[tuple(tmp_lst)] = float(lines[line_index + i].split()[0])
                node.CPT[tuple(f_tmp_lst)] = float(lines[line_index + i].split()[1])
            line_index += line_num
        
        # debug: 输出所有节点的父节点及CPT表
        # for node in self.nodes:
        #     print(node.name)
        #     print(node.fathers)
        #     for key, value in node.CPT.items():
        #         print(key,'   ',value)
        #     print()


    def _parse_query(self, query_file):
        '''
        解析query文件，获得queries
            queries格式为((node1, 'true/false'), (node2, 'true/false'), ...)，其中元组的第一项为非条件部分的节点，剩余部分为条件部分的节点
        '''
        with open(query_file, 'r') as f:
            lines = f.readlines()
        queries = []
        for line in lines:
            line = line.strip().replace('P(', '')
            line = line.replace(')', '')
            line = line.replace('|', '')
            line = line.replace(',', ' ')
            line = line.split()
            if not len(line):
                continue
            q1 = []
            q2 = []
            q1.append((line[0],'false'))
            q2.append((line[0],'true'))
            for i in range(1, len(line)):
                tmp = line[i].split('=')
                q1.append((tmp[0],tmp[1]))
                q2.append((tmp[0],tmp[1]))
            queries.append(tuple(q1))
            queries.append(tuple(q2))
        return queries

    def compute_queries(self, query_file):
        '''
        计算query_file中所有query对应的值
        '''
        queries = self._parse_query(query_file)
        for query in queries:
            print(query, str(self._compute_one(query)))

    
    def _compute_one(self, query):
        '''
        计算单个query，计算方法为通过贝叶斯公式将条件概率转换为联合概率的除法，然后调用计算联合概率的方法求解
        '''
        if len(query) == 1:
            return self._compute_lack(list(query))
        query = list(query)
        return self._compute_lack(query) / self._compute_lack(query[1:])
        
    
    def _compute_lack(self, node_val_tuple_list):
        '''
        计算联合概率，扩展为所有节点全联合概率的和
        '''
        lack_nodes = [node.name for node in self.nodes if (node.name, 'true') \
             not in node_val_tuple_list and (node.name, 'false') \
                  not in node_val_tuple_list]
        result = []
        result.append(node_val_tuple_list)
        tmp_len = len(result)

        for node in lack_nodes:
            while tmp_len > 0:
                tmp_len -= 1
                a_tmp = copy(result.pop(0))
                b_tmp = copy(a_tmp)
                a_tmp.append((node, 'true'))
                b_tmp.append((node, 'false'))
                result.append(a_tmp)
                result.append(b_tmp)
            tmp_len = len(result)
        assert len(result) == (2 ** len(lack_nodes))
        return sum([self._compute_filled(tmp) for tmp in result])
    
    def _compute_filled(self, node_val_tuple_list):
        '''
        计算所有节点全联合概率，利用公式P(x1, x2, x3, ... ,xn) = ∏(i:1->n)P(xi|Parent(xi))
        '''
        value = 1.0
        for node_name, val in node_val_tuple_list:
            node = self._search_node_by_name(node_name)
            tmp = node.self_parents_multi(node_val_tuple_list)
            value = value * tmp
        return value
            
    def _search_node_by_name(self, node_name):
        '''
        通过节点名称查找节点
        '''
        for node in self.nodes:
            if node.name == node_name:
                return node

if __name__ == '__main__':
    network_file = './lab3/carnetwork.txt'
    query_file = './lab3/carqueries.txt'
    b = Bayes_Net(network_file)
    b.compute_queries(query_file)

    # a = (('a','true'), ('b','false'))
    # a = list(a)
    # print(a)
    # print(len(a))