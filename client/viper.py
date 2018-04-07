import networkx as nx
from networkx_viewer import Viewer
import pickle
import requests
import urllib.parse
import pylab as plt
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz


class Task(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.downstream = ()

    def __lshift__(self, other):
        self._shift(other, self)
        return other

    def __rshift__(self, other):
        self._shift(self, other)
        return other

    @staticmethod
    def _shift(thing1, thing2):
        thing1.downstream = thing1.downstream + (thing2,)

    def make_graph(self, graph=None):
        # node = self.gen_hashable()
        if not graph:
            graph = nx.DiGraph()
        graph.add_node(self)
        for node in self.downstream:
            node.make_graph(graph)
            graph.add_edge(self, node)
        return graph

    def gen_hashable(self):
        hashable_task = self.__class__(self.name, self.func)
        hashable_task.downstream = None
        return hashable_task

    def render_graph(self):
        G = self.make_graph()
        layout = graphviz_layout(G)
        nx.draw(G, pos=layout, node_size=1600,
                node_color=range(len(G)),
                prog='dot')
        nx.draw_networkx_labels(G, layout, {x: x.name for x in G.nodes()})
        plt.show()
        # Viewer(self.make_graph()).mainloop()

    def run(self, host, args, kwargs):
        graph = self.make_graph()
        dump = pickle.dumps((graph, args, kwargs), -1)
        requests.post(urllib.parse.urljoin("http://" + host, "/endpoint.html"),
                      data=dump)


if __name__ == "__main__":
    task1 = Task("task1", lambda x: print("HELLO1"))
    task2 = Task("task2", lambda x: print("HELLO2"))
    task3 = Task("task3", lambda x: print("HELLO3"))
    task4 = Task("task4", lambda x: print("HELLO4"))

    task1 >> task2 >> task3 << task4 << task1
    #import IPython;IPython.embed()
    task1.render_graph()
