import time
chunk_size = 640
x = -5000
chunk_wall = 0
distance = 10000
end_point = x + distance
# Gets the chunk size
if x + distance >
    if x < 0:
        while chunk_wall > x + chunk_size:
            chunk_wall -= chunk_size
        distance = abs (x) - abs(chunk_wall)
        print("block(" + str(x) + ", y, " + str(distance) + ", y height)")
    else:
        while chunk_wall < x:
            chunk_wall += chunk_size
        distance = abs(chunk_wall) - abs(x)
        print("block(" + str(x) + ", y, " + str(distance) + ", y height)")
    x = chunk_wall
    chunk_wall = 0
    while x < end_point:
        distance = chunk_size
        if x + chunk_size > end_point:
            distance = end_point - x
            print("block(" + str(x) + ", y, " + str(distance) + ", y height)")
            break
        else:
            print("block(" + str(x) + ", y, " + str(distance) + ", y height)")
        x += chunk_size