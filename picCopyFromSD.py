# I just want to Make a easy use tool to download picture from SD card.#

__author__ = 'Septem Zhao'

from tkinter import * 
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter.scrolledtext import *
import os
import shutil,threading
from datetime import datetime
picName = ['.jpg','.cr2','.dng','.nef']
versionInfo = '2016,04,23.\nbeta 0.1'

##### Event and Function
def test(event = None):
    showinfo('no info',src+' to '+des)
def showVersion():
    global versionInfo
    showinfo('Version',versionInfo)
def getSource():
    import os
    rmdisk = []
    diskName = os.popen("wmic LOGICALDISK get name").read().split()
    diskDescription = os.popen("wmic LOGICALDISK get Description").read().split()
    for x in diskName:
        if diskDescription[diskName.index(x)]=='可移动磁盘':
            rmdisk.append(x+'\\')
    if len(rmdisk)==0:
        rmdisk.append('没有可移动磁盘')
    return rmdisk
def readPic(event = None):
    global combo1,src,messageList
    if getSource()[0]=='没有可移动磁盘' or combo1.get()=='没有可移动磁盘':
        combo1['values']=getSource()
        combo1.current(0)
        src = combo1.get()
        if src == '没有可移动磁盘':
            showinfo('注意','请插入U盘或者SD卡')
            return
    messageList['state'] = 'normal'
    messageList.delete(0.0,END)
    messageList['state'] = 'disable'   
    messageInsert(readFile(src))
def readFile(d='d:\\'):
    li = [x for x in os.listdir(d)]
    files = []
    for x in li:
        if os.path.isfile(os.path.join(d,x)):
            files.append(os.path.join(d,x))
        else :
            for x in readFile(os.path.join(d,x)):
                files.append(x)
    
    result = list(filter(isPicture,files))
    return result
def isPicture(f):
    global picName
    for x in picName:
        if os.path.splitext(f)[1].lower()==x:
            return True
    return False
def getDes(event = None):
    global labelTwo,des
    des = askdirectory()
    labelTwo['text']=des
def startCopy(Event = None):
    global des,srd
    if des=='':
        showinfo('注意','请选择保存位置！')
        return
    elif src =='' or src =='没有可移动磁盘':
        showinfo('注意','请插入U盘或者SD卡，然后点击\"读取\"按钮')
        return
    #make a new thread to run a COPY TASK,and let the main thred still running
    t1 = threading.Thread(target=copyFile)
    t1.start()
def messageInsert(l):
    global messageList
    messageList['state'] = 'normal'
    if isinstance(l,list):
        for x in l:
            messageList.insert(END,'\n'+x)
    else :
        messageList.insert(END,'\n'+l)
    messageList['state'] = 'disable'
def copyFile():
    global des,src
    today = datetime.today().strftime('%Y_%m_%d')
    desdir = des+'\\'+today
    #make DIR
    try:
        os.mkdir(desdir)
    except OSError as e:
        messageInsert('目录已经存在')
    #count the pictures
    count = 0
    timeStart = datetime.now().timestamp()
    for x in readFile(src):        
        messageInsert('文件 '+shutil.copy2(x,desdir)+' 复制成功,来自 '+x)
        count += 1
    timeOver = datetime.now().timestamp()
    timeUsed = timeOver - timeStart
    messageInsert(str(count)+' 张照片已经复制,用时 '+str(timeUsed)+' 秒')
##### Event Function /


##### Define Main Window
root = Tk()
root.title('照片下载器')
root.geometry('800x600+450+200')
root.resizable(False,False)
src = ''
des = ''
##### Define Main Window /

##### Add Component
frameTop = Frame(root)
frameMain = Frame(root)
frameBottom = Frame(root)

# add label
labelOne=Label(frameTop,text ="从这个位置获得照片")
labelTwo=Label(frameTop,text ='选择保存位置',width=20)

# add Button
button1 = Button(frameTop,text="读取")
button1.bind("<Button-1>",readPic)
button2 = Button(frameTop,text='浏览')
button2.bind('<Button-1>',getDes)
button3 = Button(frameBottom,text='开始导入')
button3.bind('<Button-1>',startCopy)

# add Menu
menuBar = Menu(root)
optionMenu = Menu(menuBar)
optionMenu.add_command(label = '设置')
optionMenu.add_command(label = '退出')
aboutMenu = Menu(menuBar)
aboutMenu.add_command(label = '说明')
aboutMenu.add_command(label = '关于',command = showVersion)

menuBar.add_cascade(label = '选项',menu = optionMenu)
menuBar.add_cascade(label = '信息',menu = aboutMenu)

root['menu'] = menuBar

#add others
combo1=Combobox(frameTop,textvariable =getSource()[0] ,value = getSource())
combo1['state'] = 'readonly'
combo1.current(0)
src = combo1.get()

messageList =ScrolledText(frameMain,width=110,height=40)
messageList['state'] = 'disable'


frameTop.pack()
frameMain.pack()
frameBottom.pack()
messageList.pack()
combo1.grid(row=0,column =1,sticky = E)
button1.grid(row=0,column=2,sticky = E)
labelOne.grid(row=0,column=0,sticky = W)
labelTwo.grid(row=0,column=3)
button2.grid(row=0,column=4)
button3.pack()
##### Add Component /


root.mainloop()