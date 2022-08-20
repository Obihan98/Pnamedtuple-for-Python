import traceback, keyword

def pnamedtuple(type_name, field_names, mutable = False,  defaults =  {}):
    digits = ['0','1','2','3','4','5','6','7','8','9']
    def show_listing(s):
        for line_number, text_of_line in enumerate(s.split('\n'),1):         
            print(f' {line_number: >3} {text_of_line.rstrip()}')

    def check_valid_type_name(type_name):
        if type(type_name) != str:
            return False
        if type_name[0] in digits or type_name in keyword.kwlist:
            return False
        return True

    def check_valid_word(names):
        for item in names:
            if item[0] in digits or item[0] == '_' or item in keyword.kwlist:
                return False
        return True

    def get_field_names(field_names):
        if type(field_names) == list:
            names = field_names
        elif type(field_names) == str:
            name = ''
            names = list()
            for i in range(len(field_names)):
                if field_names[i] == ',' or field_names[i] == ' ':
                    names.append(name)
                    name = ''
                else:
                    name += field_names[i]
                    if i == len(field_names) - 1:
                        names.append(name)
            names = [item for item in names if item]
        else:
            raise SyntaxError
        
        if check_valid_word(names):  
            return names
        else:
            raise SyntaxError
    
    def construct_init(field_names, defaults):
        bind = ''
        params = ''
        for i in range(len(field_names)):
            bind += '        ' + 'self.' + field_names[i] + ' = ' + field_names[i] + '\n'
            if field_names[i] in defaults:
                if i == len(field_names) - 1:
                    params += field_names[i] + '=' + str(defaults[field_names[i]])
                else:
                    params += field_names[i] + '=' + str(defaults[field_names[i]]) + ', '
            else:
                if i == len(field_names) - 1:
                    params += field_names[i]
                else:
                    params += field_names[i] + ', '
        return bind, params
    
    def construct_repr(bind):
        bind = bind.split()
        repr = ''
        for i in range(int(len(bind)/3)):
            if i == int(len(bind)/3) - 1:
                repr += bind[(i*3)+2] + '={' + bind[(i*3)] + '}'
            else:
                repr += bind[(i*3)+2] + '={' + bind[(i*3)] + '},'
        return repr
          
    def construct_get(field_names):  
        get = ''
        for item in field_names:
            get += '    def get_' + item +'(self):\n        return self.' + item + '\n\n'
        return get
    
    def construct_index_with_int(field_names):
        index_with_int = '' 
        index_with_int += 'if index == 0:\n                return self.get_' + field_names[0] + '()'
        for i in range(0, len(field_names[1:])):
            index_with_int += '\n            elif index == ' + str(i+1) + ':\n' + '                return self.get_' + field_names[i+1] + '()'
        return index_with_int
    
    def construct_make(bind):
        bind = bind.split()
        repr = ''
        for i in range(int(len(bind)/3)):
            if i == int(len(bind)/3) - 1:
                repr += bind[(i*3)+2] + '=iterable[' + str(i) + ']'
            else:
                repr += bind[(i*3)+2] + '=iterable[' + str(i) + '],'
        return repr

    if not check_valid_type_name(type_name):
        raise SyntaxError

    field_names = get_field_names(field_names)
    bind, params = construct_init(field_names, defaults)
    repr = construct_repr(bind)
    get = construct_get(field_names)
    index_with_int = construct_index_with_int(field_names)
    make = construct_make(bind)

    class_template = '''\
class {type_name}:
    _fields = {field_names}
    _mutable = {mutable}
        
    def __init__(self, {params}):
{bind}
    def __repr__(self):
        return f'{type_name}({repr})'
            
{get}    def __getitem__(self, index):
        if type(index) == int:
            {index_with_int}
            else:
                raise IndexError
        elif type(index) != int:
            if index in self.__dict__:
                return self.__dict__[index]
            else:
                raise IndexError
    def __eq__(self, right):
        if type(right) == {type_name}:
            try:
                for k, v in self.__dict__.items():
                    if v != right.__dict__[k]:
                        return False
            except:
                return False
            return True
        else:
            return False
            
    def _asdict(self):
        return self.__dict__
                
    def _make(iterable):
        return {type_name}({make})
        
    def _replace(self, **kargs):
        for k, v in kargs.items():
            if k not in self.__dict__:
                raise TypeError
        if self._mutable == True:
            for k, v in kargs.items():
                self.__dict__[k] = v
            return None
        else:
            new = self.__dict__.copy()
            for k, v in kargs.items():
                new[k] = v
            iterable = [v for _, v in new.items()]
            return {type_name}({make})
    def __setattr__(self, name, value):
        if self._mutable == True:
            self.__dict__[name] = value
        else:
            if name in self.__dict__:
                raise AttributeError
            self.__dict__[name] = value
    '''

    class_definition = \
    class_template.format(type_name = type_name, \
                          field_names = field_names, \
                          bind = bind, params = params, \
                          mutable = mutable, \
                          repr = repr, \
                          get = get, \
                          index_with_int = index_with_int, \
                          make = make
                          )

    name_space = dict( __name__ = f'pnamedtuple_{type_name}' )                  
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):                      
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]