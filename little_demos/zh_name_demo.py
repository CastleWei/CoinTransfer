from pprint import pprint

d = dict(
    名称='以太坊',
    交易手续费比例=0.002,
    提现手续费定额=0.003
)

print(d)
pprint(d)
print(d['交易手续费比例'])

def 测试(参数):
    变量 = '锟斤拷' + 参数
    print(type(变量))
    print(len(变量))
    print(变量)

    for 字 in 变量:
        print(字,',')

if __name__ == '__main__':
    测试('参数')
    
