import sys, struct  #enables us to import arguments from command line, and
                    #allows us to import strings as binary data

voltfactor=4      #76/voltfactor = the maximum positive voltage in the signal
rpm=6000          #total rpm of the signal

infile = sys.argv[1] # use the value we passed in the cmd lineas the source filename

with open(infile, "rb") as f: #openf the input file for read binary (rb)
  
    pixel = f.read(3) # grab the first 3 bytes from the file	

    pixelcount=0     #this will be a count variable that says how many pixels have gone past in the program
    
    voltage=[]       # These two tuples hold final value of point
    time=[]

    while pixel:   # loop through 3 bytes at a time until cmplete
        r,g,b = struct.unpack("BBB", pixel) # split the bytes into the individual color components
        if r==0:    #looks to see if the pixel currently selected is black, as black hex code is 00 00 00 
                    #and white is ff ff ff,
          
          row= (pixelcount/178) #gives height from the top of the image in pixels
          vertheight= 76-row    #0v point was found to be on row 76, therefore this sets this point as y=0
          t= pixelcount-(row*178) #calulates x position on picture as picture is 178 pixels wide
          
          volt=round((vertheight/voltfactor),2) #sets variable to calulate voltage at a point and round to 2 d.p.

          timeposition=round(((t/177.0)/rpm)*1000,3) #calulates x-pos in seconds, then times by 1000
                                                          #to give answer in ms, then round to 3 d.p.

          
          print vertheight, t, volt, timeposition       #allows user to check it's working in the console
    
          time+=(timeposition,)     #adds time value of pixel to time tuple
          voltage+=(volt,)          #adds volt value of pixel to volt tuple
        pixelcount=pixelcount+1        
        # read the next 3 bytes from the file
        pixel = f.read(3)
    
    total= zip (time, voltage)  #puts both tuples together to make tuple of tuples. Each entry has two values

def getKey(item):
  return item[0]            #creates a variable that allows us to sort the tuples by the time variable

sort=sorted(total, key=getKey)  #creates new tuple with each value ordered by time variable

o=open("output_maxrpm.txt", "w") #creates a text file so that we can write values into it and sets it to write

firstvals=[x[0] for x in sort]  #defines firstvals as the time values
secondvals=[x[1] for x in sort] #defines secondvals as the voltage values

for i in range(len(sort)):    #runs through the sort tuple per value
  print>>o, str(firstvals[i]) + "m", " ", str(secondvals[i]) + "\r\n" #prints time then appends with letter 'm'
                                                                      #adds tab then prints time and newline.
