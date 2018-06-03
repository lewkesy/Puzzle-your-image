import numpy as np
from IPython import embed
from PIL import Image
import os

####################################
#                                  #
# Here are what you need to change #
#                                  #
####################################


# path of images package for puzzle
path = "G:\\BaiduYunDownload\\animationCG\\"

# path of image needed to be puzzled
main_img_path = "122.bmp"

# path of saved image
save_img_path = "puzzled_img.bmp"

#Opacity
alpha = 0.9

#size of puzzled image
main_img_width = 1280
main_img_heigh = 720

#size of element images
part_img_width = 10
part_img_heigh = 10

#Just try to higher it when "Refreshing" comes out frequently
threshold = 60

###############################################

width_piece = int(main_img_width/part_img_width)
heigh_piece = int(main_img_heigh/part_img_heigh)

img_list = []
img_rgb_list = []
if_img_used = []


# init the name of imgs
def rename():
    count = 0
    for root, names, files in os.walk(path):
        for file in files:
            os.rename(os.path.join(path,file),os.path.join(path, str(count) + ".bmp"))
            count += 1


def clean_if_img_used():
    print("Refreshing……")
    for i in range(len(if_img_used)):
        if_img_used[i] = 0


def resize_img(im, type='main'):
    if type == 'main':
        im = im.resize((main_img_width, main_img_heigh))
    else:
        im = im.resize((part_img_width, part_img_heigh))
    return im


def cal_rgb(im):

    r_pixels = np.zeros((im.size[0], im.size[1]))
    g_pixels = np.zeros((im.size[0], im.size[1]))
    b_pixels = np.zeros((im.size[0], im.size[1]))

    for w in range(im.size[0]):
        for h in range(im.size[1]):
            pixel = im.getpixel((w, h))
            r_pixels[w][h] = pixel[0]
            g_pixels[w][h] = pixel[1]
            b_pixels[w][h] = pixel[2]

    rgb = {'r': r_pixels,
           'g': g_pixels,
           'b': b_pixels}

    return rgb


def load_all_imgs():
    count = 0
    for root, names, files in os.walk(path):
        for file in files:

            im = Image.open(path + file)
            im = resize_img(im, type='part')
            rgb = cal_rgb(im)

            img_list.append(im)
            img_rgb_list.append(rgb)
            if_img_used.append(0)
            count += 1
            print(count)


def cal_dist(rgb1, rgb2):
    r_dist = abs(rgb1['r'] - rgb2['r']).sum() / rgb1['r'].size
    g_dist = abs(rgb1['g'] - rgb2['g']).sum() / rgb1['g'].size
    b_dist = abs(rgb1['b'] - rgb2['b']).sum() / rgb1['b'].size

    dist = r_dist + g_dist + b_dist

    return dist/3


def match_part_img(part_main_im):

    min_dist = threshold
    min_position = 0
    checkpoint = True

    part_main_rgb = cal_rgb(part_main_im)

    for i in range(len(img_rgb_list)):
        dist = cal_dist(part_main_rgb, img_rgb_list[i])

        if dist < min_dist and if_img_used[i] == 0:
        # if dist < min_dist:
            min_dist = dist
            min_position = i
            checkpoint = False

    if checkpoint:
        clean_if_img_used()
        return match_part_img(part_main_im)
    else:
        if_img_used[min_position] = 1
        return min_position


if __name__ == '__main__':
    load_all_imgs()
    print("Loading finished!")

    main_img = Image.open(path + main_img_path)
    main_img = resize_img(main_img)

    count = 0
    for w in range(width_piece):
        for h in range(heigh_piece):
            box = (w * part_img_width, h * part_img_heigh, (w + 1) * part_img_width, (h + 1) * part_img_heigh)
            part_main_img = main_img.crop(box)
            num = match_part_img(part_main_img)

            main_img.paste(img_list[num], box)
            count += 1
            print(count)

    combined_img = main_img
    combined_img = combined_img.convert('RGBA')

    main_img = Image.open(path + main_img_path)
    main_img = resize_img(main_img, type='main')
    main_img = main_img.convert('RGBA')

    combined_img = Image.blend(main_img, combined_img, alpha)

    combined_img.show()
    combined_img.save(path + save_img_path)