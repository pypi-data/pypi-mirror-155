#基于Windows.Forms的tkinter webview组件
#事实上，该com组件依赖于系统的浏览器内核
#所以，以Windows10为例，内核是edge而非ie
from tkinter import Tk,Frame
import ctypes
user32=ctypes.windll.user32
import threading

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
from clr import System
from System.Windows.Forms import *
from System.Threading import Thread,ApartmentState,ThreadStart

app=Application

class MyForm:

    def __init__(self):
        pass


class WebView(Frame):

    def __init__(self,parent,width:int,height:int,url='',**kw):
        Frame.__init__(self,parent,width=width,height=height,**kw)
        form=MyForm()
        def getweb(form,w,h):
            web=WebBrowser()
            form.web=web
            web.Width=w
            web.Height=h
        getweb(form,width,height)
        ie=form.web
        ie.ScriptErrorsSuppressed=True
        self.iehwnd=int(str(ie.Handle))
        user32.SetParent(self.iehwnd,self.winfo_id())
        user32.MoveWindow(self.iehwnd,0,0,width,height,True)
        if url!='':
            ie.Navigate(url)
        self.ie=ie
        self._go_bind()

    def _go_bind(self):
        self.bind('<Configure>',self.__resize_webview)
        self.bind('<Destroy>',self.__delete_ie)

    def __resize_webview(self,event):
        self.ie.Width=self.winfo_width()
        self.ie.Height=self.winfo_height()

    def __delete_ie(self,event):
        self.ie.Dispose()
        del self.ie

    def navigate(self,url:str):
        self.ie.Navigate(url)

    def goback(self):
        self.ie.GoBack()

    def goforward(self):
        self.ie.GoForward()

    def gosearch(self):
        self.ie.GoSearch()

    def gohome(self):
        self.ie.GoHome()

    def refresh(self):
        self.ie.Refresh()



def main():
    a=Tk()
    a.geometry('1200x600')
    w=WebView(a,1200,550,'www.baidu.com')
    w.pack(side='bottom',fill='both')

    w.ie.IsWebBrowserContextMenuEnabled=False#禁用快捷键、菜单
    w.ie.Navigating+=before_navigate#打开新的链接
    w.ie.NewWindow+=before_window#打开新的窗口
    
    a.mainloop()
def before_navigate(sender,e):#显示新链接
    print(e.Url)
def before_window(sender,e):#在本控件打开新窗口
    a=sender.Document.ActiveElement.GetAttribute("href")
    sender.Navigate(a)
    e.Cancel=True

def go():
    main()
if __name__ == "__main__":
    t = Thread(ThreadStart(go))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
