"""This is a python module for generating a password."""
def pass_word(len_pass : int, numbers = False, Number_of_numbers = None) -> str:
    """
    parameters:
        len_pass: length of your password
        numbers: if False, it won't add any digits in your password, else it will add.
        Number_of_numbers: Only works when numbers is True. sets the number of numbers you
                           want to use in your password."""
    import string
    import random
    if numbers == True and Number_of_numbers == len_pass:
        raise ValueError("Password must contain characters!")
    elif numbers:
        digits = []
        len_digits = []
        for _ in range(Number_of_numbers):
            len_digits.append(_)
        for k in string.digits:
            digits.append(k)
        words = []
        for p in string.ascii_letters:
            words.append(p)
        while len(words) != (len_pass - Number_of_numbers):
            words.pop(random.choice(range(0, len(words))))
        while len(digits) != len(len_digits):
            digits.pop(random.choice(range(0, len(len_digits))))
        for l in digits:
                words.insert((len_pass-Number_of_numbers)+1, l)
        random.shuffle(words)
        return ''.join(words)
    else:
        printable = string.ascii_letters
        words = []
        lst1 = []
        for i in printable:
            words.append(i)
        for j in range(len_pass):
            lst1.append(random.choice(words))
        password = ''.join(lst1)
        return password

def get_output(password : str, file_drive = 'C:\\', file_folder = None, file_name = None):
    """ 
    parameters:
        file_drive: the drive that you want your password be's in.
        file_folder: the folder that you want your password file be's in
        file_name: the name of your .txt file.
    """
    from os.path import join
    #if file_drive == None and file_folder != None and file_name != None:
    #    raise ValueError('You should enter the drive of your file.')
    if file_drive != None and file_name == None:
        raise ValueError("You should enter the name of your file.")
    path = join(file_drive, file_folder, file_name+'.txt')
    with open(r'%s'%path, mode = 'w') as fl:
        fl.write(f"password = {password}")
    
__version__ = "0.10.2"