import random, time, re
#import matplotlib.pyplot as plt
#import numpy as np
import pprint
import scipy
#Measure total processing time
start = time.time()


simulations = 50
#Trial Design
participants = 104
interventions = {
    'Metformin': 2,     #1 active, 1 placebo
    'Exercise': 2,      #1 exercise, 1 no exercise
}

#Randomisation
onlyInitiallyVariable = False
followingBlockSize = 4
trueRandomisation = True
variability = [20,100]
blockSizes = [8,4]

number_ageBlocks = 2

#Variables of Interest                              (variable name, cumulative probabilities for each outcome)
characteristics = {
    'Gender': [49, 100],                            #male = 0, female = 1
    #'2_Age': [5,6,7,8,9,10,12,14,16,18,20,23,26,29,33,39,46,50,54,59,66,67,68,66,60,54,47,39,30,22],
    #'2_Age': [5,6,7,8,9,10,12,14,16,18,20,23,26,29,33,38,43,49,56,62,67,72,76,78,79,78,75,70,60,45],
    #'2_Age': [5,6,7,8,9,10,12,14,16,18,20,23,26,29,32,36,40,45,51,57,63,68,72,75,76,74,70,64,56,46],
    str(number_ageBlocks)+'_Age': [5,6,7,8,9,10,12,14,16,19,22,25,28,31,35,39,44,50,56,61,65,68,69,67,63,57,49,39,28,16],
    'Metformin': [70, 100],                         #non-user = 0, user = 1
    #'Smoker': [25,100],                              #smoker = 0, non-smoker = 1
    #'4_Social Class': [(n+1)*10 for n in range(10)],   #Arbitrary classes 0-4
    #'Osteopenic': [5,100],                          # Osteopenic = 0, Healthy = 1
}
print(len(characteristics[str(number_ageBlocks)+'_Age']))
print(characteristics[str(number_ageBlocks)+'_Age'])
#Matched Variables
matched_variables = [
    'Gender',
    #'Metformin',
     str(number_ageBlocks)+'_Age_grouped'
]

for characteristic in characteristics.keys():
    if len(characteristics[characteristic]) > 5:
        sum = sum(characteristics[characteristic])
        print(sum)
        tempArray = [0]*len(characteristics[characteristic])
        for item in range(len(characteristics[characteristic])):
            if item > 0:
                tempArray[item] = round(characteristics[characteristic][item]/sum*100 + tempArray[item-1],2)
                if item == len(characteristics[characteristic]) - 1:
                    tempArray[item] = 100
            else:
                tempArray[item] = round(characteristics[characteristic][item]/sum*100,2)
        characteristics[characteristic] = tempArray

print(len(characteristics[str(number_ageBlocks)+'_Age']))
print(characteristics[str(number_ageBlocks)+'_Age'][0:int(len(characteristics[str(number_ageBlocks)+'_Age'])/4)])
print(characteristics[str(number_ageBlocks)+'_Age'][int(len(characteristics[str(number_ageBlocks)+'_Age'])/4):int(len(characteristics[str(number_ageBlocks)+'_Age'])/4*2)])
print(characteristics[str(number_ageBlocks)+'_Age'][int(len(characteristics[str(number_ageBlocks)+'_Age'])/4*2):int(len(characteristics[str(number_ageBlocks)+'_Age'])/4*3)])
print(characteristics[str(number_ageBlocks)+'_Age'][int(len(characteristics[str(number_ageBlocks)+'_Age'])/4*3):])

#Create Grouped Variables in Characteristics
for characteristic in list(characteristics.keys()):
    if len(characteristics[characteristic]) > 5:
        characteristics[characteristic+'_grouped'] = [0]*int(characteristic[0])

#Create Trial Arms
def createTrialArms(trialArms={}, interventionsDone=0, armDescriptor=''):
    origDescriptor = armDescriptor
    listOfInterventions = [key for key in interventions.keys()]
    for n in range(interventions[listOfInterventions[interventionsDone]]):
        armDescriptor = origDescriptor + listOfInterventions[interventionsDone] + ' ' + str(n) + ' | '
        if interventionsDone + 1 < len(interventions):
            createTrialArms(trialArms, interventionsDone+1, armDescriptor)
        else:
            trialArms[armDescriptor] = []
    return trialArms


#Create Strata
def createStrata(strata={}, strataDone=0, keyName=''):
    origKeyName = keyName
    for n in range(len(characteristics[matched_variables[strataDone]])):
        keyName = origKeyName +  matched_variables[strataDone] + ' ' + str(n) + ' | '
        if strataDone + 1 < len(matched_variables):
            createStrata(strata, strataDone + 1, keyName)
        else:
            strata[keyName] = []
    return strata


#Create Participants
def createParticipantArray():
    participantArray = []
    for participant in range(participants):
        person = {'Id':participant}
        for characteristic in characteristics.keys():
            dice = random.randint(1,100)
            if len(characteristics[characteristic]) > 5:
                dice = random.randint(1,10000)/100
            for n in range(len(characteristics[characteristic])):
                if dice <= characteristics[characteristic][n]:
                    person[characteristic] = n
                    if len(characteristics[characteristic]) > 5:
                        for x in range(int(characteristic[0])):
                            if n <= len(characteristics[characteristic])/int(characteristic[0]) * (x+1):
                                person[characteristic+'_grouped'] = x
                                break
                    break
        participantArray.append(person)
    return participantArray


#Move to Strata
def stratify():
    for participant in participantArray:
        characterisingKey = ''
        for variable in matched_variables:
            characterisingKey += variable + ' ' + str(participant[variable]) + ' | '
        strata[characterisingKey].append(participant)


#Randomise
def chooseBlockSize(firstBlock):
    if onlyInitiallyVariable == False or firstBlock == True:
        for n in range(len(variability)):
            dice = random.randint(1,100)
            if dice <= variability[n]:
                blockSize = blockSizes[n]
                break
    else:
        blockSize = followingBlockSize
    return blockSize

def randomise(stratum, trialArms):
    firstBlock = True
    while len(stratum) > 0:
        multiplier = int( chooseBlockSize(firstBlock) / len(listOfArms) )
        randomisationOrder = sorted([num for num in range(len(listOfArms))] * multiplier)
        if trueRandomisation == True:
            random.shuffle(randomisationOrder)
        for n in randomisationOrder:
            if len(stratum) > 0:
                trialArms[n].append(stratum[0])
                del stratum[0]
        firstBlock = False

pValues = []
def characteristicDistribution(distributionDict, avgDict):
    print(''.ljust(181,'-'))
    print(''.ljust(27)+'| ')
    for arm in trialArms.items():
        print((arm[0] + ':').ljust(35)+'| '),
    for key in characteristics.keys():
        print('\n'.ljust(181,'-')),
        #Create Array of Avg of semi-continuous variables (e.g. age)
        if len(characteristics[key]) > 5:
            if key not in avgDict.keys(): avgDict[key] = {}
            averages = []
            print('\n'+(key[2:]+' (Average):').ljust(27)+'| '),
            for arm in sorted(trialArms.items()):
                sumCharacteristic = 0
                for participant in arm[1]:
                    sumCharacteristic += participant[key]
                avgCharacteristic = round(sumCharacteristic/len(arm[1]))
                if 'Age' in key:
                    avgCharacteristic = round(sumCharacteristic/len(arm[1]) , 1) + 45
                averages.append(avgCharacteristic)
                print(str(averages[-1]).ljust(35)+'|  '),
            avgDifference = max(averages)-min(averages)
            if avgDifference in avgDict[key]:
                num = avgDict[key][avgDifference][1]
                avgDict[key][avgDifference] = ([i for i in averages],num+1)
            else:
                avgDict[key][avgDifference] = ([i for i in averages],1)
            #Create Arrays of All Ages
            if "Age" in key:
                maxIndex = averages.index(max(averages))
                minIndex = averages.index(min(averages))
                youngestArm = list(sorted(trialArms.items()))[minIndex]
                oldestArm = list(sorted(trialArms.items()))[maxIndex]
                ageArrays = [[],[]]
                for participant in youngestArm[1]:
                    ageArrays[0].append(participant[key])
                for participant in oldestArm[1]:
                    ageArrays[1].append(participant[key])
                #Perform T-test and add to overall p-value array
                
        #Create Array of proportions of binary or categorical variables (e.g. gender or social class)
        else:
            sets_of_proportions = []
            for arm in trialArms.items():
                amount = [0]*len(characteristics[key])
                for participant in arm[1]:
                    amount[participant[key]] += 1
                proportions = [n/len(arm[1]) for n in amount]
                sets_of_proportions.append(proportions)
            for proportion in range(len(sets_of_proportions[0])):
                tempArray = []
                nameOfVariable = key+' '+str(proportion)
                print('\n'+(nameOfVariable+':').ljust(27)+'| '),
                if nameOfVariable not in distributionDict.keys():
                    distributionDict[nameOfVariable] = {}
                for set in sets_of_proportions:
                    rounded_num = int(round(set[proportion]*100))
                    print(str(rounded_num).ljust(35)+'|  '),
                    tempArray.append(rounded_num)
                if max(tempArray)-min(tempArray) in distributionDict[nameOfVariable]:
                    num = distributionDict[nameOfVariable][max(tempArray)-min(tempArray)][1]
                    distributionDict[nameOfVariable][max(tempArray)-min(tempArray)] = ([i for i in tempArray],num+1)
                else:
                    distributionDict[nameOfVariable][max(tempArray)-min(tempArray)] = ([i for i in tempArray],1)
    print('\n'.ljust(181,'-'))
    return (distributionDict, avgDict)

def checkInterventionSizes(trialArms, armSizes):
    print('\nIntervention Sizes:')
    for intervention in interventions.keys():
        for n in range(interventions[intervention]):
            if (intervention + ' ' + str(n)) not in armSizes.keys():
                armSizes.update({intervention + ' ' + str(n):[]})
            counter = 0
            for arm in trialArms.keys():
                if (intervention + ' ' + str(n)) in arm:
                    counter += len(list(trialArms[arm]))
            print((intervention + ' ' + str(n) + ': ').ljust(15,' ')+ str(counter))
            armSizes[intervention + ' ' + str(n)].append(counter)
    return armSizes


#Run Simulations
distributionDict = {}
avgDict = {}
firstAgeArray = []
for n in range(simulations):
    print('\n\n' + (' Simulation number: '+str(n+1)+' ').center(150,'='))
    trialArms = createTrialArms()
    strata = createStrata()
    participantArray = createParticipantArray()
    #Put Participants in Strata
    stratify()
    print('\nFilled Strata:')
    for item in strata.items():
        print('Contains', str(len(item[1])).rjust(2), item[0])
        for n in range(len(item[1])):
            if n % 2 == 0:
                print(str(item[1][n])+', ')
            else:
                print(item[1][n])
        print('\n')
    #Randomise
    listOfArms = list(trialArms.values())
    for stratum in strata.values():
        randomise(stratum, listOfArms)
    #Print Arms
    print('\nTrialArms')
    for item in trialArms.items():
        #print('Contains', str(len(item[1])).rjust(2), item)
        print('\nContains', str(len(item[1])).rjust(2), item[0])
        for n in range(len(item[1])):
            if n % 2 == 0:
                print(str(item[1][n])+','),
            else:
                print(item[1][n])
        print('\n')
    #Statistics on Characteristics
    print('\nCharacteristic Distribution')
    distributionDict, avgDict = characteristicDistribution(distributionDict, avgDict)
    #Statistics on Intervention Sizes
    if 'armSizes' not in globals():
        armSizes = {}
    armSizes = checkInterventionSizes(trialArms, armSizes)
    #Create Array to Count People of Each Age (And to Graph)
    #firstAgeArray = []
    for person in participantArray:
        firstAgeArray.append(person[str(number_ageBlocks)+'_Age']+45)

    
def printPercentile(num,space=''):
    #for arm in armSizes.keys():
    #    print(((str(num)+'%:').ljust(7) + space + str(int(np.percentile(armSizes[arm], num)))).ljust(25)+''),
    print('\n')

#Create Function to Print Intervention Sizes
def printInterventionSizes():
    for arm in armSizes.keys():
        print((arm+':').ljust(25)+''),
    print('\n')
    printPercentile(1)
    printPercentile(5,' ')
    printPercentile(25,'  ')
    printPercentile(50,'   ')
    printPercentile(75,'  ')
    printPercentile(95,' ')
    printPercentile(99)
    printPercentile(100)
    print('\n')

#Create Functions to Print Characteristic Skewing
def printCategoricalVariableSkewing(characteristic):
    if characteristic[0].isdigit() and characteristic[1] == '_':
        print('\n'+characteristic[2:]+':')
    else:
        print('\n'+characteristic+':')
    nextPercentile = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1]
    num = 0
    n = 0 
    for difference in sorted(distributionDict[characteristic].keys()):
        num += distributionDict[characteristic][difference][1]
        while num >= nextPercentile[n]*simulations:
            visualArray = distributionDict[characteristic][difference][0]
            print(((str(int(nextPercentile[n]*100))+'.').ljust(4) +' percentil: ').ljust(20)),
            print((str(difference).ljust(3) + ' procentpoint differens').ljust(33)),
            print('(' + (str(max(visualArray))+'%').ljust(5) + 'vs. ' + (str(min(visualArray))+'%').ljust(3) + ')')
            n += 1
            if n >= len(nextPercentile):
                break

def printSemiContinuousVariableSkewing(characteristic):
    if characteristic[0].isdigit() and characteristic[1] == '_':
        print('\n'+characteristic[2:]+':')
    else:
        print('\n'+characteristic+':')
    nextPercentile = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99, 1]
    num = 0
    n = 0
    for difference in sorted(avgDict[characteristic].keys()):
        num += avgDict[characteristic][difference][1]
        while num >= nextPercentile[n]*simulations:
            visualArray = avgDict[characteristic][difference][0]
            print(((str(int(nextPercentile[n]*100))+'.').ljust(4) +' percentil: ').ljust(20)),
            print((str(round(difference,1)).ljust(4) + ' units difference').ljust(33)),
            print('(' + (str(max(visualArray))+' units ').ljust(5) + 'vs. ' + (str(min(visualArray))+' units').ljust(3) + ')')
            n += 1
            if n >= len(nextPercentile):
                break

#Print Stuff
print('\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n')

print('Matched Variables: '+str(matched_variables))
#total processing time
end = time.time()
print(end - start,'seconds for',simulations,'simulations with',participants,'patients\n\n')


print('How characteristics differ between groups. Differences betweeen the trial arm with highest proportion vs. arm w/ lowest proportion shown:')
sortedCharacteristics = [characteristic for characteristic in sorted(distributionDict.keys())]
#for n in range(0, len(sortedCharacteristics), 2):
for n in range(len(sortedCharacteristics)):
    printCategoricalVariableSkewing(sortedCharacteristics[n])
    print('\n')

sortedCharacteristics = [characteristic for characteristic in sorted(avgDict.keys())]
#for n in range(0, len(sortedCharacteristics), 2):
for n in range(len(sortedCharacteristics)):
    printSemiContinuousVariableSkewing(sortedCharacteristics[n])
    print('\n')


print('\nHow many participants receiving each intervention in total:')
printInterventionSizes()


if onlyInitiallyVariable == False:
    print('Variable Blocks(?): '.ljust(20)+str(blockSizes))
    print('Chances: '.ljust(20)+str(variability))
else:
    print('Only first blocks are variable. All following blocks are '+str(followingBlockSize)+'-blocks.')

if trueRandomisation == True:
    print('Randomly Distributed')
else:
    print('Ordered Distribution')


#Age Distribution Averaged (Graph)
firstAgeArray = sorted(firstAgeArray)
newAgeArray = [0]*75
for n in range(len(firstAgeArray)):
    newAgeArray[firstAgeArray[n]] += 1
#plt.plot(range(45,len(newAgeArray)),newAgeArray[45:])
#plt.show()