def gen_expn_colors():
    """Generates the Experian brand colors

    Parameters
    ----------
    None

    Returns
    ----------
    list of Experian brand colors

    """

    expn_colours=[
        "#26478d", # Dark Blue
        "#632678", # Purple
        "#406eb3", # Light Blue
        "#982881", # Maroon
        "#ba2f7d", # Pink
        "#575756", # Grey
        # Light shaded versions
        '#7d91bb',
        '#a17dae',
        '#8ca8d1',
        '#c17eb3',
        '#d682b1',
        '#9a9a9a',
        ]

    return expn_colours

def gen_gradient_cmap(start, end, steps=50):
    """Generates a seaborn graduated color map

    Parameters
    ----------
    start: tuple
        rgb color
    end: tuple
        rgb color
    steps: int, optional
        The number of increments to return in the color gradient, default is 50

    Returns
    ----------
    list of colors for use in saeborn color maps

    """

    cmap = []
    red_step = (end[0] - start[0])/steps
    green_step = (end[1] - start[1])/steps
    blue_step = (end[2] - start[2])/steps

    start_hex = '#' + ''.join('{:02x}'.format(c) for c in start)

    cmap.append(start_hex)

    for i in range(1,steps-1):
        temp_rgb=[0,0,0]

        temp_rgb[0] = int(start[0] + i*red_step)
        temp_rgb[1] = int(start[1] + i*green_step)
        temp_rgb[2] = int(start[2] + i*blue_step)

        temp_hex = '#' + ''.join('{:02x}'.format(c) for c in temp_rgb)

        cmap.append(temp_hex)

    end_hex = '#' + ''.join('{:02x}'.format(c) for c in end)
    cmap.append(end_hex)

    return cmap
