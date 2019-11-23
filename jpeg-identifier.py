#!/usr/bin/python
import os
import sys

print('Aplikasi Identifikasi file JPEG')
print('dengan model Deterministic Finite State Automata (DFSA)')
print('================================================================')
print('Silakan ketikkan lokasi/path file yang akan diidentifikasi..')
file = input('File path : ')

def getSize(filename):
    st = os.stat(filename)
    return st.st_size

fsize = getSize(file)

sys.setrecursionlimit(fsize)

rlimit = sys.getrecursionlimit()
fhead = False
ffoot = False

fh = open(file, 'rb')

def main():
    try:
        state = 'start'
        byte = fh.read(1).hex()
        ofs = 0
        while byte != "":
            if(state=='start'):
                state = 'q0'
                
            if(state=='q0'):
                q = Q0(byte)
                if(q == True):
                    state = 'q1'
                    #print('[' + byte + '] -> Q0(' + byte + ') -> Q1')
                else:
                    state = 'q0'
                    fhead = False
                    #print('[' + byte + '] -> Q0(' + byte + ') -> Q0')
            elif(state=='q1'):
                q = Q1(byte)
                if(q == True):
                    state = 'q2'
                    #print('[' + byte + '] -> Q1(' + byte + ') -> Q2')
                else:
                    state = 'q0'
                    fhead = False
                    #print('[' + byte + '] -> Q1(' + byte + ') -> Q0')
            elif(state=='q2'):
                q = Q2(byte)
                if(q == True):
                    state = 'q3'
                    fhead = True
                    print('[' + byte + '] -> Q2(' + byte + ') -> Q3' + '(JPEG header ditemukan pada offset ' + str(format(ofs, '02x')) + '.)')
                else:
                    state = 'q0'
                    fhead = False
                    #print('[' + byte + '] -> Q2(' + byte + ') -> Q0')
            elif(state=='q3'):
                q = Q3(byte)
                if(q == True):
                    state = 'q4'
                    #print('[' + byte + '] -> Q3(' + byte + ') -> Q4')
                else:
                    state = 'q3'
                    ffoot = False
                    #print('[' + byte + '] -> Q3(' + byte + ') -> Q3')
            elif(state=='q4'):
                q = Q4(byte)
                if(q == True):
                    state = 'q5'
                    ffoot = True
                    print('[' + byte + '] -> Q4(' + byte + ') -> Q5' + '(JPEG footer ditemukan pada offset ' + str(format(ofs, '02x')) + '.)')
                else:
                    state = 'q3'
                    ffoot = False
                    #print('[' + byte + '] -> Q4(' + byte + ') -> Q3')
                    
            byte = fh.read(1).hex()
            ofs += 1
    finally:
        fh.close
        print('<<< EoF >>> : ' + str(format(ofs-1, '02x')))
        if(fhead == True and ffoot == True):
            print('Result : File JPEG teridentifikasi!')
        else:
            print('Result : Tidak ada file JPEG yang teridentifikasi!')
    fh.close()

def Q0(byte):
    if(byte == 'ff'):
        return True
    else:
        return False

def Q1(byte):
    if(byte=='d8'):
        return True
    else:
        return False

def Q2(byte):
    if(byte == 'ff'):
        return True
    else:
        return False

def Q3(byte):
    if(byte == 'ff'):
        return True
    else:
        return False

def Q4(byte):
    if(byte == 'd9'):
        return True
    else:
        return False

    
if __name__ == "__main__":
        main()
