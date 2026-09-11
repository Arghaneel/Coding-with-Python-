class complex:
    def _init_(self,realp = 0 , imagp = 0):
        self.realp = realp
        self.imagp = imagp
    def setComplex(self,realp, imagp):
        self.realp = realp
        self.imagp = imagp
    def readComplex(self):
        self.realp = int(input("enter the real part:"))
        self.imagp = int(input("enter the imaginary part:"))
    def showComplex(self):
        print(self.realp,"i",self.imagp)
    def addcomplex(self,c2):
        c3 = complex()
        c3.realp = self.realp + c2.realp
        c3.imagp = self.imagp + c2.imagp
        return c3
def add2complex(a,b):
        return a.addcomplex(b)
 
def main():
        c1 = complex(1,5)
        c2 = complex(2,6)
        c1.showComplex()
        c2.showComplex()

        c3 = add2complex(c1,c2)
        c3.showComplex()

        n = int(input("enter the number of comolex numebers for the list:"))
        complist = []

        for i in range(n):
             print("object ", i + 1)
             obj = complex()
             obj.readComplex()
             complist.append(obj)
        for obj in complist:
             obj.showComple()
        sumcomp = complex()
        for obj in complist:
             sumcomp = add2complex(sumcomp,obj)
             sumcomp.showComple()
        
if __name__ == "_main_":
     main()


        
