import math as Math

def too_low(result):
    if 'e' in result:
        index = result.index('e')
        power = result[index+1:]
        if int(power) < 5:
            return True
    return False

def calcFunction(function,point):
    point = str(point)
    temp = function.replace('x',point)
    converted = convert(temp)
    result = math(converted)
    return result

def convert(text):
    temp = ''
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in ['*','x','/',':','+','-','^','(',')','!']:
            if temp != '':
                result.append(temp.strip())
                temp = ''
            result.append(char)
        elif i < len(text)-1 and char+text[i+1] == 'ln':
            if temp != '':
                result.append(temp.strip())
                temp = ''
            result.append(char+text[i+1])
            i = i+1
        elif i < len(text)-2 and char+text[i+1]+text[i+2] in ['sin','tan','cos']:
            if temp != '':
                result.append(temp.strip())
                temp = ''
            result.append(char+text[i+1]+text[i+2])
            i += 2
        else:
            temp += char
        i += 1
    if temp != '':
        result.append(temp)
    return result

def math(list):
    i = 0
    while i < len(list):
        c = list[i]
        if c == '(':
            temp = []
            j = i+1
            while list[j] != ')':
                temp.append(list[j])
                j += 1
            result_temp = math(temp)
            list[i] = result_temp
            for h in range(j-i):
                list.pop(i+1)
        i += 1
    i = 0
    while i < len(list):
        c = list[i]
        if c in ['ln','cos','sin','tan']:
            number1 = list[i+1]
            result = operation(number1,'',list[i])
            list[i] = result
            list.pop(i+1)
            i = i-1
        i += 1
    i = 0
    while i < len(list):
        c = list[i]
        if c in ['^','!']:
            number1 = list[i-1]
            if c == '!':
                result = operation(number1,'',list[i])
            else:
                number2 = list[i+1]
                result = operation(number1,number2,list[i])
            list[i] = result
            list.pop(i-1)
            if c != '!':
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
    if list[0] == 'pi':
        return Math.pi
    elif list[0] == 'e':
        return Math.exp(1)
    return list[0]

def operation(n1,n2,operator):
    number1 = getNumber(n1)
    if n2 != '':
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
    elif operator == '!':
        result = number1
        for i in range(number1-1,0,-1):
            result *= i
        return str(result)
    elif operator == 'ln':
        return Math.log(number1)
    elif operator == 'cos':
        result = Math.cos(number1)
        if too_low(str(result)):
            return 0
        else:
            return result
    elif operator == 'sin':
        result = Math.sin(number1)
        if too_low(str(result)):
            return 0
        else:
            return result
    elif operator == 'tan':
        result = Math.tan(number1)
        if too_low(str(result)):
            return 0
        else:
            return result


def getNumber(text):
    number1 = text
    if number1 == 'e':
        return 2.718281
    elif number1 == 'pi':
        return Math.pi
    if '.' in number1:
        number1 = float(number1)
    else:
        number1 = int(number1)
    return number1
