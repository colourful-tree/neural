from numpy import *
import random

def initNet(inDim,hiddenDim,outDim):
    global input2hidden,hidden2output
    input2hidden = array([random.uniform(-1/inDim**0.5,1/inDim**0.5) for i in range(inDim*hiddenDim)]).reshape(inDim,hiddenDim)
    hidden2output = array([random.uniform(-1/hiddenDim**0.5,1/hiddenDim**0.5) for i in range(hiddenDim*outDim)]).reshape(hiddenDim,outDim)

def sigmod(x):
    return ones(x.size)/(ones(x.size)+e**(zeros(x.size) - x))

def forward(x):
    global input2hidden,hidden2output
    global inDim, hiddenDim, outDim
    input = array(x).reshape(1, inDim)
    hidden = sigmod(dot(input, input2hidden))
    #hidden = dot(input, input2hidden)
    output = sigmod(dot(hidden, hidden2output))
    #print input, hidden, output
    return input, hidden, output

def loadData():
    global data_in,data_in
    with open("data.txt","r") as fin:
        for i in fin:
            line = i.strip().split(",")
            data_in.append([float(i) for i in line[:4]])
            if line[4] == "Iris-setosa":
                data_out.append([1,0,0])
            elif line[4] == "Iris-versicolor":
                data_out.append([0,1,0])
            else:
                data_out.append([0,0,1])
def cal_loss(target,out):
    return dot((target - out),(target-out).transpose())

def print_loss():
    global loss
    for i in range(len(loss)):
        if i % 10 == 0:
            print loss[i]

def testP():
    total = len(data_in)
    cnt = 0.0
    for i in range(total):
        res = forward(data_in[i])[2].argmax(axis=1)
        if data_out[i][res[0]] == 1:
            cnt += 1
    return cnt/total
    
data_in = []
data_out = []

max_epoch = 200
step = 0.05

input2hidden = None
hidden2output = None
loss = []
inDim, hiddenDim, outDim = 4, 10, 3
initNet(inDim,hiddenDim,outDim)
loadData()

for i in range(max_epoch):
    loss_epoch = 0
    for data in range(len(data_in)):
        input, hidden, output = forward(data_in[data])
        loss_epoch += cal_loss(data_out[data],output)
        # w* = w + n * input * (T-out)
        # h2o
        for n in range(hiddenDim):
            fx1_fx = output * (ones(outDim) - output)
            #print fx1_fx
            hidden2output[n,:] += step * dot(hidden[:,n],(array(data_out[data]) - output)) * fx1_fx[0]
        #print "---"
        # w* = w + n * input * ()
        # i2h
        for n in range(inDim):
            tmp = dot(hidden2output, (array(data_out[data]) - output).transpose())
            #print hidden       
            fx1_fx = hidden * (ones(hiddenDim) - hidden)
            #print fx1_fx[0]
            #print step * dot(input[:,n], tmp.transpose())
            input2hidden[n,:] += step * dot(input[:,n], tmp.transpose()) * fx1_fx[0]
    loss.append(loss_epoch)


print testP()
print_loss()
#print forward([6.3,3.4,5.6,2.4])[2]
#print forward([6.3,3.4,5.6,2.4])[2].argmax(axis=1)
