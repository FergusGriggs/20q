import random, pygame, sys
from pygame.locals import *
while 1:
    inp=str(input("console version or pygame version? (0 or 1)"))
    if inp=="0":mode="text";break
    if inp=="1":mode="pygame";break
screenW=300
screenH=400
if mode =="pygame":
    screen=pygame.display.set_mode((screenW,screenH))
    pygame.display.set_caption('20Q Game Window')
    pygame.init()
    sliderValue=0
    resetPos=True
    sliderPos=(150,150)
    font=pygame.font.Font(None,20)
    lFontSize=30
    lfont=pygame.font.Font(None,lFontSize)
    xlfont=pygame.font.Font(None,90)
    bqText=xlfont.render("20Q",True,(0,0,0))
    sliderValText=font.render(str(round(sliderValue,4)),True,(0,0,0))
    sliderText=font.render("",True,(0,0,0))
    submitText=font.render("submit",True,(255,255,255))
    submitRect=Rect(220,175,60,15)
    questionText=lfont.render("",True,(0,0,0))
    probableText=lfont.render("",True,(0,0,0))
    leastGuessedFont=pygame.font.Font(None,24)
    nextQuestion=False
    pressed=False
    pyguessed=False
    
    
IDS=[]
questionNum=0
answers=[]
questions=[]
guessed=False
sliderPressed=False
totalGames=0
                

def r():run()
def updateSlider():
    global sliderPos, sliderValue, sliderValText, resetPos, pressed, sliderPressed, sliderText
    if pygame.mouse.get_pressed()[0]:
        if Rect(sliderPos[0]-20,sliderPos[1]-20,40,40).collidepoint(pygame.mouse.get_pos()):
            resetPos=False
            sliderPos=(sliderPos[0]+rel[0],sliderPos[1])
            if sliderPos[0]<20:
                sliderPos=(20,sliderPos[1])
            if sliderPos[0]>280:
                sliderPos=(280,sliderPos[1])
            sliderText=font.render(updateSliderText(sliderValue),True,(0,0,0))
            sliderPressed=True
        elif Rect(20,135,260,30).collidepoint(pygame.mouse.get_pos()) or sliderPressed:
            resetPos=False
            sliderPos=(pygame.mouse.get_pos()[0],sliderPos[1])
            if pygame.mouse.get_pos()[0]<20:
                sliderPos=(20,sliderPos[1])
            elif pygame.mouse.get_pos()[0]>280:
                sliderPos=(280,sliderPos[1])
            sliderText=font.render(updateSliderText(sliderValue),True,(0,0,0))
            sliderPressed=True
        elif submitRect.collidepoint(pygame.mouse.get_pos()):
            if not pressed:
                pressed=True
                sumbitAnswer()
        sliderValue=(sliderPos[0]-150)/130
        sliderValText=font.render(str(round(sliderValue,3)),True,(0,0,0))
    elif resetPos or sliderValue>-0.05 and sliderValue<0.05:
        if abs((sliderPos[0]-150)/130)>0.005:
            sliderPos=(sliderPos[0]-(sliderPos[0]-150)/500,sliderPos[1])
            sliderValue=(sliderPos[0]-150)/130
            sliderValText=font.render(str(round(sliderValue,2)),True,(0,0,0))
            if resetPos:
                sliderText=font.render("",True,(0,0,0))
        else:
            resetPos=False
            sliderPos=(150,sliderPos[1])
    if not pygame.mouse.get_pressed()[0]:
        pressed=False
        sliderPressed=False
def sumbitAnswer():
    global resetPos, nextQuestion
    resetPos=True
    nextQuestion=True
def updateSliderText(override):
    if override>0.8:
        text="Yes"
    elif override>0.6:
        text="Mostly"
    elif override>0.3:
        text="Sometimes"
    elif override>0.05:
        text="Sort of"
    elif override>-0.05:
        text="Unknown"
    elif override>-0.3:
        text="Not really"
    elif override>-0.6:
        text="Probably Not"
    elif override>-0.8:
        text="Mostly Not"
    else:
        text="No"
    return text
def drawUI():
    pygame.draw.line(screen,(90,90,90),(20,150),(280,150),10)
    pygame.draw.circle(screen,(225*(1-((1+sliderValue)/2)),225*(abs(1+sliderValue)/2),0),(int(sliderPos[0]),int(sliderPos[1])),20,0)
    pygame.draw.circle(screen,(90,90,90),(int(sliderPos[0]),int(sliderPos[1])),20,4)
    screen.blit(sliderValText,(150-sliderValText.get_width()/2,175))
    screen.blit(sliderText,(150-sliderText.get_width()/2,115))
    pygame.draw.rect(screen,(0,235,0),submitRect,0)
    screen.blit(submitText,(submitRect.centerx-submitText.get_width()/2,submitRect.top))
    screen.blit(questionText,(150-questionText.get_width()/2,75))
    screen.blit(bqText,(150-bqText.get_width()/2,10))
    screen.blit(probableText,(150-probableText.get_width()/2,97))
class question():
    def __init__(self,string):
        self.string=string
        self.ID=getNewID()
        self.index=len(questions)  
    def ask(self):
        global items, answers
        print(self.string)
        a=getInput()
        for i in range(len(items)):
            items[i].updateCertainty(a)
        answers.append(a)
class item():
    def __init__(self,name,guessNum,questionFloats):
        self.name=name
        self.guessNum=guessNum
        self.ID=getNewID()
        self.questionFloats=questionFloats
        self.index=len(items)
        self.certainty=0
    def updateCertainty(self,val):
        self.certainty+=(1-abs(val-self.questionFloats[questionNum-1]))/len(questions)
def addItem():
    name=str(input("Name of thing: "))
    questionFloats=[]
    for i in range(len(questions)):
        print(questions[i].string)
        a=getInput()
        questionFloats.append(a)
    items.append(item(name,1,questionFloats))
    print("Thanks for adding "+name.capitalize()+"\nto the system!")
    save()
def removeQuestion():
    q=str(input("Enter question: "))
    found=False
    for i in range(len(questions)):
        if questions[i].string.upper()==q.upper():
            print("deleting",q)
            selected=i
            found=True
    if found:
        for i in range(len(items)):
            del items[i].questionFloats[selected]
        questions.remove(questions[selected])
        save()
    else:
        print("not a question")
    
def getInput():
    a=str(input())
    if a[0].upper()=="Y":
        a=1
    elif a[0].upper()=="N":
        a=-1
    elif a.upper()=="PROBABLY":
        a=0.2
    elif a.upper()=="P":
        a=0.2
    elif a.upper()=="PROBABLY NOT":
        a=-0.2
    elif a.upper()=="PN":
        a=-0.2
    else:
        a=0
    return a
def detectUncertainties(itemIndex):
    first=True
    for i in range(len(items[itemIndex].questionFloats)):
        if (1-abs(answers[i]-items[itemIndex].questionFloats[i]))<0.7:
            if first:
                first=False
                print("Contradictions Detected!\n")
            print(questions[i].string+" you answered "+updateSliderText(answers[i])+" ("+str(answers[i])+"), the answer taught by players was "+updateSliderText(items[itemIndex].questionFloats[i])+" ("+str(items[itemIndex].questionFloats[i])+")")#,(1-abs(answers[i]-items[itemIndex].questionFloats[i])))
def evaluateCertainties():
    maxi=0
    selected=-1
    for i in range(len(items)):
        if items[i].certainty>maxi:
            maxi=items[i].certainty
            selected=i
    return [selected, maxi]
def getNewID():
    global IDS
    ID=0
    while ID in IDS:
        ID = random.randint(0,10000)
    IDS.append(ID)
    return ID
def help0():
    print("\"Hey, it's like that 20 questions thing but more limited\"\n")
    print("List of commands:\n")
    print("run() - runs the main program\nlistItems() - lists all available items\nsave() - saves question and item data to files\naddQuestion() - creates a new question of your choice\nremoveQuestion() - removes the given question\naddItem() - directly adds a new item\nhelp0() - brings this up\n")
    print("If it can't get your item then it will ask for it's name\nand add it to the system. (only your client)\n")
    print("------------------------------------------------------------\n")
def clearTemps():
    global answers, questionNum, items, guessed
    questionNum=0
    answers=[]
    guessed=False
    for i in range(len(items)):
        items[i].certainty=0
def listItems():
    ilist=[]
    for i in range(len(items)):
        ilist.append(items[i].name.capitalize())
    slist=sorted(ilist)
    for i in range(len(slist)):
        print(slist[i])
def run():
    global questionNum, answers, guessed
    for i in range(len(questions)):
        questions[i].ask()
        a=evaluateCertainties()
        if 100*a[1] >65:
            if not guessed:
                guessed=True
                print("Pre guess:",items[a[0]].name,round(100*a[1],2),"%")
        questionNum+=1
    selectedData=evaluateCertainties()
    print("I guess "+items[selectedData[0]].name.capitalize()+"?"+" (Certainty of "+str(round(100*selectedData[1],2))+"%)")
    a=getInput()
    if a==1:
        print("Great, i'll add your data to the system!")
        updateFloats(selectedData[0])
    else:
        name=str(input("Tell me what it was: "))
        if name==str(items[selectedData[0]].name):
            print("(lol, that's what i said)")
        found=False
        for i in range(len(items)):
            if items[i].name==name:
                found=True
                updateFloats(i)
                print("Damn, i'll be better for next time!")
        if not found:
            print("I didn't have a \""+name.capitalize()+"\" in my records.")
            print("Would you like to add \"",name.capitalize()+"\"?")
            a=getInput()
            if a==1:   
                items.append(item(name,1,answers))
                save()
                print("done!")
            else:
                print("fine i'll leave out",name.capitalize())
    detectUncertainties(selectedData[0])
    clearTemps()
def load():
    global items
    itemData=open("itemData.txt")
    data=itemData.readlines()
    for i in range(len(data)):
        subdata=data[i].rstrip("\n").split(":")
        questionFloats=subdata[2][1:-1].split(",")
        for i in range(len(questionFloats)):
            questionFloats[i]=round(float(questionFloats[i]),4)
        items.append(item(subdata[0],int(subdata[1]),questionFloats))
    questionData=open("questionData.txt")
    data=questionData.readlines()
    for i in range(len(data)):
        questions.append(question(data[i].rstrip("\n")))
    questionData.close()
def addquestion():
    q=str(input("Enter question: "))
    print("answer your question\nfor the following items: ")
    for i in range(len(items)):
        print(items[i].name)
        a=getInput()
        items[i].questionFloats.append(a)
    questions.append(question(q))
    save()
        
def save():
    items.sort(key=lambda x: x.name)
    itemData=open("itemData.txt","w")
    for i in range(len(items)):
        itemData.write(items[i].name+":"+str(items[i].guessNum)+":"+str(items[i].questionFloats)+"\n")
    itemData.close()
    questionData=open("questionData.txt","w")
    for i in range(len(questions)):
        questionData.write(questions[i].string+"\n")
    questionData.close()
    print("\n--Data saved!--\n")
def updateFloats(INDEX):
    global items
    for i in range(len(items[INDEX].questionFloats)):
        items[INDEX].questionFloats[i]=round(((items[INDEX].questionFloats[i]*items[INDEX].guessNum)+answers[i])/(items[INDEX].guessNum+1),4)
    items[INDEX].guessNum+=1
    save()
items=[]
load()
help0()
def drawTotalGames():
    t=font.render("Games: "+str(totalGames),True,(128,0,128))
    screen.blit(t,(0,0))
def updateTotalGames():
    global totalGames
    total=0
    for i in range(len(items)):
        total+=items[i].guessNum
    totalGames=total
def updateLeastGuessed():
    global leastGuessedItems
    leastGuessedItems=sorted(items,key=lambda x: x.guessNum)[0:10]
updateLeastGuessed()
updateTotalGames()
def drawLeastGuessed():
    t=leastGuessedFont.render("Least Guessed Items",True,(128,0,128))
    screen.blit(t,(150-t.get_width()/2,220))
    for i in range(len(leastGuessedItems)):
        t=leastGuessedFont.render(str(i+1)+": "+leastGuessedItems[i].name.capitalize(),True,(0,0,0))
        screen.blit(t,(10+(i//5)*130,250+i*30-(i//5)*150))
def putOnScreen(string):
    global lFontSize, lfont, questionText
    lFontSize=30
    lfont=pygame.font.Font(None,lFontSize)
    questionText=lfont.render(string,True,(0,0,0))
    while questionText.get_width()>300:
        lFontSize-=1
        lfont=pygame.font.Font(None,lFontSize)
        questionText=lfont.render(string,True,(0,0,0))
if mode=="pygame":
    putOnScreen(questions[questionNum].string)
    while 1:
        rel=pygame.mouse.get_rel()
        updateSlider()
        if nextQuestion:
            nextQuestion=False
            if pyguessed:
                if sliderValue>0:
                    putOnScreen("Great, i'll add your data to the system!")
                    updateFloats(selectedData[0])
                else:
                    name=str(input("Tell me what it was: "))
                    found=False
                    for i in range(len(items)):
                        if items[i].name==name:
                            found=True
                            updateFloats(i)
                            putOnScreen("Damn, i'll be better for next time!")
                    if not found:
                        print("I didn't have a \""+name.capitalize()+"\" in my records.")
                        print("Would you like to add \"",name.capitalize()+"\"?")
                        a=getInput()
                        if a>0:   
                            items.append(item(name,0,answers))
                            save()
                            print("done!")
                        else:
                            print("fine i'll leave out",name.capitalize())
                detectUncertainties(selectedData[0])
                clearTemps()
                pyguessed=False
                probableText=font.render("",True,(255,125,0))
                updateLeastGuessed()
            else:
                answers.append(round(sliderValue,4))
                if questionNum==len(questions)-1:
                    selectedData=evaluateCertainties()
                    putOnScreen("I guess "+items[selectedData[0]].name.capitalize()+"?"+" (Certainty of "+str(round(100*selectedData[1],2))+"%)")
                    pyguessed=True
                else:
                    if questionNum>18:
                        probableText=font.render("Most probable answer: "+items[evaluateCertainties()[0]].name.capitalize(),True,(255,125,0))
                    questionNum+=1
                    putOnScreen(questions[questionNum].string)
                    for i in range(len(items)):
                        items[i].updateCertainty(sliderValue)
        screen.fill((255,255,255))
        drawUI()
        drawLeastGuessed()
        drawTotalGames()
        updateTotalGames()
        for event in pygame.event.get():
           if event.type==QUIT:
              pygame.quit()
              sys.exit()
           if event.type==KEYDOWN:
               if event.key==K_ESCAPE:
                   pygame.quit()
                   sys.exit()
               if event.key==K_y:
                   sliderValue=1.0
                   sliderPos=(280,sliderPos[1])
                   resetPos=False
                   sliderValText=font.render(str(round(sliderValue,2)),True,(0,0,0))
               if event.key==K_n:
                   sliderValue=-1.0
                   sliderPos=(20,sliderPos[1])
                   resetPos=False
                   sliderValText=font.render(str(round(sliderValue,2)),True,(0,0,0))
               if event.key==K_m:
                   sliderValue=0.2
                   sliderPos=(180,sliderPos[1])
                   resetPos=False
                   sliderValText=font.render(str(round(sliderValue,2)),True,(0,0,0))
           if event.type==KEYUP:
               if event.key==K_RETURN:
                   sumbitAnswer()

        pygame.display.update()
        pygame.display.flip()
elif mode=="text":
    r()
