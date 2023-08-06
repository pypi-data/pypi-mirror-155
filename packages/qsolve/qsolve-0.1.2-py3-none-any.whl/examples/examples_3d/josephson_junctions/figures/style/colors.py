import matplotlib as mpl

# -------------------------------------------------------------------------------------------------
color_gridlines_major = '#666666'
color_gridlines_minor = '#999999'
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
black = '#000000'
white = '#ffffff'
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# flat_ui_palette_v1

peter_river = '#3498db'
wet_asphalt = '#34495e'
orange      = '#f39c12'
alizarin    = '#e74c3c'
emerald     = '#2ecc71'
sun_flower  = '#f1c40f'
pomegranate = '#c0392b'
silver      = '#bdc3c7'
clouds      = '#ecf0f1'
wisteria    = '#8e44ad'
belize_hole = '#2980b9'
amethyst    = '#9b59b6'
turquoise   = '#1abc9c'
green_sea   = '#16a085'
nephritis   = '#27ae60'
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# aussie palette
pure_apple   = '#6ab04c'
carmine_pink = '#eb4d4b'
turbo        = '#f9ca24'
quince_jelly = '#f0932b'
pink_glamour = '#ff7979'
exodus_fruit = '#686de0'
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# spanish palette
summer_sky      = '#34ace0'
fluorescent_red = '#ff5252'
celestial_green = '#33d9b2'
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
radical_red = '#ff355e'
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# name_cmap = 'jet'
# name_cmap = 'plasma'
# name_cmap = 'Blues'
# name_cmap = 'inferno'
# name_cmap = 'bwr'
# name_cmap = 'CMRmap'
# name_cmap = 'gnuplot2'

# my_cmap = plt.get_cmap(name_cmap)
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
cmap_black_white = mpl.colors.ListedColormap(['black', 'white'])
# -------------------------------------------------------------------------------------------------

colormap_1 = mpl.colors.LinearSegmentedColormap.from_list(
    'colormap_1',
    [
    black,
    wisteria,
    belize_hole,
    peter_river,
    emerald,
    sun_flower,
    alizarin,
    white
    ],
    N=256)

colormap_2 = mpl.colors.LinearSegmentedColormap.from_list(
    'colormap_2',
    [
    sun_flower,
    black,
    peter_river
    ],
    N=256)

"""
colormap_2 = mpl.colors.LinearSegmentedColormap.from_list('colormap_2', 
                                                                    [
                                                                    sun_flower,
                                                                    emerald,
                                                                    'black',
                                                                    amethyst,
                                                                    peter_river,
                                                                    ], 
                                                                    N=256)
"""

colormap_3 = mpl.colors.LinearSegmentedColormap.from_list('colormap_3', 
                                                                    [
                                                                    'black',
                                                                    peter_river,
                                                                    'white'
                                                                    ], 
                                                                    N=256)


colormap_4 = mpl.colors.LinearSegmentedColormap.from_list('colormap_4', 
                                                                    [
                                                                    peter_river,
                                                                    orange,
                                                                    alizarin,
                                                                    ], 
                                                                    N=256)

"""
print(peter_river)

# h = input('Enter hex: ').lstrip('#')

h = '#3498db'.lstrip('#') 

print(h)

rgb_peter_river = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

peter_river_red   = rgb_peter_river[0] / 256
peter_river_green = rgb_peter_river[1] / 256
peter_river_blue  = rgb_peter_river[2] / 256

print(rgb_peter_river)
print(peter_river_red)
print(peter_river_green)
print(peter_river_blue)


input("press enter\n")

cdict1 = {'red':   ((0.0, 0.0, 0.0),
                    (0.9, peter_river_red, peter_river_red),
                    (1.0, 1.0, 1.0)),

         'green':  ((0.0, 0.0, 0.0),
                    (0.9, peter_river_green, peter_river_green),
                    (1.0, 1.0, 1.0)),

         'blue':   ((0.0, 0.0, 0.0),
                    (0.1, peter_river_blue, peter_river_blue),
                    (1.0, 1.0, 1.0))
        }

my_cmap = mpl.colors.LinearSegmentedColormap('BlueRed1', cdict1)
"""






