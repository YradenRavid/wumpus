

class ShotestPath:
    
    @staticmethod
    def which_turn(curr_orientation,next_orientation):
        if curr_orientation == next_orientation:
            return "Forward"
        
        possible_orientations = ["East","North","West","South"]
        left_ind = possible_orientations.index(curr_orientation)
        right_ind = left_ind
        for i in range(len(possible_orientations)):
            left_ind = (left_ind + 1) % len(possible_orientations)
            left_orientation = possible_orientations[left_ind]
            if left_orientation == next_orientation:
                return "TrunLeft"
            right_ind = (right_ind - 1) % len(possible_orientations)
            right_orientation = possible_orientations[right_ind]
            if right_orientation == next_orientation:
                return "TrunRight"

    @staticmethod
    def calc_next_step_escape(agent_location,agent_orientation,escape_plan):
        next_location = escape_plan[escape_plan.index(agent_location) + 1]
        return ShotestPath.calc_next_step(agent_location,agent_orientation,next_location)

    @staticmethod
    def calc_next_step(agent_location,agent_orientation,next_location):
        if next_location[0] < agent_location[0]:
            next_orientation = "South"
        elif next_location[0] > agent_location[0]:
            next_orientation = "North"
        elif next_location[1] < agent_location[1]:
            next_orientation = "West"
        else:
            next_orientation = "East"
        return ShotestPath.which_turn(agent_orientation,next_orientation)

    @staticmethod
    def find_neighbors(location,safe_locations):
        cells = []
        if (location[0]-1,location[1]) in safe_locations:
            cells.append((location[0]-1,location[1]))
        if (location[0],location[1]-1) in safe_locations:
            cells.append((location[0],location[1]-1))
        if (location[0]+1,location[1]) in safe_locations:
            cells.append((location[0]+1,location[1]))
        if (location[0],location[1]+1) in safe_locations:
            cells.append((location[0],location[1]+1))
        return cells

    @staticmethod
    def safe_locations_to_graph(safe_locations):
        graph = {}
        for location in safe_locations:
           graph[location] = ShotestPath.find_neighbors(location,safe_locations)
        return graph

    @staticmethod
    def bfs_escape_plan(graph, curr_node, end_node):
        path_list = [[curr_node]]
        path_index = 0
        # To keep track of previously visited nodes
        previous_nodes = {curr_node}
        if curr_node == end_node:
            return path_list[0]
            
        while path_index < len(path_list):
            current_path = path_list[path_index]
            last_node = current_path[-1]
            next_nodes = graph[last_node]
            # Search goal node
            if end_node in next_nodes:
                current_path.append(end_node)
                return current_path
            # Add new paths
            for next_node in next_nodes:
                if not next_node in previous_nodes:
                    new_path = current_path[:]
                    new_path.append(next_node)
                    path_list.append(new_path)
                    # To avoid backtracking
                    previous_nodes.add(next_node)
            # Continue to next path in list
            path_index += 1
        # No path is found
        print("No path is found")
        return []
