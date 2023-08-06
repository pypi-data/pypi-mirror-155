from typing import List, Dict, NamedTuple, Tuple, Set, Callable
from math import nan


class Face(NamedTuple):
    p: int
    adj_list: Set[int]


class Cell(NamedTuple):
    nodes: List[int]
    p: int


class Group:
    id: int
    vers: Set[int]
    edges: Set[Tuple[int, int]]
    faces: Set[Tuple[int, int, int]]
    cells: Set[int]

    def __init__(self, id: int, vers: Set[int], edges: Set[Tuple[int, int]],
                 faces: Set[Tuple[int, int, int]], cells: Set[int]):
        self.id, self.vers, self.edges, self.faces, self.cells = id, vers, edges, faces, cells


class Mesh:
    pts: List[List[float]]
    edges: Dict[Tuple[int, int], int]
    faces: Dict[Tuple[int, int, int], Face]
    cells: List[Cell]
    groups: int

    def __init__(self, pts: List[List[float]], tets: List[List[int]], p: int, rcm: bool = True):
        if rcm:
            graph = rcm_graph(len(pts), tets)
            pts = [pts[node] for node in graph]
            tets = [[graph[node] for node in nodes] for nodes in tets]
        cells, edges, faces = [], {}, {}
        for idx, nodes in enumerate(tets):
            nodes.sort()
            for line in lines(nodes):
                edges[line] = p
            for tri in tris(nodes):
                if tri not in faces:
                    faces[tri] = Face(p, set())
                faces[tri].adj_list.add(idx)
            cells.append(Cell(nodes, p))
        cells.sort(key=lambda cell: cell[0])
        self.pts, self.edges, self.faces, self.cells, self.groups = pts, edges, faces, cells, 0

    def def_group(self, cond: Callable[[float, float, float], bool]) -> Group:
        self.groups += 1
        vers, edges, faces, cells = set(), set(), set(), set()
        for ver, [x, y, z] in enumerate(self.pts):
            if cond(x, y, z):
                vers.add(ver)
        for edge in self.edges:
            if edge[0] in vers and edge[1] in vers:
                edges.add(edge)
        for face in self.faces:
            if face[0] in vers and face[1] in vers and face[2] in vers:
                faces.add(face)
        for idx, cell in enumerate(self.cells):
            n0, n1, n2, n3 = cell.nodes
            if n0 in vers and n1 in vers and n2 in vers and n3 in vers:
                cells.add(idx)
        return Group(self.groups, vers, edges, faces, cells)

    def def_outer(self) -> Group:
        self.groups += 1
        vers, edges, faces = set(), set(), set()
        for (nodes, face) in self.faces.items():
            if len(face.adj_list) < 2:
                for node in nodes:
                    vers.add(node)
                n0, n1, n2 = nodes
                for edge in [(n0, n1), (n0, n2), (n1, n2)]:
                    edges.add(edge)
                faces.add(nodes)
        return Group(self.groups, vers, edges, faces, cells=set())

    def plot_sys(self, group: Group = None) -> Tuple[List[float], List[float], List[float]]:
        x, y, z = [], [], []
        if group is None:
            for (n0, n1) in self.edges:
                [x0, y0, z0], [x1, y1, z1] = self.pts[n0], self.pts[n1]
                x.extend([x0, x1, nan])
                y.extend([y0, y1, nan])
                z.extend([z0, z1, nan])
        else:
            for (n0, n1) in group.edges:
                [x0, y0, z0], [x1, y1, z1] = self.pts[n0], self.pts[n1]
                x.extend([x0, x1, nan])
                y.extend([y0, y1, nan])
                z.extend([z0, z1, nan])
        return x, y, z


def face_edges(face: Tuple[int, int, int]) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    n0, n1, n2 = face
    return (n0, n1), (n0, n2), (n1, n2)


def lines(cell: List[int]) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int],
                                    Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    [n0, n1, n2, n3] = cell
    return (n0, n1), (n0, n2), (n1, n2), (n0, n3), (n1, n3), (n2, n3)


def tris(cell: List[int]) -> Tuple[Tuple[int, int, int], Tuple[int, int, int],
                                   Tuple[int, int, int], Tuple[int, int, int]]:
    [n0, n1, n2, n3] = cell
    return (n0, n1, n2), (n0, n2, n3), (n0, n1, n3), (n1, n2, n3)


def rcm_graph(size: int, cells: List[List[int]]) -> Dict[int, int]:
    adj_list = {}
    for nodes in cells:
        for node in nodes:
            if node not in adj_list:
                adj_list[node] = set()
            for adj_node in nodes:
                if adj_node != node:
                    adj_list[node].add(adj_node)
    start = min([(len(adj_nodes), node) for node, adj_nodes in adj_list.items()])[1]
    graph = [start]
    used = {start}
    for idx in range(0, size):
        node = graph[idx]
        next_nodes = [(len(adj_list[n]), n) for n in adj_list[node]]
        next_nodes.sort()
        for (_, n) in next_nodes:
            if n not in used:
                graph.append(n)
                used.add(n)
    graph.reverse()
    return {node: idx for idx, node in enumerate(graph)}
