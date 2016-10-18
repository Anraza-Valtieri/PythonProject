# PythonProject
Assignment1

The Detail Requirements
The dataset given is in one CSV file “sample_data.csv”. The sample dataset consists the receipts from different merchants. Each merchant includes multiple receipts with various information and one unique receipt_id. The specific requirements are provides as follows.
 Program Input: one CSV file with the receipt information from different merchants. Please note that you will be provided another dataset with much more information to evaluate your program during the project final demonstration and evaluation. However, for simplicity, you can assume the receipts in the final dataset are from the same companies as in the sample dataset with the same format.
The functionalities/features that your program should support are listed below:
 Function 1 (5 Marks): As the starting UI, it should allow users to choose the dataset that they want to process. One way to do this is to allow users input the path of the CSV file.
 Function 2 (5 Marks): Read the CSV file and export each receipt information into one text file in the disk. For instance, if there are 10-receipt information, the output of this function will be ten “.txt” files under one folder.
 Function 3 (5 Marks): List the total number of receipts of each merchant in the file.
 Function 4 (10 Marks): List the total sales amount for each merchant.
 Function 5 (10 Marks): List all the items sold in each merchant.
 Function 6 (30 Marks): Extract the most important data information from each receipt and store
them into another CSV file. The information that you have to extract includes Receipt ID, merchant name, merchant address, shopping date, shopping time, shopping items (separated by “,”), the number of items (separated by “,”), cost of per item (separated by “,”), total cost.
 Function 7 (20 Marks): Discover all the associated items or user shopping patterns. You may need to use existing association algorithms or propose your own algorithm to detect the correlated items which the customers always purchase together. All of correlated items or shopping patterns can be utilized to help the business perform promotions or recommendations to different customers.
 Function 8 (15 Marks): This is an open question where you can propose your own idea about how you can analyze the dataset to better make sense of the data. In order to improve the merchant’s business, you may propose and implement one your self-defined function to better analyze and utilize the data you have.

You need to design one user-friendly UI such that your program is easy to use. As one example, the program should be able to allow users to choose which function to perform and display the result nicely. You can build any innovative UI. Note that it is not compulsory to build a GUI. However, building one GUI will be considered as one advanced features of your program.
Please keep in mind that, in a big data world, the datasets you are handling can be large. Hence, you may want to optimize your code to be memory/algorithm efficient and effective.