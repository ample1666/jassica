import numpy as np
import pandas as pd

data = pd.read_csv("result.csv")
'''
文件中包含的字段：
bikeNo,timeStamp,userGuid,faultType,desWordLen,hasOrderId,
allRideCount,userRideCount,userRideTime,userIssueFaultCount,userConfirmedIssueFaultCount,userHasMonthCard,
allAverageRideTime,allAverageRideDistance,allAverateRideSpeed,
recent1DayRideCount,rencent1DayAverageRideTime,recent1DayAverageDistance,recent1DayRideSpeed,
recent3DayRideCount,rencent3DayAverageRideTime,recent3DayAverageDistance,recent3DayRideSpeed,
recent5DayRideCount,rencent5DayAverageRideTime,recent5DayAverageDistance,recent5DayRideSpeed,
recent7DayRideCount,rencent7DayAverageRideTime,recent7DayAverageDistance,recent7DayRideSpeed,
idleHour,serveDay,
afterFault1HourRideCount,afterFault1HourAveTime,afterFault1HourAveRideDistance,afterFault1HourAveRideSpeed,
afterFault2HourRideCount,afterFault2HouraveTime,afterFault2HourAveRideDistance,afterFault2HourAveRideSpeed,
afterFault3HourRideCount,afterFault3HouraveTime,afterFault3HourAveRideDistance,afterFault3HourAveRideSpeed,
afterFault6HourRideCount,afterFault6HouraveTime,afterFault6HourAveRideDistance,afterFault6HourAveRideSpeed,
afterFault12HourRideCount,afterFault12HouraveTime,afterFault12HourAveRideDistance,afterFault12HourAveRideSpeed,
afterFault24HourRideCount,afterFault24HouraveTime,afterFault24HourAveRideDistance,afterFault24HourAveRideSpeed,
reportFaultCount,correctFaultCount,processingFaultCount,
recent1DayIssueFaultUserCount,recent1DayIssueFaultTypeCount,typefixResult,bikefixResult
'''

allCounts = data.shape[0] # 报障总数
faultCounts = data[data.bikefixResult == 1].shape[0] # 误报总数
trueCounts = data[data.bikefixResult == 0].shape[0] # 正确报障的总数

def computeWeight(x, y):
    if x * y == 0:
        return 0
    else:
        return np.log(x*trueCounts/(y*faultCounts))

def type_X_Weight(type):
    a = data[(data.bikefixResult == 1) & (data.faultType == type)].shape[0]
    b = data[(data.bikefixResult == 0) & (data.faultType == type)].shape[0]
    return computeWeight(a, b)

def getWeight():
    weight = []
    x = data[(data.bikefixResult == 1) & (data.hasOrderId == 1)].shape[0]
    y = data[(data.bikefixResult == 0) & (data.hasOrderId == 1)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.bikefixResult == 1) & (data.hasOrderId == 0)].shape[0]
    y = data[(data.bikefixResult == 0) & (data.hasOrderId == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.bikefixResult == 1) & (data.desWordLen > 20)].shape[0]
    y = data[(data.bikefixResult == 0) & (data.desWordLen > 20)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.bikefixResult == 1) & (data.desWordLen <= 20)].shape[0]
    y = data[(data.bikefixResult == 0) & (data.desWordLen <= 20)].shape[0]
    weight.append(computeWeight(x, y))

    for i in range(0, 7):
        weight.append(type_X_Weight(i))
    for i in range(7, 16):
        weight.append(type_X_Weight(i+3))
    for i in range(16, 29):
        weight.append(type_X_Weight(i+85))
    for i in range(29, 34):
        weight.append(type_X_Weight(i+172))

    x = data[(data.recent7DayRideCount > 22) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.recent7DayRideCount > 22) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.recent7DayRideCount <= 22) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.recent7DayRideCount <= 22) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.afterFault3HouraveTime > 600) & (data.afterFault3HourRideCount > 2) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.afterFault3HouraveTime > 600) & (data.afterFault3HourRideCount > 2) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.afterFault3HouraveTime > 600) & (data.afterFault3HourRideCount <= 2) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.afterFault3HouraveTime > 600) & (data.afterFault3HourRideCount <= 2) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.afterFault3HouraveTime <= 600) & (data.afterFault3HourRideCount > 2) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.afterFault3HouraveTime <= 600) & (data.afterFault3HourRideCount > 2) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.afterFault3HouraveTime <= 600) & (data.afterFault3HourRideCount <= 2) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.afterFault3HouraveTime <= 600) & (data.afterFault3HourRideCount <= 2) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.recent1DayIssueFaultUserCount > 3) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.recent1DayIssueFaultUserCount > 3) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.recent1DayIssueFaultUserCount <= 3) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.recent1DayIssueFaultUserCount <= 3) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.userConfirmedIssueFaultCount/data.userIssueFaultCount < 0.2) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.userConfirmedIssueFaultCount/data.userIssueFaultCount < 0.2) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    x = data[(data.userConfirmedIssueFaultCount/data.userIssueFaultCount >= 0.2) & (data.bikefixResult == 1)].shape[0]
    y = data[(data.userConfirmedIssueFaultCount/data.userIssueFaultCount >= 0.2) & (data.bikefixResult == 0)].shape[0]
    weight.append(computeWeight(x, y))

    weight.append(np.log(faultCounts / trueCounts))
    return weight

np.savetxt("weight.txt", getWeight(), fmt="%.6f")

