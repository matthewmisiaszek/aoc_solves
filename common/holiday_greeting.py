import os
if __name__ == '__main__':
    module_path = ''
else:
    module_path = os.path.dirname(__file__) + '/'
greetingfile = 'holiday_greeting.txt'
holiday_greeting = open(module_path+greetingfile).read().strip()