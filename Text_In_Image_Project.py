'''
AUSTIN DRAPER
CS 353
RUNNING IN PYTHON 2.7.12
RUNNING ON WINDOWS 10 OS
'''
from PIL import Image
import math
import array

def string2bits(msg):
    s = msg
    #convert a string of characters into 8 bit binary
    return [bin(ord(x))[2:].zfill(8) for x in s]

def encode_image(img, msg):
    """
    Use the red section of the image (r, g, b) tuple to
    hide the msg characters as binary values. Red value
    of the first pixel is used for length of msg
    """
    length = len(msg) #length of the message in characters
    msg_length = len(msg) * 8 #length of the message in bits
    #limit length of message to 255 bits
    if msg_length > 255:
        print("text too long! (don't exeed 255 bits)")
        return False
    if img.mode != 'RGB':
        print("image mode needs to be RGB")
        return False
    #use a copy of image to hide the text in
    encoded = img.copy()
    width, height = img.size
    index = 0
    row = 0
    col = 0
    while index <= length:
        r, g, b = img.getpixel((col, row))
        #first value is length of msg
        if row == 0 and col == 0 and index < length:
            leng = msg_length
            encoded.putpixel((col, row), (leng, g , b))
            col = col+1
        elif index <= length:
            c = msg[index -1]
            asc = int(c)
            temp = asc
            #for length of the binary, encode it 
            for i in range(len(str(abs(asc)))):
                if temp % 2 == 1:
                    #encode 1 in red section
                    encoded.putpixel((col, row), (1, g , b))
                    #set outer most bit to zero and remove that zero
                    temp -= 1
                    temp /= 10
                    if col < width:
                        col = col+1
                    else:
                        col = 0
                        row = row+1
                else:
                    #encode 0 in red section
                    encoded.putpixel((col, row), (0, g , b))
                    #remove outer most zero
                    temp /= 10
                    if col < width:
                        col = col+1
                    else:
                        col = 0
                        row = row+1
            #add in leading zeros until length of binary is 8
            leadzero = 8 - len(str(abs(asc)))
            while leadzero > 0:
                #encode 0 in red section
                encoded.putpixel((col, row), (0, g , b))
                leadzero -= 1
                if col < width:
                    col = col+1
                else:
                    col = 0
                    row = row+1
        #move onto the next 8 bits of binary
        index += 1
    return encoded

def decode_image(img):
    """
    check the red portion of an image (r, g, b) tuple for
    hidden message characters (ASCII values)
    """
    width, height = img.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                #need to add transparency a for some pngs
                r, g, b, a = img.getpixel((col, row))		
            #first pixel value is length of msg
            if row == 0 and col == 0:
                length = r
                #declare a zero filled array size of number of bits
                x = [0 for i in xrange(length)]
            elif index <= length:
                #fill the array with all the msg bits
                x[index-1] = r
            index += 1
            if index+1 > length:
                #turn binary into string
                str1 = ''.join(str(e) for e in x)
                #reverse the array to put bits in proper order
                #msg is still backward, needs to be reversed again later
                str2 = ''.join(reversed(str1))
                allDataz = bytearray()
                bitTracker = 0
                while bitTracker < length:
                    #turn string back into int and separate them by
                    #groups of size 8 bits
                    tempDataz = int(str2[bitTracker:bitTracker+8],2)
                    Dataz = chr(tempDataz)
                    allDataz = allDataz + bytearray(Dataz)
                    #track the bits until you've gone through all bits
                    bitTracker = bitTracker + 8
                #change type of all bits from integer to string
                a = str(allDataz)
                #reverse the string so message looks normal
                z = ''.join(reversed(a))
                msg = z
                return msg
            
    return msg

#Calls decode_image and writes the result to output.txt 
def extraction(encoded_picture):
    img2 = Image.open(encoded_picture)
    hidden_text = decode_image(img2)
    print("Hidden text:\n{}".format(hidden_text))
    fh = open("output.txt", 'w')
    fh.write(hidden_text)
    fh.close()
    return 0

'''
Control the flow of the entire program. Can choose the
Encryption path, Decryption path, or Quit the program
'''
running = True
while running:
    try:
        objective = input("Enter 1 to Encrypt, 2 to Decrypt, any other key to Quit:")
    except NameError:
        objective = 'Q'
    if objective == 1:
        #pick a .jpg file you have in the working directory
        #or give full path name
        picture = raw_input("Enter name of .jpg to encript: ")
        img = Image.open(picture)
        #image mode needs to be 'RGB'
        print(img, img.mode)
        #create a new filename for the encoded image
        encoded_picture = "enc_" + picture
        encoded_picture = encoded_picture[:-3]
        encoded_picture = encoded_picture + "png"
        #don't exceed 255 bits in the message
        dataPath = raw_input("Enter name of .txt to read message from: ")
        dataInput = open(dataPath, 'r')
        Dataz = (dataInput.read())
        Dataz = string2bits(Dataz)
        img_encoded = encode_image(img, Dataz)
        dataInput.close()
               
        if img_encoded:
            #save the image with the hidden text
            img_encoded.save(encoded_picture)
            print("{} saved!".format(encoded_picture))
            #view the saved file, works with Windows only
            #behaves like double-clicking on the saved file
            #import os
            #os.startfile(encoded_picture)
            '''
            this code works on more OS's
            import webbrowser
            webbrowser.open(encoded_image_file)
            '''
    elif objective == 2:
        enc_picture = raw_input("Enter name of .png to decode: ")
        #get the hidden text back ...
        end = extraction(enc_picture)
    else:
        #end the program
        running = False
        
exit(0)

