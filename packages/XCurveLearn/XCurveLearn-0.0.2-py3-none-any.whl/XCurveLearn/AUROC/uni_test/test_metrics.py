import pytest
import sys
sys.path.append("./")
import torch


@pytest.mark.skip()
def gen_data(num_classes):
    y_true = torch.randint(0, num_classes, (256, 1)).numpy()
    if num_classes == 2:
        y_pred = torch.randn((256, 1))
        y_pred = torch.sigmoid(y_pred).numpy()
    else:
        y_pred = torch.randn((256, num_classes))
        y_pred = torch.softmax(y_pred, dim=1).numpy()
    return y_true, y_pred

def test_metrics():
    from metrics import AUC
    from metrics import p2AUC

    eps = 1e-4
    for num_classes in range(3,10):
        for i in range(20):
            y_true, y_pred = gen_data(num_classes)
            # print(y_true, y_pred)
            auc_ovo = AUC(y_true, y_pred, 'ovo', acc=False)
            auc_ova = AUC(y_true, y_pred, 'ova', acc=False)
            auc_ovo_acc = AUC(y_true, y_pred, 'ovo', acc=True)
            assert abs(auc_ovo - auc_ovo_acc) < eps, \
                'auc: %.2f, auc_acc: %.2f'%(auc_ovo, auc_ovo_acc)

    for i in range(20):
        y_true, y_pred = gen_data(2)
        auc_ovo = AUC(y_true, y_pred, 'ovo', acc=False)
        pauc_03 = p2AUC(y_true, y_pred, 1, 0.3)
        pauc_06 = p2AUC(y_true, y_pred, 1, 0.6)
        pauc_10 = p2AUC(y_true, y_pred, 1, 1.0)
        p2auc_03 = p2AUC(y_true, y_pred, 0.3, 0.3)
        p2auc_06 = p2AUC(y_true, y_pred, 0.6, 0.6)

        assert abs(auc_ovo - pauc_10) < eps
        assert pauc_03 <= pauc_06 <= pauc_10
        assert p2auc_03 <= pauc_03
        assert p2auc_06 <= pauc_06
        assert p2auc_03 <= p2auc_06

if __name__ == '__main__':
    test_metrics()
