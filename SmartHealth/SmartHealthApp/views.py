from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import os
import json
from web3 import Web3, HTTPProvider

global userid, hospital, pnameValue, pdateValue

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'SmartHealth.json' #Smart Health contract code
    deployed_contract_address =0x1193f2E9bc2293D05e6DBBD13d4F1bD21b09adBd #'0xF275EcAEa7f2c61509eD29e67E0277FFC2F4cBea' #hash address to access Smart Health contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'hospital':
        details = contract.functions.getHospital().call() #call getHospital function to access all hospital details
    if contract_type == 'patient':
        details = contract.functions.getPatient().call()
    if contract_type == 'prescription':
        details = contract.functions.getPrescription().call()
    if contract_type == 'disease':
        details = contract.functions.getDisease().call()      
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'SmartHealth.json' #Smart Health contract file
    deployed_contract_address = 0x1193f2E9bc2293D05e6DBBD13d4F1bD21b09adBd#'0xF275EcAEa7f2c61509eD29e67E0277FFC2F4cBea' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'hospital':
        details+=currentData
        msg = contract.functions.setHospital(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'patient':
        details+=currentData
        msg = contract.functions.setPatient(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'prescription':
        details+=currentData
        msg = contract.functions.setPrescription(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'disease':
        details+=currentData
        msg = contract.functions.setDisease(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)    

def getPrescription(pname, pdate):
    global details
    readDetails("prescription")
    rows = details.split("\n")
    output = "Pending"
    doctor = "Pending"
    for i in range(len(rows)-1):
        arr = rows[i].split("#")
        if arr[0] == "prescription":
            if arr[1] == pname and arr[2] == pdate:
                output = arr[3]
                doctor = arr[4]
    return output, doctor

def Prescription(request):
    if request.method == 'GET':
        global pnameValue, pdateValue
        pnameValue = request.GET['pname']
        pdateValue = request.GET['pdate']
        print(pnameValue+" "+pdateValue)
        context= {'data':"Patient Name: "+pnameValue}
        return render(request, 'Prescription.html', context)
        
def PrescriptionAction(request):
    global pnameValue, pdateValue, userid
    prescription = request.POST.get('t1', False)
    today = date.today()
    data = "prescription#"+pnameValue+"#"+pdateValue+"#"+prescription+"#"+userid+"#"+str(today)+"\n"
    saveDataBlockChain(data,"prescription")
    context= {'data':'Prescription details added'}
    return render(request, 'DoctorScreen.html', context)
    
def ViewPatientReport(request):
    if request.method == 'GET':
        global hospital
        readDetails("patient")
        rows = details.split("\n")
        output = ""
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "patient":
                temp = arr[4].split(",")
                flag = 0
                for k in range(len(temp)):
                    if temp[k] == hospital:
                        flag = 1
                        break
                if flag == 1:
                    prescription, doctor = getPrescription(arr[1],arr[6])
                    output+='<tr><td><font size="" color="black">'+str(arr[1])+'</td>'
                    output+='<td><font size="" color="black">'+str(arr[2])+'</td>'
                    output+='<td><font size="" color="black">'+str(arr[3])+'</td>'
                    output+='<td><font size="" color="black">'+str(arr[4])+'</td>'
                    output+='<td><font size="" color="black">'+str(arr[5])+'</td>'
                    output+='<td><font size="" color="black">'+str(arr[6])+'</td>'
                    output+='<td><img src="/static/reports/'+arr[5]+'" width="200" height="200"></img></td>'
                    output+='<td><font size="" color="black">'+prescription+'</td>'
                    output+='<td><font size="" color="black">'+doctor+'</td>'
                    if prescription == "Pending":
                        output+='<td><a href=\'Prescription?pname='+arr[1]+'&pdate='+arr[6]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
                    else:
                        output+='<td><font size="" color="black">Prescription Already Generated</td></tr>'
        context= {'data':output}
        return render(request, 'ViewPatientReport.html', context)          

def ViewHealth(request):
    if request.method == 'GET':
        global userid
        readDetails("patient")
        rows = details.split("\n")
        output = ""
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "patient" and arr[1] == userid:
                prescription, doctor = getPrescription(arr[1],arr[6])
                output+='<tr><td><font size="" color="black">'+str(arr[1])+'</td>'
                output+='<td><font size="" color="black">'+str(arr[2])+'</td>'
                output+='<td><font size="" color="black">'+str(arr[3])+'</td>'
                output+='<td><font size="" color="black">'+str(arr[4])+'</td>'
                output+='<td><font size="" color="black">'+str(arr[5])+'</td>'
                output+='<td><font size="" color="black">'+str(arr[6])+'</td>'
                output+='<td><img src="/static/reports/'+arr[5]+'" width="200" height="200"></img></td>'
                output+='<td><font size="" color="black">'+prescription+'</td>'
                output+='<td><font size="" color="black">'+doctor+'</td>'
        context= {'data':output}
        return render(request, 'ViewHealth.html', context)        

def ViewPatientHospital(request):
    if request.method == 'GET':
        readDetails("hospital")
        rows = details.split("\n")
        output = ""
        for i in range(len(rows)-1):
            row = rows[i].split("#")
            if row[0] == "hospital":
                output+='<tr><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="" color="black">'+str(row[4])+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td>'
                output+='<td><font size="" color="black">'+str(row[6])+'</td>'
                output+='<td><font size="" color="black">'+str(row[7])+'</td>'
                output+='<td><font size="" color="black">'+str(row[8])+'</td>'
               
                
        context= {'data':output}
        return render(request, 'ViewPatientHospital.html', context)


def AddHealthAction(request):
    if request.method == 'POST':
        global userid
        age = request.POST.get('t1', False)
        symptoms = request.POST.get('t2', False)
        myfile = request.FILES['t3']
        fname = request.FILES['t3'].name
        hospitals = request.POST.getlist('t4')
        hospitals = ','.join(hospitals)
        today = date.today()
        fs = FileSystemStorage()
        filename = fs.save('SmartHealthApp/static/reports/'+fname, myfile)
        data = "patient#"+userid+"#"+age+"#"+symptoms+"#"+hospitals+"#"+fname+"#"+str(today)+"\n"
        saveDataBlockChain(data,"patient")
        context= {'data':'Your report shared with '+hospitals}
        return render(request, 'PatientScreen.html', context)

def AddHealth(request):
    if request.method == 'GET':
        output = ""
        names = []
        readDetails("hospital")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "hospital":
                if arr[8] not in names:
                    names.append(arr[8])
                    output += '<option value="'+arr[8]+'">'+arr[8]+'</option>'
        context= {'data1':output}            
        return render(request, 'AddHealth.html', context)

def ViewHospitalDetails(request):
    if request.method == 'GET':
        readDetails("hospital")
        rows = details.split("\n")
        output = ""
        for i in range(len(rows)-1):
            row = rows[i].split("#")
            if row[0] == "hospital":
                output+='<tr><td><font size="" color="black">'+str(row[1])+'</td>'
                output+='<td><font size="" color="black">'+str(row[2])+'</td>'
                output+='<td><font size="" color="black">'+str(row[3])+'</td>'
                output+='<td><font size="" color="black">'+str(row[4])+'</td>'
                output+='<td><font size="" color="black">'+str(row[5])+'</td>'
                output+='<td><font size="" color="black">'+str(row[6])+'</td>'
                output+='<td><font size="" color="black">'+str(row[7])+'</td>'
                output+='<td><font size="" color="black">'+str(row[8])+'</td>'
                                
        context= {'data':output}
        return render(request, 'ViewHospitalDetails.html', context)

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def AddDisease(request):
    if request.method == 'GET':
       return render(request, 'AddDisease.html', {})    

def PatientLogin(request):
    if request.method == 'GET':
       return render(request, 'PatientLogin.html', {})    

def DoctorLogin(request):
    if request.method == 'GET':
       return render(request, 'DoctorLogin.html', {})

def PatientSignup(request):
    if request.method == 'GET':
       return render(request, 'PatientSignup.html', {})    

def AddDoctor(request):
    if request.method == 'GET':
       return render(request, 'AddDoctor.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})
    
def SearchDoctor(request):
    if request.method == 'GET':
       return render(request, 'SearchDoctor.html', {})       

def AdminLoginAction(request):
    if request.method == 'POST':
        global userid
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if user == "admin" and password == "admin":
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid Login'}
            return render(request, 'AdminLogin.html', context)

def PatientSignupAction(request):
    if request.method == 'POST':
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        email = request.POST.get('t3', False)
        contact = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        record = 'none'
        readDetails("patient")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == user:
                    record = "exists"
                    break
        if record == 'none':
            data = "signup#"+user+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"patient")
            context= {'data':'Signup process completd and record saved in Blockchain'}
            return render(request, 'PatientSignup.html', context)
        else:
            context= {'data':user+'Username already exists'}
            return render(request, 'PatientSignup.html', context)

def AddDiseaseAction(request):
    if request.method == 'POST':
        disease = request.POST.get('t1', False)
        symptoms = request.POST.get('t2', False)
        medicines = request.POST.get('t3', False)
        doctor = request.POST.get('t4', False)
        data = disease+"#"+symptoms+"#"+medicines+"#"+doctor+"\n"
        saveDataBlockChain(data,"disease")
        context= {'data':'Disease & Symptoms details added to Blockchain'}
        return render(request, 'AddDisease.html', context)

def SearchDoctorAction(request):
    if request.method == 'POST':
        symptom = request.POST.get('t1', False)
        symptom = symptom.strip().lower()
        readDetails("disease")
        rows = details.split("\n")
        output = ""
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            data = arr[0]+" "+arr[1]
            data = data.strip().lower()
            if symptom in data:
                output+='<tr><td><font size="" color="black">'+str(arr[0])+'</td>'
                output+='<td><font size="" color="black">'+str(arr[1])+'</td>'
                output+='<td><font size="" color="black">'+str(arr[2])+'</td>'
                output+='<td><font size="" color="black">'+str(arr[3])+'</td>'
        if len(output) == 0:
            output = '<tr><td><font size="" color="black">No details found for given symptoms. You can go for Blood Test</td>'
        context= {'data':output}
        return render(request, 'SymptomReport.html', context)       
        
        
def PatientLoginAction(request):
    if request.method == 'POST':
        global userid
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        readDetails("patient")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "signup":
                if arr[1] == user and arr[2] == password:
                    status = 'success'
                    userid = user
                    break
        if status == 'success':
            file = open('session.txt','w')
            file.write(user)
            file.close()
            context= {'data':"Welcome "+user}
            return render(request, 'PatientScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'PatientLogin.html', context) 


def AddDoctorAction(request):
    if request.method == 'POST':
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        email = request.POST.get('t3', False)
        contact = request.POST.get('t4', False)
        qualification = request.POST.get('t5', False)
        experience = request.POST.get('t6', False)
        hospital = request.POST.get('t7', False)
        address = request.POST.get('t8', False)
        record = 'none'
        readDetails("hospital")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "hospital":
                if arr[1] == user:
                    record = "exists"
                    break
        if record == 'none':
            data = "hospital#"+user+"#"+password+"#"+contact+"#"+email+"#"+address+"#"+qualification+"#"+experience+"#"+hospital+"\n"
            saveDataBlockChain(data,"hospital")
            context= {'data':'New Doctor & Hospital details saved in Blockchain'}
            return render(request, 'AddDoctor.html', context)
        else:
            context= {'data':username+'Username already exists'}
            return render(request, 'AddDoctor.html', context)


def DoctorLoginAction(request):
    if request.method == 'POST':
        global userid, hospital
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        status = 'none'
        readDetails("hospital")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == "hospital":
                if arr[1] == user and arr[2] == password:
                    status = 'success'
                    userid = user
                    hospital = arr[8]
                    break
        if status == 'success':
            file = open('session.txt','w')
            file.write(user)
            file.close()
            context= {'data':"Welcome "+user}
            return render(request, 'DoctorScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'DoctorLogin.html', context) 










        
    
