from queue import Queue, PriorityQueue


def heuristic_astar(node, goal, steps):
    return max(abs(node[0] - goal[0]), abs(node[1] - goal[1])) * steps  # suurim koordinaadi nihe


def heuristic_greedy(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def map1():
    lava_map1 = [
        "      **               **      ",
        "     ***     D        ***      ",
        "     ***                       ",
        "                      *****    ",
        "           ****      ********  ",
        "           ***          *******",
        " **                      ******",
        "*****             ****     *** ",
        "*****              **          ",
        "***                            ",
        "              **         ******",
        "**            ***       *******",
        "***                      ***** ",
        "                               ",
        "                s              ",
    ]
    return [[x for x in y] for y in lava_map1]


def map2():
    lava_map2 = [
        "     **********************    ",
        "   *******   D    **********   ",
        "   *******                     ",
        " ****************    **********",
        "***********          ********  ",
        "            *******************",
        " ********    ******************",
        "********                   ****",
        "*****       ************       ",
        "***               *********    ",
        "*      ******      ************",
        "*****************       *******",
        "***      ****            ***** ",
        "                               ",
        "                s              ",
    ]
    return [[x for x in y] for y in lava_map2]


def get_lava_map(filename):
    with open(filename) as f:
        return [[map_char for map_char in map_line.strip()] for map_line in f.readlines() if len(map_line) > 1]


lava_map_original = [map1(), map2(), get_lava_map("cave300x300"), get_lava_map("cave600x600"), get_lava_map(
    "cave900x900")][4]

lava_map = [[x for x in y] for y in lava_map_original]

map_height = len(lava_map)
map_width = len(lava_map[0])

# (y, x)
parent_map = [[(-1, -1) for x in range(map_width)] for y in range(map_height)]

start_y = 0
start_x = 0

end_y = 0
end_x = 0

for y_coord, line in enumerate(lava_map):
    for x_coord, char in enumerate(line):
        if char == "s":
            start_y = y_coord
            start_x = x_coord
        if char == "D":
            end_y = y_coord
            end_x = x_coord

end_pos = (end_y, end_x)


def move_astar(cur_pos, new_pos, queue, steps):
    if 0 <= new_pos[0] < map_height and 0 <= new_pos[1] < map_width and lava_map[new_pos[0]][new_pos[1]] in " D":
        queue.put((heuristic_astar(new_pos, end_pos, steps), (steps + 1, new_pos)))
        lava_map[new_pos[0]][new_pos[1]] = "x"  # rip map
        parent_map[new_pos[0]][new_pos[1]] = cur_pos  # update parent map


def move_greedy(cur_pos, new_pos, queue):
    if 0 <= new_pos[0] < map_height and 0 <= new_pos[1] < map_width and lava_map[new_pos[0]][new_pos[1]] in " D":
        queue.put((heuristic_greedy(new_pos, end_pos), new_pos))
        lava_map[new_pos[0]][new_pos[1]] = "x"  # rip map
        parent_map[new_pos[0]][new_pos[1]] = cur_pos  # update parent map


def move_dijkstra(cur_pos, new_pos, queue):
    if 0 <= new_pos[0] < map_height and 0 <= new_pos[1] < map_width and lava_map[new_pos[0]][new_pos[1]] in " D":
        queue.put(new_pos)
        lava_map[new_pos[0]][new_pos[1]] = "x"  # rip map
        parent_map[new_pos[0]][new_pos[1]] = cur_pos  # update parent map


def aStar():
    queue = PriorityQueue()
    queue.put((0, (0, (start_y, start_x))))
    iterations = 0

    while 1:
        iterations += 1
        _, (steps, (cur_y, cur_x)) = queue.get()  # Get with lowest first index

        if cur_y == end_y and cur_x == end_x:
            return iterations

        move_astar((cur_y, cur_x), (cur_y + 1, cur_x), queue, steps)
        move_astar((cur_y, cur_x), (cur_y - 1, cur_x), queue, steps)
        move_astar((cur_y, cur_x), (cur_y, cur_x + 1), queue, steps)
        move_astar((cur_y, cur_x), (cur_y, cur_x - 1), queue, steps)


def dijkstra():
    queue = Queue()
    queue.put((start_y, start_x))
    iterations = 0

    while 1:
        iterations += 1
        cur_y, cur_x = queue.get()  # Get with lowest first index

        if cur_y == end_y and cur_x == end_x:
            return iterations

        move_dijkstra((cur_y, cur_x), (cur_y + 1, cur_x), queue)
        move_dijkstra((cur_y, cur_x), (cur_y - 1, cur_x), queue)
        move_dijkstra((cur_y, cur_x), (cur_y, cur_x + 1), queue)
        move_dijkstra((cur_y, cur_x), (cur_y, cur_x - 1), queue)


def greedy():
    queue = PriorityQueue()
    queue.put((0, (start_y, start_x)))
    iterations = 0

    while 1:
        iterations += 1
        _, (cur_y, cur_x) = queue.get()  # Get with lowest first index

        if cur_y == end_y and cur_x == end_x:
            return iterations

        move_greedy((cur_y, cur_x), (cur_y + 1, cur_x), queue)
        move_greedy((cur_y, cur_x), (cur_y - 1, cur_x), queue)
        move_greedy((cur_y, cur_x), (cur_y, cur_x + 1), queue)
        move_greedy((cur_y, cur_x), (cur_y, cur_x - 1), queue)


iterations = aStar()

print("Map with all the moves made. Iteration count = ", iterations)
# [print("".join(x)) for x in lava_map]

parent = (end_y, end_x)

# parent tracking
path = []
while 1:
    parent = parent_map[parent[0]][parent[1]]
    if parent[0] == start_y and parent[1] == start_x:
        break
    path.append((parent[0], parent[1]))
    lava_map_original[parent[0]][parent[1]] = "."

print()
print("----------------------------------------------")
print()
print("Shortest path was: ", len(path))
# [print("".join(x)) for x in lava_map_original]
