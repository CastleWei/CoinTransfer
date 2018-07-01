from time import sleep

n=1
def nstr(n):
    s='__%06d__, '%n
    return s*10

while True:
    with open('output/out.txt', 'wt') as f:
        f.write(nstr(n))
    print(n)
    n+=1
    sleep(0.1)
