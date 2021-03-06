import copy
import math
import random
import heapq

class FifteenPuzzle:

    class Tile:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return '{} {}'.format(self.x, self.y)

    def __init__(self, r = 4, c = 4):
        self.tiles = [[x * c + y for y in range(1, c+1)] for x in range(0, r)]
        self.r, self.c = r, c
        self.blank = self.Tile(self.r-1, self.c-1)
        self.tiles[-1][-1] = 0

    def __copy__(self):
        copy = FifteenPuzzle()
        copy.tiles = [list(t) for t in self.tiles]
        copy.r, copy.c = self.r, self.c
        copy.blank = self.blank
        return copy

    def __gt__(self, fp2):
        return True

    def __hash__(self):
        out = 0
        for tp in self.allTilePos():
            out = (self.r ** 2 * out) + self.tile(tp)
        return out

    def __eq__(self, other):
        for tp in self.allTilePos():
            if self.tile(tp) != other.tile(tp):
                return False
        return True

    def __str__(self):
        s = ''
        for i in self.tiles:
            s+='|'.join([str(j).rjust(2, ' ') for j in i]) + '\n'
        return s

    # def __repr__(self):
    #     return str(self)

    def allTilePos(self):
        return [self.Tile(i, j) for i in range(self.r) for j in range(self.c)]

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
        if tp.x < 0 or tp.x >= self.r:
            return False
        if tp.y < 0 or tp.y >= self.c:
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
        if not self.isValidMove(tp):
            raise Exception
        self.tiles[self.blank.x][self.blank.y] = self.tiles[tp.x][tp.y]
        self.tiles[tp.x][tp.y] = 0
        self.blank = tp

    def moveClon(self, tp):
        fp = copy.copy(self)
        fp.move(tp)
        return fp

    def shuffle(self, n=5):
        for i in range(n):
            possible = self.allValidMoves()
            w = random.randrange(len(possible))
            mv = possible[w]
            self.move(mv)

    def numOfMisplacedTiles(self):
        wrong = 0
        for i in range(self.r):
            for j in range(self.c):
                if self.tiles[i][j] > 0 and self.tiles[i][j] != SOLVED.tiles[i][j]:
                    wrong+=1
        return wrong

    def manhattanDistance(self):
        sum = 0
        for tp in self.allTilePos():
            val = self.tile(tp)
            if val > 0:
                correct = SOLVED.whereIs(val)
                correct.x, correct.y = tp.x, tp.y
                sum += abs(correct.x) + abs(correct.y)
        return sum

    def estimateError(self):
        # return self.numOfMisplacedTiles()
        return self.manhattanDistance()

    def isSolved(self):
        return self.numOfMisplacedTiles() == 0

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
        global SOLVED
        SOLVED = FifteenPuzzle(self.r, self.c)
        predecessor, depth, score, toVisit = {}, {}, {}, []

        predecessor[self] = None
        depth[self] = 0
        score[self] = self.estimateError()
        heapq.heappush(toVisit, (score[self], self))

        cnt = 0
        while len(toVisit) > 0:
            candidate = toVisit.pop()[1]
            cnt+=1
            if cnt % 10000 == 0:
                print('Considered {} positions'.format(cnt))
            if candidate.isSolved():
                solution = []
                backtrace = candidate
                while backtrace is not None:
                    solution.insert(0, backtrace)
                    backtrace = predecessor[backtrace]
                return (solution, 'A* algorithm considered {} boards'.format(cnt))

            for fp in candidate.allAdjacentPuzzles():
                if fp not in predecessor:
                    predecessor[fp] = candidate
                    depth[fp] = depth[candidate] + 1
                    estimate = fp.estimateError()
                    score[fp] = depth[candidate] + 1 + estimate
                    heapq.heappush(toVisit, (-score[fp], fp))
        return (None, 'No solution')

    def dijkstraSolve(self):
        global SOLVED
        SOLVED = FifteenPuzzle(self.r, self.c)
        toVisit, predecessor = [], {}

        toVisit.append(self)
        predecessor[self] = None
        cnt = 0
        while(len(toVisit)>0):
            candidate = toVisit.pop()
            cnt+=1
            if cnt % 10000 == 0:
                print('Considered {} positions'.format(cnt))
            if candidate.isSolved():
                solution = []
                backtrace = candidate
                while backtrace is not None:
                    solution.insert(0, backtrace)
                    backtrace = predecessor[backtrace]
                return (solution, 'Dijkstra algorithm considered {} boards'.format(cnt))
            for fp in candidate.allAdjacentPuzzles():
                if fp not in predecessor:
                    predecessor[fp] = candidate
                    toVisit.append(fp)
        return (None, 'No solution')

def showSolution(solution):
    if solution is not None:
        print('Success!  Solution with {} moves:\n'.format(len(solution)))
        for sp in solution:
            sp.show()
    else:
        print('Did not solve.')

board = FifteenPuzzle(4, 4)
board.shuffle(5)
solution = board.aStarSolve()[0]
showSolution(solution)
