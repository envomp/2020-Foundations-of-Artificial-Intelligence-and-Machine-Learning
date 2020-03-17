BREEZE = 1
STENCH = 2
WUMPUS = 4
POTENTIAL_WUMPUS = 8
GUARANTEED_NO_WUMPUS = 16
PIT = 32
POTENTIAL_PIT = 64
GUARANTEED_NO_PIT = 128
GOLD = 256
UNKNOWN = 512
OK = 1024
NO_MAP_TO_EXPLORE = 2048

# for testing
world1 = [[STENCH | OK,     OK,                             BREEZE | OK,    PIT],
          [WUMPUS,          BREEZE | STENCH | GOLD | OK,    PIT,            BREEZE | OK],
          [STENCH | OK,     OK,                             BREEZE | OK,    OK],
          [OK,              BREEZE | OK,                    PIT,            BREEZE | OK]]

observable_world1 = [[UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
                     [UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
                     [UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN],
                     [OK,      UNKNOWN, UNKNOWN, UNKNOWN]]

observable_world2 = [[UNKNOWN,      UNKNOWN,        UNKNOWN,        UNKNOWN],
                     [UNKNOWN,      UNKNOWN,        STENCH | OK,    UNKNOWN],
                     [BREEZE | OK,  STENCH | OK,    BREEZE | OK,    OK],
                     [OK,           BREEZE | OK,    UNKNOWN,        UNKNOWN]]


def deal_with_sensor_attribute(board, x, y, attribute, world_exists, target):
    counter = 0
    if y > 0:
        if not board[y - 1][x] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            board[y - 1][x] |= attribute
            counter += 1
        elif board[y - 1][x] & target:
            counter += 1

    if y < len(board) - 1:
        if not board[y + 1][x] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            board[y + 1][x] |= attribute
            counter += 1
        elif board[y + 1][x] & target:
            counter += 1

    if x > 0:
        if not board[y][x - 1] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            board[y][x - 1] |= attribute
            counter += 1
        elif board[y][x - 1] & target:
            counter += 1

    if x < len(board[0]) - 1:
        if not board[y][x + 1] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            board[y][x + 1] |= attribute
            counter += 1
        elif board[y][x + 1] & target:
            counter += 1
    return counter


def resolve_STENCH(x, y, board, world_exists):
    if deal_with_sensor_attribute(board, x, y, POTENTIAL_WUMPUS, world_exists, WUMPUS) == 1:
        if y > 0 and not board[y - 1][x] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            if board[y - 1][x] & GUARANTEED_NO_PIT and board[y - 1][x] & POTENTIAL_WUMPUS:
                board[y - 1][x] ^= GUARANTEED_NO_PIT | POTENTIAL_WUMPUS | WUMPUS

        if y < len(board) - 1 and not board[y + 1][x] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            if board[y + 1][x] & GUARANTEED_NO_PIT and board[y + 1][x] & POTENTIAL_WUMPUS:
                board[y + 1][x] ^= GUARANTEED_NO_PIT | POTENTIAL_WUMPUS | WUMPUS

        if x > 0 and not board[y][x - 1] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            if board[y][x - 1] & GUARANTEED_NO_PIT and board[y][x - 1] & POTENTIAL_WUMPUS:
                board[y][x - 1] ^= GUARANTEED_NO_PIT | POTENTIAL_WUMPUS | WUMPUS

        if x < len(board[0]) - 1 and not board[y][x + 1] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            if board[y][x + 1] & GUARANTEED_NO_PIT and board[y][x + 1] & POTENTIAL_WUMPUS:
                board[y][x + 1] ^= GUARANTEED_NO_PIT | POTENTIAL_WUMPUS | WUMPUS


def resolve_NO_STENTCH(x, y, board, world_exists):
    deal_with_sensor_attribute(board, x, y, GUARANTEED_NO_WUMPUS, world_exists, WUMPUS)


def resolve_BREEZE(x, y, board, world_exists):
    if deal_with_sensor_attribute(board, x, y, POTENTIAL_PIT, world_exists, PIT) == 1:
        if y > 0 and not board[y - 1][x] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            if board[y - 1][x] & GUARANTEED_NO_WUMPUS and board[y - 1][x] & POTENTIAL_PIT:
                board[y - 1][x] ^= GUARANTEED_NO_WUMPUS | POTENTIAL_PIT | PIT

        if y < len(board) - 1 and not board[y + 1][x] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            if board[y + 1][x] & GUARANTEED_NO_WUMPUS and board[y + 1][x] & POTENTIAL_WUMPUS:
                board[y + 1][x] ^= GUARANTEED_NO_PIT | POTENTIAL_PIT | PIT

        if x > 0 and not board[y][x - 1] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            if board[y][x - 1] & GUARANTEED_NO_WUMPUS and board[y][x - 1] & POTENTIAL_WUMPUS:
                board[y][x - 1] ^= GUARANTEED_NO_PIT | POTENTIAL_PIT | PIT

        if x < len(board[0]) - 1 and not board[y][x + 1] & (PIT | WUMPUS | OK | NO_MAP_TO_EXPLORE if world_exists else 0):
            if board[y][x + 1] & GUARANTEED_NO_WUMPUS and board[y][x + 1] & POTENTIAL_WUMPUS:
                board[y][x + 1] ^= GUARANTEED_NO_PIT | POTENTIAL_PIT | PIT


def resolve_NO_BREEZE(x, y, board, world_exists):
    deal_with_sensor_attribute(board, x, y, GUARANTEED_NO_PIT, world_exists, PIT)


def resolve_OK(x, y, board, world):
    if world:  # Check only when world is known. When no world, then there is nowhere to go
        if y > 0 and board[y - 1][x] & UNKNOWN:
            if not world[y - 1][x] & OK:
                print("Player walked to it's death..")
            board[y - 1][x] ^= UNKNOWN
            board[y - 1][x] |= OK
            board[y - 1][x] |= world[y - 1][x]

        if y < len(board) - 1 and board[y + 1][x] & UNKNOWN:
            if not world[y + 1][x] & OK:
                print("Player walked to it's death..")
            board[y + 1][x] ^= UNKNOWN
            board[y - 1][x] |= OK
            board[y + 1][x] |= world[y + 1][x]

        if x > 0 and board[y][x - 1] & UNKNOWN:
            if not world[y][x - 1] & OK:
                print("Player walked to it's death..")
            board[y][x - 1] ^= UNKNOWN
            board[y - 1][x] |= OK
            board[y][x - 1] |= world[y][x - 1]

        if x < len(board[0]) - 1 and board[y][x + 1] & UNKNOWN:
            if not world[y][x + 1] & OK:
                print("Player walked to it's death..")
            board[y][x + 1] ^= UNKNOWN
            board[y - 1][x] |= OK
            board[y][x + 1] |= world[y][x + 1]
    else:
        if y > 0:
            board[y - 1][x] = clearThreat(board[y - 1][x])

        if y < len(board) - 1:
            board[y + 1][x] = clearThreat(board[y + 1][x])

        if x > 0:
            board[y][x - 1] = clearThreat(board[y][x - 1])

        if x < len(board[0]) - 1 and board[y][x + 1]:
            board[y][x + 1] = clearThreat(board[y][x + 1])


def getSquare(element):
    square = []
    if element & GOLD:
        square.append("GOLD")
    if element & STENCH:
        square.append("STENCH")
    if element & BREEZE:
        square.append("BREEZE")
    if element & WUMPUS:
        square.append("WUMPUS")
    if element & PIT:
        square.append("PIT")
    if element & POTENTIAL_PIT:
        square.append("POTENTIAL_PIT")
    if element & POTENTIAL_WUMPUS:
        square.append("POTENTIAL_WUMPUS")
    if element & GUARANTEED_NO_WUMPUS:
        square.append("GUARANTEED_NO_WUMPUS")
    if element & GUARANTEED_NO_PIT:
        square.append("GUARANTEED_NO_PIT")
    if element & OK:
        square.append("OK")
    if element & UNKNOWN:
        square.append("UNKNOWN")
    if element & NO_MAP_TO_EXPLORE:
        square.append("NO_MAP_TO_EXPLORE")
    return square


def print_human_readable_board(board):
    for row in board:
        for position in row:
            print(" v ".join(getSquare(position)).ljust(36), end=" | ")
        print()


def clearThreat(position):
    if position & POTENTIAL_WUMPUS:
        position ^= POTENTIAL_WUMPUS
    if position & POTENTIAL_PIT:
        position ^= POTENTIAL_PIT
    return position


def game_loop(starting_board, real_board):
    for i in range(10):
        for y in range(len(starting_board)):
            for x in range(len(starting_board[y])):

                if starting_board[y][x] & GUARANTEED_NO_PIT and starting_board[y][x] & GUARANTEED_NO_WUMPUS:  # position is marked as safe
                    starting_board[y][x] ^= GUARANTEED_NO_PIT | GUARANTEED_NO_WUMPUS

                    if real_board:
                        starting_board[y][x] |= OK
                    else:
                        starting_board[y][x] |= NO_MAP_TO_EXPLORE

                    if starting_board[y][x] & UNKNOWN:
                        starting_board[y][x] ^= UNKNOWN

                if starting_board[y][x] & UNKNOWN or starting_board[y][x] & POTENTIAL_WUMPUS or starting_board[y][x] & POTENTIAL_PIT:
                    continue  # dangerous

                if starting_board[y][x] & OK and not (starting_board[y][x] & BREEZE) and not (starting_board[y][x] & STENCH):
                    resolve_OK(x, y, starting_board, real_board)

                if starting_board[y][x] & BREEZE:  # Sensor detected breeze
                    resolve_BREEZE(x, y, starting_board, real_board is None)
                else:  # no breeze
                    resolve_NO_BREEZE(x, y, starting_board, real_board is None)
                    pass

                if starting_board[y][x] & STENCH:  # Sensor detected stench
                    resolve_STENCH(x, y, starting_board, real_board is None)
                else:  # no stench
                    resolve_NO_STENTCH(x, y, starting_board, real_board is None)
                    pass

    print_human_readable_board(starting_board)


if __name__ == '__main__':
    game_loop(observable_world2, None)
