import numpy as np

# https://support.pix4d.com/hc/en-us/articles/202977149-What-does-the-Output-Params-Folder-contain#label3

def read_camparams(path):
    """Reads "<...>_calibrated_camera_parameters.txt"  Pix4D output
        camera parameters and stores them in a dictionary.
        Parsing the text file depends on the line-by-line contents of the file."""
    with open(path, "r") as f:
            res = [line.strip() for line in f.readlines()[8:]] #data starts on line 8
    data_list = []
    counter = 0

    for idx, re in enumerate(res):
        data = dict()
        res_copy = res.copy()
        image_data = res_copy[counter:counter+10]
            
        line_0 = image_data[0].split(" ")
        data["fileName"] = line_0[0]
        data["imageWidth"] =  np.uint16(line_0[1])
        data["imageHeight"] = np.uint16(line_0[2])
        
        cam_matrix_1x3 = [np.float64(x) for x in image_data[1].split(" ")]
        cam_matrix_2x3 = [np.float64(x) for x in image_data[2].split(" ")]
        cam_matrix_3x3 = [np.float64(x) for x in image_data[3].split(" ")]
        data["camera_matrix_K"] = np.array([cam_matrix_1x3, cam_matrix_2x3, cam_matrix_3x3])
        data["radial_distortion"] =  [np.float64(x) for x in image_data[4].split(" ")]
        data["tangential_distortion"] = [np.float64(x) for x in image_data[5].split(" ")]
        data["camera_position_t"] = [np.float64(x) for x in image_data[6].split(" ")]
        data["camera_rotation_R"] = [np.float64(x) for x in image_data[7].split(" ")]
        data["camera_model_m"] = [np.float64(x) for x in image_data[8].split(" ")]
        data_list.append(data)
        
        counter += 10
        if counter +1 > len(res):
            break
    return data_list

def read_internal_camparams(path):
    """Reads "<...>_calibrated_internal_camera_parameters.cam Pix4D output
        internal camera parameters and stores them in a dictionary.
        Parsing the text file depends on the line-by-line contents of the file."""

    with open(path, "r") as f:
        res = [line.strip() for line in f.readlines()]
    data = dict()
    prev_re = ""
    for re in res:
        if "camera_calibration_file " in re:
            data["camera_calibration_file"] = int(re.split("camera_calibration_file ")[1])
        if "#Focal Length (mm) assuming a sensor width of " in re:
            sensor_width = re.split("#Focal Length (mm) assuming a sensor width of ")[1]
            sensor_width_w = sensor_width.split("x")[0]
            sensor_width_l = sensor_width.split("x")[1].strip("mm")
            data['sensor_width_w'] = np.float64(sensor_width_w)
            data["sensor_width_l"] = np.float64(sensor_width_l)
            continue
        if "#Image size " in re:
            imgsize = re.split("#Image size ")[1].split("x")
            image_size_w_pix = imgsize[0]
            image_size_l_pix = imgsize[1].split(" ")[0]
            data['image_size_w_pix'] = np.float64(image_size_w_pix)
            data['image_size_l_pix'] = np.float64(image_size_l_pix)
            continue
        if "FOCAL" in re:
            focal = np.float64(re.split(" ")[1])
            data["focal"] = focal
            continue
        if "#Principal Point Offset xpoff ypoff in mm" in prev_re:
            if "XPOFF" in re:
                data["xpoff_mm"] = np.float64(re.split("XPOFF")[1])
                continue
        if "xpoff_mm" in data and "ypoff_mm" not in data:     
            if "YPOFF" in re:
                data["ypoff_mm"] = np.float64(re.split("YPOFF")[1])
                continue
        if "#Principal Point Offset xpoff ypoff in pixel" in prev_re:
            if "XPOFF" in re:
                data["xpoff_pix"] = np.float64(re.split("XPOFF")[1])
                continue
        if "xpoff_pix" in data and "ypoff_pix" not in data:
            data["ypoff_pix"] = np.float64(re.split("YPOFF")[1])
            continue
        prev_re = re
    return data

def read_external_camparams(path):
    """ Reads <...>_calibrated_external_camera_parameters.txt file generated
        by Pix4D. """
    with open(path, "r") as f:
        res = [line.strip() for line in f.readlines()[1:]]
    data_list = []
    for line in res:
        line = line.split(" ")
        data = dict()
        data["imageName"] = line[0]
        data["X"] = np.float64(line[1])
        data["Y"] = np.float64(line[2])
        data["Z"] = np.float64(line[3])
        data["Omega"] = np.float64(line[4])
        data["Phi"] = np.float64(line[5])
        data["Kappa"] = np.float64(line[6])
        data_list.append(data)
    return data_list

def read_pix4d_internal_camparams(path):
    with open(path, "r") as f:
        res = [line.strip() for line in f.readlines()]
    
    data = dict()
    data["camera_calibration_file"] = np.float64(res[0].split(" ")[-1])
    data["F"] = np.float64(res[2].split(" ")[1])
    data["Px"] = np.float64(res[4].split(" ")[1])
    data["Py"] = np.float64(res[5].split(" ")[1])
    data["K1"] = np.float64(res[7].split(" ")[1])
    data["K2"] = np.float64(res[8].split(" ")[1])
    data["K3"] = np.float64(res[9].split(" ")[1])
    data["T1"] = np.float64(res[11].split(" ")[1])
    data["T2"] = np.float64(res[12].split(" ")[1])
        
    return data


def read_camera(path):
    """ Reads <...>_camera.ssk file generated
        by Pix4D. """
    with open(path, "r") as f:
        res = [line.strip() for line in f.readlines()]

    keys = [line.split(":")[0] for line in res[1:-1]]
    data = dict()
    for key, line in zip(keys, res[1:-1]):
        line = line.split(":")
        line = [x.strip(" ") for x in line][1].split(" ")
        line = list(filter(None, line))
        data[key] = list(map(np.float64,line)) if len(line) > 1 else line[0]
    return data

def read_pmatrix(path):
    with open(path, "r") as f:
        res = [line.strip() for line in f.readlines()]
    res[0].split(" ")
    data_list = []
    for re in res:
        data = dict()
        imgdata = re.split(" ")
        data["fileName"] = imgdata[0]
        row1 = [np.float(x) for x in imgdata[1:5]]
        row2 = [np.float(x) for x in imgdata[5:9]]
        row3 = [np.float(x) for x in imgdata[9:13]]

        data["pmatrix"] = np.array((row1, row2, row3))
        data_list.append(data)
    return data_list
