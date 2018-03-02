#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os, sys, re
import threading as thd
import time
if sys.version_info[0] == 2:
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    from tkinter import *
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()
 
class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Form1')
        self.master.geometry('389x339')
        self.createWidgets()
 
    def createWidgets(self):
        self.top = self.winfo_toplevel()
 
        self.style = Style()
 
        self.TabStrip1 = Notebook(self.top)
        self.TabStrip1.place(relx=0.062, rely=0.071, relwidth=0.887, relheight=0.876)
        self.TabStrip1__Tab1 = Frame(self.TabStrip1)
        self.TabStrip1__Tab1Lbl = Label(self.TabStrip1__Tab1, text="Loading ...")
        self.TabStrip1__Tab1Lbl.place(relx=0.1,rely=0.2)
        self.TabStrip1.add(self.TabStrip1__Tab1, text='主机信息')
 
        self.TabStrip1__Tab2 = Frame(self.TabStrip1)
        self.TabStrip1__Tab2Can1 = Canvas(self.TabStrip1__Tab2, bg='black')
        self.TabStrip1__Tab2Can1.place(relx=0.05,rely=0.05, relw=0.9, relh=0.4)
        self.TabStrip1__Tab2Can2 = Canvas(self.TabStrip1__Tab2, bg='black')
        self.TabStrip1__Tab2Can2.place(relx=0.05,rely=0.5, relw=0.9, relh=0.4)
        self.TabStrip1.add(self.TabStrip1__Tab2, text='监视图')
        
        
        self.TabStrip1__Tab3 = Frame(self.TabStrip1)
        self.TabStrip1__ProcessTree = Treeview(self.TabStrip1__Tab3, show="headings", columns= ("PID", "Name", "CPU", "Mem"))
        self.TabStrip1__ProcessTree.column("PID", width=5)
        self.TabStrip1__ProcessTree.column("Name", width=50)
        self.TabStrip1__ProcessTree.column("CPU", width=5)
        self.TabStrip1__ProcessTree.column("Mem", width=8)
        self.TabStrip1__ProcessTree.heading("PID", text="PID")
        self.TabStrip1__ProcessTree.heading("Name", text="进程名")
        self.TabStrip1__ProcessTree.heading("CPU", text="CPU")
        self.TabStrip1__ProcessTree.heading("Mem", text="内存")
        self.TabStrip1__ProcessTreeBar = Scrollbar(self.TabStrip1__Tab3, orient=VERTICAL, command=self.TabStrip1__ProcessTree.yview)
        self.TabStrip1__ProcessTree.configure(yscrollcommand=self.TabStrip1__ProcessTreeBar.set)
        self.TabStrip1__ProcessTree.place(relx=0.05,rely=0.05, relw=0.85, relh=0.9)
        self.TabStrip1__ProcessTreeBar.place(relx=0.9, rely=0.05, relh=0.9, relw=0.05)
        self.TabStrip1.add(self.TabStrip1__Tab3, text='进程信息')
class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        cpuinfo = os.popen("cat /proc/cpuinfo").read()
        Application_ui.__init__(self, master)
        self.cpu_idle = 0
        self.cpu_time = 0
        self.pids = dict()
        self.cores = (len(cpuinfo) - len(cpuinfo.replace("processor",""))) / len("processor")
        self.release = os.popen("cat /proc/sys/kernel/osrelease").read()[:-1]
        self.hostname = os.popen("cat /proc/sys/kernel/hostname").read()[:-1]
        self.version = os.popen("cat /proc/sys/kernel/ostype").read()[:-1]
        mem = self.get_mem()
        self.total_mem = float(mem[0])/1024
        self.cpu_record = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.mem_record = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        thd.Timer(0,self.update_info).start()
        self.refresh_process()


    def update_info(self):
        mem = self.get_mem()
        uptime = os.popen("cat /proc/uptime").read()
        self.get_cpu_pressure()
        message = """
            Hostname: %s
            Version: %s %s
            CPU Core: %d
            Mem: %0.1f MB
            
            Uptime: %0.0f hours %02.0f:%02.0f
            CPU Loadavg: %s
            CPU usage: %02.2f %%
            Mem usage: %02.2f %%
                """ % (
                # Hostname 
                self.hostname,
                # Version
                self.version, 
                self.release,
                # Core
                self.cores,
                # Mem Total
                float(mem[0]) / 1024,
                # Uptime 
                float(re.compile(r' [0-9.]*\n').sub("",uptime))/ 3600,  
                float(re.compile(r' [0-9.]*\n').sub("",uptime)) % 3600 / 60 ,
                float(re.compile(r' [0-9.]*\n').sub("",uptime)) % 60,
                # Loadavg
                re.match("[0-9.]+ [0-9.]+ [0-9.]+ ",os.popen("cat /proc/loadavg").read()).group(0),
                # CPU usage
                self.cpu_usage * 100,
                # Mem
                mem[3] ,
            )
        self.TabStrip1__Tab1Lbl['text'] = message
        self.update_canvas()
        thd.Timer(1,self.update_info).start()
    
    def get_mem(self):
        info = os.popen("cat /proc/meminfo").read()
        infos = info.split("\n")
        total_mem = int(re.search(r"[0-9]+",infos[0]).group(0))
        free_mem = int(re.search(r"[0-9]+",infos[1]).group(0))
        available = int(re.search(r"[0-9]+",infos[2]).group(0))
        return (total_mem, free_mem, available, 100.0 - float(available) / total_mem * 100)
    
    @staticmethod    
    def get_pids():
        pid = re.search("[0-9\n]*[0-9]",os.popen("ls /proc").read()).group(0).split('\n')
        pids = list()
        for i in pid:
            pids.append(int(i))
        pids.sort()
        return pids
        
    def refresh_process(self):
        # Clear origin items
        for _ in map(self.TabStrip1__ProcessTree.delete, self.TabStrip1__ProcessTree.get_children("")):
            pass
        # Insert new items
        items = list()
        for i in self.get_pids():
            items.append(self.get_process_info(i))
        for i in items:
            self.TabStrip1__ProcessTree.insert("", "end", values=i)
        self.TabStrip1__ProcessTree.after(3000, self.refresh_process)
    
    def get_cpu_pressure(self):
        cpu_stat = os.popen("cat /proc/stat").read().split('\n')[0][5:]
        count = 0
        for i in cpu_stat.split(' '):
            count += int(i)
        idle = int(cpu_stat.split(' ')[3])
        pressure = 1.0 - float(idle - self.cpu_idle) / float(count - self.cpu_time)
        self.cpu_idle = idle
        self.cpu_time = count
        self.cpu_usage = pressure
        return pressure
    
    def get_process_info(self, pid):
        p_stat = os.popen("if [ -e /proc/%d/stat ]; then\n cat /proc/%d/stat \nfi" % (pid,pid)).read()
        cpu_stat = os.popen("cat /proc/stat").read().split('\n')[0][5:]
        try:
            p_statm = int(os.popen("if [ -e /proc/%d/statm ]; then\n cat /proc/%d/statm \nfi" % (pid,pid)).read().split(" ")[1])
        except:
            p_statm = 0
        try:
            p_name = re.search("\([\s\S]+\)",p_stat).group(0)[1:-1]
        except:
            p_name = 'unknow'
        total_p_time = 0
        count = 0
        for _ in p_stat.split(" ")[13:17]:
            total_p_time += int(_)
        for i in cpu_stat.split(' '):
            count += int(i)
        try:
            cpu_time = int(self.pids[str(pid)]["cpu_time"]) - count
            p_time = int(self.pids[str(pid)]["p_time"]) - total_p_time
        except:
            cpu_time = 1
            p_time = 0
        self.pids[str(pid)] = {
            "p_time":  total_p_time,
            "cpu_time": count
        }
        p_mem = "%d KB" % (p_statm * 4) if p_statm < 1024 else "%.2f MB" % (p_statm * 4 / 1024)
        return(str(pid),p_name, "%.2f %%" % abs(float(p_time) / float(cpu_time) * 100 * self.cores) , p_mem )
    
    @staticmethod
    def draw_canvas(canvas, record, title):
        width = canvas.winfo_width() / 30
        offset = 20
        height = canvas.winfo_height() - offset - 10
        canvas.delete("all")
        canvas.create_text(width * 15 - 10, 13, text=title+ " - %.2f%%" % record[29], font = "time 12 bold", fill='white')
        canvas.create_text(15,offset + 5, text="100%", font = "time 10", fill="green")
        canvas.create_line(0, offset, width * 30, offset, fill="red", dash=(4,4))
        canvas.create_text(15,offset + height / 2 - 5, text="50%", font = "time 10", fill="green")
        canvas.create_line(0, offset + height / 2, width * 30, offset + height / 2, fill="red", dash=(4,4))
        canvas.create_text(15,offset+ height - 5, text="0%", font = "time 10", fill="green")
        canvas.create_line(0, offset+height, width * 30, offset+height, fill="red", dash=(4,4))
        for i in range(0,len(record) - 1):
            canvas.create_line(i * width, offset+ height - int(float(record[i]) * height / 100) ,i * width + width, offset + height - int(float(record[i+1]) * height / 100), fill="green")
    
    def update_canvas(self):
        self.cpu_record.pop(0)
        self.cpu_record.append(self.cpu_usage * 100)
        self.mem_record.pop(0)
        self.mem_record.append(self.get_mem()[3])
        self.draw_canvas(self.TabStrip1__Tab2Can1, self.cpu_record, "cpu")
        self.draw_canvas(self.TabStrip1__Tab2Can2, self.mem_record, "memory")

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()