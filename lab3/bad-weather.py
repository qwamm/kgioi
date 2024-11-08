from gimpfu import *
import time

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def bw(img, drawable, blur, brightAdjust, contrastAdjust):
    
    # disable undo for the image
    img.undo_group_start()
    pdb.gimp_context_push()

    # copy the layer
    copyLayer1 = pdb.gimp_layer_new_from_visible(img, img, "BaseCopy")
    pdb.gimp_image_insert_layer(img, copyLayer1, None, -1)

    # desaturate and colorize the new layer
    # pdb.gimp_desaturate_full(copyLayer1, 1)
    # pdb.gimp_colorize(copyLayer1, 215, 11, 0)

    pdb.gimp_drawable_brightness_contrast(copyLayer1, brightAdjust, contrastAdjust)

    # blur the shadow layer
    pdb.plug_in_gauss_iir(img, copyLayer1, blur, True, True)

    # enable undo again
    pdb.gimp_displays_flush()
    pdb.gimp_context_pop()
    img.undo_group_end()




register(
    "python-fu-bad-weather",
    N_("Add a bad weather effect"),
    "Adds a bad weather effect on image.",
    "Ivan Afonin",
    "Ivan Afonin",
    "2024,2024",
    N_("_BadWeather..."),
    "RGB*, GRAY*",
    [
        (PF_IMAGE, "image",       "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
        (PF_SLIDER, "blur", _("_Shadow blur"), 6, (1, 30, 1)),
        (PF_SLIDER, "brightAdjust", "Brightness", 0.4, (-0.5, 0.5, 0.1)),
        (PF_SLIDER, "contrastAdjust", "Contrast", 0.3, (-0.5, 0.5, 0.1))
    ],
    [],
    bw,
    menu="<Image>/Filters/Decor",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()