from PIL import Image, ImageDraw, ImageFont

def getFont(top,middle,bottom):
    fontPath = r'c:\windows\fonts\arial.ttf'
    size = 90
    font = ImageFont.truetype(fontPath, size)
    sizeTop = font.getlength(top)
    sizeMiddle = font.getlength(middle)
    sizeBottom = font.getlength(bottom)
    if sizeTop >= sizeMiddle:
        if sizeTop >= sizeBottom:
            text = top
        else:
            text = bottom
    elif sizeMiddle >= sizeBottom:
        text = middle
    else:
        text = bottom
    temp = font.getlength(text)
    while temp > im.width:
        size -= 2
        font = ImageFont.truetype(fontPath, size)
        temp = font.getlength(text)
    font = ImageFont.truetype(fontPath, size)
    return [font,size]

def draw(image,top = '', middle = '', bottom = ''):
    temp = getFont(top,middle,bottom)
    font = temp[0]
    fontSize = temp[1]
    draw = ImageDraw.Draw(image)
    if top != '':
        draw.text((0,0),top,font = font)
    if middle != '':
        draw.text((0,(image.height-fontSize)/2),middle,font = font)
    if bottom != '':
        draw.text((0, image.height-fontSize),bottom,font = font)

im = Image.open("bigHappyDanny.png")
text = 'Danniel'
position = 'middle'
draw(im,'TOP','MIDDLE','BOTTOM')
im.save('test.png')
#size = (int(im.width*1.5),int(im.height*1.5))
#new = im.resize(size)
#new.save("bigHappyDanny.png")
