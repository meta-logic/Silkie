from django.shortcuts import render
import subprocess
import os

# Loads Main landing page of JSCoq
# If you get here after uploading an sml file
# then it loads the corresponding .v file 
# into JSCoq
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
            print("SML FILE Uploaded")
            
            # Save the file temporarily in local storage
            with smlfile.open() as smlf:
                tmp = open("/silkie/static/sml-to-coq/tmpsml.sml","wb")  ## obvious concurrency bug / fix later
                tmp.writelines(smlf.readlines())
                tmp.close()

            # Load the SML-to-Coq heap image to convert the SML file to a Coq file
            print(subprocess.run('cd /silkie/static/sml-to-coq && sml @SMLload sml2coq.amd64-darwin tmpsml.sml ../vfiles/tmp2.v', shell=True))
            
            # Remove temp SML file
            if os.path.isfile('/silkie/static/sml-to-coq/tmpsml.sml'):
                os.remove('/silkie/static/sml-to-coq/tmpsml.sml')

            with open('/silkie/static/vfiles/tmp2.v') as vfile:
                txt = vfile.readlines()
            
            print(txt)
            idx = txt.index('Generalizable All Variables.\n')

            code = txt[idx+2:]
            indices = [i for i in range(len(code)) if 'Equations' in code[i] or 'Fixpoint' in code[i] or 'Inductive' in code[i]]
            print(f"\n indices are {indices}")

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
            
            print(f"\n\n {EQS} \n {FIX} \n {IND}\n")
            return render(request, 'index3.html', {'txt1': txt[:idx+2], 'txt2' : IND, 'txt3' : FIX, 'txt4' : EQS})
    return render(request, 'index3.html')

def uploadPage(request):
    #print(subprocess.run('cd jscoq_test/static/sml-to-coq && sml @SMLload test-img.amd64-darwin induction.sml ../vfiles/pytest.v', capture_output=True, shell=True))
    return render(request, 'index.html')

def usagePage(request):
    #print(subprocess.run('cd jscoq_test/static/sml-to-coq && sml @SMLload test-img.amd64-darwin induction.sml ../vfiles/pytest.v', capture_output=True, shell=True))
    return render(request, 'index3-og.html')
    
def secondPage(request):
    return render(request, 'test_page1.html')

def q1(request):
    return render(request, 'test_page2.html')

def q2(request):
    return render(request, 'test_page3.html')

def q3(request):
    return render(request, 'test_page4.html')

def q4(request):
    return render(request, 'test_page5.html')

def submit(request):
    return render(request, 'test_page6.html')
