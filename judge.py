import sys

def parse_file(file, content_offse):
    with open(file) as f:
        f.readline()
        pictures = []
        for line, content in enumerate(f.readlines()):
            content_split = content.split(" ")
            rotation = content_split[0]
            tags = set([str(x).strip() for x in content_split[content_offse:]])
            pictures.append(tags)

    return pictures

def loader(name):
    origin = parse_file(name, 2) 
    with open(name + ".out") as f :
        f.readline()
        solution = [ [int(val) for val in entry.split(" ")] for entry in f.readlines()]
    return origin, solution

def score(a, b):
    return len(min(a.difference(b), b.difference(a), a.intersection(b), key=len))

origin, solution = loader(sys.argv[1])
summe = 0
for i in range(len(solution)-1):
    a = origin[solution[i][0]].union(origin[solution[i][1]])  if len(solution[i]) > 1 else origin[solution[i][0]]
    b = origin[solution[i+1][0]].union(origin[solution[i+1][1]])  if len(solution[i+1]) > 1 else origin[solution[i+1][0]]
    summe += score(a, b)
    
print(summe)


