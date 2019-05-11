# 乐高项目代码
# 模块依赖安装: pip install -r requirements.txt
import urllib.request
import PIL
import tkinter as tk
import io
import ctypes
import os
from tkinter import *
from PIL import ImageTk
from PIL import Image


whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)

def main():
    startup = Tk() # 启动加载
    # tk.Label(startup, image=ImageTk.PhotoImage(Image.open(r'icon.png'))).pack()
    startup.title('启动')
    startup.resizable(0,0)
    startup.iconbitmap('icon.ico')
    try:
        os.mkdir("source")
    except:
        dir_status = True
    try:
        obj = urllib.request.urlopen("https://konachan.com/post", timeout=10).read()
    except:
        user = ctypes.windll.LoadLibrary("user32.dll")
        user.MessageBoxW(None, '无法连接到 Konachan', '错误', 0x10)
        return ()
    obj = obj.decode('utf-8')
    rating = re.findall(
        r'<img src=".+?" style="margin-left: 0px;" alt="Rating: (.+?)Score: .+?" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
        obj)
    score = re.findall(
        r'<img src=".+?" style="margin-left: 0px;" alt=".+?Score: (.+?)Tags: .+?" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
        obj)
    user1 = re.findall(
        r'<img src=".+?" style="margin-left: 0px;" alt=".+?User: (.+?)" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
        obj)
    content = re.findall(
        r'<img src="(.+?)" style="margin-left: 0px;" alt=".+?" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
        obj)

    tags = re.findall(
        r'<img src=".+?" style="margin-left: 0px;" alt=".+?Tags: (.+?)User: .+?" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
        obj)
    link = re.findall(r'<span class="plid">#pl (.+?)</span>', obj)

    def print_item(event):
        root.title('加载中...')
        global num
        i = listb.get(listb.curselection())
        if i in content:
            loc = content.index(i)
            label2['text'] = "标签: " + tags[loc] + \
                             "\n链接: " + link[loc] + \
                             "\n用户: " + user1[loc] + \
                             "\n评级: " + rating[loc] + \
                             "\n评分: " + score[loc]
        else:
            loc = content2.index(i)
            label2['text'] = "标签: " + tags2[loc] + \
                             "\n链接: " + link2[loc] + \
                             "\n用户: " + user2[loc] + \
                             "\n评级: " + rating2[loc] + \
                             "\n评分: " + score2[loc]
        num = loc
        try:
            image_bytes = urllib.request.urlopen(i, timeout=10).read()
        except Exception as e:
            user = ctypes.windll.LoadLibrary("user32.dll")
            user.MessageBoxW(None, 'Konachan 连接超时: ' + str(e), '错误', 0x10)
            root.title('Konachan')
            return()
        data_stream = io.BytesIO(image_bytes)
        pil_image = PIL.Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_image)
        label.configure(image=tk_image)
        root.title('Konachan')
        raise RuntimeError("小C大佬太牛逼了") # 抛出异常以正常显示图片

    def create():
        try:
            i = listb.get(listb.curselection())
        except:
            user = ctypes.windll.LoadLibrary("user32.dll")
            user.MessageBoxW(None, '请先选中图片', '错误', 0x10)
            root.title('Konachan')
            return ()
        try:
            if i in content:
                obj = urllib.request.urlopen(str(link[num]), timeout=10).read()
            else:
                obj = urllib.request.urlopen(str(link2[num]), timeout=10).read()
        except Exception as e:
            user = ctypes.windll.LoadLibrary("user32.dll")
            user.MessageBoxW(None, 'Konachan 连接超时: ' + str(e), '错误', 0x10)
            root.title('Konachan')
            return()

        top = Toplevel()
        # top.attributes("-fullscreen", 1)
        obj = obj.decode('utf-8')
        image = re.findall(r'<img alt=".+?" class="image" height=".+?" id="image" large_height=".+?" large_width=".+?" src="(.+?)"',obj)
        image_bytes3 = urllib.request.urlopen(image[-1]).read()
        data_stream3 = io.BytesIO(image_bytes3)
        pil_image3 = PIL.Image.open(data_stream3)
        tk_image3 = ImageTk.PhotoImage(pil_image3)
        label3 = tk.Label(top, image=tk_image3)
        label3.pack()
        top.mainloop()
    def nextClicked():
        root.title('加载中...')
        page = var_list[0]
        page = page + 1
        var_list[0] = page
        changePage(page)

    def lastClicked():
        root.title('加载中...')
        page = var_list[0]
        if page == 1:
            root.title('Konachan Page ' + str(page))
            return
        page = page - 1
        var_list[0] = page
        changePage(page)

    def changePage(page):
        try:
            response = urllib.request.urlopen("https://konachan.com/post?page=" + str(page), timeout=10)
        except Exception as e:
            user = ctypes.windll.LoadLibrary("user32.dll")
            user.MessageBoxW(None, 'Konachan 连接超时: ' + str(e), '错误', 0x10)
            root.title('Konachan')
            return ()
        obj = response.read()
        obj = obj.decode('utf-8')
        global content2, tags2, link, link2, rating2, score2, user2
        content2 = re.findall(
            r'<img src="(.+?)" style="margin-left: 0px;" alt=".+?" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
            obj)
        rating2 = re.findall(
            r'<img src=".+?" style="margin-left: 0px;" alt="Rating: (.+?)Score: .+?" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
            obj)
        tags2 = re.findall(
            r'<img src=".+?" style="margin-left: 0px;" alt=".+?Tags: (.+?)User: .+?" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
            obj)
        score2 = re.findall(
            r'<img src=".+?" style="margin-left: 0px;" alt=".+?Score: (.+?)Tags: .+?" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
            obj)
        user2 = re.findall(
            r'<img src=".+?" style="margin-left: 0px;" alt=".+?User: (.+?)" class=".+?" title=".+?"  width="\d+?" height="\d+?">',
            obj)
        link2 = re.findall(r'<span class="plid">#pl (.+?)</span>', obj)
        link = link2
        listb.delete(0, tk.END)
        for i in content2:
            listb.insert(0, i)
        root.title('Konachan Page ' + str(page))

    def save():
        root.title('保存中...')
        user = ctypes.windll.LoadLibrary("user32.dll")
        try:
            i = listb.get(listb.curselection())
        except:
            user.MessageBoxW(None, '请先选中图片', '错误', 0x10)
            root.title('Konachan')
            return ()
        try:
            if i in content:
                obj = urllib.request.urlopen(str(link[num]), timeout=10).read()
            else:
                obj = urllib.request.urlopen(str(link2[num]), timeout=10).read()
        except Exception as e:
            user.MessageBoxW(None, 'Konachan 连接超时: ' + str(e), '错误', 0x10)
            root.title('Konachan')
            return ()

        obj = obj.decode('utf-8')
        image = re.findall(
            r'<a class="highres-show" href="(.+?)">View larger version</a>',
            obj)
        if image:
            test = None
        else:
            image = re.findall(
                r'<img alt=".+?" class="image" height=".+?" id="image" large_height=".+?" large_width=".+?" src="(.+?)"',
                obj)
        try:
            try:
                filename = str(tags[num])
            except:
                filename = str(tags2[num])
            if os.path.isfile('source/' + filename + '.jpg'):
                user.MessageBoxW(None, '文件已存在: source/' + filename + '.jpg', '错误', 0x10)
                root.title('Konachan')
                return ()
            urllib.request.urlretrieve(image[-1], 'source/' + filename + '.jpg')
        except Exception as e:
            user.MessageBoxW(None, '保存文件失败: ' + str(e), '错误', 0x10)
            root.title('Konachan')
            return ()
        user.MessageBoxW(None, '保存成功: source/' + filename + '.jpg' , '信息', 0x40)
        root.title('Konachan')

    def quit():
        root.destroy()

    startup.destroy()
    startup.mainloop()




    root = Tk() # 主界面
    frm1 = Frame(root)
    frmB = Frame(frm1)
    root.title('Konachan')
    root.resizable(0,0)
    root.iconbitmap('icon.ico')
    frmU = Frame(frm1)
    varList1 = StringVar()
    listb = Listbox(frmU, listvariable=varList1)
    listb['width'] = 43
    for i in content:
        listb.insert(0, i)
    listb.pack(side="left", padx=5)
    scr1 = Scrollbar(root)
    listb.configure(yscrollcommand=scr1.set)
    scr1['command'] = listb.yview
    scr1.pack(side='right',fill="both")



    label2 = tk.Label(root, text="标签: " + tags[-1] +
                                 "\n链接: " + link[-1] +
                                 "\n用户: " + user1[-1] +
                                 "\n评级: " + rating[-1] +
                                 "\n评分: " + score[-1], width=43, justify='left', wraplength=300)
    label2.pack(side='right')



    listb.bind('<ButtonRelease-1>', print_item)
    try:
        image_bytes = urllib.request.urlopen(i, timeout=10).read()
    except Exception as e:
        user = ctypes.windll.LoadLibrary("user32.dll")
        user.MessageBoxW(None, 'Konachan 连接超时: ' + str(e), '错误', 0x10)
        return ()
    data_stream = io.BytesIO(image_bytes)
    pil_image = PIL.Image.open(data_stream)
    tk_image = ImageTk.PhotoImage(pil_image)
    label = tk.Label(root, image=tk_image)
    label.pack(padx=5, pady=5)

    var_list = [1]

    Button(frmB, text='上一页', command=lastClicked).pack(side='left', padx=2.5, pady=5)
    Button(frmB, text='下一页', command=nextClicked).pack(side='right', padx=2.5, pady=5)
    Button(frmB, text='退出', command=quit).pack(side='right', padx=2.5, pady=5)
    Button(frmB, text='保存原图', command=save).pack(side='right', padx=2.5, pady=5)
    Button(frmB, text='查看大图', command=create).pack(side='right', padx=2.5, pady=5)

    frmU.pack()
    frmB.pack()
    frm1.pack()
    root.mainloop()


if __name__ == '__main__':
    main()