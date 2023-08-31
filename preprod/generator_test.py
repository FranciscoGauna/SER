def gen_1():
    listita = [1, 2, 3]
    for x in listita:
        yield x


def gen_2():
    listita = [4, 5, 6]
    for x in listita:
        yield x


def gen_3(generators):
    generators = [g() for g in generators]
    n_s = [next(g) for g in generators]
    while generators[0]:
        yield n_s
        try:
            n_s = [next(g) for g in generators]
        except StopIteration:
            return


def gen_permute(prev, next_gen):
    gen = next_gen[0]
    if len(next_gen) == 1:
        for i in gen():
            yield [*prev, i]
    else:
        for i in gen():
            for j in gen_permute([*prev, i], next_gen[1:]):
                yield j


print(list(gen_permute([], [gen_1, gen_1, gen_2])))
