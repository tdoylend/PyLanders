def yn(prompt):
    while True:
        d=raw_input(prompt)
        if d.upper().startswith('Y'): return True
        if d.upper().startswith('N'): return False
        print 'Please answer yes or no.'

sign = lambda n: -1 if n < 0 else 1

class Box:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)
   
