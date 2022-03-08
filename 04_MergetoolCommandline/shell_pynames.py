from cmd import Cmd
import pynames.generators
from pynames import GENDER, LANGUAGE
from inspect import getmembers
import shlex
import readline


def parse(arg):
    return tuple(map(str, arg.split()))


class Pynames_CMD(Cmd):
    intro = 'Welcome to the Pynames shell.   Type help or ? to list commands.\n'
    prompt = '(Pynames) '
    file = None
    lang_mode = LANGUAGE.RU
    ask_lang = False
        
        
    def do_language(self, arg):
        args = parse(arg)
        if len(args) >= 1:
            if args[0] == "RU":
                self.lang_mode = LANGUAGE.RU
            elif args[0] == "EN":
                self.lang_mode = LANGUAGE.EN

 
    def process_args(self, arg):
        self.gender = GENDER.ALL
        self.ask_lang = False
        args = shlex.split(arg)
        if len(args) == 0 or len(args) > 3:
            self.help_generate()
            return
        gender_idx = None
        if len(args) == 3:
            gender_idx = 2
        elif len(args) > 1 and (args[1] == 'male' or args[1] == 'female' or args[1] == 'language'):
            gender_idx = 1
        if gender_idx is not None:
            if args[gender_idx].lower() == 'female':
                self.gender = GENDER.FEMALE
            elif args[gender_idx].lower() == 'male':
                self.gender = GENDER.MALE
            elif args[gender_idx].lower() == 'language':
                self.ask_lang = True
        available_gens = eval(f"getmembers(pynames.generators.{args[0].lower()})")
        gen = None
        if gender_idx is not None and gender_idx != 1:
            for (name, obj) in available_gens:
                if args[1] in name:
                    gen = obj()
                    break
        else:
            for (name, obj) in available_gens:
                if 'generator' in name.lower() and 'name' in name.lower():
                    gen = obj()
                    break
        return gen

    
    def do_info(self, arg):
        gen = self.process_args(arg)
        if gen is not None:
            if not self.ask_lang:
                print(gen.get_names_number(self.gender))
            else:
                name = gen.get_name()
                members = getmembers(name)
                langs = []
                for (name, val) in members:
                    if name == 'translations':
                        if 'ru' in str(val):
                            langs += ['ru']
                        if 'en' in str(val):
                            langs += ['en']
                print(langs)

    
    def do_generate(self, arg):
        gen = self.process_args(arg)
        if gen is not None:
            if self.gender == GENDER.ALL:
                print(gen.get_name_simple(GENDER.FEMALE, self.lang_mode) + gen.get_name_simple(GENDER.MALE, self.lang_mode), flush=True)
            else:
                print(gen.get_name_simple(self.gender, self.lang_mode), flush=True)
    
    
    def do_bye(self, arg):
        print("Thanks for using!")
        return True
    
    
    def complete_info(self, text, line, begidx, endidx):
        last_arg = shlex.split(text)
        to_print = [""]
        classnames = getmembers(pynames.generators)
        if len(last_arg) == 0:
            for (name, val) in classnames:
                if name == "__all__":
                    to_print = val
                    break
        else:
            last_arg = last_arg[0]
            possible_arguments = ['male', 'female', 'language']
            if last_arg in classnames:
                subclassnames = eval(f'getmembers(pynames.generators.{last_arg})')
                for (name, _) in subclassnames:
                    namel = name.lower()
                    if 'generator' in namel and 'list' not in namel:
                        split1 = namel.split('full')
                        if (len(split1) == 1):
                            split1 = namel.split('name')
                            possible_arguments += [split1[0]]
                to_print = possible_arguments
            elif last_arg not in possible_arguments:
                to_print = possible_arguments
        print()
        print(*to_print)

    
    def complete_generate(self, text, line, begidx, endidx):
        last_arg = shlex.split(text)
        to_print = [""]
        classnames = getmembers(pynames.generators)
        if len(last_arg) == 0:
            for (name, val) in classnames:
                if name == "__all__":
                    to_print = val
                    break
        else:
            last_arg = last_arg[0]
            possible_arguments = ['male', 'female']
            if last_arg in classnames:
                subclassnames = eval(f'getmembers(pynames.generators.{last_arg})')
                for (name, _) in subclassnames:
                    namel = name.lower()
                    if 'generator' in namel and 'list' not in namel:
                        split1 = namel.split('full')
                        if (len(split1) == 1):
                            split1 = namel.split('name')
                            possible_arguments += [split1[0]]
                to_print = possible_arguments
            elif last_arg not in possible_arguments:
                to_print = possible_arguments
        print()
        print(*to_print)
            
            
    def complete_language(self, text, line, begidx, endidx):
        last_arg = shlex.split(text)
        if len(last_arg) == 0:
            print()
            print('ru', 'en')
        elif last_arg[0].lower() in 'ru':
            print('ru')
        elif last_arg[0].lower() in 'en':
            print('en')


pn = Pynames_CMD()
pn.cmdloop()