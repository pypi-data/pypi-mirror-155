import pytest
import json
import sys
sys.path.append("./")
from easydict import EasyDict as edict


@pytest.mark.skip()
def load_json(dataset=None):
    with open('XCurveOpt/AUROC/uni_test/configs/base_config.json', 'r') as f:
        args = json.load(f)
        args = edict(args)

    if dataset is not None:
        with open('XCurveOpt/AUROC/uni_test/configs/datasets/%s.json'%dataset, 'r') as f:
            args.dataset.update(edict(json.load(f)))

    return args.dataset

def test_resampler():
    from XCurveOpt.AUROC.dataloaders import get_datasets
    from XCurveOpt.AUROC.dataloaders.base_dataset import (EmptyResampler, TLResampler, IHTResampler, 
            NMResampler, BSResampler, ADAResampler)

    resampler_type_2_cls = {
        'None': EmptyResampler,
        'TL': TLResampler,
        'IHT': IHTResampler,
        'NM': NMResampler,
        'BS': BSResampler,
        'ADA': ADAResampler
    }

    args = load_json()
    for rs_type in resampler_type_2_cls.keys():
        args.resampler_type = rs_type
        train_set, val_set, test_set = get_datasets(args)
        assert train_set.resampler == resampler_type_2_cls[args.resampler_type]
        assert val_set.resampler == EmptyResampler
        assert test_set.resampler == EmptyResampler

def test_single_dataset():
    from XCurveOpt.AUROC.dataloaders import get_datasets

    for dataset in ['debug_data_npy']:
        args = load_json(dataset)
        train_set, val_set, test_set = get_datasets(args)
        
        img, lbl = train_set.__getitem__(0)
        assert img.shape == (3, args.input_size[0], args.input_size[1])

def test_dataloader_binary_cls():
    from XCurveOpt.AUROC.dataloaders import get_datasets
    from XCurveOpt.AUROC.dataloaders import get_data_loaders

    for dataset in ['debug_data_npy']:
        args = load_json(dataset)
        train_set, val_set, test_set = get_datasets(args)
        train_loader, val_loader, test_loader = get_data_loaders(
            train_set,
            val_set,
            test_set,
            32,
            32
        )

        for i, (img, lbl) in enumerate(train_loader):
            assert img.shape[1:] == (3, args.input_size[0], args.input_size[1])
            assert img.shape[0] == lbl.shape[0]
            assert len(lbl.shape) == 1, lbl.shape
            assert lbl.max() == 1 and lbl.min() == 0
            if (i+1)%10 == 0:
                break

def test_dataloader_multi_cls():
    from XCurveOpt.AUROC.dataloaders import get_datasets
    from XCurveOpt.AUROC.dataloaders import get_data_loaders

    for dataset in ['debug_data_npy']:
        args = load_json(dataset)
        train_set, val_set, test_set = get_datasets(args)
        train_loader, val_loader, test_loader = get_data_loaders(
            train_set,
            val_set,
            test_set,
            32,
            32
        )

        for i, (img, lbl) in enumerate(train_loader):
            assert img.shape[1:] == (3, args.input_size[0], args.input_size[1])
            assert img.shape[0] == lbl.shape[0]
            assert len(lbl.shape) == 1
            assert lbl.max() == max(list(args.class2id.values())) and lbl.min() == 0
            if (i+1)%10 == 0:
                break

if __name__ == '__main__':
    test_resampler()
    test_single_dataset()
    test_dataloader_binary_cls()
    test_dataloader_multi_cls()
