#widgets.py

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
PhoneFormat  = FormEntryFormat_dc(re.compile('^(\d{1,3}(-(\d{1,3}(-(\d{1,4})?)?)?)?)?$'      ), '-' , [3, 7], True)   
PhoneFormat2 = FormEntryFormat_dc(re.compile('^(\d{1,3}(-(\d{1,7})?)?)?$'                    ), '-' , [3]   , True)   


''' FormEntry
    an entry with format behavior
'''
class FormEntry(tk.Entry):
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