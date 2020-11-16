def convert(text):
    temp = ''
    result = []
    i = 0
    for char in text:
        if char in ['*','x','/',':','+','-','^']:
            result.append(temp.strip())
            result.append(char)
            temp = ''
        else:
            temp += char
    result.append(temp)
    return result

def math(list):
    i = 0
    while i < len(list):
        c = list[i]
        if c == '^':
            number1 = list[i-1]
            number2 = list[i+1]
            result = operation(number1,number2,list[i])
            list[i] = result
            list.pop(i-1)
            list.pop(i)
            i = i-1
        i += 1
    i = 0
    while i < len(list):
        c = list[i]
        if c in ['*','x','/',':']:
            number1 = list[i-1]
            number2 = list[i+1]
            result = operation(number1,number2,list[i])
            list[i] = result
            list.pop(i-1)
            list.pop(i)
            i = i-1
        i += 1
    i = 0
    while i < len(list):
        c = list[i]
        if c in ['-','+']:
            number1 = list[i-1]
            number2 = list[i+1]
            result = operation(number1,number2,list[i])
            list[i] = result
            list.pop(i-1)
            list.pop(i)
            i = i-1
        i += 1
    return list[0]

def operation(n1,n2,operator):
    number1 = getNumber(n1)
    number2 = getNumber(n2)
    if operator == '+':
        return str(number1+number2)
    elif operator == '-':
        return str(number1-number2)
    elif operator in ['x','*']:
        return str(number1*number2)
    elif operator in ['/',':']:
        return str(number1/number2)
    elif operator == '^':
        return str(number1**number2)

def getNumber(text):
    number1 = text
    if '.' in number1:
        number1 = float(number1)
    else:
        number1 = int(number1)
    return number1
