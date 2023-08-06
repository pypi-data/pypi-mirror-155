# from matplotlib.pyplot import get
import pystripe
import os
# from pprint import pprint
import configparser
from pathlib import Path
import csv
# import asyncio
# import argparse
# from argparse import RawDescriptionHelpFormatter
# from pathlib import Path
import os
# import numpy as np
# from scipy import fftpack, ndimage
# from skimage.filters import threshold_otsu
# import tifffile
# import imageio as iio
# import pywt
import multiprocessing
# import tqdm
# from dcimg import DCIMGFile
# from pystripe import raw
# from pystripe.lightsheet_correct import correct_lightsheet
# import warnings
# warnings.filterwarnings("ignore")
import time


def get_configs(config_path):
    config = configparser.ConfigParser()   
    config.read(config_path)
    return config

def run_pystripe(dir, configs):
    input_path = Path(dir['path'])
    output_path = Path(dir['output_path'])
    sig_strs = dir['metadata']['Destripe'].split('/')
    sigma = list(int(sig_str) for sig_str in sig_strs)
    workers = int(configs['params']['workers'])
    chunks = int(configs['params']['chunks'])

    pystripe.batch_filter(input_path,
                output_path,
                workers=workers,
                chunks=chunks,
                sigma=sigma,
                auto_mode=True)

    rename_images(dir)

def rename_images(dir):
    output_path = dir['output_path']
    input_path = dir['path']
    file_path = os.path.join(output_path, 'destriped_image_list.txt')
    with open(file_path, 'r') as f:
        image_list = f.readlines()
        f.close()
    os.remove(file_path)
    for image in image_list:
        image = image.strip()
        try:
            os.rename(image, os.path.splitext(image)[0] + '.orig')
        except:
            pass

def get_acquisition_dirs(input_dir, output_dir):
    ac_dirs = []
    for (root,dirs,files) in os.walk(input_dir):
        if 'metadata.txt' in files:
            ac_dirs.append({
                'path': root,
                'output_path': os.path.join(output_dir, os.path.relpath(root, input_dir))
            })
    for dir in ac_dirs:
        get_metadata(dir)

    unfinished_dirs = []
    for dir in ac_dirs:
        if in_progress(dir):
            unfinished_dirs.append(dir)

    return unfinished_dirs

def pair_key_value_lists(keys, values):
    d = {}
    for i in range(0, len(keys)):
        key = keys[i]
        val = values[i]
        if key != '':
            d[key] = val
    return d

def get_metadata(dir):
    metadata_path = os.path.join(dir['path'], 'metadata.txt')

    metadata_dict = {
        'channels': [],
        'tiles': []
    }
    sections = {
        'channel_vals': [],
        'tile_vals': []
    }
    with open(metadata_path, encoding="utf8", errors="ignore") as f:
        reader = csv.reader(f, dialect='excel', delimiter='\t')
        section_num = 0
        for row in reader:
            if section_num == 0:
                sections['gen_keys'] = row
                section_num += 1
                continue
            if section_num == 1:
                sections['gen_vals'] = row
                section_num += 1
                continue
            if section_num == 2:
                sections['channel_keys'] = row
                section_num += 1
                continue
            if section_num == 3:
                if row[0] != 'X':
                    sections['channel_vals'].append(row)
                    continue
                else:
                    sections['tile_keys'] = row
                    section_num += 2
                    continue
            if section_num == 5:
                sections['tile_vals'].append(row)
        f.close()

    d = pair_key_value_lists(sections['gen_keys'], sections['gen_vals'])
    metadata_dict.update(d)

    for channel in sections['channel_vals']:
        d = pair_key_value_lists(sections['channel_keys'], channel)
        metadata_dict['channels'].append(d)

    for tile in sections['tile_vals']:
        d = pair_key_value_lists(sections['tile_keys'], tile)
        metadata_dict['tiles'].append(d)
    
    dir['metadata'] = metadata_dict
    dir['target_number'] = get_target_number(dir)

def in_progress(dir):
    destripe_tag = dir['metadata']['Destripe']
    return 'D' not in destripe_tag and 'A' not in destripe_tag

def get_target_number(dir):
    skips = list(int(tile['Skip']) for tile in dir['metadata']['tiles'])
    return sum(skips) * int(dir['metadata']['Z_Block']) / int(dir['metadata']['Z step (m)'])

def finish_directory(dir):
    # prepend 'D' to 'Destripe' label in metadata.txt
    metadata_path = os.path.join(dir['path'], 'metadata.txt')
    with open(metadata_path, encoding="utf8", errors="ignore") as f:
        reader = csv.reader(f, dialect='excel', delimiter='\t')
        line_list = list(reader)
        f.close()
    os.remove(metadata_path)
    destripe = line_list[1][6]
    line_list[1][6] = 'D' + destripe
    with open(metadata_path, 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel', delimiter='\t')
        for row in line_list:
            writer.writerow(row)
        f.close()

    # prepend 'DST_' to output directory name
    output_split = os.path.split(dir['output_path'])
    new_dir_name = 'DST_' + output_split[1]
    new_path = os.path.join(output_split[0], new_dir_name)
    try:
        os.rename(dir['output_path'], new_path)
    except:
        pass

    # convert .orig images to .tiff
    for (root,dirs,files) in os.walk(dir['path']):
        for file in files:
            if Path(file).suffix == '.orig':
                file_path = os.path.join(root, file)
                base = os.path.splitext(file_path)[0]
                os.rename(file_path, base + '.tiff')

def update_status(ac_dirs):
    current_dirs = []
    for dir in ac_dirs:
        extensions = pystripe.core.supported_extensions
        dir['unprocessed_images'] = []
        orig_images = []
        processed_images = []

        # get lists of processed and unprocessed images in input directory and processed images in output directory
        for (root,dirs,files) in os.walk(dir['path']):
            for file in files:
                if Path(file).suffix in extensions:
                    dir['unprocessed_images'].append(os.path.join(root, file))
                elif Path(file).suffix == '.orig':
                    orig_images.append(file)
        for (root, dirs, files) in os.walk(dir['output_path']):
            for file in files:
                if Path(file).suffix in extensions:
                    processed_images.append(file)

        if len(processed_images) >= dir['target_number']:
            finish_directory(dir)
        else:
            current_dirs.append(dir)
    return current_dirs

def look_for_images(input_dir, output_dir, configs):
    counter = 0
    procs = []
    while True:
        counter += 1
        time.sleep(1)
            
        acquisition_dirs = get_acquisition_dirs(input_dir, output_dir)
        acquisition_dirs = update_status(acquisition_dirs)

        if any(p.is_alive() for p in procs):
            continue
        
        if len(acquisition_dirs) == 0:
            print('\n{}\nNo images to be processed\n'.format(counter))
            continue

        acquisition_dirs.sort(key=lambda x: x['path'])
        dir = acquisition_dirs[0]
        print(
            '\n{}\nQueue: {}\nNext to be destriped: {}\nImages to process: {}\n'.format(
                counter,
                list(dir['path'] for dir in acquisition_dirs),
                acquisition_dirs[0]['path'],
                acquisition_dirs[0]['unprocessed_images']
            )
        )
        if len(dir['unprocessed_images']) > 0:
            p = multiprocessing.Process(target=run_pystripe, args=(dir, configs))
            procs.append(p)
            p.start()

def main():
    config_path = 'config.ini'
    configs = get_configs(config_path)
    input_dir = Path(configs['paths']['input_dir'])
    output_dir = Path(configs['paths']['output_dir'])

    look_for_images(input_dir, output_dir, configs)

if __name__ == "__main__":
    main()