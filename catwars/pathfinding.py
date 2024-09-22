from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Pathfinding():
    def __init__(self, game):
        self.game = game

        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.world_matrix = self.get_world_matrix()

    def get_world_matrix(self):
        matrix = []
        for r in range(self.game.world.dimensions[1]):
            row = []
            for c in range(self.game.world.dimensions[0]):
                row.append(1 if self.game.world.is_walkable(c, r) else 0)
            matrix.append(row)
        return matrix

    def find(self, source, target):
        grid = Grid(matrix=self.world_matrix)
        start = grid.node(*source)
        end = grid.node(*target)
        path, runs = self.finder.find_path(start, end, grid)
        print('operations:', runs, 'path length:', len(path), 'path:', path)
        print(grid.grid_str(path=path, start=start, end=end))
        return path
