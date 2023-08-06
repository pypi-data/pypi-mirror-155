import pytest
import json
import sys
sys.path.append("./")
from easydict import EasyDict as edict
import torch


@pytest.mark.skip()
def load_json(dataset=None, loss=None):
    with open('./uni_test/configs/base_config.json', 'r') as f:
        args = json.load(f)
        args = edict(args)

    if dataset is not None:
        with open('./uni_test/configs/datasets/%s.json'%dataset, 'r') as f:
            args.dataset.update(edict(json.load(f)))
    
    if loss is not None:
        with open('./uni_test/configs/losses/%s.json'%loss, 'r') as f:
            args.training.update(edict(json.load(f)))

    return args

def test_losses_type():
    '''
        check if the loss function type is correct
    '''
    from losses import (get_losses, SquareAUCLoss, \
          HingeAUCLoss, ExpAUCLoss, PAUCLoss)

    for loss_type in ['SquareAUCLoss', 'ExpAUCLoss', 'HingeAUCLoss', 'OPAUCLoss', 'TPAUCLoss']:
        args = load_json(loss=loss_type)
        criterion = get_losses(args.training)
        assert type(criterion) == eval(args.training.loss_type)

def test_losses_decrese():
    '''
        check if the loss can drop normally
    '''
    from dataloaders import get_datasets
    from dataloaders import get_data_loaders
    from models import generate_net
    from losses import get_losses

    for dataset in ['cifar-10-long-tail', 'tiny-imagenet-200']:
        args = load_json(dataset)
        train_set, val_set, test_set = get_datasets(args.dataset)
        train_loader, val_loader, test_loader = get_data_loaders(
            train_set,
            val_set,
            test_set,
            32,
            32
        )
        for loss_type in ['SquareAUCLoss', 'ExpAUCLoss', 'HingeAUCLoss', 'OPAUCLoss', 'TPAUCLoss']:
            args = load_json(dataset, loss_type)
            model = generate_net(args.model).cuda()
            criterion = get_losses(args.training)
            optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

            train_loss = []
            for i, (img, lbl) in enumerate(train_loader):
                img = img.cuda()
                lbl = lbl.cuda()
                out = model(img)
                if out.shape[1] == 1:
                    out = torch.sigmoid(out)
                else:
                    out = torch.softmax(out, dim=1)

                loss = criterion(out, lbl)
                train_loss.append(loss.item())
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                if (i+1)%100 == 0:
                    break

            assert sum(train_loss[:10]) > sum(train_loss[-10:]), train_loss

if __name__ == '__main__':
    test_losses_type()
    test_losses_decrese()
