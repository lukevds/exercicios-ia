from random import random
from typing import List, Tuple
from enum import StrEnum




PlaneDirection = StrEnum('PlaneDirection', ['LEFT', 'DOWN', 'UP', 'RIGHT'])


class Portion:
    isClean: bool = True
    hasRobot: bool = False

    def __init__(self, isClean, hasRobot = False):
        self.isClean = isClean
        self.hasRobot = hasRobot


PortionPlane = List[List[Portion]]


class World:
    portions: PortionPlane
    height: int
    width: int

    def __init__(self, portions: PortionPlane):
        self.portions = portions
        self.height = len(portions)
        self.width = len(portions[0])


class DirtDetector:
    def detect(self, position: List[int], world: World) -> bool:
        return world.portions[position[0]][position[1]].isClean


class WorldDetector:
    position: List[int]
    portion: Portion
    canGoLeft: bool
    canGoDown: bool
    canGoUp: bool
    canGoRight: bool

    def getRobotPosition(self, world) -> bool:
        found: bool = False
        for height, row in enumerate(world.portions):
            for width, portion in enumerate(row):
                if portion.hasRobot:
                    self.position = [height, width]
                    self.portion = portion
                    found = True
                    break
                else:
                    continue
            else:
                continue
            break
        if not found:
            return False
        self.canGoLeft  = self.position[1] != 0
        self.canGoDown  = self.position[0] != world.height - 1
        self.canGoUp    = self.position[0] != 0
        self.canGoRight = self.position[1] != world.width - 1
        return True


class DirtCleaner:
    def clean(self, portion: Portion):
        portion.isClean = True


class HoverBoard:
    def move(self, direction: PlaneDirection, currentPosition: List[int], world: World) -> bool:
        nextPosition: List[int] = currentPosition.copy()
        if direction == PlaneDirection.LEFT:
            nextPosition[1] = currentPosition[1] - 1
        elif direction == PlaneDirection.DOWN:
            nextPosition[0] = currentPosition[0] + 1
        elif direction == PlaneDirection.UP:
            nextPosition[0] = currentPosition[0] - 1
        else:
            nextPosition[1] = currentPosition[1] + 1
        world.portions[currentPosition[0]][currentPosition[1]].hasRobot = False
        world.portions[nextPosition[0]][nextPosition[1]].hasRobot = True
        return True
        

class ReflexiveRobot:
    world: World
    
    dirtDetector: DirtDetector
    worldDetector: WorldDetector

    dirtCleaner: DirtCleaner
    hoverBoard: HoverBoard

    # finge que a direcao que o robo esta virado nao e uma pequena
    # forma de modelar o problema
    facing: PlaneDirection

    # criar constructor com tamanho e posicao do robo
    # (factory ou parametro com default)
    def __init__(self, world: World, dirtDetector: DirtDetector,
                 worldDetector: WorldDetector, dirtCleaner: DirtCleaner,
                 hoverBoard: HoverBoard, facing: PlaneDirection):
        self.world = world
        self.dirtDetector = dirtDetector
        self.worldDetector = worldDetector
        self.dirtCleaner = dirtCleaner
        self.hoverBoard = hoverBoard

        self.facing = facing

    
    def _moveToNextPosition(self):
        """ Rotina de movimento que funciona para planos de tamanho NxN."""
        nextPos: PlaneDirection
        facingLeft: bool  = self.facing == PlaneDirection.LEFT
        facingDown: bool  = self.facing == PlaneDirection.DOWN
        facingUp: bool    = self.facing == PlaneDirection.UP
        facingRight: bool = self.facing == PlaneDirection.RIGHT

        if facingRight:
            if self.worldDetector.canGoRight:
                nextPos = PlaneDirection.RIGHT
            elif self.worldDetector.canGoDown:
                nextPos = PlaneDirection.DOWN
            elif self.worldDecetcor.canGoUp:
                nextPos = PlaneDirection.UP
            else:
                nextPos = PlaneDirection.LEFT
        elif facingDown:
            if self.worldDetector.canGoLeft:
                nextPos = PlaneDirection.LEFT
            elif self.worldDetector.canGoRight:
                nextPos = PlaneDirection.RIGHT
            elif self.worldDetector.canGoDown:
                nextPos = PlaneDirection.DOWN
            else:
                nextPos = PlaneDirection.UP
        elif facingLeft:
            if self.worldDetector.canGoLeft:
                nextPos = PlaneDirection.LEFT
            elif self.worldDetector.canGoUp:
                nextPos = PlaneDirection.UP
            elif self.worldDetector.canGoDown:
                nextPos = PlaneDirection.DOWN
            else:
                nextPos = PlaneDirection.RIGHT
        else:
            if self.worldDetector.canGoRight:
              nextPos = PlaneDirection.RIGHT
            elif self.worldDetector.canGoLeft:
                nextPos = PlaneDirection.LEFT
            elif self.worldDetector.canGoUp:
                nextPos = PlaneDirection.UP
            else:
                nextPos = PlaneDirection.DOWN

        self.facing = nextPos
        
        self.hoverBoard.move(nextPos, self.worldDetector.position,
                             self.world)
        
            

    def cleaningRoutine(self):
        for i in range(10):
            self.worldDetector.getRobotPosition(self.world)
            position = self.worldDetector.position
            
            isClean = self.dirtDetector.detect(position, self.world)
            if not isClean:
                self.dirtCleaner.clean(self.worldDetector.portion)
            self._moveToNextPosition()
            # escrever prints

class ReflexiveRobotFactory:
    def threeByThree() -> Tuple[World, ReflexiveRobot]:
        portions: PortionPlane = []
        for i in range(3):
            row: List[Portion] = []
            for j in range(3):
                portion = Portion(
                    int(random()*10) % 2 == 0,
                    False
                )
                row.append(portion)
            portions.append(row)

        portions[0][0].hasRobot = True
        
        world = World(portions)

        dirtDetector = DirtDetector()
        worldDetector = WorldDetector()
        
        dirtCleaner = DirtCleaner()
        hoverBoard = HoverBoard()

        return ReflexiveRobot(
            world,
            dirtDetector,
            worldDetector,
            dirtCleaner,
            hoverBoard,
            PlaneDirection.RIGHT
        )


def main():
    robo = ReflexiveRobotFactory.threeByThree()
    robo.cleaningRoutine()
    print('oi')


if __name__ == '__main__':
    main()
        
