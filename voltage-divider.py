#!/usr/bin/env python3

# Formula:
# Vout =    Vs * R2
#           -------
#           R1 + R2
#
# where Vs is the source voltage
# R1 and R2 two resistors (or series of resistors)
# and Vout is the output voltage
def calculate_v_out(vs, r1, r2):
    return (vs * r2) / (r1 + r2)

def ohms(r):
    if r < 1000:
        prefix = ''
    elif r < 1000000:
        prefix = 'k'
        r = r / 1000
    else:
        prefix = 'M'
        r = r / 1000000
    if int(r) == r:
        r = int(r)
    return str(r) + prefix + '\u2126'

# Here are the resistors I have on hand:
def k(val):
    return val*1000

resistors = (10, 22, 47, 100, 150, 200, 220, 270, 330, 470, 510, 680, k(1), k(2), k(2.2), k(3.3), k(4.7), k(5.1), k(6.8), k(10), k(20), k(47), k(51), k(68), k(100), k(220), k(300), k(470), k(680), 1000000)

def find_resistors(v_src, v_out, margin=5.0):
    """
    Finds the two resistor values that will step down v_src to v_out,
    within the acceptable margin/tolerance (default: +/- 5 %)
    Returns a list of tuples (r1, r2, actual_v_out, error)
    """
    results = []
    split = len(resistors) // 2
    # Bruteforce
    for r1 in resistors[:split]:
        for r2 in resistors[split:]:
            this_v_out = calculate_v_out(v_src, r1, r2)
            error = abs(this_v_out - v_out) / v_out
            if error < margin/100.0:
                results.append( (r1, r2, this_v_out, error) )
    # sort by error (taking two decimals into consideration), then R1, then R2
    results.sort(key=lambda tup: (tup[3], tup[0], tup[1]))
    return results

if __name__ == '__main__':
    import sys
    margin = 0.0
    results = []
    while not results:
        results = find_resistors(float(sys.argv[1]), float(sys.argv[2]), margin)
        margin += 1.0

    for r in results:
        print("%5s   %5s   %.2f" % (ohms(r[0]), ohms(r[1]), r[2]))
