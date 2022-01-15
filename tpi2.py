#encoding: utf8
# Joao Santos 76912

from semantic_network import *
from bayes_net import *


class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        # IMPLEMENT HERE (if needed)
        pass

    def source_confidence(self,user):
        
        correct = 0
        wrong = 0
        data_dict = {}

        for declaration in self.declarations:
            # if declaration.user != user and isinstance(declaration.relation, AssocOne):
            if isinstance(declaration.relation, AssocOne):
                
                name = declaration.relation.name
                entity1 = declaration.relation.entity1
                entity2 = declaration.relation.entity2

                if entity1 not in data_dict:
                    data_dict[entity1] = {}

                if name not in data_dict[entity1]:
                    data_dict[entity1][name] = {}

                if entity2 in data_dict[entity1][name]:
                    data_dict[entity1][name][entity2] += 1
                else: 
                    data_dict[entity1][name][entity2] = 1

        for declaration in self.declarations:

            if declaration.user == user and isinstance(declaration.relation, AssocOne):
                name = declaration.relation.name
                entity1 = declaration.relation.entity1
                entity2 = declaration.relation.entity2

                if (entity1 in data_dict.keys()) and (name in data_dict[entity1].keys()):

                    data_point = data_dict[entity1][name]
                    max_count = max(data_point.values())
                    max_values = [k for k,v in data_point.items() if v == max_count]

                    if entity2 in max_values:
                        correct += 1
                    else:
                        wrong += 1
                        
                else:
                    correct += 1

        conf = (1-(0.75**correct))*(0.75**wrong)
        return conf

    def query_with_confidence(self, entity, assoc):

        # n = 0
        # T = 0
        # print('='*10)
        # print(f'entity {entity} | assoc {assoc}')


        # print(self.query(entity, assoc))
        
        # self.query_local(e1=entity, relname=assoc)
        # self.show_query_result()
        
        # print(len(self.query(entity)))
        # print('='*10)
        
        

        return None

    

    def query(self, entity, assoc=None):
        
        # TODO remove method
        queries_pred_b = [self.query(d.relation.entity2, assoc) for d in self.declarations if isinstance(d.relation, (Member, Subtype)) and d.relation.entity1 == entity]
        
        return [d for sublist in queries_pred_b for d in sublist] + self.query_local(e1=entity, relname=assoc)

    # def query_local(self,user=None,e1=None,rel=None,e2=None,rel_type=None):

    #     self.query_result = \
    #         [ d for d in self.declarations
    #             if  (user == None or d.user==user)
    #             and (e1 == None or d.relation.entity1 == e1)
    #             and (rel == None or d.relation.name == rel)
    #             and (rel_type == None or isinstance(d.relation,rel_type))]

    #     return self.query_result



class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # IMPLEMENT HERE (if needed)
        pass

    def individual_probabilities(self):
        # SOURCE: https://github.com/Rui-FMF/IA/blob/main/TPI2/tpi2.py

        res = {}

        variables = [k for k in self.dependencies.keys()]

        for v in variables:
            temp_vars = [k for k in self.dependencies.keys() if k != v]
            res[v] = sum([ self.jointProb([(v, True)] + conj) for conj in self._generate_conjunctions(temp_vars) ])
        
        return res

    def _generate_conjunctions(self, variaveis):
        # SOURCE: https://github.com/Rui-FMF/IA/blob/main/TPI2/tpi2.py

        if len(variaveis) == 1:
            return [ [(variaveis[0], True)] , [(variaveis[0], False)] ]

        l = []
        for c in self._generate_conjunctions(variaveis[1:]):
            l.append([(variaveis[0], True)] + c)
            l.append([(variaveis[0], False)] + c)

        return l


