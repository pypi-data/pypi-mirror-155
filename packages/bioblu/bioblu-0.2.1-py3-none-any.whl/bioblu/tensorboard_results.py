#!/usr/bin/env python3

import os
import tensorboard
import shutil
import subprocess
import webbrowser


def show_results(fpath):
    fpath = fpath.replace("file://", "")
    print(fpath)
    for file in sorted(os.listdir(fpath)):
        if file.endswith("tfevents"):
            print(f"Found tf events file: {file}")

    os.system(f"tensorboard --logdir={fpath}")
    os.system(f"firefox http://localhost:6006/")
    # webbrowser.get("firefox").open_new_tab("http://localhost:6006/")
    # webbrowser.open("http://localhost:6006/")


if __name__ == '__main__':


    FDIR = '/media/findux/DATA/Documents/Malta_II/radagast_transport/3303_2022-02-07_201522_on_dataset_01/'
    FDIR = "/home/findux/Desktop/tmp/2022-04-25_0002/"
    FDIR = "/media/findux/DATA/Documents/Malta_II/colab_outputs/2022-04-25_0002/"
    FDIR = "/media/findux/DATA/Documents/Malta_II/results/5239_2022-05-07_052041/"
    FDIR = "/media/findux/DATA/Documents/Malta_II/results/5763_2022-05-26_183938/"
    FDIR = "file:///media/findux/DATA/Documents/Malta_II/results/5767_2022-05-26_204302"
    FDIR = "/media/findux/DATA/Documents/Malta_II/results/5780_2022-05-27_174243/"
    FDIR = "/media/findux/DATA/Documents/Malta_II/results/5785_2022-05-29_011750/"
    show_results(FDIR)

    # then open http://localhost:6006/ in browser.