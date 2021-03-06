# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/dataflow.py
# Compiled at: 2020-04-24 19:37:56
# Size of source mod 2**32: 22713 bytes
import collections, itertools, logging
from typing import Dict, Iterator, List, Tuple
import cached_property, pulp
from haoda import ir, util
_logger = logging.getLogger().getChild(__name__)

class SuperSourceNode(ir.Module):
    __doc__ = "A node representing the super source in the dataflow graph.\n\n  A super source doesn't have parent nodes.\n\n  Attributes:\n      fwd_nodes (Dict[Tuple[str, int], ForwardNode]): Dict mapping tuples of\n        (tensor name, offset) to nodes.\n      cpt_nodes (Dict[Tuple[str, int], ComputeNode]): Dict mapping tuples of\n        (stage_name, pe_id) to nodes.\n      super_sink (SuperSinkNode): The super sink node of this DAG.\n  "

    def __init__(self, fwd_nodes, cpt_nodes, super_sink):
        super().__init__()
        self.fwd_nodes = fwd_nodes
        self.cpt_nodes = cpt_nodes
        self.super_sink = super_sink

    @property
    def graphviz(self) -> str:
        output = 'digraph {\n'
        for src, dst in self.dfs_edge_gen():
            output += f'  "{repr(src)}" -> "{repr(dst)}"\n'

        output += '}\n'
        return output

    def update_module_depths(self, depths: Dict[(int, int)], min_depth: int=2) -> None:
        """Update module pipeline depths and FIFO depths.

    The FIFO depths are determined by solving an ILP problem:

    + Optimization objective: minimize the sum (weighted by FIFO width) of all
    FIFO depths.
    + Constraints: the whole DAG can be fully pipelined without artificial
    stalls.

    For every non-overlapping path between a pair of nodes,
    the latency of each token is the maximum minimum latency among all paths.
    To enable full pipelining,
    this latency must not exceed the maximum latency of any path.
    The minimum latency of each path is the sum of the FIFO write latency in
    each module and the number of edges (FIFOs),
    since the minimum latency of a FIFO is 1.
    The maximum latency of each path is the sum of the FIFO write latency in
    each module and the total depth of FIFOs.

    Args:
        depths (Dict[int, int]): Dict mapping module ids to pipeline depths.
        min_depth (int): Minimum possible FIFO depth, default to 2.
    """
        for src_node in self.tpo_valid_node_gen():
            for dst_node in src_node.children:
                module_id = self.module_table[src_node][1]
                depth = depths.get(module_id)
                if depth is not None:
                    fifo = src_node.fifo(dst_node)
                    if fifo.write_lat != depth:
                        _logger.debug('%s write latency changed %s -> %d', fifo, fifo.write_lat, depth)
                        fifo.write_lat = depth

        lp_problem = pulp.LpProblem('optimal_fifo_depths', pulp.LpMinimize)
        lp_vars = {}
        for src_node, dst_node in self.bfs_valid_edge_gen():
            lp_vars[(src_node, dst_node)] = pulp.LpVariable(name=f"depth_{src_node.fifo(dst_node).c_expr}",
              lowBound=min_depth,
              cat='Integer')

        lp_problem += sum(x.fifo(y).haoda_type.width_in_bits * v for (x, y), v in lp_vars.items())
        prev_path_table = {}
        path_table = {}

        def dfs(node, path):
            path.append(node)
            prev_path = prev_path_table.get(node)
            prev_path_table[node] = path[:]
            if prev_path is not None:
                idx = 0
                for node1, node2 in zip(prev_path[1:], path[1:]):
                    if node1 is node2:
                        idx += 1
                    else:
                        break

                key = (
                 path[idx], path[(-1)])
                path_table.setdefault(key, [prev_path[idx:]]).append(path[idx:])
            else:
                for child in node.children:
                    dfs(child, path)

            path.pop()

        dfs(self, [])
        for paths in path_table.values():
            min_latency_list = []
            max_latency_list = []
            for path in paths:
                module_latency = sum(x.get_latency(y) for x, y in zip(path[:-1], path[1:]) if is_valid_edge((x, y)))
                min_fifo_latency = len(path) - 1
                max_fifo_latency = sum(lp_vars[edge] for edge in zip(path[:-1], path[1:]) if is_valid_edge(edge))
                min_latency_list.append(module_latency + min_fifo_latency)
                max_latency_list.append(module_latency + max_fifo_latency)

            max_min_latency = max(min_latency_list)
            lp_problem.extend(max_min_latency <= x for x in max_latency_list)

        lp_status = lp_problem.solve()
        if lp_status != pulp.LpStatusOptimal:
            lp_status_str = pulp.LpStatus[lp_status]
            _logger.error('ILP error: %s\n%s', lp_status_str, lp_problem)
            raise util.InternalError('unexpected ILP status: %s' % lp_status_str)
        for (src_node, dst_node), lp_var in lp_vars.items():
            depth = int(pulp.value(lp_var))
            fifo = src_node.fifo(dst_node)
            if fifo.depth != depth:
                _logger.debug('%s * depth %d -> %d', fifo, fifo.depth, depth)
                fifo.depth = depth

        if _logger.isEnabledFor(logging.DEBUG):
            for (first, last), paths in path_table.items():
                _logger.debug('reconvergent paths %s ==> %s', repr(first), repr(last))
                for path in paths:
                    module_latency = sum(x.get_latency(y) for x, y in zip(path[:-1], path[1:]) if is_valid_edge((x, y)))
                    min_fifo_latency = len(path) - 1
                    max_fifo_latency = sum(x.fifo(y).depth for x, y in zip(path[:-1], path[1:]) if is_valid_edge((x, y)))
                    _logger.debug('  latency: [%d, %d] = %d + [%d, %d] path: %s', module_latency + min_fifo_latency, module_latency + max_fifo_latency, module_latency, min_fifo_latency, max_fifo_latency, path)

    @property
    def name(self):
        return 'super_source'

    def __repr__(self) -> str:
        return '\x1b[35msuper source\x1b[0m'

    @cached_property.cached_property
    def module_table(self) -> Dict[(ir.Node, Tuple[(ir.ModuleTrait, int)])]:
        """Module table maps an IR node to (module_trait, module_id).

    Returns:
      A dict mapping an IR node to (module_trait, module_id) tuple.
    """
        self._module_traits = collections.OrderedDict()
        module_table = collections.OrderedDict()
        for node in self.tpo_valid_node_gen():
            self._module_traits.setdefault(ir.ModuleTrait(node), []).append(node)

        for idx, module_trait in enumerate(self._module_traits):
            for node in self._module_traits[module_trait]:
                module_table[node] = (
                 module_trait, idx)

        return module_table

    @cached_property.cached_property
    def module_traits(self) -> Tuple[(ir.ModuleTrait, ...)]:
        return tuple(self.module_trait_table)

    @property
    def module_trait_table(self) -> Dict[(ir.ModuleTrait, List[ir.Node])]:
        self.module_table
        return self._module_traits

    def tpo_valid_node_gen(self):
        """Traverse valid descendant nodes in tpological order.

    Load and store nodes are ordered in the same way as they are specified in
    soda files.

    Yields:
        Iterator[ir.Module]: Nodes that are not super source or super sink.
    """
        yield from self.load_nodes
        yield from filter(lambda x: not isinstance(x, MemoryNode) and is_valid_node(x), super().tpo_node_gen())
        yield from self.store_nodes
        if False:
            yield None

    def bfs_valid_edge_gen(self) -> Iterator[ir.Module]:
        return filter(is_valid_edge, self.bfs_edge_gen())

    @property
    def load_nodes(self) -> Tuple[('LoadNode', Ellipsis)]:
        return self.children

    @property
    def store_nodes(self) -> Tuple[('StoreNode', Ellipsis)]:
        return self.super_sink.parents


class SuperSinkNode(ir.Module):
    __doc__ = "A node representing the super sink in the dataflow graph.\n\n  A super sink doesn't have child nodes.\n  "

    @property
    def name(self):
        return 'super_sink'

    def __repr__(self) -> str:
        return '\x1b[34msuper sink\x1b[0m'


class ForwardNode(ir.Module):
    __doc__ = 'A node representing a forward module in the dataflow graph.\n\n  Attributes:\n    tensor: Tensor corresponding to this node.\n    offset: Int representing the offset of this tensor.\n  '

    def __init__(self, **kwargs):
        super().__init__()
        self.tensor = kwargs.pop('tensor')
        self.offset = kwargs.pop('offset')

    def __repr__(self):
        return '\x1b[32mforward %s @%d\x1b[0m' % (self.tensor.name, self.offset)

    @property
    def name(self):
        return '{}_offset_{}'.format(self.tensor.name, self.offset)


class ComputeNode(ir.Module):
    __doc__ = 'A node representing a compute module in the dataflow graph.\n\n  Attributes:\n    tensor: Tensor corresponding to this node.\n    pe_id: Int representing the PE id.\n    fifo_map: {str: {idx: Node}}\n  '

    def __init__(self, **kwargs):
        super().__init__()
        self.tensor = kwargs.pop('tensor')
        self.pe_id = kwargs.pop('pe_id')
        self.fifo_map = collections.defaultdict(dict)

    def __repr__(self):
        return '\x1b[31mcompute %s #%d\x1b[0m' % (self.tensor.name, self.pe_id)

    @property
    def name(self):
        return '{}_pe_{}'.format(self.tensor.name, self.pe_id)


class MemoryNode(ir.Module):

    def __init__(self, var, bank):
        super().__init__()
        self.var = var
        self.bank = bank

    @property
    def name(self) -> str:
        return f"{self.var}_bank_{self.bank}"

    def __str__(self) -> str:
        return f"dram<bank {self.bank} {self.var}>"


class LoadNode(MemoryNode):

    def __repr__(self) -> str:
        return f"\x1b[33mload {self.var} bank {self.bank}\x1b[0m"


class StoreNode(MemoryNode):

    def __repr__(self) -> str:
        return f"\x1b[36mstore {self.var} bank {self.bank}\x1b[0m"


def is_valid_node(node: ir.Module) -> bool:
    return not isinstance(node, (SuperSourceNode, SuperSinkNode))


def is_valid_edge(edge: Tuple[(ir.Module, ir.Module)]) -> bool:
    return all(map(is_valid_node, edge))


def create_dataflow_graph(stencil):
    chronological_tensors = stencil.chronological_tensors
    super_source = SuperSourceNode(fwd_nodes={}, cpt_nodes={}, super_sink=(SuperSinkNode()))
    load_nodes = {stmt.name:tuple(LoadNode(var=(stmt.name), bank=bank) for bank in stmt.dram) for stmt in stencil.input_stmts}
    store_nodes = {stmt.name:tuple(StoreNode(var=(stmt.name), bank=bank) for bank in stmt.dram) for stmt in stencil.output_stmts}
    for mem_node in (itertools.chain)(*load_nodes.values()):
        super_source.add_child(mem_node)

    for mem_node in (itertools.chain)(*store_nodes.values()):
        mem_node.add_child(super_source.super_sink)

    def color_id(node):
        if isinstance(node, LoadNode):
            return f"\x1b[33mload {node.var}[bank{node.bank}]\x1b[0m"
        else:
            if isinstance(node, StoreNode):
                return f"\x1b[36mstore {node.var}[bank{node.bank}]\x1b[0m"
            else:
                if isinstance(node, ForwardNode):
                    return f"\x1b[32mforward {node.tensor.name} @{node.offset}\x1b[0m"
                if isinstance(node, ComputeNode):
                    return f"\x1b[31mcompute {node.tensor.name} #{node.pe_id}\x1b[0m"
            return 'unknown node'

    def color_attr(node):
        result = []
        for k, v in node.__dict__.items():
            if (
             node.__class__, k) in ((SuperSourceNode, 'parents'),
             (SuperSinkNode,
              'children')):
                pass
            else:
                if k in ('parents', 'children'):
                    result.append('%s: [%s]' % (k, ', '.join(map(color_id, v))))
                else:
                    result.append('%s: %s' % (k, repr(v)))

        return '{%s}' % ', '.join(result)

    def color_print(node):
        return '%s: %s' % (color_id(node), color_attr(node))

    print_node = color_id
    if stencil.replication_factor > 1:
        replicated_next_fifo = stencil.get_replicated_next_fifo()
        replicated_all_points = stencil.get_replicated_all_points()
        replicated_reuse_buffers = stencil.get_replicated_reuse_buffers()

        def add_fwd_nodes(src_name):
            dsts = replicated_all_points[src_name]
            reuse_buffer = replicated_reuse_buffers[src_name][1:]
            nodes_to_add = []
            for dst_point_dicts in dsts.values():
                for offset in dst_point_dicts:
                    if (
                     src_name, offset) in super_source.fwd_nodes:
                        pass
                    else:
                        fwd_node = ForwardNode(tensor=(stencil.tensors[src_name]),
                          offset=offset,
                          depth=(stencil.get_replicated_reuse_buffer_length(src_name, offset)))
                        _logger.debug('create %s', print_node(fwd_node))
                        init_offsets = [start for start, end in reuse_buffer if start == end]
                        if offset in init_offsets:
                            if src_name in [stencil.input.name]:
                                load_node_count = len(load_nodes[src_name])
                                load_nodes[src_name][(load_node_count - 1 - offset % load_node_count)].add_child(fwd_node)
                            else:
                                super_source.cpt_nodes[(src_name, 0)].add_child(fwd_node)
                            super_source.fwd_nodes[(src_name, offset)] = fwd_node
                            if offset in replicated_next_fifo[src_name]:
                                nodes_to_add.append((
                                 fwd_node, (src_name, replicated_next_fifo[src_name][offset])))

            for src_node, key in nodes_to_add:
                src_node.add_child(super_source.fwd_nodes[key])

        add_fwd_nodes(stencil.input.name)
        for stage in stencil.get_stages_chronologically():
            cpt_node = ComputeNode(stage=stage, pe_id=0)
            _logger.debug('create %s', print_node(cpt_node))
            super_source.cpt_nodes[(stage.name, 0)] = cpt_node
            for input_name, input_window in stage.window.items():
                for i in range(len(input_window)):
                    offset = next(offset for offset, points in replicated_all_points[input_name][stage.name].items() if points == i)
                    fwd_node = super_source.fwd_nodes[(input_name, offset)]
                    _logger.debug('  access %s', print_node(fwd_node))
                    fwd_node.add_child(cpt_node)

            if stage.is_output():
                super_source.cpt_nodes[(stage.name,
                 0)].add_child(store_nodes[stage.name][0])
            else:
                add_fwd_nodes(stage.name)

    else:
        next_fifo = stencil.next_fifo
        all_points = stencil.all_points
        reuse_buffers = stencil.reuse_buffers

        def add_fwd_nodes(src_name):
            dsts = all_points[src_name]
            reuse_buffer = reuse_buffers[src_name][1:]
            nodes_to_add = []
            for dst_point_dicts in dsts.values():
                for offset in dst_point_dicts:
                    if (
                     src_name, offset) in super_source.fwd_nodes:
                        pass
                    else:
                        fwd_node = ForwardNode(tensor=(stencil.tensors[src_name]), offset=offset)
                        _logger.debug('create %s', print_node(fwd_node))
                        init_offsets = [next(end for start, end in reuse_buffer if start == unroll_idx) for unroll_idx in reversed(range(stencil.unroll_factor))]
                        _logger.debug('reuse buffer: %s', reuse_buffer)
                        _logger.debug('init offsets: %s', init_offsets)
                        if offset in init_offsets:
                            if src_name in stencil.input_names:
                                load_node_count = len(load_nodes[src_name])
                                load_nodes[src_name][(load_node_count - 1 - offset % load_node_count)].add_child(fwd_node)
                            else:
                                cpt_offset = next(unroll_idx for unroll_idx in range(stencil.unroll_factor) if init_offsets[unroll_idx] == offset)
                                cpt_node = super_source.cpt_nodes[(src_name, cpt_offset)]
                                cpt_node.add_child(fwd_node)
                            super_source.fwd_nodes[(src_name, offset)] = fwd_node
                            if offset in next_fifo[src_name]:
                                nodes_to_add.append((
                                 fwd_node, (src_name, next_fifo[src_name][offset])))

            for src_node, key in nodes_to_add:
                src_node.add_child(super_source.fwd_nodes[key])

        for input_name in stencil.input_names:
            add_fwd_nodes(input_name)

        for tensor in chronological_tensors:
            if tensor.is_input():
                continue
            else:
                for unroll_index in range(stencil.unroll_factor):
                    pe_id = stencil.unroll_factor - 1 - unroll_index
                    cpt_node = ComputeNode(tensor=tensor, pe_id=pe_id)
                    _logger.debug('create %s', print_node(cpt_node))
                    super_source.cpt_nodes[(tensor.name, pe_id)] = cpt_node
                    for input_name, input_window in tensor.ld_indices.items():
                        for i in range(len(input_window)):
                            offset = next(offset for offset, points in all_points[input_name][tensor.name].items() if pe_id in points if points[pe_id] == i)
                            fwd_node = super_source.fwd_nodes[(input_name, offset)]
                            _logger.debug('  access %s', print_node(fwd_node))
                            fwd_node.add_child(cpt_node)

                if tensor.is_output():
                    for pe_id in range(stencil.unroll_factor):
                        super_source.cpt_nodes[(tensor.name, pe_id)].add_child(store_nodes[tensor.name][(pe_id % len(store_nodes[tensor.name]))])

                else:
                    add_fwd_nodes(tensor.name)

    for src_node in super_source.tpo_valid_node_gen():
        for dst_node in filter(is_valid_node, src_node.children):
            if isinstance(src_node, LoadNode):
                write_lat = 0
            else:
                if isinstance(src_node, ForwardNode):
                    write_lat = 2
                else:
                    if isinstance(src_node, ComputeNode):
                        write_lat = src_node.tensor.st_ref.lat
                    else:
                        raise util.InternalError('unexpected source node: %s' % repr(src_node))
                    fifo = ir.FIFO(src_node, dst_node, depth=0, write_lat=write_lat)
                    lets = []
                    if isinstance(src_node, LoadNode):
                        expr = ir.DRAMRef(haoda_type=(dst_node.tensor.haoda_type),
                          dram=(
                         src_node.bank,),
                          var=(dst_node.tensor.name),
                          offset=((stencil.unroll_factor - 1 - dst_node.offset) // len(stencil.stmt_table[dst_node.tensor.name].dram)))
                    else:
                        if isinstance(src_node, ForwardNode):
                            if isinstance(dst_node, ComputeNode):
                                dst = src_node.tensor.children[dst_node.tensor.name]
                                src_name = src_node.tensor.name
                                unroll_idx = dst_node.pe_id
                                point = all_points[src_name][dst.name][src_node.offset][unroll_idx]
                                idx = list(dst.ld_indices[src_name].values())[point].idx
                                _logger.debug('%s%s referenced by <%s> @ unroll_idx=%d is %s', src_name, util.idx2str(idx), dst.name, unroll_idx, print_node(src_node))
                                dst_node.fifo_map[src_name][idx] = fifo
                            else:
                                delay = stencil.reuse_buffer_lengths[src_node.tensor.name][src_node.offset]
                                offset = src_node.offset - delay
                                for parent in src_node.parents:
                                    for fifo_r in parent.fifos:
                                        if fifo_r.edge == (parent, src_node):
                                            break

                                if delay > 0:
                                    for let in src_node.lets:
                                        if isinstance(let.expr, ir.DelayedRef) and let.expr.ref == fifo_r:
                                            var_name = let.name
                                            var_type = let.haoda_type
                                            break
                                    else:
                                        var_name = 'let_%d' % len(src_node.lets)
                                        var_type = fifo_r.haoda_type
                                        lets.append(ir.Let(haoda_type=var_type, name=var_name,
                                          expr=ir.DelayedRef(delay=delay, ref=fifo_r)))

                                    expr = ir.Var(name=var_name, idx=[])
                                    expr.haoda_type = var_type
                                else:
                                    expr = fifo_r
                        else:
                            if isinstance(src_node, ComputeNode):

                                def replace_refs_callback(obj, args):
                                    if isinstance(obj, ir.Ref):
                                        _logger.debug('replace %s with %s', obj, src_node.fifo_map[obj.name][obj.idx])
                                        return src_node.fifo_map[obj.name][obj.idx]
                                    else:
                                        return obj

                                _logger.debug('lets: %s', src_node.tensor.lets)
                                lets = [_.visit(replace_refs_callback) for _ in src_node.tensor.lets]
                                _logger.debug('replaced lets: %s', lets)
                                _logger.debug('expr: %s', src_node.tensor.expr)
                                expr = src_node.tensor.expr.visit(replace_refs_callback)
                                _logger.debug('replaced expr: %s', expr)
                                if isinstance(dst_node, StoreNode):
                                    dram_ref = ir.DRAMRef(haoda_type=(src_node.tensor.haoda_type),
                                      dram=(
                                     dst_node.bank,),
                                      var=(src_node.tensor.name),
                                      offset=(src_node.pe_id // len(stencil.stmt_table[src_node.tensor.name].dram)))
                                    dst_node.lets.append(ir.Let(haoda_type=None, name=dram_ref, expr=fifo))
                            else:
                                raise util.InternalError('unexpected node of type %s' % type(src_node))
            src_node.exprs[fifo] = expr
            src_node.lets.extend(_ for _ in lets if _ not in src_node.lets)
            _logger.debug('fifo [%d]: %s%s => %s', fifo.depth, color_id(src_node), '' if fifo.write_lat is None else ' ~%d' % fifo.write_lat, color_id(dst_node))

    super_source.update_module_depths({})
    return super_source