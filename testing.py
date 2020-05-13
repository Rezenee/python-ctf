chunk_size = 640
class block:
    def __init__(self, x, y, length, height, colour):
        self.x = x
        self.y = y
        self.l = length
        self.h = height
        self.colour = colour
        self.x_cord = self.x // chunk_size
        self.y_cord = self.y // chunk_size

walls = {
        'ground': block(-5000, 0, 10000, 20, 'grey'),
        'wall': block(-25, -100, 25, 25, 'grey'), 
        'wall2': block(50, -45, 5, 25, 'grey')
        }
for wall in walls:
    chunk_overlap = 0
    x_checkChunk = walls[wall].x
    if x_checkChunk > 0:
        
        # Sees how close it is to the edge of chunk, then sees if with the length it goes into 2 chunks.
        while x_checkChunk > chunk_size:
           x_checkChunk -= chun_size 
           chunks_overlap += 1
        if x_checkChunk + walls[wall].l> 640:
            # -5000 turns into -520
            for i in range(chunks_overlap):
                walls[wall + str(i)] = block(
            del walls[wall]

    else:
        while x_checkChunk < -chunk_size:
            x_checkChunk += chunk_size
            print(x_checkChunk)
        if x_checkChunk - walls[wall].l< -chunk_size:
            print("oh god")
