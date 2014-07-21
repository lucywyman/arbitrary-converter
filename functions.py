##This is where the magic happens

from flask import Flask, request, render_template
from decimal import *
import alphabet
import os
import string
import math

def getinfo():
    newnumber = 0 
    """Get information from html form (protip: this is
what request.form does!)"""
    try:
        base1 = float(request.form['base1'])
        base2 = float(request.form['base2'])
    except ValueError:
        return render_template('index.html', error=1)
    if (base1 < -36 or
            (base1 >= -1 and base1 < 1) or
            base1 > 36 or
            base2 < -36 or
            (base2 >= -1 and base2 < 1) or
            base2 > 36):
        return render_template('index.html', error=1)
    """Number can't be forced to be int since it may have
base greater than 10.  Python automatically types all
input as string, so then all we have to do is make sure
it's lower case so that the dictionary will work."""
    number = request.form['number'].lower()
    # Get rid of any whitespace the user may have input
    number.join(number.split())
    return [number, base1, base2]

def process(number, base1, base2):
    isnegative = False
    # If number is negative, change it to be not negative
    if (number[0] == "-"):
        isnegative = True
        number = number[1:]
    #If the number is a decimal, pass it to removeRadix
    if "." in number:
        result = removeRadix(base1, base2, number)
    else:
        result = convert(base1, base2, number)
    if (isnegative):
        result = "-" + result
        number = "-" + number
    return [number, base2, result]

def removeRadix(base1, base2, number):
    d = Decimal(number)
    factor = radix = -d.as_tuple().exponent
    """Multiply by the length of the fraction to remove decimal--there are
better algorithms for doing this which will likely be implemented at a later date, ie. Euclid's algorithm"""
    denominator = int(10**factor)
    numerator = int(d*denominator)
    newdenom = str(convert(base1, base2, denominator))
    newnum = str(convert(base1, base2, numerator))
    ##This line is terrifying, but it works and I'm not sure how best to fix it
    result = divide(newnum, newdenom, base2)
    print result
    return result

def divide(dividend, divisor, base2):
    result = []
    print dividend, divisor
    a = dividend[:len(divisor)]
    print a
    for i in range (0, len(dividend)):
        if(dividend < divisor) and not '.' in result:
            result.append('.')
        if (a >= divisor):
            result.append(a-divisor)
        else:
            result.append(0)
        a = subtract(a, divisor, base2)
        a.append(dividend[divisor+i+1])
    print result

def subtract(a, b, base2):
    isnegative = 0
    if(b>a): 
        temp = b
        b = a
        a = temp
        isnegative = 1
    for i in range (0, len(a)-len(b)):
        b.prepend(0)
    for i in range (0, len(a)):
        if (a[len(a)-i]<b[len(a)-i]):
            a[len(a)-i] = a[len(a)-i]+base2
            a[len(a)-i-1] = a[len(a)-i-1]-1
        result.prepend(a[len(a)-i]-b[len(a)-i])
    print result
                
"""I got this algorithm from a great stackoverflow post here
(it's not just copy paste)
http://cs.stackexchange.com/questions/10318/the-math-behind-converting-from-any-base-to-any-base-without-going-through-base"""
def toDigits(number, base2):
    result = []
    rem = 0
    while number != 0:
        rem = number % base2
        number = number // base2
        # Uncomment at your own risk
        # number, rem = divmod(number, base2)
        if (rem < 0):
            number = number + 1
            rem = rem - base2
        result.insert(0, int(rem))
    count = 0
    for digit in result:
        if (digit > 10):
            result[count] = str(unichr(int(digit) + 86))
        count += 1
    """Since the number is now an array, we convert it to a string,
concatenate the string"""
    result = str(''.join(map(str, result)))
    return result


def fromDigits(number, base1):
    s = str(number)
    digits = []
    n = 0
    for digit in s:
        if digit.isalpha():
            digit = alphabet[digit]
            digits.append(int(digit))
        else:
            digits.append(int(digit))
    for a in digits:
        n = base1 * n + a
    int(n)
    return n

# Now, using these two functions, we can actually convert stuff!
def convert(base1, base2, number):
    result = toDigits(fromDigits(number, base1), base2)
    return result



