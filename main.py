import zgzcw
import bilibili
import fzdm
import sys

if __name__ == '__main__':
    print(sys.argv)
    if (sys.argv[1] == "zgzcw"):
        m =  zgzcw.Zgzcw()
    elif (sys.argv[1] == "bilibili"):
        m = bilibili.Bilibili()
    elif (sys.argv[1] == "fzdm"):
        m = fzdm.Fzdm()
    m.run()