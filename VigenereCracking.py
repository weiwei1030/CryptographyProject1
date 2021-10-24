import numpy
import string
import math

def aishift(l, n):
    return l[n:]+l[:n]

def duplication_check(arr, hnum):
    shift = arr.index(hnum)+1
    same = [shift]
    for i in range(len(arr)):
        if arr[i] == hnum and i+1 != shift:
            same.append(i+1)
        gcf = math.gcd(shift, same[0])
        for j in range(len(same)):
            if j != 0:
                gcf = math.gcd(gcf, same[j])
    return gcf


letter2num = dict(zip(range(0, 26), string.ascii_lowercase))  # assign 0-26 to each english letter
freq = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025,
        0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.0236, 0.0015,
        0.01974, 0.00074]
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
ct = input('Enter the Cipher text: ').casefold()
ct = list(ct)
count = 0
shadow_ct = ct
num_of_coincidence = []
#print(numpy.roll(ct,0))
#find the number of coincidence
for i in range(0, 20):
    shadow_ct = numpy.roll(shadow_ct, 1)
    shadow_ct[0] = None
    for x, y in zip(ct, shadow_ct):
        if x == y:
            count += 1
    num_of_coincidence.append(count)
    print('Number of coincidence for {} shift is: {}'.format(i+1, count))
    count = 0

#Top 5 highest number of coincidence
high1 = max(num_of_coincidence)
high2 = sorted(set(num_of_coincidence))[-2]
high3 = sorted(set(num_of_coincidence))[-3]
high4 = sorted(set(num_of_coincidence))[-4]
high5 = sorted(set(num_of_coincidence))[-5]
shift1 = duplication_check(num_of_coincidence, high1)
shift2 = duplication_check(num_of_coincidence, high2)
shift3 = duplication_check(num_of_coincidence, high3)
shift4 = duplication_check(num_of_coincidence, high4)
shift5 = duplication_check(num_of_coincidence, high5)
possible_keylen = [shift1, shift2, shift3, shift4, shift5]
print('\nThe highest coincidence is {} with {} shifts'.format(high1, shift1))
print('The 2nd highest coincidence is {} with {} shifts'.format(high2, shift2))
print('The 3rd highest coincidence is {} with {} shifts'.format(high3, shift3))
print('The 4th highest coincidence is {} with {} shifts'.format(high4, shift4))
print('The 5th highest coincidence is {} with {} shifts\n'.format(high5, shift5))

#Find the key
for x in range(0, 5):
    print("Taking {} as the key length to find the key".format(possible_keylen[x]))
    parts = [[] for z in range(0, possible_keylen[x])]
    en_key = []
    length = int(len(ct)/possible_keylen[x])+1
    #dividing the cipertext into L parts
    w = 0
    while w < possible_keylen[x]:
        for w1 in range(w, len(ct), possible_keylen[x]):
            parts[w].append(ct[w1])
        w += 1
    #cracking shift cipher for each part
    for a in range(0, possible_keylen[x]):
        w = []
        #counting the occurrence of each letter
        for char in letters:
            occurrence = (parts[a].count(char))/26
            occurrence = round(occurrence, 7)
            w.append(occurrence)

        i = 0
        bigger = 0
        id = 0
        while i <= 25:
            ai = aishift(freq, i)
            innerp = round(numpy.dot(w, ai), 6)
            if innerp > bigger:
                bigger = innerp
                id = i
            i += 1
        id = 26-id
        key = letter2num[id].upper()
        en_key.append(key)
        p = []
        #diciphering and get the plain text of first L part
        for ch in parts[a]:
            char_num = ord(ch) - 97
            char_num = (char_num - id)
            char_num = char_num % 26
            p.append(letter2num[char_num])
        parts[a] = p
    print('The Encryption Key is: {}'.format(''.join(en_key)))
    pt = []
    p = 0
    for v in range(0, len(parts[0])):
        for w in range(0, len(parts)):
            if v < len(parts[w]):
                pt.append(parts[w][v])
        p += 1
    print('The deciphered text is: \n{}\n'.format(''.join(str(m) for m in pt)))
