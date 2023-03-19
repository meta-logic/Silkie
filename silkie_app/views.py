from django.shortcuts import render
import subprocess
import os
import sys
import random
import string

from django.http import HttpResponse, Http404
import json

from django.views.decorators.csrf import ensure_csrf_cookie

# If you get here after uploading an sml file
# then it loads the corresponding .v file 
# into JSCoq

@ensure_csrf_cookie
def startPage(request):
    
    # No file has been uploaded
    if request.method == "GET":
        return render(request, 'index3-og.html')

    # Verify the existence of the uploaded file
    # and check that is an SML file
    if 'smlcode' in request.FILES:
        smlfile = request.FILES['smlcode']
        filename = str(request.FILES['smlcode'])
        if filename.endswith(".sml"):
            letters = list(set(string.ascii_letters + string.digits) - set(['.']))
            fname = ''.join(random.choice(letters) for i in range(10))
            ## Use sessionID to name temp file

            path2tmp = "/afs/qatar.cmu.edu/course/15/logic/silkie/tmp_files/" + fname + ".sml"
            path2v = "/afs/qatar.cmu.edu/course/15/logic/silkie/tmp_files/" + fname + ".v"
            print(f"saving to {path2tmp}", file=sys.stderr)
            # Save the file temporarily in local storage
            with smlfile.open() as smlf:
                tmp = open(path2tmp,"wb")
                tmp.writelines(smlf.readlines())
                tmp.close()

            # Load the SML-to-Coq heap image to convert the SML file to a Coq file
            print(subprocess.run("cd /afs/qatar.cmu.edu/course/15/logic/silkie/silkie_app/static/sml-to-coq && sml @SMLload sml2coq.amd64-linux " + path2tmp + " " +  path2v, shell=True),file=sys.stderr)

            # Remove temp SML file
            with open(path2v) as vfile:
                txt = vfile.readlines()
            
            print(txt, file=sys.stderr)
            idx = txt.index('Generalizable All Variables.\n')

            code = txt[idx+2:]
            indices = [i for i in range(len(code)) if 'Equations' in code[i] or 'Fixpoint' in code[i] or 'Inductive' in code[i]]
            print(f"\n indices are {indices}", file=sys.stderr)

            EQS = []
            IND = []
            FIX = []

            num_idx = len(indices)
            for k in range(num_idx):
                if k < num_idx - 1:
                    end = indices[k + 1]
                else:
                    end = len(code)
                
                if 'Equations' in code[indices[k]]:
                    EQS += code[indices[k] : end]
                
                elif 'Fixpoint' in code[indices[k]]:
                    FIX += code[indices[k] : end]
                
                else:
                    IND += code[indices[k] : end]
            

            ## Trimming extra whitespace

            if EQS != [] and EQS[len(EQS) - 1] == '\n':
                EQS = EQS[:len(EQS) - 1]
            
            if FIX != [] and FIX[len(FIX) - 1] == '\n':
                FIX = FIX[:len(FIX) - 1]
            
            if IND != [] and IND[len(IND) - 1] == '\n':
                IND = IND[:len(IND) - 1]
            
            print(f"\n\n {EQS} \n {FIX} \n {IND}\n", file=sys.stderr)
            return render(request, 'index3.html', {'txt1': txt[:idx+2], 'txt2' : IND, 'txt3' : FIX, 'txt4' : EQS})
    return render(request, 'index3.html')

def uploadPage(request):
    
    return render(request, 'index.html')

def usagePage(request):
    
    return render(request, 'index3-og.html')
   
@ensure_csrf_cookie
def secondPage(request):
    return render(request, 'test_page1.html')

@ensure_csrf_cookie
def q1(request):
    context = {}

    if "answer1" in request.session:
        context = {"reply" : request.session["answer1"]}

    return render(request, 'test_page2.html', context)

@ensure_csrf_cookie
def q2(request):
    context = {}

    if "answer2" in request.session:
        context = {"reply" : request.session["answer2"]}
    
    return render(request, 'test_page3.html')

@ensure_csrf_cookie
def q3(request):
    context = {}

    if "answer3" in request.session:
        context = {"reply" : request.session["answer3"]}
    
    return render(request, 'test_page4.html')

@ensure_csrf_cookie
def q4(request):
    context = {}

    if "answer4" in request.session:
        context = {"reply" : request.session["answer4"]}
    
    return render(request, 'test_page5.html')

@ensure_csrf_cookie
def submit(request):

    # Save answers here
    return render(request, 'test_page6.html')

@ensure_csrf_cookie
def checkPerm(request):
    with open("/afs/qatar.cmu.edu/course/15/logic/silkie/test_perm/test.txt","r") as t:
        print (t.readlines(), file=sys.stderr)

    return render(request, 'test_page1.html')

def processAnswer(s):
    ans = s.replace("∀","forall")
    ans = ans.replace("ℙ", "Prop")
    ans = ans.replace("ℕ", "nat")
    ans = ans.replace("∃", "exists")
    ans = ans.replace("→", "->")
    ans = ans.replace("⇒", "=>")
    ans = ans.replace("←", "<-")
    ans = ans.replace("↔", "<->")
    ans = ans.replace("↣", ">->")
    ans = ans.replace("⊢", "|-")
    ans = ans.replace("∧", "/\\")
    ans = ans.replace("∨", "\\/")
    ans = ans.replace("≤", "<=")
    ans = ans.replace("≥", ">=")
    ans = ans.replace("≠", "<>")
    ans = ans.replace("λ", "fun")
    ans = ans.replace("ℝ", "Real")
    return ans

def loadanswer(request):
    if "answer1" in request.POST:
        request.session["answer1"] = processAnswer(request.POST["answer1"])

    if "answer2" in request.POST:
        request.session["answer2"] = processAnswer(request.POST["answer2"])

    if "answer3" in request.POST:
        request.session["answer3"] = processAnswer(request.POST["answer3"])

    if "answer4" in request.POST:
        request.session["answer4"] = processAnswer(request.POST["answer4"])

    return HttpResponse(json.dumps({'dm' : "dummy_text"}),content_type='application/json')



