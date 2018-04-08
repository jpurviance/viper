import networkx as nx
import cloudpickle as pickle
import requests
import urllib.parse
from networkx.drawing.nx_agraph import graphviz_layout
import json
import time

from common import executor


class Task(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.downstream = ()
        self.result = None
        self.job_id = None
        self.total_time = None

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
        #plt.show()
        # Viewer(self.make_graph()).mainloop()

    def run(self, host, args, kwargs):
        graph = self.make_graph()
        dump = pickle.dumps((graph, args, kwargs), -1)
        r = requests.post(urllib.parse.urljoin("http://" + host, "/submit"),
                      data=dump)
        return r.content

    def run_debug(self, args=None, kwargs=None):
        graph = self.make_graph()
        return executor.execute(graph, args, kwargs)


def func(number=None, *args, **kwargs):
    time.sleep(2)
    return {"number": number + 1}


def get_job_status(host, job_id):
    r = requests.post(urllib.parse.urljoin("http://" + host, "/job_status"),
                      data={"job_id": job_id})
    return r.content


def get_job_results(host, job_id):
    r = requests.post(urllib.parse.urljoin("http://" + host, "/job_results"),
                      data={"job_id": job_id})
    return pickle.loads(r.content)


if __name__ == "__main__":
    task1 = Task("task1", func)
    task2 = Task("task2", func)
    task3 = Task("task3", func)
    task4 = Task("task4", func)

    task1 >> task2 >> task3 << task4 << task1
    # import IPython;IPython.embed()
    job_id = task1.run("localhost:8000", None, {"number": 0})
    while True:
        job_status = get_job_status("localhost:8000", job_id)
        print(job_status.decode('ascii'))
        if all(x['status'] == "completed" for x in json.loads(job_status)):
            break
        time.sleep(1)




    # task1.render_graph()
