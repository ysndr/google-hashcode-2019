from picture import Picture
from os import environ


def parse_file(file):
    with open(file) as f:
        f.readline()
        pictures = []
        for line, content in enumerate(f.readlines()):
            content_split = content.strip().split(" ")
            rotation = content_split[0]
            tags = set([str(x) for x in content_split[2:]])
            pictures.append(Picture(str(line), rotation, tags))

            if line == 80000:
                break

    return pictures


def prepare(pictures_):
    pictures = dict()
    tags = dict()

    picture_h = [pic for pic in pictures_ if pic.rotation == "H"]

    picture_v = [pic for pic in pictures_ if pic.rotation == "V"]
    picture_v = sorted(picture_v, key=lambda p: len(p.tags))

    picture_v = zip(
        picture_v[:len(picture_v)//2],
        reversed(picture_v[len(picture_v)//2:])
    )

    picture_vv = [Picture(a.id + " " + b.id, "H", a.tags.union(b.tags))
                  for (a, b) in picture_v]

    picture_h.extend(picture_vv)

    for picture in picture_h:
        pictures[picture.id] = picture
        for tag in picture.tags:
            tags[tag] = tags.get(tag, set([]))
            tags[tag].add(picture.id)
    return (pictures, tags)


def run(pictures, tags):
    i = 0
    current = None
    while pictures:
        i += 1
        if not current:
            current = list(pictures.values())[0]
            print("nope")
        print(i)
        yield current.id
        current = next(pictures, tags, current)


def next(pictures, tags, current):
    targets = {}
    for tagId in current.tags:
        neighbours = tags[tagId]
        for neighbour_id in neighbours:
            if not neighbour_id in pictures or neighbour_id == current.id:
                continue
            targets[neighbour_id] = targets.get(neighbour_id, 0) + 1

    for ptag in pictures[current.id].tags:
        tags[ptag].remove(current.id)
    del pictures[current.id]

    if not targets:
        return None

    next_one = max(targets, key=targets.get)

    return pictures[next_one]


if __name__ == "__main__":

    for f in [
        #"a_example.txt",
        #"b_lovely_landscapes.txt",
        #"c_memorable_moments.txt",
        #"d_pet_pictures.txt",
        "e_shiny_selfies.txt"
    ]:
        (pictures, tags) = prepare(parse_file(f))
        with open(f + ".out", "w") as file:
            acc = []
            for line in run(pictures, tags):
                acc.append(line)

            file.write(str(len(acc)) + '\n')
            file.write('\n'.join(acc))
