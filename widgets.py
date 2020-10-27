import tkinter as tk, re
from tkinter import ttk
from dataclasses import dataclass, field
from typing import List, Pattern, Iterable
from copy import deepcopy

Char: Pattern = re.compile('[a-z0-9]', re.I)


''' FormEntryFormat_dc
    this serves as a configuration for the behavior of FormEntry
'''
@dataclass
class FormEntryFormat_dc:
    valid      :Pattern        = None                        #pattern to validate text by
    separator  :str            = None                        #the separator to use
    marks      :List           = field(default_factory=list) #list of positions to apply separator
    strict     :bool           = False                       #True|False strict typing
        
    def config(self, ascopy:bool=True, **data):
        c = deepcopy(self) if ascopy else self
        for key in c.__dict__:
            if key in data:
                c.__dict__[key] = data[key]                  #assign new value
        return c
    

#prepare a few formats        
TimeFormat   = FormEntryFormat_dc(re.compile('^(\d{1,2}(:(\d{1,2}(:(\d{1,2})?)?)?)?)?$'      ), ':' , [2, 5])
DateFormat   = FormEntryFormat_dc(re.compile('^(\d{1,2}(\\\\(\d{1,2}(\\\\(\d{1,4})?)?)?)?)?$'), '\\', [2, 5])
IdFormat  = FormEntryFormat_dc(re.compile('^(\d{1,5}(-(\d{1,5}(-(\d{1,5})?)?)?)?)?$'      ), '-' , [5,11], True)   
PhoneFormat2 = FormEntryFormat_dc(re.compile('^(\d{1,3}(-(\d{1,7})?)?)?$'                    ), '-' , [3]   , True)   


''' FormEntry
    an entry with format behavior
'''
class FormEntry(ttk.Entry):
    @property
    def input(self) -> str:
        return self.get()
        
    def offset(self, separator:str, marks:Iterable):
        sep_marks = [] #cache for positions of already inserted separators
        offset    = 0  #the overall offset between inserted and expected separator marks
        
        #get a mark for every current separator
        for i, c in enumerate(self.input):
            if c == separator:
                sep_marks.append(i)
        
        #if any sep_marks ~ subtract the value of sep_marks last index 
        #~from the value of the corresponding index in marks
        n = len(sep_marks)
        if n:       
            offset = max(0, marks[n-1]-sep_marks[-1])
            
        return offset
    
    def __init__(self, master, frmt:FormEntryFormat_dc, **kwargs):
        ttk.Entry.__init__(self, master, **kwargs)
        
        self.valid = frmt.valid
        if self.valid:
            #register validatecommand and assign to options
            vcmd = self.register(self.validate)
            self.configure(validate="all", validatecommand=(vcmd, '%P'))
            
        if frmt.marks and frmt.separator:
            #bind every key to formatting
            self.bind('<Key>', lambda e: self.format(e, frmt.separator, frmt.marks, frmt.strict))
        
    def validate(self, text:str):      
        return not (self.valid.match(text) is None) #validate with regex

    def format(self, event, separator:str, marks:Iterable, strict:bool):
        if event.keysym != 'BackSpace':             #allow backspace to function normally
            i = self.index('insert')                #get current index
            if Char.match(event.char) is None and (i in marks or not strict):
                event.char = separator              #overwrite with proper separator
            else:
                #automatically add separator
                if i+self.offset(separator, marks) in marks:
                    event.char = f'{separator}{event.char}'
                    
            self.insert(i, event.char)              #validation will check if this is allowed
            
            return 'break'

class ToolTip():
    '''
    Custom Tooltips, easy to use, specify widget and text as positional arguments\n
    Additional Arguments:\n
    triggerkey - Which key triggers the placeholder\n
    releasekey - Which key hides the placeholder\n
    bg - Background color of tooltip window(default-yellow-ish), accepts hex and standard colors\n
    fg - Foreground color/Font color of the text, accepts hex and standard colors\n
    fadeout - Default set to 'enabled', set to 'disabled' to disable fadeout or tooltip\n
    ISSUE: What if user want it on left side?
    '''

    def __init__(self, widget, text, triggerkey='<Enter>', releasekey='<Leave>', bg='#ffffe0', fg='black', fadeout='enabled'):
        # basic widget attributes
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.fadeout = fadeout

        # making the tooltip
        self.master = tk.Toplevel(bg=self.bg)
        self.master.attributes('-alpha', 0)  # hide the window
        self.master.overrideredirect(1)
        self.master.attributes('-topmost', True)
        self.frame = tk.Frame(self.master, bg=self.bg, highlightbackground="black",
                              highlightcolor="black", highlightthickness=1)
        self.frame.pack(expand=1, fill='x')
        self.label = tk.Label(self.frame, text=self.text,
                              bg=self.bg, justify=tk.LEFT, fg=self.fg)
        self.label.grid(row=0, column=0)

        # widget binding
        self.widget.bind(triggerkey, self.add)
        self.widget.bind(releasekey, self.remove)
        self.widget.bind('<ButtonPress>', self.remove)

        # reference to window status
        self.hidden = True

    def add(self, event):
        # calculating offset
        offset_x = event.widget.winfo_width() + 2
        offset_y = int((event.widget.winfo_height() -
                        self.widget.winfo_height())/2)
        # get geometry
        w = self.label.winfo_width() + 10
        h = self.label.winfo_height()
        self.x = event.widget.winfo_rootx() + offset_x
        self.y = event.widget.winfo_rooty() + offset_y
        # apply geometry
        self.master.geometry(f'{w}x{h}+{self.x}+{self.y}')
        # bringing the visibility of the window back
        self.master.attributes('-alpha', 1)
        self.hidden = False  # setting status to false

    def remove(self, *args):
        if self.fadeout == 'enabled':  # if fadeout enabled

            if not self.hidden:  # if window is not hidden
                alpha = self.master.attributes('-alpha')
                if alpha > 0:
                    alpha -= 0.10
                    self.master.attributes('-alpha', alpha)
                    self.master.after(25, self.remove)

            else:
                self.master.attributes('-alpha', 0)  # hide the window

        elif self.fadeout == 'disabled':  # if fadeout disabled
            if not self.hidden:
                self.master.attributes('-alpha', 0)
                self.hidden = True

        else:
            raise tk.TclError('Unknown value for option -fadeout')
