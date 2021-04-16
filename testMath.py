from strMath import*

def convertFunction(text,variable):
    temp = ''
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in ['*','/',':','+','-','^','(',')','!']:
            if char == '-' and text[i-1] in ['*','/',':','+','-','^','(',')','!']:
                temp += char
            else:
                if temp.strip() != '':
                    result.append(temp.strip())
                    temp = ''
                result.append(char)
        elif i < len(text)-1 and char+text[i+1] == 'ln':
            if temp.strip() != '':
                result.append(temp.strip())
                temp = ''
            result.append(char+text[i+1])
            i = i+1
        elif i < len(text)-2 and char+text[i+1]+text[i+2] in ['sin','tan','cos']:
            if temp.strip() != '':
                result.append(temp.strip())
                temp = ''
            result.append(char+text[i+1]+text[i+2])
            i += 2
        elif char == variable:
            if temp.strip() != '':
                result.append(temp.strip())
                temp = ''
            result.append(char)
        else:
            temp += char
        i += 1
    if temp != '':
        result.append(temp)
    return result

def derivate(list,variable):#2x ^ 2 - 3x
    i = 0
    while i < len(list):
        if 'x' in list[i]:
            pass


        i += 1




#separator for addition +  for substraction - for multiplication * or x for divsion / or :
text = '22/7'
print(text)
#temp = convert(text)
temp = convertFunction(text,'x')
print(temp)
#result = derivate(temp,'x')

print(temp)
result = math(temp)
print(result)


#converted = convert(text)
#print(converted)
#result = str(math(converted))
#print(result)
        #set to 0
#result = add(text)
#print(result)
