import importlib.resources
import os

class Program:
    """
        Usage: Create an object of Program() with the program number in integer as an argument
        Example: obj = Program(6)
                 print(obj)
       
        Attributes
        ----------
            file : str
                contents of the file
        
    """
    def __init__(self, prog: int = None) -> int:
        """
            Parameters
            ----------
                prog : int
                    program number
        """

        self.file = ''
        if prog == None:
            print('Create an object of class Program() and pass the program number as a parameter')

        elif prog > 0 and prog < 11:
            self.file = importlib.resources.read_text('pondos', 'program{}.txt'.format(prog))

        else:
            print('Enter a valid program number')
    def __str__(self):
        return self.file
