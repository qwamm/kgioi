from gimpfu import *
import sys
sys.stderr = open( 'C:\\Users\\anoni\\Documents\\gimpstderr.txt', 'w')
sys.stdout = open( 'C:\\Users\\anoni\\Documents\\gimpstdout.txt', 'w')

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def create_matrix(matrix, copyLayer1, i, j, width, height, matrix_r, matrix_g, matrix_b):

    for m in range(3):
        for n in range(3):
            if j - 1 + n > 0 and j - 1 + n < width and i + 1 - m > 0 and i + 1 - m < height :
                matrix[m][n] = pdb.gimp_drawable_get_pixel(copyLayer1, j - 1 + n, i + 1 - m)[1]
            else:
                matrix[m][n] = pdb.gimp_drawable_get_pixel(copyLayer1, j, i)[1]

    for i in range(3):
            for j in range(3):
                matrix_r[i][j] = matrix[i][j][0]
    for i in range(3):
            for j in range(3):
                matrix_g[i][j] = matrix[i][j][1]
    for i in range(3):
            for j in range(3):
                matrix_b[i][j] = matrix[i][j][2]

def compute_pixel(src):
    #convolution matrices
    H1 = [[1,0,-1],
          [1,0,-1],
          [1,0,-1]]
    H2 = [[-1,-1,-1],
          [0,0,0],
          [1,1,1]]
    P = 0
    Q = 0
    for i in range(3):
        for j in range(3):
            P += H1[i][j]*src[i][j]
            Q += H2[i][j]*src[i][j]
    if P > 255:
        P = 255
    elif P < 0:
        P = 0
    if Q > 255:
        Q = 255
    elif Q < 0:
        Q = 0
    return max(P,Q)

def prewitt_algorithm(img, drawable, direction):
    # disable undo for the image
    img.undo_group_start()
    pdb.gimp_context_push()

    # copy the layer
    copyLayer1 = pdb.gimp_layer_new_from_visible(img, img, "BaseCopy")
    copyLayer2 = pdb.gimp_layer_new_from_visible(img, img, "BaseCopy")
    pdb.gimp_image_insert_layer(img, copyLayer1, None, -1)

    # desaturate and colorize the new layer
    # pdb.gimp_desaturate_full(copyLayer1, 1)
    # pdb.gimp_colorize(copyLayer1, 215, 11, 0)
    width, height = copyLayer1.width, copyLayer1.height
    out_pixel = pdb.gimp_drawable_get_pixel(copyLayer1, 0, 0)
    matrix = [[0]*3 for i in range(3)]
    r = [[0]*3 for i in range(3)]
    g = [[0]*3 for i in range(3)]
    b = [[0]*3 for i in range(3)]
    for i in range(height):
        for j in range(width):
            in_pixel = pdb.gimp_drawable_get_pixel(copyLayer2, j, i)[1]
            create_matrix(matrix, copyLayer2, i, j, width, height, r, g, b)
            alpha = in_pixel[3]
            out_r = compute_pixel(r)
            out_g = compute_pixel(g)
            out_b = compute_pixel(b)
            out_alpha = alpha;  # copy alpha
            out_pixel = (out_r, out_g, out_b, out_alpha)
            pdb.gimp_drawable_set_pixel(copyLayer1, j, i, 4, out_pixel)


    # enable undo again
    pdb.gimp_displays_flush()
    pdb.gimp_context_pop()
    img.undo_group_end()


register(
    "python-fu-prewitt-algorithm",
    N_("Apply a Prewitt convolution algorithm"),
    "Apply a Prewitt convolution algorithm.",
    "Ivan Afonin",
    "Ivan Afonin",
    "2024,2024",
    N_("_PrewittAlgorithm..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_STRING, "direction", "Prewitt compass gradient algorithm direction:", "Direction")
    ],
    [],
    prewitt_algorithm,
    menu="<Image>/Filters/Decor",
    domain=("gimp20-python", gimp.locale_directory)
)

main()