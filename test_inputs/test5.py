def myfunc(listitems): 
    final=[] 
    for strchar in listitems: 
        for letters in strchar: 
            if letters in ('a','e','i','o','u', 'A','E','I','O','U'): 
                strchar = strchar.replace(letters,"") 
        final.append(strchar) 
        return final