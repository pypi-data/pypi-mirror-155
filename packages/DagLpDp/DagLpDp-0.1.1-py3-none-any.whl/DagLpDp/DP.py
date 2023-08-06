# -*- coding: utf-8 -*-
class DAGLP:
    def __init__(self,graph):
        self.graph = graph #{(from_node,to_node):value,...}
        self.starts = set()
        self.ends = set()
        self.from_nodes={} # from_node as key
        self.to_nodes={} # to_node as key
        self.nodePV={} # node:{path,value}        
        for edge,value in self.graph.items():
            self.starts.add(edge[0])
            self.ends.add(edge[1])
            parent = self.to_nodes.get(edge[1],None)
            if parent is None:
                parent = set()
            parent.add(edge[0])
            self.to_nodes[edge[1]] = parent            
        for edge,value in self.graph.items():
            self.starts.discard(edge[1])
            self.ends.discard(edge[0])
            child = self.from_nodes.get(edge[0],None)
            if child is None:
                child = set()
            child.add(edge[1])
            self.from_nodes[edge[0]] = child
        for i in self.starts:
            self.nodePV[i]=([i],0)            
        self.calcLP()        
    def calcLP(self):
        copystarts = self.starts.copy()
        while len(copystarts)>0:
            start = copystarts.pop()
            spv = self.nodePV[start]
            if start in self.ends:
                continue
            for child in self.from_nodes[start]:
                self.to_nodes[child].discard(start)
                if len(self.to_nodes[child])==0:
                    copystarts.add(child)
                cpv = self.nodePV.get(child,None) 
                ev = self.graph[(start,child)] # edge value
                if (cpv is not None) and (cpv[1] > ev + spv[1]):
                    continue
                self.nodePV[child]=(spv[0]+[child],ev + spv[1])