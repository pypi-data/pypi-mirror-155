
class struct:
    """
    Returns a dummy dictionary.
    """
    def __init__(self, tag=None, **kwargs):
        self.tag = tag
        self.__dict__.update(**kwargs)
        
    def copy(self, **kw):
        aa = self.__dict__.copy()
        aa.update(kw)
        return struct(**aa)
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__   
    
    def __repr__(self):
        return str(self.__dict__)

def get_mp_data(source, **kwargs):

    '''
    source : path for ase readable file | ase.Atoms object | mp-id as string
    returns: mp_api.Summary object
    '''
    
    from ase.io import read
    import pymatgen as pg
    from mp_api import MPRester
    import ase
    
    mpr = MPRester("R5mXfMsamJjSWfVMcFh0SrP8IrUS4Xy8")
    
    if type(source)==str:
        try:
            at = read(source)
            a  = pg.io.ase.AseAtomsAdaptor().get_structure(at)
            mpid = mpr.find_structure(a, **kwargs)
        except:
            mpid = source
            
    elif type(source)==ase.atoms.Atoms:
        a  = pg.io.ase.AseAtomsAdaptor().get_structure(source)
        mpid = mpr.find_structure(a, **kwargs)
        
    else:
        print("Please enter structure file or Atoms object or mp id\n")   
        
    
    return mpr.summary.get_data_by_id(mpid)

def load_data(filename,head=0):
        import numpy as np
        f = open(filename, 'r')
        lines = [i.split() for i in f.readlines()[head:]]
        f.close()

        for n, i in enumerate(lines):
            for o, j in enumerate(i):
                try:
                    lines[n][o] = float(j)
                except:
                    lines[n][o] = j

        length = max(map(len, lines))
        y=np.array([xi+[None]*(length-len(xi)) for xi in lines])

        return y

def pair_sort(x,y):
        '''
        Returns sorted_x, y_values_wrto_sorted_x
        '''
        import numpy as np
        a = np.argsort(x)
        sorted_y = []

        for i in range(len(a)):
            sorted_y.append(y[a[i]])

        return np.sort(x), np.array(sorted_y)
