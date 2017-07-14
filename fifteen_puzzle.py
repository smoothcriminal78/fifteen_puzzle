import copy
import random
import heapq

class FifteenPuzzle:

    class Tile:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return '{} {}'.format(self.x, self.y)

    DIMS = 4
    def __init__(self):
        self.tiles = [[x + y for x in range(self.DIMS)]
                        for y in range(1, self.DIMS ** 2, self.DIMS)]
        self.blank = self.Tile(self.DIMS-1, self.DIMS-1)
        self.tiles[-1][-1] = 0

    def __copy__(self):
        copy = FifteenPuzzle()
        copy.tiles = [list(t) for t in self.tiles]
        copy.blank = self.blank
        return copy

    def __gt__(self, fp2):
        return True

    def __hash__(self):
        out = 0
        for tp in self.allTilePos():
            out = (self.DIMS ** 2 * out) + self.tile(tp)
        return out

    def __eq__(self, other):
        for tp in self.allTilePos():
            if self.tile(tp) != other.tile(tp):
                return False
        return True

    def __str__(self):
        # return str(self.tiles)
        s = ''
        for i in self.tiles:
            s+='|'.join([str(j).rjust(2, ' ') for j in i]) + '\n'
        return s

    # def __repr__(self):
    #     return str(self)

    def allTilePos(self):
        return [self.Tile(i, j) for i in range(self.DIMS) for j in range(self.DIMS)]

    def show(self):
        for i in self.tiles:
            print('|'.join([str(j).rjust(2, ' ') for j in i]))
        print('\n')

    def tile(self, t):
        return self.tiles[t.x][t.y]

    def whereIs(self, n):
        for tp in self.allTilePos():
            if self.tile(tp) == n:
                return tp
        return None

    def isValidMove(self, tp):
        if tp.x < 0 or tp.x >= self.DIMS or tp.y < 0 or tp.y >= self.DIMS:
            return False

        dx, dy = self.blank.x - tp.x, self.blank.y - tp.y
        if abs(dx) + abs(dy) != 1 or dx*dy != 0:
            return False

        return True

    def allValidMoves(self):
        moves = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                tp = self.Tile(self.blank.x + x, self.blank.y + y)
                if self.isValidMove(tp):
                    moves.append(tp)
        return moves

    def move(self, tp):
        # if not isValidMove(): throw Exception
        self.tiles[self.blank.x][self.blank.y] = self.tiles[tp.x][tp.y]
        self.tiles[tp.x][tp.y] = 0
        self.blank = tp

    def moveClon(self, tp):
        fp = copy.copy(self)
        fp.move(tp)
        return fp

    def shuffle(self, n):
        for i in range(n):
            possible = self.allValidMoves()
            w = int(random.random()) * len(possible)
            mv = possible[w]
            self.move(mv)

    def numOfMisplacedTiles(self):
        wrong = 0
        for i in range(self.DIMS):
            for j in range(self.DIMS):
                if self.tiles[i][j] > 0 and self.tiles[i][j] != SOLVED.tiles[i][j]:
                    wrong+=1
        return wrong

    def isSolved(self):
        return self.numOfMisplacedTiles() == 0

    def estimateError(self):
        return self.numOfMisplacedTiles()

    def moveClone(self, tp):
        out = copy.copy(self)
        out.move(tp)
        return out

    def allAdjacentPuzzles(self):
        out = []
        for tp in self.allValidMoves():
            out.append(self.moveClone(tp))
        return out

    def aStarSolve(self):
        predecessor, depth, score, toVisit = {}, {}, {}, []

        predecessor[self] = None
        depth[self] = 0
        score[self] = self.estimateError()
        heapq.heappush(toVisit, (score[self], self))

        cnt = 0
        while len(toVisit) > 0 and len(toVisit) < 100:
            candidate = toVisit.pop()[1]
            cnt+=1
            if cnt % 10000 == 0:
                print('Considered {} positions'.format(cnt))
            if candidate.isSolved():
                print('Solution considered {} boards'.format(cnt))
                solution = []
                backtrace = candidate
                while backtrace is not None:
                    solution.insert(0, backtrace)
                    backtrace = predecessor[backtrace]
                return solution

            for fp in candidate.allAdjacentPuzzles():
                if fp not in predecessor:
                    predecessor[fp] = candidate
                    depth[fp] = depth[candidate] + 1
                    estimate = fp.estimateError()
                    score[fp] = depth[candidate] + 1 + estimate
                    heapq.heappush(toVisit, (-score[fp], fp))
        return None

def showSolution(solution):
    if solution is not None:
        print('Success!  Solution with {} moves:\n'.format(len(solution)))
        for sp in solution:
            sp.show()
    else:
        print('Did not solve.')


SOLVED = FifteenPuzzle()
fp = FifteenPuzzle();
fp.shuffle(3);
print('Shuffled board:')
fp.show()

print('Solving with A*')
solution = fp.aStarSolve()
showSolution(solution);
