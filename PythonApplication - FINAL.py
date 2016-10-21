
import csv #Read/Write .csv
import itertools #To obtain permutations in our 'findAssociations' function
import os #To export data in new '.csv'
 
from Tkinter import * #GUI
import tkFileDialog #GUI
import sys #GUI
 
 
merchantsales = {} #This stores MERCH ID and Number of sales in Dict format
receiptvalue = {} #This stores receipt ID and Value in Dict format
receiptids = [] #Receipt IDs in a list
#receiptDict = {} #Dictionary where Keys=ID, Data=Receipt
merchantDict = {} #Dictionary where Keys=Merchant Name, Data=ID
sortedmerchantDict = {} #Sorted merchantDict
 
root = Tk()
labelvar = StringVar()
displayBox = Text(root,wrap=WORD,height=15)
selectedMerc = StringVar(root)
selectedOp = StringVar(root)
dropdownOptions = {}
 
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
        row1 = Frame(root)
        row1.pack(fill=X)
 
        btn1 = Button(row1, text='Load CSV', command=self.readCSV)
        btn1.pack(side=LEFT,padx=30,pady=5,ipadx=60,ipady=10)
 
        labelvar.set("No CSV Loaded")
        labelTop = Label( row1, textvariable=labelvar)
        labelTop.pack(side=LEFT)
 
        displayBox.pack(fill=X,padx=20,pady=20)
        displayBox.yview()
         
        _platform = sys.platform
        if _platform == "linux" or _platform == "linux2":
            # linux
            print "Linux"
        elif _platform == "darwin":
            # MAC OS X
            print "MacOS"
 
            row6 = Frame(root)
            row6.pack(fill=X)
            opList = ['Export to File', 'List Total Receipt by Merchant', 'Total Sales', 'All Items sold','Export to CSV','Log sheet']
            selectedOp.set('Select Operation')
            optionMac = OptionMenu(row6, selectedOp, *opList)
            optionMac.pack(side=LEFT,padx=30)
            optionMac.configure(height=2,width=50)
 
            btn9 = Button(row6, text='Execute', command=self.findSelectedOperation, height=4, width=20)
            btn9.pack(side=LEFT,pady=20)
        elif _platform == "win32":
            # Windows
            row2 = Frame(root)
            row2.pack(fill=X)
            btn2 = Button(row2, text='Export to File\n', command=self.exportDataToFile, height=4, width=35)
            btn2.pack(side=LEFT,padx=30,pady=10)
            btn3 = Button(row2, text='List Total Receipt\n by Merchant', command=self.listTotalReceipts, height=4, width=35)
            btn3.pack(side=LEFT)
 
            row3 = Frame(root)
            row3.pack(fill=X)
            btn4 = Button(row3, text='Total Sales\n', command=self.totalSales, height=4, width=35)
            btn4.pack(side=LEFT,padx=30,pady=10)
            btn5 = Button(row3, text='All Items Sold\n', command=self.listAllSoldItems, height=4, width=35)
            btn5.pack(side=LEFT)
 
            row4 = Frame(root)
            row4.pack(fill=X)
            btn6 = Button(row4, text='Export to CSV', command=self.exportCSV, height=4, width=35)
            btn6.pack(side=LEFT,padx=30,pady=10)
            btn7 = Button(row4, text='Log Sheet', command=self.logSheet, height=4, width=35)
            btn7.pack(side=LEFT)
 
 
        row5 = Frame(root)
        row5.pack(fill=X)
 
        mercList = ['Chin Wan Logic PTE LTD', 'COQ SEAFOOD']
        selectedMerc.set('Chin Wan Logic PTE LTD')
        option1 = OptionMenu(row5, selectedMerc, *mercList)
        option1.pack(side=LEFT,padx=30)
        option1.configure(height=2,width=50)
 
         
        btn8 = Button(row5, text='Find Associations & \nRecommendations', command=self.findMercAssoc, height=4, width=20)
        btn8.pack(side=LEFT,pady=20)
         
         
        top = self.winfo_toplevel()
        self.menuBar = Menu(top) # Create Top menu bar
        top["menu"] = self.menuBar
        self.subMenu = Menu(self.menuBar) #Sub menu in Menu button
        self.menuBar.add_cascade(label = "Load CSV", menu = self.subMenu)  #File
        self.subMenu.add_command(label = "Open",command = self.readCSV)  #Read data
        self.subMenu.add_command(label = "Export to File",command = self.exportDataToFile) # Function 2
        self.subMenu.add_command(label = "List Total Receipt by Merchant",command = self.listTotalReceipts) # Function 3
        self.subMenu.add_command(label = "Total Sales", command = self.totalSales) # Function 4
        self.subMenu.add_command(label = "All Items Sold", command = self.listAllSoldItems) # Function 5
        self.subMenu.add_command(label = "Export data to CSV", command = self.exportCSV) # Function 6 exportCSV
        self.subMenu.add_command(label = "Find Association & Recommendation", command = self.findMercAssoc) # Function 7 findMercAssoc
        self.subMenu.add_command(label = "Log Sheet", command = self.logSheet) # Function 8
 
    def clearAll(self): 
        '''
        This ensures a clean state so we don't carry over old data.
        - Jerry
        '''
        receiptids[:] = []
        receiptvalue.clear()
        merchantsales.clear()
     
    def updateDisplaybox(self, cleanscreen, text): 
        '''
        Updates the Display box :
        A true in Cleanscreen empties the displayBox. 
        Text is basically the string you want to print
        - Jerry 
        '''
        if cleanscreen:
            displayBox.delete(0.0, END)
         
        if text != "":
            displayBox.insert(END, text+"\n")
 
    def sortDict(self):
        '''Clean Up data for MerchID'''
        for mercId in merchantDict.keys():
            for data in merchantDict[mercId]:
                if mercId in sortedmerchantDict:
                    sortedmerchantDict[mercId].append(receiptvalue[data])
                else:
                    sortedmerchantDict[mercId] = [receiptvalue[data]]
 
    def readCSV(self): #-------------- | FUNCTION 1 | --------------# DONE BY JERAHMEEL
        ''' 
        This is the primary function of the program. Takes the CSV files and reads it line by line.
        from there we store and sort the data out into different list and dict types for our needs.
        This function can be runned more than one to update the data within.
        updated list/dict
        merchantsales = {} #This stores MERCH ID and Number of sales in Dict format
        receiptvalue = {} #This stores receipt ID and Value in Dict format
        receiptids = [] #Receipt IDs in a list
        #receiptDict = {} #Dictionary where Keys=ID, Data=Receipt
        merchantDict = {} #Dictionary where Keys=Merchant Name, Data=ID
        sortedmerchantDict = {} #Sorted merchantDict
        - Jerry
        '''
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
 
                    #Build dictionary where Keys=Merchant Name, Data=ID
                    if row[1] in merchantDict: #If Merch name exist in dict add the receipt id
                        merchantDict[row[1]].append(row[0])
                    else: # If Merch name does not exist, new array with the first item row[0]
                        merchantDict[row[1]] = [row[0]]
 
                    if row[1] in merchantsales: #If Merch name exist in dict
                        merchantsales[row[1]] += 1; #INC. number
                    else: # If Merch name does not exist in dict
                        merchantsales[row[1]] = 1; # Create
 
            self.sortDict()
            f.close()  
            labelvar.set(csvfile_dir[csvfile_dir.rfind("/")+1:]+" loaded")
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
        ''' Creates Directory safely - Jerry
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
        - Jerry
        '''
        self.makeDirectory(os.path.dirname(path))
        return open(path, 'w')
     
 
    def writetoFile(self, path, data):
        ''' 
        This Function should be used to create files into the disk with data written into it.
        example will be writetoFile(Path of file with .type at the end, stringofData) 
        - Jerry
        '''
        with self.safeopenPath(path) as output_file: #Begin write process
            output_file.write(str(data)+"\n")
 
 
 
    def exportDataToFile(self): #-------------- | FUNCTION 2 | --------------# DONE BY JERAHMEEL
        ''' 
        This function causes the program to export all stored receipt in memory to an output file based on receiptids
        IDs. No extra data required. This function is I/O Heavy, use sparingly 
        - Jerry
        '''
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR: Receiptvalue is empty - Have you loaded CSV data?')
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
        ''' Jerry -
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
         
    def matchWords(self, data1, data2): 
        '''
        Checks for data1, in LIST data2 
        usage: self.matchWords("Word", list) 
        - Jerry
        '''
        if data1 in data2:
            return True
        else:
            return False
             
 
 
    def listTotalReceipts(self): #-------------- | FUNCTION 3 | --------------#
        '''
        As merchantsales has already been compiled during our 'readCSV' function,
        we simply use as 'if' statement to validate if a file has been read and if so,
        use a for loop to print it in order accordingly.
        - Lucas
        '''
        if not merchantsales:
            print "merchantsales is empty"
            self.updateDisplaybox(True, 'ERROR: merchantsales is empty - Have you loaded CSV data?')
            return False
 
        #print "storedata3 sorted"
        print "Number of Total receipt by Merchants:"
        self.updateDisplaybox(True, 'Number of Total receipt by Merchants:')
        for key in sorted(merchantsales):
            print "%s: %s" %(key, merchantsales[key])
            self.updateDisplaybox(False, "%s: %s" %(key, merchantsales[key]))
             
 
 
    def totalSales(self): ##-------------- | FUNCTION 4 | --------------#
        '''
        Get Total sales from data 
        - Jerry
        '''
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR: Receiptvalue is empty - Have you loaded CSV data?')
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
 
 
 
    def listAllSoldItems(self): #-------------- | FUNCTION 5 | --------------#
        ''' Dylan & Jun Loong
        '''
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR: Receiptvalue is empty - Have you loaded CSV data?')
            return False
             
        itemlist1 = [] # Assign empty list to variable itemlist1 for storing sold items from merchant "COQ SEAFOOD".
        itemlist2 = [] # Assign empty list to variable itemlist2 for storing sold items from merchant "Chin Wan Logic PTE LTD".
        dict = {} # Create empty dictionary.
        endString = '----------------------------------' # Search parameter assigned to variable endString.
        for merchantname in sortedmerchantDict: 
            for receiptdata in sortedmerchantDict[merchantname]: 
                if merchantname == 'COQ SEAFOOD': # if condition to check which merchantname the for loop has iterated to.
                    linestart = 10 # preset parameter analysed from csv file.
                    count = 0
                    while count == 0:
                        if receiptdata[linestart] != endString: # condition set to pattern analysed from csv file where data which needs to be extracted is between linestart and endString.
                            extractline = receiptdata[linestart]
                            extractline = extractline[3:32].strip() # strip line of data so that only the item name is left.
                            itemlist1.append(extractline)
                        else:
                            count = 1 # exit loop.
 
                        linestart += 1
                else: # merchantname == "Chin Wan Logic PTE LTD".
                    linestart = 8 # preset parameter analysed from csv file.
                    count = 0
                    while count == 0:
                        if receiptdata[linestart] != endString: # condition set to pattern analysed from csv file where data which needs to be extracted is between linestart and endString.
                            extractline2 = receiptdata[linestart]
                            extractline2 = extractline2[3:32].strip() # strip line of data so that only the item name is left.
                            itemlist2.append(extractline2)
                        else:
                            count = 1 # exit loop.
 
                        linestart += 1

        setlist2 = set(itemlist2) # Convert itemlist2 into a set to remove multiple repeated values.
        newlist2 = list(setlist2) # Convert setlist2 back into a list to get a list with unique values.
        Merchantname1 = sortedmerchantDict.keys()[0] # Assign merchant names to variables.
        Merchantname2 = sortedmerchantDict.keys()[1]
        dict[Merchantname1] = [n for n in newlist2] # Create dictionary where each value in list is assigned to merchant name as key.
        dict[Merchantname2] = [n for n in itemlist1]
        solditem1 = " and ".join([",".join(str(n) for n in dict[Merchantname1][0:-1]), dict[Merchantname1][-1]]) # convert each value in dict[Merchantname1] from range 0 to -1 to string and join them with ",". The last value in dict[Merchantname1] is then joined to the previous string with "and".
        solditem2 = " and ".join([",".join(str(n) for n in dict[Merchantname2][0:-1]), dict[Merchantname2][-1]]) # convert each value in dict[Merchantname2] from range 0 to -1 to string and join them with ",". The last value in dict[Merchantname2] is then joined to the previous string with "and".
        print "The items sold in %s are %s.\n" %(Merchantname1, solditem1)
        print "The items sold in %s are %s." %(Merchantname2, solditem2)
         
        self.updateDisplaybox(True, "The items sold in %s are :" %(Merchantname1))
        self.updateDisplaybox(False, "%s.\n" %(solditem1))
        self.updateDisplaybox(False, "")
        self.updateDisplaybox(False, "The items sold in %s are :" %(Merchantname2))
        self.updateDisplaybox(False, "%s." %(solditem2))
 
 
 
    def exportCSV(self): #-------------- | FUNCTION 6 | --------------#
        '''Dylan & Jun Loong
        '''
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR: Receiptvalue is empty - Have you loaded CSV data?')
            return False
 
        #Begin creating/rewriting file named 'csvOutput.csv'
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
 
    def findAssociations(self, merchant,itemLine,endString,dataDict): #-------------- | FUNCTION 7 | --------------# DONE BY DANIEL
        ''' Daniel
        This function is basically a customised receipt reader. It was developed to cope with the different receipt formats in our
        sample data its arguments accept the item line number and end string for a given receipt. For example, in COQ SEAFOOD's
        format, the items start at line 11 and the end string is ----------------------------------. It uses string operations
        in a loop to slice only the item name. The items are stored in 2 separate dictionaries, one for single items and one
        more for each paired item-set. This function returns both dictionaries.
        
        '''
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
        '''
        Using the correlation found in Function 7, we parse our values through four pre-defined scenarios to
        estimate based on certain assumptions what an appropriate promotion would be for the merchant.
        - Lucas & Daniel
        '''
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
            print "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease1*100,'%', breakEvenDate)
            print "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct)
            self.updateDisplaybox(False, "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease1*100,'%', breakEvenDate))
            self.updateDisplaybox(False, "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct))
             
        elif  0.2 <= (correlation/anchorProductCount) < 0.5:
            promoBudget = subCount*corIncrease2*breakEvenDate
            promoAmount = promoBudget/promoDuration/subCount*100
            print "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease2*100,'%', breakEvenDate)
            print "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct)
            self.updateDisplaybox(False, "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease2*100,'%', breakEvenDate))  
            self.updateDisplaybox(False, "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct))
       
        elif  0 <= (correlation/anchorProductCount) < 0.2:
            promoBudget = subCount*corIncrease3*breakEvenDate
            promoAmount = promoBudget/promoDuration/subCount*100
            print "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease3*100,'%', breakEvenDate)
            print  "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct)
            self.updateDisplaybox(False, "Assuming 30%s of customers who buy %s also decide to buy %s during the promotion period, an estimated increase of %0.1f%s is expected in the correlation, profits will be made after %s days" %('%',anchorProduct, relatedProduct, corIncrease3*100,'%', breakEvenDate))
            self.updateDisplaybox(False, "Recommended promotion is: Buy one %s at %0.2f%s off with any purchase of %s!" %(relatedProduct,promoAmount,'%',anchorProduct))

 
    def logSheet(self): #-------------- | FUNCTION 8 | --------------# DONE BY LUCAS
        '''
        Furthering the use of our data, a logsheet would allow the merchants to see which cashier/waiter was working at what time.
        This would have anti-fraud and dispute handling applications as it would be clear if a cashier/waiter was making transactions when it was not their shift etc. 
        - Lucas
        '''
        if not receiptvalue:
            print "receiptvalue is empty"
            self.updateDisplaybox(True, 'ERROR: Receiptvalue is empty - Have you loaded CSV data?')
            return False
 
        #displayBox.delete(0.0, END)
        self.updateDisplaybox(True, '')
        for merchant in sortedmerchantDict:
            if merchant == "COQ SEAFOOD":
                print ""
                print "COQ SEAFOOD"
                print "DATE       TIME  WAITER CASHIER"
                self.updateDisplaybox(False, "COQ SEAFOOD")
                self.updateDisplaybox(False, "DATE       TIME  WAITER CASHIER")
                 
     
            elif merchant == "Chin Wan Logic PTE LTD":
                print ""
                print "Chin Wan Logic PTE LTD"
                print "DATE       TIME  WAITER CASHIER"
                self.updateDisplaybox(False, "Chin Wan Logic PTE LTD")
                self.updateDisplaybox(False, "DATE       TIME  WAITER CASHIER")
     
            for receiptsList in sortedmerchantDict[merchant]:
                logSheet = ""
                if merchant == "COQ SEAFOOD": #If it is COQ SEAFOOD, the format to obtain the relevant information would be as follows
                    lineNum = [7,8]
                    for line in lineNum:
                        timeStamp = receiptsList[line] #Grab the date
                        if line == 7:
                            logSheet += timeStamp[0:16].strip() #Grab the time
                            logSheet += " "
                        elif line == 8:
                            logSheet += timeStamp[19:24].strip() #Grab the waiter
                            logSheet += "  "                  
                    logSheet += "N/A"
                    print logSheet
                    self.updateDisplaybox(False, logSheet)
     
                elif merchant == "Chin Wan Logic PTE LTD": #If it is Chin Wan Logic, the format to obtain the relevant information would be as follows
                    lineNum = [0,4,6]
                    for line in lineNum:
                        timeStamp = receiptsList[line] #Grab the date
                        if line == 4:
                            logSheet += timeStamp[0:16].strip() #Grab the time
                            logSheet += " N/A    "
                        elif line == 6:
                            logSheet += timeStamp[9:12].strip() #Grab the cashier                   
                    print logSheet
                    self.updateDisplaybox(False, logSheet)
                     
                else:
                    print "COMPANY NOT RECOGNIZED"
                    self.updateDisplaybox(False, "COMPANY NOT RECOGNIZED")
 
    def findSelectedOperation(self):
        '''
        This Function is specifically designed for MacOS, as buttons do not scale the way we want, we have
        to design new ways instead of using buttons - Jerry
        '''
         
        if selectedOp.get() == "Export to File":
            self.exportDataToFile()
        elif selectedOp.get() == "List Total Receipt by Merchant":
            self.listTotalReceipts()
        elif selectedOp.get() == "Total Sales":
            self.totalSales()
        elif selectedOp.get() == "All Items sold":
            self.listAllSoldItems()
        elif selectedOp.get() == "Export to CSV":
            self.exportCSV()
        elif selectedOp.get() == "Log sheet":
            self.logSheet()
        else:
            print "Operation not selcted"
            self.updateDisplaybox(True, 'ERROR: Select operation in drop down menu first.')
            return False
 
 
    def findMercAssoc(self): #-------------- | FUNCTION 7&8 | --------------# DONE BY DANIEL & LUCAS
        '''
        Combining our Function 7 together with an application to interpret the correlations,
        this function allows the user to select a merchant, after which they are able to select from two dropdown lists
        which two products they would like to compare. This function also does the calculations for association concepts
        like Support and Confidence which are displayed after the user selects the 2 products to compare.
        - Daniel & Lucas
        '''
        if not sortedmerchantDict:
            print "sortedmerchantDict is empty"
            self.updateDisplaybox(True, 'ERROR: sortedmerchantDict is empty - Have you loaded CSV data?')
            return False
 
         
        if selectedMerc.get()=="Chin Wan Logic PTE LTD":
            retList = self.findAssociations("Chin Wan Logic PTE LTD",8,'----------------------------------',sortedmerchantDict)
        else:
            retList = self.findAssociations("COQ SEAFOOD",11,'----------------------------------',sortedmerchantDict)
             
        combiDict = retList[0]
        singleDict = retList[1]
 
        assocText = '============ Using Apriori Association Algorithm ============'
        assocText +='\n{0:30} {1}     Database Size:{2}'.format('ITEM-SET','SUPPORT',merchantsales[selectedMerc.get()])
 
        for item in singleDict:
            if singleDict[item]>2:
                assocText +='\n{0:30} {1}'.format(item,str(singleDict[item]))
        for item in combiDict:
            if combiDict[item]>2:
                assocText +='\n{0:30} {1}'.format(item,str(combiDict[item]))
             
        assocText +='\nItem-set size limited to 2 due to small size of dataset'
        assocText +='\nMin support is 3, item-sets with less are not shown'
        assocText +='\nPlease select a pair using the dropdown list to see recommendation'
        self.updateDisplaybox(True, assocText)
         
        def paFunction(): #PromoAdviser window
            if var1.get()==var2.get():
                self.updateDisplaybox(True, 'ERROR - You have selected the same item twice')
                return False
             
            sf = "Find associations and show recommendations"
            root.title(sf)
 
            total = merchantsales[selectedMerc.get()] #total no. of receipts for current merchant
            x = singleDict[var1.get()] #occurences of x
            xy = combiDict[(var1.get()+", "+var2.get())] #occurences of xANDy
            support = round(float(xy)/float(total)*100,1) #percent xy/total aka support
            confidence = round(float(xy)/float(x)*100,1) #percent xy/x aka Confidence
             
            assocText = '============ Selected: %s, %s ============' % (var1.get(),var2.get())
            assocText +='\nSupport (How frequently the item-set appears in the database):\n '+str(xy)+'/'+str(total)+' (~'+str(support)+'%)'
            assocText +='\nConfidence (How often the rule has been found to be true):\n '+str(xy)+'/'+str(x)+' (~'+str(confidence)+'%)\n\n'
             
            self.updateDisplaybox(True, assocText)
            print assocText
             
            self.promoAdviser(var1.get(),var2.get(),singleDict[var1.get()],combiDict[(var1.get()+", "+var2.get())])
 
        root = Tk()
        root.geometry("500x150")
        root.title("Option Window")
        root.resizable(0,0)
        var1 = StringVar(root)
        var1.set(singleDict.keys()[0])
  
        firstList = singleDict.keys() #Sets the menu options to the keys in singledict aka the items
        option1 = OptionMenu(root, var1, *firstList)
        option1.pack(side='left', padx=10, pady=10)
  
        var2 = StringVar(root)
        var2.set(singleDict.keys()[1])
        secondList = singleDict.keys() 
        option2 = OptionMenu(root, var2, *secondList)
        option2.pack(side='left', padx=10, pady=10)
  
        button = Button(root, text="GO", command=paFunction,height=3,width=15)
        button.pack(side='left', padx=10, pady=10)
        root.mainloop()
 
app = ApplicationMain()
app.master.title("Main Window") #Title is set here
_platform = sys.platform
if _platform == "linux" or _platform == "linux2":
   # linux
   app.master.geometry("600x750") # windows
elif _platform == "darwin":
   # MAC OS X
   app.master.geometry("780x600") # Mac
elif _platform == "win32":
   # Windows
   app.master.geometry("600x750") # windows
 
app.master.resizable(0,0)
app.mainloop()

