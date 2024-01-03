def calc_len(dx_n):
    total, i = 0, 1
    while total < dx_n:
        total += i
        i += 1

    return i if total == dx_n else 0 # +1, nes 0 irgi included

def remove_first_occurrence(lst, value):
    lst_copy = lst.copy()
    lst_copy.remove(value)
    return lst_copy

def gaukDelta(x):
   dx = []
   l = len(x)
   for i in range(l):
      for j in range(i+1,l):
         dx.append(x[j]-x[i])
   dx.sort()
   return dx

def skiena(dx):
    def is_valid(x, dx):
        dx_copy = dx.copy()
        dx_copy.sort()
        dx_copy.pop(0)
        valid = True
        i = 0
        for i, a in enumerate(x):
            if not valid: break
            for j, b in enumerate(x[i+1:], start=i+1):
                c = abs(a - b)
                valid = False
                for di, d in enumerate(dx_copy):
                    if c == d:
                        dx_copy.pop(di)
                        valid = True
                        break
        return valid

    def skiena_recurse(x, dx, depth=0):
        if len(x) == n:
            if is_valid(x, dx+x):
                # print("   "*depth,x)
                # print(x)
                # print(depth)
                return x
            else:
                return None

        # print("   "*depth,x)
        for d in set(dx): # set(), kad liktų tik unique
            new_x = x + [d]
            if is_valid(new_x, dx+x):
                
                result = skiena_recurse(new_x, remove_first_occurrence(dx, d), depth + 1)
                if result:
                    return result
        return None

    n = calc_len(len(dx))
    x = [0, max(dx)]
    return skiena_recurse(x, remove_first_occurrence(dx, max(dx)))

# dx = [2, 3, 3, 3, 5, 6, 6, 8, 9, 11]
# dx = [2,3,4,5,7,9]

# dx = [1, 1, 2, 2, 3, 4, 4, 6, 7, 8, 8, 12, 14, 15, 16]
# dx = [15, 16, 1, 2, 2, 3, 4, 4, 6, 7, 8, 1, 8, 12, 14]
x = [2**i for i in range(0,10)] + [i for i in range(600,607)] + [i**2+800 for i in range(0,10)] + [1000]
if x != None: x.sort()
print(f"x original: {x}")

dx = gaukDelta(x)
print(f"dx: {dx}")
x = skiena(dx)

if x != None: x.sort()
print(f"x calculated: {x}")
