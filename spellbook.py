from copy import deepcopy

master_default = {
    "genome_size": "62m",
}

flye_default = deepcopy(master_default)
flye_default.update({
    "m": '-',
    "hash": "eb89c9ef000f6dbcea426dcb430db92290546196",
    "plasmids": False,
    "meta": True,
})

wtdbg2_default = deepcopy(master_default)
wtdbg2_default.update({
    "pmer": 21,
    "kmer": 0,
    "sampler": 1,
    "edge": 3,
    "length": 5000,
    "max_k": 10000,
    "max_node": 10000,
    "hash": "904f2b3ebdaa1e6f268cc58937767891a00d5bcb",
})


flye25 = deepcopy(flye_default)
flye25.update({
    "hash": "af246d6a942bbc57fe02049bee92645f43c87b62",
})


flye28 = deepcopy(flye_default)
flye28.update({
    "hash": "91e8b13d69293dbf32330b54180384245a0f6f67",
    "genome_size": "-"
})

flye25_0polish = deepcopy(flye25)
flye25_0polish.update({
    "iterations": 0,
})


redbean24 = deepcopy(wtdbg2_default)
redbean24.update({
    "hash": "6a0691e308b3644b6f718a03679f697d058e2be6",
})


# lame way of doing this
spells = {
    "flye25-0polish" : flye25_0polish,
    "flye25" : flye25,
    "flye28": flye28,
    "wtdbg2-24" : redbean24
}
