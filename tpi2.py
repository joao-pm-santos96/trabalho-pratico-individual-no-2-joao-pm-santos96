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
        # IMPLEMENT HERE
        
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

                    if entity2 in [k for k,v in data_point.items() if v == max_count]:
                        correct += 1
                    else:
                        wrong += 1
                        
                else:
                    correct += 1

        conf = (1-(0.75**correct))*(0.75**wrong)
        return conf

    def query_with_confidence(self,entity,assoc):
        # IMPLEMENT HERE
        pass



class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # IMPLEMENT HERE (if needed)
        pass

    def individual_probabilities(self):
        # IMPLEMENT HERE
        pass


