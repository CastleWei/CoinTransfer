inf = dict(
    key='$eth',
    交易手续费比例=0.002,
    提现手续费定额=0.003,
    update_time=0,
    卖盘=[(1,2),(3,4)],
    买盘=[(1,2),(3,4)],
    卖1=0,
    买1=3
)
try:
    assert inf['卖盘'][0][0] > 0
    assert inf['买盘'][0][1] > 0
    assert inf['卖1'] > 0
    assert inf['买1'] > 0
except (KeyError, TypeError, AssertionError) as e:
    print('catched', e.__class__.__name__, e)