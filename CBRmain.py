# -*- coding: utf-8 -*-
"""
Template
"""
import csv as csv
import urllib
import json
#==============================================================================
# this is the main function
#==============================================================================
def main():  
    
    # step 1
    print "LOAD CASE BASE"  
    # using csv
    # into array of classes
    filepath = 'C:\\Users\\Liam\\Dropbox\\Documents\\University\\Modules\\Year 3\\Intelligent Systems\\Term 2\\Assignment\\CASEBASE.txt'
    casebase = readCSVintoList(filepath)
    
    #priceArray is created
    #This array will store the previous case prices in order
    #With the recommended price then retrieved
    priceArray = []
      
    
    for case in casebase:
        print case[0]
        print case        
        tv1 = TV(case[1], case[2], case[3], case[4]) 
        #All prices are added to the array
        priceArray.append(case[4])
    
    
    # step 2
    print " "
    print "GET USER INPUT" 
    tv_name =                       raw_input("Enter the TV brand and model: ")
    tv_year_release =               input("Enter the TV's year release: ")
    tv_resolution =                 input("Enter the TV's resolution: ")
    tv_size =                       input("Enter the TV's size: ")
    tv_price =                      0
    unknowncase = TV(tv_name, tv_year_release, tv_resolution, tv_size, tv_price)
    
    # step 3
    print "CALCULATE SIMILARITY"
    
    #Each similarity value is stored to the array
    similarityArray = []
    
    for case in casebase:
        tv1 =  TV(case[1], case[2], case[3], case[4]) 
        tv1.get_tv_size(), tv1.get_tv_resolution(), tv1.get_tv_year_release(), tv1.get_tv_price()
        
        
        similarity = unknowncase.similarity(tv1)
        similarityArray.append(similarity)
        
    #Get similarity value closest to 0.0
    simValue = similarityArray.index(min(similarityArray, key=lambda x:abs(x-0.0)))
        
    #Get's recommended price by usinG the same index as element closest to 0.0 
    from operator import itemgetter 
    searchArray = [simValue]
    price = itemgetter(*searchArray)(priceArray)
    print " "
    print "Your recommended price for your TV is:"
    print "£", price
    
    #Getting the new entered case's number to save reviews
    review = simValue + 1  
    
    #Each review's sentimental analysis label is saved to an array
    reviewAnalysis = []
    
    #sentimentAnalysis
    casereviewpath = 'C:\\Users\\Liam\\Dropbox\\Documents\University\\Modules\\Year 3\\Intelligent Systems\\Term 2\\Assignment\\CASE' + str(review) + '-REVIEW1.txt'
    reviewfile = open(casereviewpath, 'r')
    mainreview = {"text": reviewfile.read()}
    reviewAnalysis.append(doSentimentAnalysisAndPrint(mainreview))
    
    casereviewpath = 'C:\\Users\\Liam\\Dropbox\\Documents\University\\Modules\\Year 3\\Intelligent Systems\\Term 2\\Assignment\\CASE' + str(review) + '-REVIEW2.txt'
    reviewfile = open(casereviewpath, 'r')
    mainreview = {"text": reviewfile.read()}
    reviewAnalysis.append(doSentimentAnalysisAndPrint(mainreview))
    
    casereviewpath = 'C:\\Users\\Liam\\Dropbox\\Documents\University\\Modules\\Year 3\\Intelligent Systems\\Term 2\\Assignment\\CASE' + str(review) + '-REVIEW3.txt'
    reviewfile = open(casereviewpath, 'r')
    mainreview = {"text": reviewfile.read()}
    reviewAnalysis.append(doSentimentAnalysisAndPrint(mainreview))
    
    positive = reviewAnalysis.count('pos')
    negative = reviewAnalysis.count('neg')
    
    print "Amount of positive reviews of compared item: " , positive
    print "Amount of negative reviews of compared item: " , negative
    
    #New case is saved to CASEBASE.txt    
    with open("CASEBASE.txt", "a") as myfile:
       myfile.write("\n" + str(unknowncase.get_tv_name()) + "," + str(unknowncase.get_tv_year_release()) + "," + str(unknowncase.get_tv_resolution()) + "," + str(unknowncase.get_tv_size()) + "," + str(price))
    
    #User will have to input three reviews to save
    print "Please enter the three reviews of your product:-"
    
    REVIEW1 =   raw_input("Review 1: ")
    REVIEW2 =   raw_input("Review 2: ")
    REVIEW3 =   raw_input("Review 3: ")
    
    #newCaseNo is the variable for new case's number, in order to save the new reviews    
    newCaseNo = len(priceArray) + 1
       
    with open("C:\\Users\\Liam\\Dropbox\\Documents\University\\Modules\\Year 3\\Intelligent Systems\\Term 2\\Assignment\\CASE" + str(newCaseNo) + "-REVIEW1.txt", "a") as myfile:
        myfile.write(str(REVIEW1))
    
    with open("C:\\Users\\Liam\\Dropbox\\Documents\University\\Modules\\Year 3\\Intelligent Systems\\Term 2\\Assignment\\CASE" + str(newCaseNo) + "-REVIEW2.txt", "a") as myfile:
        myfile.write(str(REVIEW2))
        
    with open("C:\\Users\\Liam\\Dropbox\\Documents\University\\Modules\\Year 3\\Intelligent Systems\\Term 2\\Assignment\\CASE" + str(newCaseNo) + "-REVIEW3.txt", "a") as myfile:
        myfile.write(str(REVIEW3))
    
    
    print "Thank you for using CBR today."
#==============================================================================
# someFunction - just returns the same string forever
#==============================================================================
def readCSVintoList(filepath):

    with open(filepath, 'rb') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    
    return your_list
    # [['This is the first line', 'Line1'],
    #  ['This is the second line', 'Line2'],
    #  ['This is the third line', 'Line3']]
    
    # If you need tuples:

    # with open('test.csv', 'rb') as f:
    #    reader = csv.reader(f)
    #   your_list = map(tuple, reader)
    
    # print your_list
    # [('This is the first line', ' Line1'),
    #  ('This is the second line', ' Line2'),
    #  ('This is the third line', ' Line3')]
    
    
    
    return "Finished list."

#==============================================================================

#==============================================================================

def doSentimentAnalysisAndPrint(mainreview):  
           
    data = urllib.urlencode(mainreview) 
    u = urllib.urlopen("http://text-processing.com/api/sentiment/", data)
    json_string = u.read()   
    
    # results come back as this json format
    # {"probability": {"neg": 0.46267699890675162, "neutral": 0.42842239473738813, "pos": 0.53732300109324838}, "label": "pos"}            
    parsed_json = json.loads(json_string)
    label = parsed_json['label']
    
    return label
#==============================================================================

#==============================================================================
class TV(object):
       
    def __init__(self, tv_name="",tv_year_release=0, tv_resolution=0, tv_size=0, tv_price=0):
        self.tv_name = tv_name                    # e.g. Serial Shot Mode
        self.tv_year_release = tv_year_release                            # e.g. 5x, or 8x
        self.tv_resolution = tv_resolution              # e.g. 1/2.3
        self.tv_size = tv_size  # e.g. 16.1MP, or 20.1MP 
        self.tv_price = tv_price
 
 
    def get_tv_name(self):
        return self.tv_name
        
    def get_tv_year_release(self):
        return self.tv_year_release

    def get_tv_resolution(self):
        return self.tv_resolution

    def get_tv_size(self):
        return self.tv_size 
        
    def get_tv_price(self):
        return self.tv_price


    def similarity(self, TV):
        sim = (float(self.tv_year_release) - float(TV.tv_year_release))/2016   #Current year
        sim = sim + (float(self.tv_resolution) - float(TV.tv_resolution))/4000 #Highest TV resolution
        sim = sim + (float(self.tv_size) - float(TV.tv_size))/60               #Largest TV size
        return sim/3
        
#==============================================================================
# main switch - just get used to writing it
#==============================================================================
if __name__ == '__main__':
    main()