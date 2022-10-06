def nxywh2xywh(x, y, w, h, imgshape):
    ht = imgshape[0]
    wd = imgshape[1]
    pix_x = (x + w/2) * wd
    pix_y = (y + h/2) * ht
    new_w = w * wd
    new_h = h * ht
    return int(pix_x), int(pix_y), new_w, new_h

