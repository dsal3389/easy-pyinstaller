import time
import os
import shutil
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

class Window_first(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self._real_path = os.getcwd()
        self._file = None
        self._image = None
        self._location = None
        
        self.master = master
        self.Win()

    def Win(self):
        self.pack(fill=BOTH, expand=1)
        program_title = self.master.title('Easy pyinstaller')
        
        # =================Functions===============

        def clear():
            ans = messagebox.askokcancel('Warning', 'Are you sure you want to reset your settings')
            if ans is False:
                return
            self._file = None
            self._image = None
            self._location = None
            settings_list.delete(0, END)
        
        def image_select():
            select = filedialog.askopenfilename(initialdir='/', title='Image selection')
            if select == '':
                return
            ls = select.split('.')
            if ls[-1] != 'ico':
                messagebox.showwarning('Error', 'The given image is not .ico')
                return
            self._image = select
            settings_list.insert(END, 'Image: ' +select)

        def file_selection():
            select = filedialog.askopenfilename(initialdir='/', title='File selection', filetypes=(('Python files', '*py;*.pyw'), ('all files', '*.*')))
            if select == '':
                return
            ls = select.split('.')
            print(ls[-1])
            if ls[-1] != 'py' and ls[-1] != 'pyw':
                messagebox.showwarning('Error', 'The given file is not\n.py or .pyw')
                return
            file_name = select.split('/')
            fix_space = file_name[-1].split('.')
            fixed = fix_space[0].split()
            os.rename(file_name[-1], '_'.join(fixed) + '.' + ls[-1])
            select = '/'.join(file_name[:-1]) + '/' +'_'.join(fixed) + '.' + ls[-1]
            self._file = select
            settings_list.insert(END, 'File: ' +select)

        def install_location():
            select = filedialog.askdirectory()
            if select == '':
                return
            self._location = select
            settings_list.insert(END, 'Install to: ' +select)

        def converter():
            ans = ask()
            if ans is False:
                return
            command = ['-F']
            if pyw.get() == 1:
                command.append('-w')
            if self._image is not None:
                command.append('-i')
                command.append('"{}"'.format(self._image))
            ls = self._file.split('/')
            os.chdir('/'.join(ls[:-1]))
            os.system('/'.join(ls[:-1]))
            os.system('pyinstaller %s {}'.format(ls[-1]) %(' '.join(command)))
            dirs = ['build', '__pycache__']
            for directory in dirs:
                try:
                    shutil.rmtree(str(directory))
                except Exception:
                    pass
            os.system('cd dist')
            try:
                shutil.move(str('/'.join(ls[:-1])) +'/dist/{}.exe'.format(ls[-1].split('.')[0]), self._location)
            except FileNotFoundError:
                messagebox.showwarning('Error', 'Something went wrong')
                shutil.rmtree('dist')
                os.remove(ls[-1].split('.')[0] +'.spec')
                os.chdir(self._real_path)
                return
            except shutil.Error:
                messagebox.showwarning('Error', 'file already exists')
                os.remove(ls[-1].split('.')[0] +'.spec')
                shutil.rmtree('dist')
                os.chdir(self._real_path)
                return
            shutil.rmtree('dist')
            os.remove(ls[-1].split('.')[0] +'.spec')
            os.chdir(self._real_path)
            messagebox.showinfo('Done', 'All is done\nthe file is where you wanted it to be')

        def _checker():
            if self._file is None:
                messagebox.showwarning('Error', 'No file was given')
                return False
            if self._location is None:
                messagebox.showwarning('Error', 'No install location was given')
                return False
            return True

        def ask():
            check = _checker()
            if check is False:
                return False
            ans = messagebox.askyesno('Settings', 'Sure?\nFile: {0._file}\nImage: {0._image}\nInstall to: {0._location}'.format(self))
            return ans

        def helper():
            helper_but.config(text='Hide', command=hide)
            self.master.geometry('310x510')

        def hide():
            helper_but.config(text='Show help', command=helper)
            self.master.geometry('310x250')


        # =================vars===============

        pyw = IntVar()

        # ================menu===============
        menu = Menu(self)
        other = Menu(menu)
        other.add_command(label='Clear', command=clear)
        menu.add_cascade(label='Other', menu=other)
        self.master.config(menu=menu)
        
        # ==================stuff===============

        version_test = Label(self, text='Version 1.2 Win version', font=('arial', 7))
        page_title = Label(self, text='Easy pyinstaller', font=('arial', 30, 'bold'), fg='white')
        settings_list = Listbox(self)
        file_selection = Button(self, text='Select file', command=file_selection, bg='gray34', fg='white')
        image_selection = Button(self, text='Select image', command=image_select, bg='gray34', fg='white')
        location_to_install = Button(self, text='Install location', command=install_location, bg='gray34', fg='white')
        file_hidden = Checkbutton(self, text='.pyw', variable=pyw, bg='dim gray')
        converte = Button(self, text='Convert', command=converter, bg='gray34', fg='white')
        helper_but = Button(self, text='Show help', command=helper, bg='gray34', fg='white')
        help_text = Text(self, height=15, width=37, bg='gray34', fg='white')
        help_text.insert(END, 'Creator: Daniel sonbolian\n\n'
                         'Select file: select the file that you\nwant to convert to exe\n\nSelect image: If you want to\nadd image'
                         '(Must be .ico)\n\nInstall location: this is where\nyou want your file to\nbe when he is ready\n\nThe box of ".pyw"'
                         ' is if your file\nis hidden so you are useing pyw')
        help_text.config(state=DISABLED)

        # ==============placeing============
        
        page_title.place(x=0, y=0)
        settings_list.place(x=5, y=55, width=200)
        file_selection.place(x=210, y=53)
        image_selection.place(x=210, y=83)
        location_to_install.place(x=210, y=113)
        file_hidden.place(x=210, y=150)
        converte.place(x=210, y=192)
        version_test.place(x=0, y=230)
        helper_but.place(x=240, y=221)
        help_text.place(x=5, y=260)

        # ========== colors ============

        self.config(bg='dim gray')
        page_title.config(bg='dim gray')
        settings_list.config(bg='gray18', fg='white')



        

root = Tk()
root.geometry('310x250')
root.resizable(width=False, height=False)
app = Window_first(root)
root.mainloop()
