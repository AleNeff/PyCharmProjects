import math

class Msort(object):
    
    def msort(Msort, list):
        returnList = [len(list)]
        listLength = len(returnList)
        if len(list) <= 1:
            return list
        elif len(list) == 2:
            if list[1] < list[0]:
                temp = list[0]
                list[0] = list[1]
                list[1] = temp
                return list
        splitIndex = math.ceil(listLength/2)
        Half1 = Msort.msort(list[0:splitIndex:1])
        Half2 = Msort.msort(list[splitIndex::])
        i = 0
        j = 0
        for index in range(listLength):
            if i < (len(Half1)+1) and j < (len(Half2)+1):
                if Half1[i] <= Half2[j]:
                    returnList[index] = Half1[i]
                    i += 1
                else:
                    returnList[index] = Half2[j]
                    j += 1
            if i < len(Half1):
                returnList[index] = Half1[i]
                i+=1
            elif j < len(Half2):
                returnList[index] = Half2[j]
                j+=1
            else:
                return returnList
        return returnList

Msort.msort = classmethod(Msort.msort)
MyList = [6,4,8,1,9,13,17,15,14,14,20,16]
print(Msort.msort(MyList))
