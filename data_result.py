import numpy as np
import pandas as pd

model_parameter = np.loadtxt("weight.txt")  # 1*49
data = pd.read_csv("result.csv")  #测试集
record = data.shape[0] #测试集总数

def fun():
    count1, count2 = 0, 0
    num1, num2 = 0, 0
    res = []
    for i in range(0, record):
        result = np.zeros(49)
        df = data.iloc[i:i+1]
        if list(df.hasOrderId)[0] == 1:
            result[0] = 1
        if list(df.hasOrderId)[0] == 0:
            result[1] = 1
        if list(df.desWordLen)[0] > 20:
            result[2] = 1
        if list(df.desWordLen)[0] <= 20:
            result[3] = 1
        if 0 <= list(df.faultType)[0] <= 6:
            result[list(df.faultType)[0] + 4] = 1
        if 10 <= list(df.faultType)[0] <= 18:
            result[list(df.faultType)[0] + 1] = 1
        if 101 <= list(df.faultType)[0] <= 113:
            result[list(df.faultType)[0] - 81] = 1
        if 201 <= list(df.faultType)[0] <= 205:
            result[list(df.faultType)[0] - 168] = 1
        if (list(df.recent7DayRideCount)[0] > 22):
            result[38] = 1
        if (list(df.recent7DayRideCount)[0] <= 22):
            result[39] = 1
        if (list(df.afterFault3HouraveTime)[0] > 600) and (list(df.afterFault3HourRideCount)[0] > 2):
            result[40] = 1
        if (list(df.afterFault3HouraveTime)[0] > 600) and (list(df.afterFault3HourRideCount)[0] <= 2):
            result[41] = 1
        if (list(df.afterFault3HouraveTime)[0] <= 600) and (list(df.afterFault3HourRideCount)[0] > 2):
            result[42] = 1
        if (list(df.afterFault3HouraveTime)[0] <= 600) and (list(df.afterFault3HourRideCount)[0] <= 2):
            result[43] = 1
        if (list(df.recent1DayIssueFaultUserCount)[0] > 3):
            result[44] = 1
        if (list(df.recent1DayIssueFaultUserCount)[0] <= 3):
            result[45] = 1
        if (list(df.userConfirmedIssueFaultCount/df.userIssueFaultCount)[0] < 0.2):
            result[46] = 1
        if (list(df.userConfirmedIssueFaultCount/df.userIssueFaultCount)[0] >= 0.2):
            result[47] = 1
        result[48] = 1
        res.append(result)

        if (model_parameter.dot(np.array(result)) > 1.55) and (list(df.bikefixResult)[0] == 1):
            count1 += 1
        if (model_parameter.dot(np.array(result)) > 1.55) and (list(df.bikefixResult)[0] == 0):
            count2 += 1

        if (model_parameter.dot(np.array(result)) < -1.7) and (list(df.bikefixResult)[0] == 0):
            num1 += 1
        if (model_parameter.dot(np.array(result)) < -1.7) and (list(df.bikefixResult)[0] == 1):
            num2 += 1

    np.savetxt("tmp.txt", res, fmt="%d")

    return count1,count2,num1,num2,(count1+num1)/(count1+count2+num1+num2),count1+count2+num1+num2


print(fun())