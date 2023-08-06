import typing

def encode(in_list: typing.List) -> typing.List:
    """
    Given a sequence of states
    return a list where every element is a tuple
    Each tuple has structure (state, state_duration)
    There is a tuple for each bout of a state
    """
    # Handle empty list first.

    if not in_list:
        return []

    # Init output list so that first element reflect first input item.

    out_list = [(in_list[0], 1)]

    # Then process all other items in sequence.

    for item in in_list[1:]:
        # If same as last, up count, otherwise new element with count 1.

        if item == out_list[-1][0]:
            out_list[-1] = (item, out_list[-1][1] + 1)
        else:
            out_list.append((item, 1))

    return out_list

def decompose(data):
    """
    Given a sequence of states
    return the sequence where every element is a tuple
    Each tuple has structure (state, state_start)
    There is a tuple for each bout of a state
    """

    encoded = encode(data)
    values = []
    accum_length = [0]

    for i in range(len(encoded)):
        state, duration = encoded[i]
        values.append(state)
        accum = accum_length[-1] + duration
        accum_length.append(accum)

    accum_length.pop(-1)

    return values, accum_length

def main():
    data = [e for e  in "TTTTTFFFFFFFFTTTTT"]
    print(data)
    print(encode(data))
    print(decompose(data))

if __name__ == "__main__":
    main()
