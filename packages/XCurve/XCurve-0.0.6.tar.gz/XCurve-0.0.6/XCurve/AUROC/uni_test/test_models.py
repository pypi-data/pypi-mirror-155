import pytest
import json
import sys
sys.path.append("./")
from easydict import EasyDict as edict


@pytest.mark.skip()
def load_json(dataset=None, model=None):
    with open('./uni_test/configs/base_config.json', 'r') as f:
        args = json.load(f)
        args = edict(args)

    if dataset is not None:
        with open('./uni_test/configs/datasets/%s.json'%dataset, 'r') as f:
            args.dataset.update(edict(json.load(f)))
    
    if model is not None:
        with open('./uni_test/configs/models/%s.json'%model, 'r') as f:
            args.model.update(edict(json.load(f)))

    return args

def test_model():
    from dataloaders import get_datasets
    from dataloaders import get_data_loaders
    from models import generate_net

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
        for model_type in ['mlp', 'resnet20', 'resnet18', 'densenet121']:
            args = load_json(dataset, model_type)
            if model_type == 'mlp':
                args.model.dim[0] = 3 * args.dataset.input_size[0] * args.dataset.input_size[1]
            model = generate_net(args.model).cuda()

            for i, (img, lbl) in enumerate(train_loader):
                img = img.cuda()
                lbl = lbl.cuda()
                out = model(img)
                assert out.shape == (img.shape[0], args.model.num_classes)                
                if (i+1)%4 == 0:
                    break

if __name__ == '__main__':
    test_model()
