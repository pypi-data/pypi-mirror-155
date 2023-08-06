from typing import Callable, List, Tuple, Optional

from .expr import exmat
from .mesh import Mesh, Group
from .relast import Nexus


class Dom:
    __nexus: Nexus

    def __init__(self, mesh: Mesh):
        self.__nexus = Nexus(mesh.pts, mesh.edges, mesh.faces, mesh.cells)

    def plot_sys(self) -> Tuple[List[float], List[float], List[float]]:
        return self.__nexus.plot_sys()

    def set_boundary(self, *groups):
        for group in groups:
            self.__nexus.set_boundary(group.vers, group.edges, group.faces)
        self.__nexus.set_dofs()
        self.__nexus.set_solver()

    def dofs(self) -> Tuple[int, int]:
        return self.__nexus.tot_dofs()

    def embed_bcond(self, bcond: Callable[[float, float, float], List[float]], group):
        arena, vec = exmat(bcond)
        assert len(vec) == 3
        self.__nexus.embed_bcond(list(group.vers), list(group.edges), list(group.faces), arena, vec)

    def set_force(self, force: Callable[[float, float, float], List[float]], group: Optional[Group] = None):
        if group is None:
            arena, vec = exmat(force)
            assert len(vec) == 3
            self.__nexus.set_force(0, set(), arena, vec)
        else:
            arena, vec = exmat(force)
            assert len(vec) == 3
            self.__nexus.set_force(group.id, group.cells, arena, vec)

    def set_moment(self, force: Callable[[float, float, float], List[float]], group: Optional[Group] = None):
        if group is None:
            arena, vec = exmat(force)
            assert len(vec) == 9
            self.__nexus.set_moment(0, set(), arena, vec)
        else:
            arena, vec = exmat(force)
            assert len(vec) == 9
            self.__nexus.set_moment(group.id, group.cells, arena, vec)

    def set_consts(self, c_ec: List[List[float]], c_ecm: List[List[float]], mulc: float):
        self.__nexus.set_consts(c_ec, c_ecm, mulc)

    def solve(self, tol: float = 1e-10, solver: str = "cg"):
        self.__nexus.assemble()
        self.__nexus.solve(tol, solver)

    def set_vals(self):
        self.__nexus.set_vals()

    def plot_curves(self, res: int, group: Group = None) -> Tuple[List[float], List[float], List[float]]:
        if group is None:
            return self.__nexus.plot_curves(res, set())
        else:
            return self.__nexus.plot_curves(res, group.edges)

    def plot_disp(self, res: int, group: Group = None) -> \
            Tuple[List[float], List[float], List[float], List[float], List[Tuple[int, int, int]]]:
        if group is None:
            (x, y, z, w), cells = self.__nexus.plot_disp(res, set())
            return x, y, z, w, cells
        else:
            (x, y, z, w), cells = self.__nexus.plot_disp(res, group.faces)
            return x, y, z, w, cells

    def plot_flux(self, res: int, axis: int, group: Group = None) -> \
            Tuple[List[float], List[float], List[float], List[float], List[float], List[float]]:
        assert axis == 0 or axis == 1 or axis == 2
        if group is None:
            return self.__nexus.plot_flux(res, set(), axis)
        else:
            return self.__nexus.plot_flux(res, group.cells, axis)

    def plot_dist(self, res: int, group: Group = None) -> Tuple[List[float], List[float], List[float], List[float]]:
        if group is None:
            return self.__nexus.plot_dist(res, set())
        else:
            return self.__nexus.plot_dist(res, group.cells)

    def disp_err(self, disp: Callable[[float, float, float], List[float]]) -> float:
        disp = exmat(disp)
        assert len(disp[1]) == 3
        return self.__nexus.disp_err(disp)

    def flux_err(self, flux: Callable[[float, float, float], List[float]]) -> float:
        flux = exmat(flux)
        assert len(flux[1]) == 9
        return self.__nexus.flux_err(flux)

    def energy(self) -> float:
        return self.__nexus.energy()
