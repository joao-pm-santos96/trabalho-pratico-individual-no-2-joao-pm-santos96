#encoding: utf8
# Joao Santos 76912

from semantic_network import *
from bayes_net import *


class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        # IMPLEMENT HERE (if needed)

        self.inherited = None
        self.local = None

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

        conf = lambda n,T : (n/(2*T)) + (1-(n/(2*T))) * (1 - 0.95**n) * (0.95) ** (T-n)

        local = [d for d in self.declarations if d.relation.entity1 == entity and isinstance(d.relation, AssocOne) and (assoc == None or d.relation.name == assoc)]

        inherited = [self.query_with_confidence(d.relation.entity2, assoc) for d in self.declarations if d.relation.entity1 == entity and isinstance(d.relation, (Member, Subtype))]

        local_dict = {}
        for d in local:
            e2 = d.relation.entity2 

            if e2 not in local_dict.keys():
                local_dict[e2] = 1
            else:
                local_dict[e2] += 1

        T = sum(local_dict.values())

        for k,v in local_dict.items():
            local_dict[k] = conf(v,T)

        
        # print([item for sublist in inherited for item in sublist])   
        # 

        inherited_dict = {}
        for p in inherited:
            for k,v in p.items():
                if k in inherited_dict:
                    inherited_dict[k] += v
                else:
                    inherited_dict[k] = v    

        n_parents = len(inherited)
        for k,v in inherited_dict.items():
            inherited_dict[k] = v / (n_parents if n_parents > 0 else 1) * 0.9 

        inherited = [a for a in inherited if bool(a)]

        if len(inherited) == 0: # do nothing
            return local_dict

        elif len(local) == 0: # discount 10%
            return inherited_dict

        else:
            common_dict = {}

            for k in local_dict.keys():
                common_dict[k] = None

            for k in inherited_dict.keys():
                common_dict[k] = None

            for k in common_dict.keys():

                if k in local_dict.keys() and k in inherited_dict.keys():
                    common_dict[k] = local_dict[k] * 0.9 + inherited_dict[k] * 0.1

                elif k in local_dict.keys():
                    common_dict[k] = local_dict[k] * 0.9

                elif k in inherited_dict.keys():
                    common_dict[k] = inherited_dict[k] * 0.1

            return common_dict

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


