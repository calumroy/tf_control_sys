#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from sympy import *

# For printing sympy objects
from IPython.display import display
# This changes the output of display to use mathjax which displays
# nice math objects (looks like latex).
init_printing(use_latex='mathjax')


# Example usage of the following function
# # Tunstin's method
# s,z,T,g = symbols('s z T g')

# print("complex 2pole complex 2zero controller")
# # complex 2 pz controller
# ex_numc = (0.1253*s**4+(-5.822)*s**3+414.8*s**2+1192*s+7.172)
# ex_denc = (s**4+(42.79)*s**3+715.1*s**2+1536*s+174.1)

# display(ex_numc/ex_denc)

# sample_T = (0.04)
# #s = 2*(1-1/z)/(T*(1/z+1))
# sd = 2*(1-1/z)/(sample_T*(1/z+1))

# nautiContToDis(ex_numc, ex_denc, sample_T)



def nautiContToDis(ex_numc, ex_denc, sample_T):
    # Tunstin's method
    s,z,T,g = symbols('s z T g')
    # Prewarping tunstin approach
    # This change of variable ensures the matching of the continuous and discrete time freq response at the prewarp
    # frequency ω, because of the following correspondenc pre_warp_f = 1Hz = 2*Pi rad/s
    #pre_warp_f = 2*pi
    #sd = (pre_warp_f/(tan(pre_warp_f*sample_T/S(2))))*((z-1)/(z+1))

    print("tunstin's method to convert a continuous sytem to discrete")
    print("s =")
    #s = 2*(1-1/z)/(T*(1/z+1))
    sd = 2*(1-1/z)/(sample_T*(1/z+1))
    # Prewarping tunstin approach
    # This change of variable ensures the matching of the continuous and discrete time freq response at the prewarp
    # frequency ω, because of the following correspondence
    # pre_warp_f = 1Hz = 2*Pi rad/s
    #pre_warp_f = 2*pi
    #sd = (pre_warp_f/(tan(pre_warp_f*sample_T/S(2))))*((z-1)/(z+1))

    display(sd)

    dis_numc, dis_denc = symbols('dis_numc dis_denc')


    dis_numc = ex_numc.subs({s: sd})
    dis_denc = ex_denc.subs({s: sd})

    display(dis_numc/dis_denc)

    # Y is the output U is the input
    Y, U = symbols('Y U')
    print("Y/U = \n" , "( g * (", dis_denc , ")) / \n (", dis_numc, ")")

    # Y*dis_denc = g*U*dis_nemc
    #display(expand(Y*dis_denc))
    print(simplify(Y*dis_denc))
    # Simplify didn't give a very nice result so using the following we can convert the output to something that is more usable
    res_denc = collect(cancel(collect(expand(simplify(Y*dis_denc)),z)),Y)
    display(res_denc)
    print(res_denc)

    res_numc = collect(cancel(collect(expand(simplify(g*U*(dis_numc))),z)),U)

    display(res_numc)
    print(res_numc)

    # Y*dis_denc = g*U*dis_numc
    # There is a common denominator
    res_t = (cancel(Eq(res_denc, res_numc)))
    # display(res_t)
    # res_t = factor(res_t)
    # display(res_t)
    print('\n')
    # #res_t = solve(res_t, Y)
    # res_t = cancel(res_t)
    # #res_t = simplify(res_t)
    # display(res_t)
    print('\n Get fractional parts')

    n1,d1=fraction(res_denc)
    n2,d2=fraction(res_numc)

    display('n1=', n1)
    display('d1=', d1)
    display('n2=', n2)
    display('d2=', d2)

    print('d1/d2 = ', d1/d2)
    print('d1 == d2 =', d1==d2)
    if d1==d2:
        res_t = expand(cancel(Eq(d2*res_denc, d1*res_numc)))
    else:
        print('\nTrying to simplify')
        res_t = (Eq(expand((d2*res_denc)*d1), expand((d1*res_numc)*d2)))

    print('\nSimplified Equation\n')
    display(res_t)
    print('\nPrinted Equation\n')
    print(res_t)

    print("\nY is the output at time step k \nYz is the output at timestep k+1 ...ect \n"
          "Similarly \nU is the input at time step k \n"
          "Uz is the input at timestep k+1 ...ect \n"
          "g is the overall gain of the controller\n")

    #Yk10, Yk9, Yk8, Yk7, Yk6, Yk5, Yk4, Yk3, Yk2, Yk1, Yk0 = symbols('Yk10 Yk9 Yk8 Yk7 Yk6 Yk5 Yk4 Yk3 Yk2 Yk1 Yk')
    #Uk10, Uk9, Uk8, Uk7, Uk6, Uk5, Uk4, Uk3, Uk2, Uk1, Uk0 = symbols('Uk10 Uk9 Uk8 Uk7 Uk6 Uk5 Uk4 Uk3 Uk2 Uk1 Uk')

    # Function to extract maximum numeric value from
    # a given string
    import inspect
    import re

    def extractMax(input):
        # get a list of all numbers separated by
        # z** characters
        # \d+ is a regular expression which means
        # one or more digit
        # output will be like ['100','564','365']
        numbers = re.findall('z[*][*]\d+',input)
        #print(input)
        #print(numbers)
        # Find the maximum number in the enumeration of found items
        max_num = None
        for num in numbers:
            #print(num)
            power_num = re.findall('\d+',num)
            #print(power_num)
            power_num = int(power_num[0])
            if max_num is None:
                max_num = power_num
            elif power_num > max_num:
                max_num = power_num
        print("numbers = ", numbers)
        return max_num

    # Replace Z powers with Yk
    lines = str(res_t)
    print(lines)

    # create the sympy symbols so we can convert z power into timestep variables.
    # We need to find the largest z power in the formula
    num_sym = extractMax(lines)
    print("Max z power in equation = %s" % num_sym)


    Ymax = symbols('Yk'+str(num_sym))
    display('Maximum timestep variable =', Ymax)
    Y = symbols('Y')

    out_symbols_dict = dict(('Yk%d'%k, symbols('Yk%d'%k)) for k in range(num_sym+1))
    in_symbols_dict = dict(('Uk%d'%k, symbols('Uk%d'%k)) for k in range(num_sym+1))

    print(out_symbols_dict)
    print(in_symbols_dict)


    print("\n Replacing z**x variables with Ykx and Ukx variables \n")

    # Search the string of the sympy expression and replace the Y*z**x expressions with Ykx
    # e.g Y*z**10 = the output from 10 timesteps into the future.
    #for i in range(2,num_sym+1):
    for i in reversed(range(2,num_sym+1)):
        find_str = "Y*z**"+str(i)
        jdx = lines.find(find_str)
        if jdx >= 0:
            lines = lines[:jdx] + 'Yk'+str(i) + lines[jdx + len(find_str)+1:]
        else:
            print("STOP")

    find_str = "Y*z"
    rep_str = "Yk1"
    jdx = lines.find(find_str)
    lines = lines[:jdx] + rep_str + lines[jdx + len(find_str)+1:]
    find_str = r'Y[^k]'
    rep_str = "Yk0"
    fspan = re.search(find_str, lines)
    jdx = fspan.start()
    lines = lines[:jdx] + rep_str + lines[jdx + 1:]


    # Do the same for the U*g*z**x terms.
    # U*g*z**10 = the output from 10 timesteps into the future times a gain g
    for i in reversed(range(2,num_sym+1)):
        find_str = "U*g*z**"+str(i)
        jdx = lines.find(find_str)
        if jdx >= 0:
            lines = lines[:jdx] + 'Uk'+str(i) + '*g' + lines[jdx + len(find_str)+1:]
        else:
            print("STOP")

    find_str = "U*g*z"
    rep_str = "Uk1*g"
    jdx = lines.find(find_str)
    lines = lines[:jdx] + rep_str + lines[jdx + len(find_str)+1:]
    find_str = r'U[*]g'
    rep_str = "Uk0*g"
    fspan = re.search(find_str, lines)
    jdx = fspan.start()
    lines = lines[:jdx] + rep_str + lines[jdx + 3:]

    print(lines)

    # Sympy subs function does not work very well for substituting multiple vars
    # res_n = res_n.subs(replacements)

    res_n = sympify(lines)
    display(res_n)

    print("\n Solving for the latest output \n", Ymax, '=')

    res_nn = solve(res_n,Ymax)

    display(res_nn)

    print(Ymax, '=', res_nn[0], '\n')


    for i in reversed(range(num_sym+1)):
        print('Yk%s gets converted into Yk%s the output sample from %s timesteps ago'%(i,i-num_sym,i-num_sym))

    print('\n')
    for i in reversed(range(num_sym+1)):
        print('Uk%s gets converted into Uk%s the input sample from %s timesteps ago'%(i,i-num_sym,i-num_sym))

    # Replace variables so the latest output is variable is Yk and the latest input is variable Uk
    lines = str(res_nn)
    #print('\n', lines)

    # Replace the Yk variables
    for i in reversed(range(num_sym+1)):
        find_str = r'Yk' + str(i)
        find_str_notend = find_str + r'[^0-9]'
        rep_str = "Yk" + str(i-num_sym)
        fspan = re.search(find_str_notend, lines)
        if fspan is not None:
            jdx = fspan.start()
            lines = lines[:jdx] + rep_str + lines[jdx + len(find_str) +1:]

    # Replace the Uk variables
    for i in range(num_sym+1):
        find_str = r'Uk' + str(i)
        find_str_notend = find_str + r'[^0-9]'
        rep_str = "Uk" + str(i-num_sym) + "*"
        fspan = re.search(find_str_notend, lines)
        if fspan is not None:
            jdx = fspan.start()
            lines = lines[:jdx] + rep_str + lines[jdx + len(find_str) +1:]


    print("\nDISCRETE TRANSFER FUNCTION")
    print('\nYk0=', lines)

