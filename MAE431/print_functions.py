def printTemperatures(T,title=''):
    print()
    print('--------------------')
    print(title)
    print('--------------------')
    print('Node\t | T(K)')
    print('--------------------')
    for n,temp in enumerate(T):
        print(str(n+1),'\t | ',round(temp[0],1))
        print('--------------------')
    print()

def exportTemperatures(T,name=''):
    csv = open('temperatures_' + name + '.csv','w')
    csv.write('Node;T(K)\n')
    for n,temp in enumerate(T):
        csv.write(str(n+1)+';'+str(round(temp[0],1))+'\n')
