import json
from common.utils import merge_dicts


class Executor(object):
    def __init__(self, graph, args=None, kwargs=None, job_id=None):
        self.graph = graph
        self.unsatisfied = list(graph.nodes())
        self.completed = []
        self.args = args
        self.kwargs = kwargs
        self.job_id = job_id

    def step(self, update_dict):
        self.update_results(update_dict)
        satisfied = [node for node in self.unsatisfied
                     if all(x in self.completed for x in self.graph.predecessors(node))]
        self.unsatisfied = [x for x in self.unsatisfied if x not in satisfied]
        for node in satisfied:
            preds = self.graph.predecessors(node)
            node_kwargs = merge_dicts(*([pred.result for pred in preds] + [self.kwargs]))
            node.job_id = self.job_id
            yield (node, node_kwargs)
        self.completed.extend(satisfied)

    def get_results(self):
        return {x.name: x.result for x in self.graph.nodes()
                if len(list(self.graph.successors(x))) == 0}

    def update_results(self, node):
        for item in self.completed:
            if item.name == node.name:
                item.result = node.result
                item.total_time = node.total_time

    def get_status(self):
        res = []
        for item in list(self.graph.nodes()):
            if item in self.unsatisfied:
                status = "unsatisfied"
            elif item in self.completed:
                status = "completed"
            else:
                status = "in-progress"
            res.append({"name": item.name, "total_time": item.total_time, "status": status})
        return json.dumps(res)


def execute(graph, args, kwargs, distribute=False):
    unsatisfied = list(graph.nodes())
    completed = []
    while unsatisfied:
        satisfied = [node for node in unsatisfied
                     if all(x in completed for x in graph.predecessors(node))]
        unsatisfied = [x for x in unsatisfied if x not in satisfied]
        for node in satisfied:
            preds = graph.predecessors(node)
            node_kwargs = merge_dicts(*([pred.result for pred in preds]+[kwargs]))
            res = node.func(**node_kwargs)
            node.result = res
        completed.extend(satisfied)
    return {x.name: x.result for x in completed if len(list(graph.successors(x))) == 0}
