from math import sqrt

print('Введите коофиценты a b c')
a, b, c = map(int, input().split())
D = b * b - 4 * a * c
if D < 0:
    print('D*D < 0, нет действительных корней')
elif D == 0:
    d = sqrt(D)
    print('x =', (-b) / (a * 2))
else:
    d = sqrt(D)
    if float(int(d)) == d:
        x1 = (-b - d) / (2 * a)
        x2 = (-b + d) / (2 * a)
        if float(int(x1)) == x1:
            x1 = int(x1)
        if float(int(x2)) == x2:
            x2 = int(x2)
        print('x1 =', x1, 'x2 =', x2)
    else:
        print('x1 =', (-b - d) / (2 * a), 'x2 =', (-b + d) / (2 * a))
        print('Альтернативный вид:')
        print('x1 =', '({} - {}) / {},'.format(-b, '√' + str(D), a * 2), 'x2 =',
              '({} + {}) / {}'.format(-b, '√' + str(D), a * 2))
