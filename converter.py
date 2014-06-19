from flask import Flask, render_template, request

#Create the application
app = Flask(__name__)
#app.config.from_object(__name__)

##Alphabet dictionary for bases greater than 10
alphabet = {
'a' : 11, 
'b' : 12, 
'c' : 13, 
'd' : 14, 
'e' : 15, 
'f' : 16, 
'g' : 17, 
'h' : 18, 
'i' : 19, 
'j' : 20, 
'k' : 21, 
'l' : 22, 
'm' : 23, 
'n' : 24, 
'o' : 25, 
'p' : 26, 
'q' : 27, 
'r' : 28, 
's' : 29, 
't' : 30,
'u' : 31,
'v' : 32,
'w' : 33,
'x' : 34,
'y' : 35,
'z' : 36
}

#Bring up index page
@app.route('/')
def index():
    return render_template('index.html')

#Generate convert page with results
@app.route('/convert', methods=['POST', 'GET'])
def getinfo():
    #Get information from html form (protip: this is what request.form does!)
    base1 = int(request.form['base1'])
    base2 = int(request.form['base2'])
    #Number can't be forced to be int since it may have base greater than 10.  
    #Python automatically types all input as string, so then all we have to do is make sure it's lower case so that the dictionary will work.
    oldnumber = request.form['number'].lower()
    #If the first base is greater than 10, convert number to decimal
    #and change base1 to base 10.  Kind of a cheat, but it works.
    if (base1 > 10):
        number = int(oldnumber, base1)
        base1 = 10
    result = convert(base1, base2, number)
    return render_template('/convert.html', number=oldnumber, base2=base2, result=result)

#I got this algorithm from a great stackoverflow post here
#(it's not just copy paste)
#http://cs.stackexchange.com/questions/10318/the-math-behind-converting-from-any-base-to-any-base-without-going-through-base
def toDigits(number, base2):
    result = []
    while number>0:
        result.insert(0, number%base2)
        number = number//base2
    #for digit in result:
     #   for item in alphabet:
      #      if digit == alphabet.value:
       #         digit = alphabet.key
    #Since the number is now an array, we convert it to a string, concatenate the string, then change it back to an int.
    result = int(''.join(map(str, result)))
    return result

def fromDigits(number, base1):
    s = str(number)
    digits = []
    n = 0
    for digit in s:
        digits.append(int(digit))
    for d in digits:
        n = base1*n+d
    return n
     
#Now, using these two functions, we can actually convert stuff!      
def convert(base1, base2, number):
    #Some optimizations.  Thank you, Python.
    if base1==10 and base2==2:
        return(bin(number)[2:])
    elif base1 == 10 and base2 == 8:
        return(oct(number)[2:])
    elif base1 == 10 and base2 == 16:
        return(hex(number)[2:])
    else:
        result = toDigits(fromDigits(number, base1), base2)       
        return result

#Now, run the app!  Yay!
if __name__ == '__main__':
    app.run()

