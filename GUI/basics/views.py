from django.shortcuts import render,HttpResponse,redirect
from .models import *
import math
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def index(request):
  return render(request,'index.html')


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=User.objects.filter(username=username)
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
          login(request,user)
          return redirect('COPD')
        else:
            result="Password Entered is wrong"
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

@login_required(login_url='login')
def COPD(request):
    if(request.method=="POST"):
        data=request.POST
        AGE=int(data.get("textfirstnumber"))
        PackHistory=float(data.get("texttwonumber"))
        FEV1PRED=float(data.get("textthirdnumber"))
        FVC=float(data.get("textfourthnumber"))
        FVCPRED=int(data.get("textfivenumber"))
        CAT=int(data.get("textsixnumber"))
        HAD=float(data.get("textsevennumber"))
        SGRQ=float(data.get("texteightnumber"))
        AGEquartiles=int(data.get("textninenumber"))
        copd=int(data.get("texttennumber"))
        gender=int(data.get("textelvennumber"))
        smoking=int(data.get("texttwelvenumber"))
        Diabetes=int(data.get("textthirteennumber"))
        muscular=int(data.get("textfourteennumber"))
        hypertension=int(data.get("textfifteenhnumber"))
        AtrialFib=int(data.get("textsixteennumber"))
        IHD=int(data.get("textseventeennumber"))
        if("buttonsubmitsvm" in request.POST):
            import pandas as pd
            data=pd.read_csv('C:\\Users\\kusha\\OneDrive\\Desktop\\Data\\dataset.csv')
            columns = ['Unnamed: 0','ID','MWT1','MWT2']
            data.drop(columns=columns, axis=1,inplace=True)

            inputs=data.drop(['COPDSEVERITY','MWT1Best','FEV1'],"columns")
            output=data.drop(['copd','AGE','PackHistory','MWT1Best','FEV1','FEV1PRED','FVC','FVCPRED','CAT','HAD','SGRQ','AGEquartiles','gender','smoking','Diabetes','muscular','hypertension','AtrialFib','IHD'],"columns")
            import sklearn
            from sklearn.model_selection import train_test_split
            x_train,x_test,y_train,y_test=train_test_split(inputs,output,test_size=0.2)

            from sklearn.preprocessing import StandardScaler
            sc=StandardScaler()
            x_train=sc.fit_transform(x_train)
            x_test=sc.transform(x_test)

            from sklearn.svm import SVC
            model=SVC()
            model.fit(x_train,y_train)
            y_pred=model.predict(x_test)
            from sklearn.metrics import confusion_matrix
            cm =confusion_matrix(y_test,y_pred)
            acc=(cm[0][0]+cm[1][1]+cm[2][2])/(cm[0][0]+cm[0][1]+cm[0][2]+cm[1][0]+cm[1][1]+cm[1][2]+cm[2][0]+cm[2][1]+cm[2][2])
            print(acc)
            result=model.predict([[AGE,PackHistory,FEV1PRED,FVC,FVCPRED,CAT,HAD,SGRQ,AGEquartiles,copd,gender,smoking,Diabetes,muscular,hypertension,AtrialFib,IHD]])
            return render(request,"COPD.html",context={"result":"Result of SVM="+str(result),"acc":"Accuracy of SVM="+str(math.ceil(acc*100))})

        if("buttonsubmitknn" in request.POST):
            import pandas as pd
            data=pd.read_csv('C:\\Users\\kusha\\OneDrive\\Desktop\\Data\\dataset.csv')
            columns = ['Unnamed: 0','ID','MWT1','MWT2']
            data.drop(columns=columns, axis=1,inplace=True)

            inputs=data.drop(['COPDSEVERITY','MWT1Best','FEV1'],"columns")
            output=data.drop(['copd','AGE','PackHistory','MWT1Best','FEV1','FEV1PRED','FVC','FVCPRED','CAT','HAD','SGRQ','AGEquartiles','gender','smoking','Diabetes','muscular','hypertension','AtrialFib','IHD'],"columns")
            import sklearn
            from sklearn.model_selection import train_test_split
            x_train,x_test,y_train,y_test=train_test_split(inputs,output,test_size=0.2)

            from sklearn.neighbors import KNeighborsClassifier
            model = KNeighborsClassifier(n_neighbors=11)
            model.fit(x_train,y_train) 
            y_pred = model.predict(x_test)
            from sklearn.metrics import confusion_matrix
            cm =confusion_matrix(y_test,y_pred)
            acc=(cm[0][0]+cm[1][1]+cm[2][2])/(cm[0][0]+cm[0][1]+cm[0][2]+cm[1][0]+cm[1][1]+cm[1][2]+cm[2][0]+cm[2][1]+cm[2][2])
            print(acc)
            result=model.predict([[AGE,PackHistory,FEV1PRED,FVC,FVCPRED,CAT,HAD,SGRQ,AGEquartiles,copd,gender,smoking,Diabetes,muscular,hypertension,AtrialFib,IHD]])
            return render(request,"COPD.html",context={"result":"Result of KNN="+str(result),"acc":"Accuracy of KNN="+str(math.ceil(acc*100))})
            #return render(request,"COPD.html",context={"acc":"Accuracy="+str(acc)})
    return render(request,"COPD.html")


def LogoutPage(request):
    logout(request)
    return redirect('login')
