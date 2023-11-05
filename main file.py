import random, time
import matplotlib.pyplot as plt

#Measure total processing time
start = time.time()

#User Sets Values
variableBlockMode = 'Always' #Set to 'Initial', 'Never' or 'Always'
randomisationType = 'Random' #Set to 'Random' or 'Ordered'
chance_of_variation = 1/5
num_of_sims = 10000
num_of_patients = 104
num_of_strata = 8
num_of_trial_arms = 4
stat_distribution_counter = 18


#Declare Variables
biggestDif = []
smallestDif = []

biggestBlock = []
smallestBlock = []

biggestStratum = []
smallestStratum = []

inequalAge = []
inequalGender = []
inequalTreatment = []

if variableBlockMode == 'Initial':
    eightBlocks = None
elif variableBlockMode == 'Never':
    eightBlocks = None
elif variableBlockMode == 'Always':
    eightBlocks = 1


#Make stat (distribution of arm sizes) chosen length
stat = []
for n in range(0,stat_distribution_counter):
    stat.append(0)


#Define a function to create the empty trial arms
def create_arms():
    each_stratum = []
    trial_arms = []
    for x in range(0,num_of_strata):
        each_stratum.append(0)
    for x in range(0,num_of_trial_arms):
        trial_arms.append(each_stratum[:])
    return trial_arms


#Define randomisation procedure
def randomise(participantArray):
    me_mn_pe_pn = create_arms()
    for number in range(len(participantArray)):
        if variableBlockMode == 'Initial':
            blocksize = random.choice([4,8])
            if participantArray[number] >= 8 and blocksize == 8:
                for i in range(0,4):
                    me_mn_pe_pn[i][number] += 2
                participantArray[number] -= 8
            elif participantArray[number] > 0 and blocksize == 8:
                listedArms = [0,0,1,1,2,2,3,3]
                for z in range(0,participantArray[number]):
                    randomArm = random.choice(listedArms)
                    me_mn_pe_pn[randomArm][number] += 1
                    listedArms.remove(randomArm)
                participantArray[number] = 0
        while participantArray[number] >= 8:
            blocksize = random.randint(1, int(1/chance_of_variation))
            if blocksize == eightBlocks:
                for i in range(0,4):
                    me_mn_pe_pn[i][number] += 2
                participantArray[number] -= 8
            else:
                for i in range(0,4):
                    me_mn_pe_pn[i][number] += 1
                participantArray[number] -= 4
        while participantArray[number] > 0:
            blocksize = random.randint(1, int(1/chance_of_variation))
            if blocksize == eightBlocks:
                listedArms = [0,0,1,1,2,2,3,3]
                for z in range(0,participantArray[number]):
                    randomArm = random.choice(listedArms)
                    me_mn_pe_pn[randomArm][number] += 1
                    listedArms.remove(randomArm)
                participantArray[number] = 0
            else:
                if participantArray[number] >= 4:
                    for i in range(0,4):
                        me_mn_pe_pn[i][number] += 1
                    participantArray[number] -= 4
                else:
                    listedArms = [0,1,2,3]
                    for z in range(0,participantArray[number]):
                        randomArm = random.choice(listedArms)
                        me_mn_pe_pn[randomArm][number] += 1
                        listedArms.remove(randomArm)
                    participantArray[number] = 0
    #Run printing functions
    printTrialArmsInfo(me_mn_pe_pn)
    createArmInequality(me_mn_pe_pn)
    printArmCategories(me_mn_pe_pn)
    createExtremes(ageInfo(me_mn_pe_pn),inequalAge)
    createExtremes(genderInfo(me_mn_pe_pn),inequalGender)
    createExtremes(treatmentInfo(me_mn_pe_pn),inequalTreatment)
    print('\n\n\n')


def fakeRandomise(participantArray):
    me_mn_pe_pn = create_arms()
    for number in range(len(participantArray)):
        if variableBlockMode == 'Initial':
            blocksize = random.choice([4,8])
            if blocksize == 8 and participantArray[number] >= 8:
                    for i in range(0,4):
                        me_mn_pe_pn[i][number] += 2
                    participantArray[number] -= 8
            elif blocksize == 8 and participantArray[number] > 0:
                    listedArms = [0,0,1,1,2,2,3,3]
                    for n in range(0,participantArray[number]):
                        me_mn_pe_pn[listedArms[n]][number] += 1
                    participantArray[number] = 0
        while participantArray[number] >= 8:
            blocksize = random.randint(1, int(1/chance_of_variation))
            if blocksize == eightBlocks:
                for i in range(0,4):
                    me_mn_pe_pn[i][number] += 2
                participantArray[number] -= 8
            else:
                for i in range(0,4):
                    me_mn_pe_pn[i][number] += 1
                participantArray[number] -= 4
        while participantArray[number] > 0:
            blocksize = random.randint(1, int(1/chance_of_variation))
            if blocksize == eightBlocks:
                listedArms = [0,0,1,1,2,2,3,3]
                for n in range(0,participantArray[number]):
                    me_mn_pe_pn[listedArms[n]][number] += 1
                participantArray[number] = 0
            else:
                if participantArray[number] >= 4:
                    for i in range(0,4):
                        me_mn_pe_pn[i][number] += 1
                    participantArray[number] -= 4
                else:
                    listedArms = [0,1,2,3]
                    for n in range(0,participantArray[number]):
                        me_mn_pe_pn[listedArms[n]][number] += 1
                    participantArray[number] = 0
    #Run printing functions
    printTrialArmsInfo(me_mn_pe_pn)
    createArmInequality(me_mn_pe_pn)
    printArmCategories(me_mn_pe_pn)
    createExtremes(ageInfo(me_mn_pe_pn),inequalAge)
    createExtremes(genderInfo(me_mn_pe_pn),inequalGender)
    createExtremes(treatmentInfo(me_mn_pe_pn),inequalTreatment)
    print('\n\n\n')

def modifyArray(inputArray):
    modifiedArray = [sum(item) for item in inputArray]
    return modifiedArray

#Print  info about trial arms
def printTrialArmsInfo(me_mn_pe_pn):
    name_of_arm = ['Met + Exc','Met','Pla + Exc','Pla']
    for arm in range(len(me_mn_pe_pn)):
        print('|',name_of_arm[arm].ljust(9) + ' (n=' + str(sum(me_mn_pe_pn[arm])) + ') |',end=' ')
        for num in me_mn_pe_pn[arm]:
            print(str(num).center(10),'|',end=' ')
        print('')
    print('|' + ''.center(122,'-') + '|')
    me_mn_pe_pn_modified = modifyArray(me_mn_pe_pn)
    print('|',''.ljust(120),'|')
    print('|',('Largest Arm: ' + str(max(me_mn_pe_pn_modified))).ljust(20),'|', end='')
    print(('Smallest Arm: ' + str(min(me_mn_pe_pn_modified))).center(23),'|', end='')
    print(('Difference: ' + str(max(me_mn_pe_pn_modified) - min(me_mn_pe_pn_modified))).center(23),end='')
    print(''.ljust(50),'|')
    print('|',''.ljust(120),'|')

#Print stratum categories
def printStratumCategories():
    print('|',''.ljust(17),end='|')
    for i in range(4):
        print('Males'.center(11),'|',end='')
    for i in range(4):
        print('Females'.center(11),'|',end='')
    print('\n|',''.ljust(17),end='|')
    for i in range(2):
        for x in range(2):
            print('Young'.center(11),'|',end='')
        for x in range(2):
            print('Old'.center(11),'|',end='')
    print('\n|',''.ljust(17),end='|')
    for i in range(4):
        print('Metformin'.center(11),'|',end='')
        print('Naïve'.center(11),'|',end='')
    print('\n|',''.ljust(17),end='|')
    for i in range(8):
        print(''.center(11),'|',end='')
    print('')

#Print Arm Categoires
def printArmCategories(me_mn_pe_pn):
    print('|' + ''.center(122,'-') + '|')
    print('|',''.ljust(21),end='|')
    for i in range(2):
        print('Metformin'.center(24),end='|')
    for i in range(2):
        print('Placebo'.center(24),end='|')
    print('')
    print('|',''.ljust(21),end='|')
    for i in range(2):
        print('Exercise'.center(24),end='|')
        print(''.center(24),end='|')
    print('')
    print('|',''.ljust(21),end='|')
    for x in range(4):
        print(('n = ' + str(sum(me_mn_pe_pn[x]))).center(24),end='|')
    print('')
    print('|' + ''.center(122,'-') + '|')

#Print info about characteristic 1
def genderInfo(me_mn_pe_pn):
    males = [0,0,0,0]
    for n in range(len(me_mn_pe_pn)):
        for i in range(4):
            males[n] += me_mn_pe_pn[n][i]
    print('|','Males'.ljust(21),end='|')
    for arm in males:
        print(str(arm).center(24),end='|')
    print('')
    females = [0,0,0,0]
    for n in range(len(me_mn_pe_pn)):
        for i in range(4,8):
            females[n] += me_mn_pe_pn[n][i]
    print('|','Females'.ljust(21),end='|')
    for arm in females:
        print(str(arm).center(24),end='|')
    print('')
    difGender = [0,0,0,0]
    for n in range(4):
        if females[n] != 0:
            difGender[n] = round(males[n]/(males[n]+females[n])*100,2)
        else:
            difGender[n] = 'zero'
    #print('Ratio'.ljust(21),end='|')
    print('|',('Ratio (dif = ' + str(round((max(difGender)-min(difGender)),2)) + '%)').ljust(21),end='|')
    for arm in difGender:
        print((str(arm) + '%').center(24),end='|')
    print('')
    print('|' + ''.center(122,'-') + '|')
    return difGender

#Print info about characteristic 2
def ageInfo(me_mn_pe_pn):
    young = [0,0,0,0]
    for n in range(len(me_mn_pe_pn)):
            young[n] += me_mn_pe_pn[n][0] + me_mn_pe_pn[n][1] + me_mn_pe_pn[n][4] + me_mn_pe_pn[n][5]
    print('|','<65 yrs'.ljust(21),end='|')
    for arm in young:
        print(str(arm).center(24),end='|')
    print('')
    old = [0,0,0,0]
    for n in range(len(me_mn_pe_pn)):
            old[n] += me_mn_pe_pn[n][2] + me_mn_pe_pn[n][3] + me_mn_pe_pn[n][6] + me_mn_pe_pn[n][7]
    print('|','≥65 yrs'.ljust(21),end='|')
    for arm in old:
        print(str(arm).center(24),end='|')
    print('')
    difAge = [0,0,0,0]
    for n in range(4):
        if young[n] != 0:
            difAge[n] = round(young[n]/(old[n]+young[n])*100,2)
        else:
            difAge[n] = 'zero'
    #print('Ratio'.ljust(21),end='|')
    print('|',('Ratio (dif = ' + str(round((max(difAge)-min(difAge)),2)) + '%)').ljust(21),end='|')
    for arm in difAge:
        print((str(arm) + '%').center(24),end='|')
    print('')
    print('|' + ''.center(122,'-') + '|')
    return difAge

#Print info about characteristic 3
def treatmentInfo(me_mn_pe_pn):
    metforminbehandlet = [0,0,0,0]
    for n in range(len(me_mn_pe_pn)):
            metforminbehandlet[n] += me_mn_pe_pn[n][0] + me_mn_pe_pn[n][2] + me_mn_pe_pn[n][4] + me_mn_pe_pn[n][6]
    print('|','Metformin'.ljust(21),end='|')
    for arm in metforminbehandlet:
        print(str(arm).center(24),end='|')
    print('')
    ubehandlet = [0,0,0,0]
    for n in range(len(me_mn_pe_pn)):
            ubehandlet[n] += me_mn_pe_pn[n][1] + me_mn_pe_pn[n][3] + me_mn_pe_pn[n][5] + me_mn_pe_pn[n][7]
    #print('Ubehandlet: ' + str(ubehandlet))
    print('|','Naïve'.ljust(21),end='|')
    for arm in ubehandlet:
        print(str(arm).center(24),end='|')
    print('')
    difTreatment = [0,0,0,0]
    for n in range(4):
        if ubehandlet[n] != 0:
            difTreatment[n] = round(metforminbehandlet[n]/(metforminbehandlet[n]+ubehandlet[n])*100,2)
        else:
            difTreatment[n] = 'zero'
    #print('Ratio: ' + str(difTreatment))
    print('|',('Ratio (dif = ' + str(round((max(difTreatment)-min(difTreatment)),2)) + '%)').ljust(21),end='|')
    for arm in difTreatment:
        print((str(arm) + '%').center(24),end='|')
    print('')
    print('|' + ''.center(122,'-') + '|')
    return difTreatment

def createArmInequality(inputArray):
    outputArray = modifyArray(inputArray)
    outputArray.sort()
    biggestDif.append(max(outputArray) - min(outputArray))
    smallestDif.append(outputArray[1] - outputArray[0])
    biggestBlock.append(max(outputArray))
    smallestBlock.append(min(outputArray))
    stat[max(outputArray) - min(outputArray)] += 1

def createExtremes(inputArray, outputArray):
    outputArray.append([max(inputArray),min(inputArray)])

#Run simulations
for simulation in range(num_of_sims):
    strata = []
    for x in range(0,num_of_strata):
        strata.append(0)
    for n in range(num_of_patients):
        blocknum = random.randint(0, 7)
        strata[blocknum] += 1
    biggestStratum.append(max(strata))
    smallestStratum.append(min(strata))
    print('|' + (' Simulation ' + str(simulation+1) + ' ').center(122,'=') + '|')
    printStratumCategories()
    print('|','Strata:'.ljust(17),end='|')
    for stratum in strata:
        print(str(stratum).center(11),'|',end='')
    print('')
    print('|' + ''.center(122,'-') + '|')
    if randomisationType == 'Random':
        randomise(strata)
    elif randomisationType == 'Ordered':
        fakeRandomise(strata)

#Print final characteristics
print('Summary of simulations: \n')
print('Mindste stratum blev: ' + str(min(smallestStratum)))
print('Største stratum blev: ' + str(max(biggestStratum)))
print('Mindste differens mellem mindste og største arme: ' + str(min(smallestDif)))
print('Største differens: ' + str(max(biggestDif)))
print('Mindste arm blev: ' + str(min(smallestBlock)))
print('Største arm blev: ' + str(max(biggestBlock)))

#Print distribution of block differences
for i in range(len(stat)-1):
    print(str(i).ljust(6),end=' ')
print(len(stat)-1)
for i in range(len(stat)-1):
    print(str(stat[i]).ljust(6),end=' ')
print(stat[len(stat)-1])

#Print the median and upper ranges for maximal arm size differences
sum_of_participants = 0
indexn = 0
while sum_of_participants < 0.5*num_of_sims:
    sum_of_participants += stat[indexn]
    indexn += 1
print('Median: ' + str(indexn-1))
while sum_of_participants < 0.75*num_of_sims:
    sum_of_participants += stat[indexn]
    indexn += 1
print('75-percentile: ' + str(indexn-1))
while sum_of_participants < 0.95*num_of_sims:
    sum_of_participants += stat[indexn]
    indexn += 1
print('95-percentile: ' + str(indexn-1))

#Print differences in patient characteristics
print('De størst optrådte forskelle (i procentpoint) på subgruppers repræsentation i forsøgsarme ses herunder.')
print('I parantes angives den procentvise repræsentation i største/mindste gruppe.')
print('\n'.ljust(121,'-'),'\n')
inequalAgeTwo = inequalAge[:]
for n in range(len(inequalAgeTwo)):
    inequalAgeTwo[n] = inequalAgeTwo[n][0] - inequalAgeTwo[n][1]
alder_p = [inequalAge[inequalAgeTwo.index(max(inequalAgeTwo))][0],inequalAge[inequalAgeTwo.index(max(inequalAgeTwo))][1]]
print('Alder (<65 vs ≥65):'.center(50),'\n')
print('Absolute max:'.ljust(15) + str(round(max(inequalAgeTwo),2)).ljust(9) + '(' + (str(alder_p[0]) +'%').ljust(10) + ' kontra ' + str(alder_p[1])+'%)')
inequalAgeThree = inequalAgeTwo[:]
inequalAgeThree.sort()
inequalAge_95_percentile_index = inequalAgeTwo.index(inequalAgeThree[int(num_of_sims*0.95-1)])
alder_95_p = [inequalAge[inequalAge_95_percentile_index][0],inequalAge[inequalAge_95_percentile_index][1]]
print('95 percentil:'.ljust(15) + str(round(inequalAgeTwo[inequalAge_95_percentile_index],2)).ljust(9) + '(' + (str(alder_95_p[0]) +'%').ljust(10) + ' kontra ' + str(alder_95_p[1])+'%)')
inequalAge_75_percentile_index = inequalAgeTwo.index(inequalAgeThree[int(num_of_sims*0.75-1)])
alder_75_p = [inequalAge[inequalAge_75_percentile_index][0],inequalAge[inequalAge_75_percentile_index][1]]
print('75 percentil:'.ljust(15) + str(round(inequalAgeTwo[inequalAge_75_percentile_index],2)).ljust(9) + '(' + (str(alder_95_p[0]) +'%').ljust(10) + ' kontra ' + str(alder_95_p[1])+'%)')
inequalAge_50_percentile_index = inequalAgeTwo.index(inequalAgeThree[int(num_of_sims*0.50-1)])
alder_50_p = [inequalAge[inequalAge_50_percentile_index][0],inequalAge[inequalAge_50_percentile_index][1]]
print('50 percentil:'.ljust(15) + str(round(inequalAgeTwo[inequalAge_50_percentile_index],2)).ljust(9) + '(' + (str(alder_50_p[0]) +'%').ljust(10) + ' kontra ' + str(alder_50_p[1])+'%)')
print('\n'.ljust(121,'-'),'\n')

inequalGenderTwo = inequalGender[:]
for n in range(len(inequalGenderTwo)):
    inequalGenderTwo[n] = inequalGenderTwo[n][0] - inequalGenderTwo[n][1]
køn_p = [inequalGender[inequalGenderTwo.index(max(inequalGenderTwo))][0],inequalGender[inequalGenderTwo.index(max(inequalGenderTwo))][1]]
print('Køn (Mænd vs kvinder): '.center(50),'\n')
print('Absolute max:'.ljust(15) + str(round(max(inequalGenderTwo),2)).ljust(9) + '(' + (str(køn_p[0]) +'%').ljust(10) + ' kontra ' + str(køn_p[1])+'%)')
inequalGenderThree = inequalGenderTwo[:]
inequalGenderThree.sort()
inequalGender_95_percentile_index = inequalGenderTwo.index(inequalGenderThree[int(num_of_sims*0.95-1)])
køn_95_p = [inequalGender[inequalGender_95_percentile_index][0],inequalGender[inequalGender_95_percentile_index][1]]
print('95 percentil:'.ljust(15) + str(round(inequalGenderTwo[inequalGender_95_percentile_index],2)).ljust(9) + '(' + (str(køn_95_p[0]) +'%').ljust(10) + ' kontra ' + str(køn_95_p[1])+'%)')
inequalGender_75_percentile_index = inequalGenderTwo.index(inequalGenderThree[int(num_of_sims*0.75-1)])
køn_75_p = [inequalGender[inequalGender_75_percentile_index][0],inequalGender[inequalGender_75_percentile_index][1]]
print('75 percentil:'.ljust(15) + str(round(inequalGenderTwo[inequalGender_75_percentile_index],2)).ljust(9) + '(' + (str(køn_75_p[0]) +'%').ljust(10) + ' kontra ' + str(køn_75_p[1])+'%)')
inequalGender_50_percentile_index = inequalGenderTwo.index(inequalGenderThree[int(num_of_sims*0.50-1)])
køn_50_p = [inequalGender[inequalGender_50_percentile_index][0],inequalGender[inequalGender_50_percentile_index][1]]
print('50 percentil:'.ljust(15) + str(round(inequalGenderTwo[inequalGender_50_percentile_index],2)).ljust(9) + '(' + (str(køn_50_p[0]) +'%').ljust(10) + ' kontra ' + str(køn_50_p[1])+'%)')
print('\n'.ljust(121,'-'),'\n')

inequalTreatmentTwo = inequalTreatment[:]
for n in range(len(inequalTreatmentTwo)):
    inequalTreatmentTwo[n] = inequalTreatmentTwo[n][0] - inequalTreatmentTwo[n][1]
inequalTreatment_max_index = inequalTreatmentTwo.index(max(inequalTreatmentTwo))
tidl_p = [inequalTreatment[inequalTreatment_max_index][0],inequalTreatment[inequalTreatment_max_index][1]]
print('Tidligere behandling (metformin vs ingen):'.center(50),'\n')
print('Absolute max:'.ljust(15) + str(round(max(inequalTreatmentTwo),2)).ljust(9) + '(' + (str(tidl_p[0]) +'%').ljust(10) + ' kontra ' + str(tidl_p[1])+'%)')
inequalTreatmentThree = inequalTreatmentTwo[:]
inequalTreatmentThree.sort()
inequalTreatment_95_percentile_index = inequalTreatmentTwo.index(inequalTreatmentThree[int(num_of_sims*0.95-1)])
tidl_95_p = [inequalTreatment[inequalTreatment_95_percentile_index][0],inequalTreatment[inequalTreatment_95_percentile_index][1]]
print('95 percentil:'.ljust(15) + str(round(inequalTreatmentTwo[inequalTreatment_95_percentile_index],2)).ljust(9) + '(' + (str(tidl_95_p[0]) +'%').ljust(10) + ' kontra ' + str(tidl_95_p[1])+'%)')
inequalTreatment_75_percentile_index = inequalTreatmentTwo.index(inequalTreatmentThree[int(num_of_sims*0.75-1)])
tidl_75_p = [inequalTreatment[inequalTreatment_75_percentile_index][0],inequalTreatment[inequalTreatment_75_percentile_index][1]]
print('75 percentil:'.ljust(15) + str(round(inequalTreatmentTwo[inequalTreatment_75_percentile_index],2)).ljust(9) + '(' + (str(tidl_75_p[0]) +'%').ljust(10) + ' kontra ' + str(tidl_75_p[1])+'%)')
inequalTreatment_50_percentile_index = inequalTreatmentTwo.index(inequalTreatmentThree[int(num_of_sims*0.50-1)])
tidl_50_p = [inequalTreatment[inequalTreatment_50_percentile_index][0],inequalTreatment[inequalTreatment_50_percentile_index][1]]
print('50 percentil:'.ljust(15) + str(round(inequalTreatmentTwo[inequalTreatment_50_percentile_index],2)).ljust(9) + '(' + (str(tidl_50_p[0]) +'%').ljust(10) + ' kontra ' + str(tidl_50_p[1])+'%)')
print('\n'.ljust(121,'-'),'\n')
#Print info about the simulation used
if variableBlockMode == 'Always':
    print('Variable Blocks: 4 or 8 (' + str(round(chance_of_variation*100,2)) + '% chance of 8-block)')
elif variableBlockMode == 'Never':
    print('4-blocks only')
elif variableBlockMode == 'Initial':
    print('Only first blocks have 50% chance of being 8-blocks')

if randomisationType == 'Random':
    print('Randomly Distributed')
elif randomisationType == 'Ordered':
    print('Ordered Distribution')

#Print total processing time
end = time.time()
print('\n',end - start,'seconds for '+str(int(num_of_sims/1000))+',' + str(int(num_of_sims-round(num_of_sims/1000,0)*1000)).rjust(3,'0') + ' simulations with',num_of_patients,'patients')


plt.plot(range(len(stat)),stat)
plt.show()