def move(origin, destination):
    '''
    origin, destination: str
    
    prints out movement from origin to destination
    '''
    print('Move from %s to %s.' % (origin, destination))

def hanoiTowerSolver(n, fr, to, spare):
    '''
    n: int
    fr: str, the starting rod
    to: str, the destination rod
    spare: str, the rod other than 'fr' and 'to'
    
    prints out how to move n disks from the starting rod to the the destination rod.
    '''
    if n == 1:
        move(fr, to)
    else:
        hanoiTowerSolver(n-1, fr, spare, to)
        hanoiTowerSolver(1, fr, to, spare)
        hanoiTowerSolver(n-1, spare, to, fr)

hanoiTowerSolver(5, 'A', 'B', 'C')