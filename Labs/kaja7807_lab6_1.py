from random import random
from random import uniform

from random import seed
from math import exp
#from math import max


# Tinklo su 2 sluoksniais klasė
# Idėjinis šaltinis: https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/ 
# Sigmoidė

def sigmoid(x):
    return 1.0/(1.0 + exp(-x))

def sigmoidoDifLygtis(y):
    return y*(1.0-y)

#-------------------------------------------------------------------

def ReLU(x):
    if x < 0:
       return 0
    else:
      return x

def ReLUDL(y):
    if y>0:
      return 1.0
    else:
      return 0.0

#-------------------------------------------------------------------

class Neuronas:
    def __init__(self, duomenu_dimensija):
       self.svoriu_sk = duomenu_dimensija + 1
       self.svoriai = [random() for i in range(self.svoriu_sk)]
       self.atsakas = None
       self.delta   = None
       
    def aktyvacija(self, duomenu_eilute):
       s_sk = self.svoriu_sk
       suma = self.svoriai[0]
       for i in range(1, s_sk):
          suma += self.svoriai[i] * duomenu_eilute[i-1] 
       return suma

    def skaiciuokAtsaka(self, duomenu_eilute):
       self.atsakas = sigmoid(self.aktyvacija(duomenu_eilute)) 
       #self.atsakas = ReLU(self.aktyvacija(duomenu_eilute)) 
       return self.atsakas

    def __str__(self):
       s = 'Neuronas: ' + str([float("{0:.3f}".format(x))  for x in self.svoriai])
       if self.atsakas != None:
           s = s + '; atsakas:    ' + str(float("{0:.3f}".format(self.atsakas)))
       if self.delta != None:
           s = s + '; delta:    ' + str(float("{0:.3f}".format(self.delta)))           
       return s

#-------------------------------------------------------------------
class Sluoksnis:
    def __init__(self, neuronu_skaicius, duomenu_dimensija):
       self.neuronu_sk = neuronu_skaicius
       self.neuronai = [Neuronas(duomenu_dimensija) for i in range(self.neuronu_sk)]
    
    def skaiciuokAtsaka(self, duomenu_eilute):
       for neur in self.neuronai:
          neur.skaiciuokAtsaka(duomenu_eilute)

    def __str__(self):
       s = 'sluoksnis: \n'
       for i in range(self.neuronu_sk):
          s =  s + str(self.neuronai[i]) + '\n'
       return s

#-------------------------------------------------------------------

class DuSluoksniai:
    def __init__(self, ivesciu_sk, pasleptu_sk, isvesciu_sk):
       self.tinklas=[]
       self.ivesciu_sk = ivesciu_sk
       self.isvesciu_sk = isvesciu_sk
       self.pasleptas = Sluoksnis(pasleptu_sk, ivesciu_sk)
       self.tinklas.append(self.pasleptas)
       self.isvesties = Sluoksnis(isvesciu_sk, pasleptu_sk)
       self.tinklas.append(self.isvesties)
    
    def skaiciuokAtsaka(self, duomenu_eilute):
       self.tinklas[0].skaiciuokAtsaka(duomenu_eilute)
       self.tinklas[1].skaiciuokAtsaka([neuronas.atsakas for neuronas in self.tinklas[0].neuronai])
    
    # Skaičiuojame deltas
    def skaiciuokDeltas(self, mokytojoAtsakymas):
        klaidos1 = [(mokytojoAtsakymas[i] - self.tinklas[1].neuronai[i].atsakas) for i in range(self.tinklas[1].neuronu_sk)]
        for j in range(self.tinklas[1].neuronu_sk):
            self.tinklas[1].neuronai[j].delta = klaidos1[j] * sigmoidoDifLygtis(self.tinklas[1].neuronai[j].atsakas)
	          #self.tinklas[1].neuronai[j].delta = klaidos1[j] * ReLUDL(self.tinklas[1].neuronai[j].atsakas)
        klaidos0 = list()
        for j in range(self.tinklas[0].neuronu_sk):
            klaida = 0.0
            for neuronas in self.tinklas[1].neuronai:
                klaida += neuronas.svoriai[j] * neuronas.delta
            klaidos0.append(klaida)
        for j in range(self.tinklas[0].neuronu_sk):
            self.tinklas[0].neuronai[j].delta = klaidos0[j] * sigmoidoDifLygtis(self.tinklas[0].neuronai[j].atsakas)

    # Koreguojame svorius
    def koreguokSvorius(self, duomenu_eilute, mokymo_parametras=0.5):
        for neuronas in self.tinklas[0].neuronai:
            for j in range(1,neuronas.svoriu_sk):
               neuronas.svoriai[j] += mokymo_parametras * neuronas.delta * duomenu_eilute[j-1]
            neuronas.svoriai[0] = mokymo_parametras * neuronas.delta
        
        ivestis1 = [neuronas.atsakas for neuronas in self.tinklas[0].neuronai]    
        for neuronas in self.tinklas[1].neuronai:
            for j in range(1,neuronas.svoriu_sk):
               neuronas.svoriai[j] += mokymo_parametras * neuronas.delta * ivestis1[j-1]
            neuronas.svoriai[0] = mokymo_parametras * neuronas.delta
    # Mokymas su nurodytais mokymo duomenų eilutėmis, m. parametru bei epochų skaičiumi 
    def mokymas(self, mokymoEilutes, mokymo_parametras, epochu_sk, arSpausdinti = False):
        #Mokymo eilutė sudaryta iš mokymo duomenų dalies ir mokytojo atsakymo  
        #Mokytojo atsakymo formatas: [0,0,0,..., 1, ...,0] - "1" toje vietoje, kur teisinga klasė  
        for epocha in range(epochu_sk):
           sumine_klaida = 0
           for eilute in mokymoEilutes:
              duomenu_eilute = eilute[0 : self.ivesciu_sk]
              mokytojoAtsakymas = eilute[self.ivesciu_sk:]
              self.skaiciuokAtsaka(duomenu_eilute)
              sumine_klaida += sum([(mokytojoAtsakymas[i]-self.tinklas[1].neuronai[i].atsakas)**2 for i in range(len(mokytojoAtsakymas))])
              self.skaiciuokDeltas(mokytojoAtsakymas)
              self.koreguokSvorius(duomenu_eilute, mokymo_parametras)
           if arSpausdinti:
              print('--> epocha=%d, m.parametras=%.3f, klaida=%.3f' % (epocha, mokymo_parametras, sumine_klaida))

    def prognozavimas(self, duomenu_eilute):
        self.skaiciuokAtsaka(duomenu_eilute)
        atsakymai = [neuronas.atsakas for  neuronas in self.tinklas[1].neuronai] 
        return atsakymai.index(max(atsakymai)) 


    #Spausdinimui: 
    def __str__(self):
       return '[ pasleptas ]->' + str(self.tinklas[0]) + '[ isvesties ]->' + str(self.tinklas[1])
####################################################################################################


seed(50)
ds = DuSluoksniai(2, 6, 4)
print(ds)

#Bandome mokyti NT tam, kad jis atsakytų į klausimą, kuriame ketvirtyje guli taškas (0,1,2,3) 
def ketvirtis(x,y):
   if (x >= 0) and (y >= 0):
       return 0
   if (x <= 0) and (y >= 0):
       return 1
   if (x <= 0) and (y <= 0):
       return 2
   if (x >= 0) and (y <= 0):
       return 3

#Ruošiame duomenis:
nr = 8
mokymoEilutes = list()
for i in range(nr):
   x = uniform(-2,2)
   y = uniform(-2,2)
   mok_ats = [0,0,0,0]
   mok_ats[ketvirtis(x,y)] = 1
   mokymoEilutes.append([x,y] + mok_ats)

print('Mokymo eilutes')
print(mokymoEilutes)
ds.mokymas(mokymoEilutes, 0.5, 100)

#Bandome įvertinti prognozavimo tikslumą:

teisingu = 0
pnr = 100
for i in range(pnr):
   x = uniform(-2,2)
   y = uniform(-2,2)
   if (ketvirtis(x,y) == ds.prognozavimas([x,y])):
      teisingu += 1
print("Turime prognozės tikslumą: " + str(teisingu * 1.0 / pnr))
print(ds)
