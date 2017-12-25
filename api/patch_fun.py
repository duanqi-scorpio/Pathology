import slide_fun
import config_fun
import json
import extract_path_fun
import os
from tqdm import tqdm

def _prepare_patch(data, auto_save_patch = True):
    patches = []
    for idx, item in enumerate(tqdm(data)):
        patch = []
        if 'tumor' in item['info']:
            patch = extract_path_fun.extract(item, 'pos', auto_save_patch = auto_save_patch)
        else:
            patch = extract_path_fun.extract(item, 'neg', auto_save_patch = auto_save_patch)
        patches.append({'data': item['data'][0],
                        'info': item['info'], 'patch':patch})
        print('get patches from %s, pos:%d, neg:%d\n'%
              (os.path.basename(item['data'][0]), len(patch['pos']), len(patch['neg'])))
    return patches


def generate_patch(auto_save_patch = True):
    cfg = config_fun.config()
    with open(cfg.split_file) as f:
        split_data = json.load(f)

    train_data = filter(lambda item: item['info'] == 'train_tumor' or
                                    item['info'] == 'train_normal', split_data)
    val_data   = filter(lambda item: item['info'] == 'val_tumor' or
                                    item['info'] == 'val_normal', split_data)
    test_data  = filter(lambda item: item['info'] == 'test_tumor' or
                                    item['info'] == 'test_normal', split_data)

    train_patch = _prepare_patch(train_data, auto_save_patch = auto_save_patch)
    val_patch = _prepare_patch(val_data, auto_save_patch = auto_save_patch)

