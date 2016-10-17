###
###
###
from Tkinter import *
import tkFileDialog
import csv
import sys
import itertools
import textwrap
import os
from collections import Counter
from collections import defaultdict
from collections import OrderedDict
from array import *

##########################################
### GOT TO RENAME THESE VARIABLES SOON ###
##########################################
merchantsales = {} #This stores MERCH ID and Number of sales in Dict format
receiptvalue = {} #This stores receipt ID and Value in Dict format
receiptids = [] #Receipt IDs in a list
#receiptDict = {} #Dictionary where Keys=ID, Data=Receipt
merchantDict = {} #Dictionary where Keys=Merchant Name, Data=ID
sortedmerchantDict = {} #Sorted merchantDict

root = Tk()
displayBox = Listbox(root)
tBox = Text(root, state='disabled',width=550, height=600,wrap='none')
'''
Display box is a global, use the below 2 lines to update its value i.e. change your print to below
displayBox.delete(0, END)
displayBox.insert(END, 'your string value')#change its string
'''
global csvfile_dir # GLOBAL VAR
class ApplicationMain(Frame):
    def __init__(self, master = None):
        Frame.__init__(self,master)
        self.grid()
        self.createWidgets()
        

    def createWidgets(self): #Create Widgets
        frame = Frame(root)
        frame.pack()
        
        displayBox.pack(fill=X,padx=20,pady=30)
        displayBox.yview()
        
        #tBox.insert('1.0', "TESTTESTTESTTESTTESTTESTTEST")
        btn1 = Button(root, text='Load CSV', command=self.readCSV)
        btn1.pack(fill=X,padx=50,pady=5,ipady=15)
        btn2 = Button(root, text='Export to File', command=self.exportDataToFile)
        btn2.pack(fill=X,padx=50,pady=5,ipady=5)
        btn3 = Button(root, text='List Total Receipt by Merchant', command=self.listTotalReceipts)
        btn3.pack(fill=X,padx=50,pady=5,ipady=5)
        btn4 = Button(root, text='Total Sales', command=self.totalSales)
        btn4.pack(fill=X,padx=50,pady=5,ipady=5)
        btn5 = Button(root, text='All Items Sold', command=self.listAllSoldItems)
        btn5.pack(fill=X,padx=50,pady=5,ipady=5)
        btn6 = Button(root, text='Export to CSV', command=self.exportCSV)
        btn6.pack(fill=X,padx=50,pady=5,ipady=5)
        btn7 = Button(root, text='Find Association & Show Recommendation', command=self.findAssociationindata)
        btn7.pack(fill=X,padx=50,pady=5,ipady=5)
        btn8 = Button(root, text='Log Sheet', command=self.logSheet)
        btn8.pack(fill=X,padx=50,pady=5,ipady=5)

        top = self.winfo_toplevel()
        self.menuBar = Menu(top) # Create Top menu bar
        top["menu"] = self.menuBar
        self.subMenu = Menu(self.menuBar) #Sub menu in Menu button
        self.menuBar.add_cascade(label = "Load CSV", menu = self.subMenu)  #File
        self.subMenu.add_command(label = "Open",command = self.readCSV)  #Read data
        self.subMenu.add_command(label = "Export to File",command = self.exportDataToFile) # FUNCTION 2
        self.subMenu.add_command(label = "List Total Receipt by Merchant",command = self.listTotalReceipts) # FUNCTION 3
        self.subMenu.add_command(label = "Total Sales", command = self.totalSales) # Function 4
        self.subMenu.add_command(label = "All Items Sold", command = self.listAllSoldItems) # Function 5
        self.subMenu.add_command(label = "Find Association", command = self.findAssociationindata) # Function 7 findAssociationindata

    def clearAll(self): 
        '''This ensures a clean state so we don't carry over old data.
        '''
        receiptids[:] = []
        receiptvalue.clear()
        merchantsales.clear()
    
    def updateDisplaybox(self, cleanscreen, text): 
        '''Updates the Display box - A true in Cleanscreen empties the displayBox. text is basically the string you want to print 
        '''
        if cleanscreen == True:
            displayBox.delete(0, END)
        textOut = textwrap.fill(text, 20)
        displayBox.insert(END, textOut)

    def sortDict(self):
        '''Clean Up data for MerchID''' 
        for mercId in merchantDict.keys():
            for data in merchantDict[mercId]:
                if mercId in sortedmerchantDict:
                    sortedmerchantDict[mercId].append(receiptvalue[data])
                else:
                    sortedmerchantDict[mercId] = [receiptvalue[data]]


    def readCSV(self):
        self.clearAll() # Ensure Clean state
        self.file_opt = options = {}
        options['filetypes'] = [('csv files', '.csv')] #Basically restricts to .csv files
        csvfile_dir = tkFileDialog.askopenfilename(**self.file_opt) #Dialog to open file
        if csvfile_dir != "":
            f = open(csvfile_dir, 'r') # opens the csv file
            rowid = 0
            read = csv.reader(f, delimiter = ",") # Read the CSV
            read.next() # Skip header
            for row in read:
                receiptids.append(row[0]) # Record RECEIPT IDS
                if row[0] in receiptvalue: # append the new data to the existing array at this slot
                    receiptvalue[row[0]].append(row[1]) #Record receipt data in Dict with slot receipt ID
                else: # create a new array in this slot
                    receiptvalue[row[0]] = [row[1]] #Record receipt data in Dict with slot receipt ID

                    #-------IMPORTANT TO ADD TO MAIN CODE---------
                    #Build dictionary where Keys=Merchant Name, Data=ID
                    if row[1] in merchantDict: #If Merch name exist in dict add the receipt id
                        merchantDict[row[1]].append(row[0])
                    else: # If Merch name does not exist, new array with the first item row[0]
                        merchantDict[row[1]] = [row[0]]
                    #---------------------------------------------

                    if row[1] in merchantsales: #If Merch name exist in dict
                        merchantsales[row[1]] += 1; #INC. number
                    else: # If Merch name does not exist in dict
                        merchantsales[row[1]] = 1; # Create

            self.sortDict()
            f.close()  
        
            self.updateDisplaybox(True, 'CSV read successfully!')
        ### DEBUGGING LINES ###  
        '''
        print "storedata"
        print receiptids
        print "storedata2 keys"
        print receiptvalue.keys()
        print "storedata2 values"
        print receiptvalue.values()
        print "storedata3 values"
        print merchantsales.values()
        print "storedata2 sorted"
        for key in sorted(receiptvalue):
            print "%s: %s" %(key, receiptvalue[key])
        print "storedata3 sorted"
        for key in sorted(merchantsales):
            print "%s: %s" %(key, merchantsales[key])
        '''
        ### DEBUGGING LINES ### 
    def makeDirectory(self,path):
        ''' Creates Directory safely
        '''
        try: 
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                print "FAILED TO CREATE PATH: " +str(path)
                self.updateDisplaybox(True, 'FAILED TO CREATE PATH: ' +str(path))
                raise

    def safeopenPath(self,path):
        ''' Open "path" for writing, creating any parent directories as needed.
        '''
        self.makeDirectory(os.path.dirname(path))
        return open(path, 'w')
    

    def writetoFile(self, path, data):
        ''' This Function should be used to create files into the disk with data written into it.
        example will be writetoFile(Path of file with .type at the end, stringofData)
        '''
        with self.safeopenPath(path) as output_file: #Begin write process
            output_file.write(str(data)+"\n")

    def exportDataToFile(self): ## Exports read data into files by receipt ID
        ''' This function causes the program to export all stored receipt in memory to an output file based on receiptids
            IDs. No extra data required. This function is I/O Heavy, use sparingly'''
        if not receiptvalue:
            print "receiptvalue is empty"
            #displayBox.delete(0, END)
            #displayBox.insert(END, 'ERROR in Receiptvalue - Have you loaded CSV data?')
            self.updateDisplaybox(True, 'ERROR in Receiptvalue - Have you loaded CSV data?')
            return False

        towriteData = "" #String data to be written
        for receipt_id in receiptvalue.keys(): # GET ALL THE IDS
            towriteData = "" # EMPTY TEMP HOLDER
            for data in receiptvalue[receipt_id]: # LOOP WITHING VALUE IN KEY
                if towriteData == "": #There used to be a case where the empty string causes file to have an empty line at start
                    towriteData = data
                else:
                    towriteData = towriteData + "\n" +data

            filename = "./ExportedData/"+str(receipt_id)+".txt"
            self.writetoFile(filename,towriteData)

        print "Receipt Data Sucessfully exported."
        self.updateDisplaybox(True, 'Receipt Data Sucessfully exported!')
        towriteData = "" # Ensure Clean state

    def extractFloat(self, data): #Extracts Numbers from string - self.extractFloat(string)
        '''
        This function causes the program to extract numbers from given data, returning it.
        Normally used to extract a number from a row of receipt data but can be used for alot more.

        usage:
        self.extractFloat(data in list)

        [-+]? # optional sign
        (?:
            (?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
            |
            (?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
        )
        # followed by optional exponent part if desired
        (?: [Ee] [+-]? \d+ ) ?
        '''
        result = re.findall(r"[-+]?\d*\.\d+|\d+", data)
        for i in result:
            return i
        

    def matchWords(self, data1, data2): #
        '''Checks for data1, in LIST data2 - self.matchWords("Word", list)
        '''
        if data1 in data2:
            return True
        else:
            return False

    def totalSales(self): 
        '''# Get Total sales from data
        '''
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR in Receiptvalue - Have you loaded CSV data?')
            return False

        tempdata = []
        #receiptvalue receipt id: [ Merch name... TOTAL $$$ ]
        for receiptid in receiptvalue.keys():
            for data in receiptvalue[receiptid]:
                if self.matchWords("TOTAL", data):
                    #print "TRUE: "+str(data)
                    value = self.extractFloat(data) #Send to extract value within the dataline
                    #print value
                    tempdata.append(value) # append value to a temp list
                    #print tempdata  
                else:
                    continue
                    #print "FALSE: "+str(data)
        result = 0
        for i in tempdata: #Draw out values from temp list
            result = result + float(i) # Sum them up
       
        print "Total sales: " +str(result)
        self.updateDisplaybox(True, "Total sales: " +str(result))
        tempdata = [] # Ensure Clean state
        value = 0 # Ensure Clean state
        result = 0 # Ensure Clean state
        
        

    def listTotalReceipts(self):
        if not merchantsales:
            print "merchantsales is empty"
            self.updateDisplaybox(True, 'Error: merchantsales is empty - Have you loaded CSV data?')
            return False

        #print "storedata3 sorted"
        print "Number of Total receipt by Merchants:"
        self.updateDisplaybox(True, 'Number of Total receipt by Merchants:')
        for key in sorted(merchantsales):
            print "%s: %s" %(key, merchantsales[key])
            self.updateDisplaybox(False, "%s: %s" %(key, merchantsales[key]))


    def listAllSoldItems(self):
        ''' Templates
        Chin Wan Logic PTE LTD
        ---------------------
        (ITEMS)
        ---------------------

        COQ SEAFOOD
        ===================
        (OTHERS)
        ===================
        (ITEMS)
        -------------------
        '''
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR in Receiptvalue - Have you loaded CSV data?')
            return False
            
        itemlist1 = []
        itemlist2 = []
        dict = {}
        endString = '----------------------------------'
        for merchantname in sortedmerchantDict:
            for receiptdata in sortedmerchantDict[merchantname]:
                if merchantname == 'COQ SEAFOOD': # COQ Seafood
                    linestart = 10
                    count = 0
                    while count == 0:
                        if receiptdata[linestart] != endString:
                            extractline = receiptdata[linestart]
                            extractline = extractline[3:32].strip()
                            itemlist1.append(extractline)
                        else:
                            count = 1

                        linestart += 1
                else:
                    linestart = 8
                    count = 0
                    while count == 0:
                        if receiptdata[linestart] != endString:
                            extractline2 = receiptdata[linestart]
                            extractline2 = extractline2[3:32].strip()
                            itemlist2.append(extractline2)
                        else:
                            count = 1

                        linestart += 1
        setlist2 = set(itemlist2)
        newlist2 = list(setlist2)

        Merchantname1 = sortedmerchantDict.keys()[0]
        Merchantname2 = sortedmerchantDict.keys()[1]
        dict[Merchantname1] = [n for n in newlist2]
        dict[Merchantname2] = [n for n in itemlist1]
        solditem1 = " and ".join([",".join(str(n) for n in dict[Merchantname1][0:-1]), dict[Merchantname1][-1]])
        solditem2 = " and ".join([",".join(str(n) for n in dict[Merchantname2][0:-1]), dict[Merchantname2][-1]])
        print "The items sold in %s are %s.\n" %(Merchantname1, solditem1)
        print "The items sold in %s are %s." %(Merchantname2, solditem2)
        
        self.updateDisplaybox(True, "The items sold in %s are :" %(Merchantname1))
        self.updateDisplaybox(False, "%s." %(solditem1))
        self.updateDisplaybox(False, " ")
        self.updateDisplaybox(False, "The items sold in %s are :" %(Merchantname2))
        self.updateDisplaybox(False, "%s." %(solditem2))


    def findAssociations(self, merchant,itemLine,endString,dataDict):
        itemList= []
        singleDict = {}
        combiDict = {}
        for data in dataDict[merchant]:
            #Data[n] is the line number, for COQ Seafood items start at line 11
            ln=itemLine
            flag=0
            tempList = []
             # templist to store items of single receipt
            while flag==0:
                
                if str(data[ln]) != endString:
                    rawString = data[ln] 
                    name = rawString[3:32].strip() #strips only the item name from line
                    tempList.append(name)
                    ln+=1
                else: #Reached the last item for this receipt
                    if len(tempList)!=0: #if not empty append the list to itemList
                        itemList.append(tempList)

                        for L in range(1, 3):  
                            #generate combinations and save to combiList
                            for c in itertools.permutations(tempList, L):
                                combiString = str(c)
                                combiString = combiString.strip('(')
                                combiString = combiString.strip(')')
                                combiString = combiString.replace("\'", "")

                                if L==1: #Item is a single
                                    combiString = combiString.replace(",", "")
                                    if combiString in singleDict: #If combination exists in dict add the number
                                        singleDict[combiString] += 1
                                    else: # If Merch name does not exist, new array with the first item row[0]
                                        singleDict[combiString] = 1
                                    
                                else: #Item is a pair combination
                                    if combiString in combiDict: #If combination exists in dict add the number
                                        combiDict[combiString] += 1
                                    else: # If Merch name does not exist, new array with the first item row[0]
                                        combiDict[combiString] = 1
                        tempList = []
                    flag=1        
        return [combiDict,singleDict]

    def promoAdviser(self, anchorProduct,relatedProduct,anchorProductCount,correlation): #Data types should be as follows (str,str,float,float)
        corIncrease1 = 0.05 #Estimates for the increase for each case
        corIncrease2 = 0.20
        corIncrease3 = 0.25
        anchorProductTime = 2.0
        subRate = 0.3       #The percentage of people expected to use the offer (out of all customers that buy the anchor product)
        promoDuration = 7.0 #How long the promotion will last
        breakEvenDate = 30  #A measure of when lost profits are to be earned back (e.g. 50% discount means you could have earned 50% more)
        subCount = anchorProductCount/anchorProductTime*subRate #How many people per day will use the offer
        correlation = float(correlation)
        anchorProductCount = float(anchorProductCount)
      
        if correlation/anchorProductCount > 0.8:
            self.updateDisplaybox(False, "No promotion recommended as %s and %s already have a high correlation. A promotion would not boost profits."  %(anchorProduct, relatedProduct))
            print "No promotion recommended as %s and %s already have a high correlation. A promotion would not boost profits."  %(anchorProduct, relatedProduct)
        elif  0.5 <= (correlation/anchorProductCount) <= 0.8:
            promoBudget = subCount*corIncrease1*breakEvenDate
            promoAmount = promoBudget/promoDuration/subCount*100
            self.updateDisplaybox(False, "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease1*100,'%', breakEvenDate))
            print "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease1*100,'%', breakEvenDate)
            self.updateDisplaybox(False, "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct))
            print "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct)
        elif  0.2 <= (correlation/anchorProductCount) < 0.5:
            promoBudget = subCount*corIncrease2*breakEvenDate
            promoAmount = promoBudget/promoDuration/subCount*100
            self.updateDisplaybox(False, "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease2*100,'%', breakEvenDate))
            print "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease2*100,'%', breakEvenDate)
            print "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct)
            self.updateDisplaybox(False, "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct))
      
        elif  0 <= (correlation/anchorProductCount) < 0.2:
            promoBudget = subCount*corIncrease3*breakEvenDate
            promoAmount = promoBudget/promoDuration/subCount*100
            print "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease3*100,'%', breakEvenDate)
            self.updateDisplaybox(False, "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease3*100,'%', breakEvenDate))
            print  "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct)
            self.updateDisplaybox(False, "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct))


    def findAssociationindata(self):
        if not sortedmerchantDict:
            print "sortedmerchantDict is empty"
            self.updateDisplaybox(True, 'ERROR in sortedmerchantDict - Have you loaded CSV data?')
            return False

        #retList = self.findAssociations("COQ SEAFOOD",11,'----------------------------------',sortedmerchantDict)
        retList = self.findAssociations("Chin Wan Logic PTE LTD",8,'----------------------------------',sortedmerchantDict)
        combiDict = retList[0]
        singleDict = retList[1]
        self.updateDisplaybox(True,"Finding Association within data..")
        for item in singleDict:
            
            print '\n====== %s: %s total ======' % (item,str(singleDict[item]))
            self.updateDisplaybox(False,'\n====== %s: %s total ======' % (item,str(singleDict[item])))
            for i in [key for key, value in combiDict.items() if str(item).lower() in key.lower()]:

                relation = i.split(',')
                if relation[0]==item:
                    percent = round(float(combiDict[i])/float(singleDict[item])*100,1)
                    print i+': '+str(combiDict[i])+' (~'+str(percent)+'%)'
                    displayBox.insert(END, i+': '+str(combiDict[i])+' (~'+str(percent)+'%)')

                    self.promoAdviser(relation[0],relation[1],singleDict[relation[0]],combiDict[i])
                    print '\n'
    
    def exportCSV(self):
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR in Receiptvalue - Have you loaded CSV data?')
            return False

        #Begin creating/rewriting file named 'csvOutput.csv'
        #tempFile = open('csvOutput.csv', 'w')
        #tempFile.close()
        with open('csvOutput.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Receipt ID','Name','Address','Date','Time','Items','Amount','Cost','Total'])
            for receiptid in receiptvalue.keys():
                index=1
                tempStr=''
                outputList=[]
                itemList=[]#Item list
                itemCountList=[]
                itemPriceList=[]
                total=''
                outputList.append(receiptid)
                for line in receiptvalue[receiptid]:
                    line=line.strip()
                    if not line=='':
                        #Assuming line starts from 2
                        #Assuming Company name appears in line 2, addresses appears in line 3 and 4
                        if index<=1:
                            outputList.append(line)
                        if index>1 and index<=3:
                            tempStr+=line + " "
                        if not tempStr=='' and index==4:
                            outputList.append(tempStr.strip())
                        #Search for date/time next format digit/digit/digit
                        temp = re.search('^\d+\/\\d+\/\d+', line)
                        if not temp==None:
                            
                            #Date and Time regex matching, Assuming they are on same line
                            dateStr = re.sub('\s+.*', '', line)
                            timeStr = re.sub('^\d+\/\\d+\/\d+\s*', '', line)
                            timeStr = re.sub('\s.*', '', timeStr)
                            outputList.append(dateStr)
                            outputList.append(timeStr)

                        #Search for items
                        temp = re.search('^\d+\s+\D+\s+\d', line)
                        if not temp==None:
                            item = re.sub('^\d+\s+','',line)
                            item = re.sub('\s\s+.*','',item)
                            itemList.append(item)
                            itemCount = re.sub('\s+.*','',line)
                            itemCountList.append(itemCount)
                            itemPrice = re.sub('^.*\s+','',line)
                            itemPrice = itemPrice.rstrip('0').rstrip('.')
                            itemPriceList.append(itemPrice)
                            
                        temp = re.search('^TOTAL\s*', line.upper())
                        if not temp==None:
                            total = re.sub('TOTAL\s*','',line.upper())
                            total = total.rstrip('0').rstrip('.')
                            
                    index+=1
                #Will only store all the items/item count/price
                #in list until all items are read, then join into 'outputList
                outputList.append(','.join(itemList))
                outputList.append(','.join(itemCountList))
                outputList.append(','.join(itemPriceList))
                outputList.append(total)
                writer.writerow(outputList)
        csvfile.close()
        print "Created csvOutput.csv!"
        self.updateDisplaybox(True,"Exported CSV")

    def logSheet(self):
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR in Receiptvalue - Have you loaded CSV data?')
            return False

        displayBox.delete(0, END)
        for merchant in sortedmerchantDict:
            if merchant == "COQ SEAFOOD":
                print ""
                print "COQ SEAFOOD"
                print "DATE       TIME  WAITER CASHIER"
                displayBox.insert(END, "COQ SEAFOOD")
                displayBox.insert(END, "DATE       TIME  WAITER CASHIER")
                
    
            elif merchant == "Chin Wan Logic PTE LTD":
                print ""
                print "Chin Wan Logic PTE LTD"
                print "DATE       TIME  WAITER CASHIER"
                displayBox.insert(END, "Chin Wan Logic PTE LTD")
                displayBox.insert(END, "DATE       TIME  WAITER CASHIER")
    
            for receiptsList in sortedmerchantDict[merchant]:
                logSheet = ""
                if merchant == "COQ SEAFOOD":
                    lineNum = [7,8]
                    for line in lineNum:
                        timeStamp = receiptsList[line]
                        if line == 7:
                            logSheet += timeStamp[0:16].strip()
                            logSheet += " "
                        elif line == 8:
                            logSheet += timeStamp[19:24].strip()
                            logSheet += "  "                   
                    logSheet += "N/A"
                    print logSheet
                    self.updateDisplaybox(False, logSheet)
    
                elif merchant == "Chin Wan Logic PTE LTD":
                    lineNum = [0,4,6]
                    for line in lineNum:
                        timeStamp = receiptsList[line]
                        if line == 4:
                            logSheet += timeStamp[0:16].strip()
                            logSheet += " N/A    "
                        elif line == 6:
                            logSheet += timeStamp[9:12].strip()                   
                    print logSheet
                    self.updateDisplaybox(False, logSheet)
                    
                else:
                    print "COMPANY NOT RECOGNIZED"
                    self.updateDisplaybox(False, "COMPANY NOT RECOGNIZED")


app = ApplicationMain()
app.master.title("test") #Title is set here
app.master.geometry("600x650")
app.master.resizable(0,0)
app.mainloop()


