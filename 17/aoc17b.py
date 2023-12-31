fname = r'17/input.txt'
fname = r'17/test.txt'

reverse_direction = dict(l='r', r='l', u='d', d='u') 


print('Loading heat map')
with open(fname, 'r') as fp:
    lines = fp.readlines()
heat_map = {}
for line_num, ln in enumerate(lines):
    for col_number, heat_loss in enumerate(ln.strip()):
        heat_map[(line_num, col_number)] = int(heat_loss)
last_line = line_num
last_col = col_number 
solution_upper_bound = last_line * last_col * 1e6  # do all moves at cost 1e6


# route_set = [
#   (heat_loss_this_route, recent_route, line_num, col_num), ...  # e.g. (14, 'dd'), this will sort 'd' before 'dd' if the heat is the same
# ]
route_set = {(0, 'r', 0, 1), (0, 'd', 1, 0)}  # add two options for starting directions
processed_routes = {}  # {(recent_route, line, col): min_heat_so_far, ...} e.g. {('rr', 3, 5): 12}

loop_num = 0
while True:
    loop_num += 1
    # pop shortest tile from route_list
    route_set.remove(route_tuple:=min(route_set))
    heat_loss_this_route, recent_route, line_num, col_num = route_tuple
    
    # chk--not in processed routes
    saved_tuple = (recent_route, line_num, col_num)
    if saved_tuple in processed_routes:
        continue  # we've been here before with at least as low a heat score
    
    if (this_heat_loss:=heat_map.get((line_num, col_num), None)) is None:
        continue  # location is off map
    heat_loss_this_route += this_heat_loss

    # print update
    if loop_num % 1000 == 0:
        print(f'{loop_num=}  {heat_loss_this_route=}')
 
    #   chk--(line, col) == (last_line, last_col)? return heat_loss_recent_route + current_heat_loss
    if (line_num, col_num) == (last_line, last_col):
        if len(recent_route) >= 4:
            print(f'{loop_num=}')
            print(heat_loss_this_route)
            break

    # BUG below in commented code. Runs without this optimisation, just takes a few minutes.
    # # chk--no shorter route in processed_routes (for shorter versions of recent_route)
    # if len(recent_route) > 4:
    #     drop_this_route = False
    #     for route_length in range(4, len(recent_route)):
    #         if processed_routes.get((recent_route[0]*route_length, line_num, col_num), solution_upper_bound) <= heat_loss_this_route:
    #             drop_this_route = True
    #             break
    #     if drop_this_route:
    #         break
    
    # Add to processed routes
    processed_routes[saved_tuple] = heat_loss_this_route

    # generate and check adjoining nodes (line, col, recent_route)
    next_dirs = set('rdlu')
    current_dir = recent_route[-1]
    next_dirs.discard(reverse_direction[current_dir])  # can't go backwards
    if len(recent_route) < 4:  # need to keep going straight
        next_dirs = current_dir
    if len(recent_route) == 10: # can't go any further
        next_dirs.discard(current_dir)  # can't do more than 3 steps in a row

    for next_dir in next_dirs:
        new_line_num = line_num
        new_col_num = col_num

        if next_dir == current_dir:
            new_recent_route = recent_route + next_dir
        else:
            new_recent_route = next_dir

        if next_dir == 'r':
            new_col_num += 1
        elif next_dir == 'l':
            new_col_num -= 1
        elif next_dir == 'u':
            new_line_num -= 1
        elif next_dir == 'd':
            new_line_num += 1

        route_set.add((heat_loss_this_route, new_recent_route, new_line_num, new_col_num))