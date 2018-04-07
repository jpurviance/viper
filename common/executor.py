from common.utils import merge_dicts


def execute(graph, args, kwargs):
    unsatisfied = list(graph.nodes())
    completed = []
    while unsatisfied:
        satisfied = [node for node in unsatisfied
                     if all(x in completed for x in graph.predecessors(node))]
        unsatisfied = [x for x in unsatisfied if x not in satisfied]
        for node in satisfied:
            preds = graph.predecessors(node)
            res = node.func(**merge_dicts(*([pred.result for pred in preds]+[kwargs])))
            node.result = res
        completed.extend(satisfied)
    return {x.name: x.result for x in completed if len(list(graph.successors(x))) == 0}
