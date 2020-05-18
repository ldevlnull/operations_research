class Graph:
    def __init__(self):
        self.vertices = {}

    def create_vertex(self, index):
        vertex = Vertex(index)
        self.vertices[index] = vertex

    def get_vertex(self, index):
        return self.vertices[index]

    def __contains__(self, index):
        return index in self.vertices

    def connect_vertexes(self, src_key, dest_key, weight=1):
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)

    def check_vertex_connection(self, src_key, dest_key):
        return self.vertices[src_key].has_connection_with(self.vertices[dest_key])

    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices.values())


class Vertex:
    def __init__(self, index):
        self.index = index
        self.points_to = {}

    def get_index(self):
        return self.index

    def add_neighbour(self, target_vertex, weight):
        self.points_to[target_vertex] = weight

    def get_neighbours(self):
        return self.points_to.keys()

    def get_weight(self, target_vertex):
        return self.points_to[target_vertex]

    def has_connection_with(self, target_vertex):
        return target_vertex in self.points_to


def run(g):
    vertexes_distance = {v: dict.fromkeys(g, float('inf')) for v in g}
    next_vertex = {v: dict.fromkeys(g, None) for v in g}

    for v in g:
        for n in v.get_neighbours():
            vertexes_distance[v][n] = v.get_weight(n)
            next_vertex[v][n] = n

    for v in g:
        vertexes_distance[v][v] = 0
        next_vertex[v][v] = None

    for p in g:
        for v in g:
            for w in g:
                if vertexes_distance[v][w] > vertexes_distance[v][p] + vertexes_distance[p][w]:
                    vertexes_distance[v][w] = vertexes_distance[v][p] + vertexes_distance[p][w]
                    next_vertex[v][w] = next_vertex[v][p]

    return vertexes_distance, next_vertex


def display_path(next_v, vertex1, vertex2):
    p = vertex1
    while (next_v[p][vertex2]):
        print('{} -> '.format(p.get_index()), end='')
        p = next_v[p][vertex2]
    print('{} '.format(vertex2.get_index()), end='')


def main():
    g = Graph()
    print('vertex <index>')
    print('connect <vertex1> <vertex2> <weight>')
    print('run <vertex1> <vertex2>')
    print('show')
    print('quit')

    while True:
        input_command = input('What would you like to input_command? ').split()

        operation = input_command[0]
        if operation == 'vertex':
            index = int(input_command[1])
            if index not in g:
                g.create_vertex(index)
            else:
                print('Vertex already exists.')
        elif operation == 'connect':
            src = int(input_command[1])
            target_vertex = int(input_command[2])
            weight = int(input_command[3])
            if src not in g:
                print('Vertex {} does not exist.'.format(src))
            elif target_vertex not in g:
                print('Vertex {} does not exist.'.format(target_vertex))
            else:
                if not g.check_vertex_connection(src, target_vertex):
                    g.connect_vertexes(src, target_vertex, weight)
                else:
                    print('Edge already exists.')

        elif operation == 'run':
            distance, next_v = run(g)
            start, end = g.get_vertex(int(input_command[1])), g.get_vertex(int(input_command[2]))
            print('Shortest distances:')
            if next_v[start][end]:
                print('From {} to {}: '.format(start.get_index(), end.get_index()), end='')
                display_path(next_v, start, end)
                print('(distance {})'.format(distance[start][end]))

        elif operation == 'show':
            print('Vertices: ', end='')
            for v in g:
                print(v.get_index(), end=' ')
            print()

            print('Edges: ')
            for v in g:
                for target_vertex in v.get_neighbours():
                    w = v.get_weight(target_vertex)
                    print('(src={}, target_vertex={}, weight={}) '.format(v.get_index(), target_vertex.get_index(), w))
            print()

        elif operation == 'quit':
            break


if __name__ == '__main__':
    main()