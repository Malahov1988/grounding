from P_ikviv_gor import get_P_gor
from Сoefficient_isp import K_isp_contur, K_isp_ryad
from math import pi, log


class Book:
    def __init__(self, p1, p2, h, l_vert, d_v, a1, a2, b, t, R_norm, m, tip_vert_zazem, tip_gor_zazem,
                 rasp_zazem, calc):
        '''
        p1 - удельное сопротивление верхнего слоя грунта, Ом*м;
        p2 - удельное сопротивление нижнего слоя грунта, Ом*м;
        h - толщина(мощность) верхнего слоя грунта, м.;
        l_vert - длинна вертикального заземлителя, м.;
        d_v - диаметр вертикального заземлителя, м.;
        a1 - длинна горизонтального заземлителя, сторона 1, м.;
        a2 - длинна горизонтального заземлителя, сторона 2, м.;
        t - глубина укладки горизонтального заземлителя, м.;
        R_norm - нормируемое сопротивление, Ом;
        m - число вертикальных заземлителей, шт. [2, 12];
        tip_vert_zazem - тип вертикального заземлителя;
        tip_gor_zazem - тип горизонтального заземлителя;
        rasp_zazem - расположение заземлителя;
        calc - тип расчета: False - ручной расчет, True - автоматический;
        zapas - запас;
        '''
        self.p1 = p1
        self.p2 = p2
        self.h = h
        self.l_vert = l_vert
        self.d_vert = d_v
        self.b = b
        self.t = t
        self.a1 = a1
        self.a2 = a2
        self.R_norm = R_norm
        self.m = m
        self.tip_vert_zazem = tip_vert_zazem
        self.tip_gor_zazem = tip_gor_zazem
        self.rasp_zazem = rasp_zazem
        self.calc = calc
        self.znak = 3
        self.zapas = 1.05


    @staticmethod
    def get_ikviv_diametr(tip_zazem: str, value: float) -> float:
        '''Расчет эквивалентного диаметра см. книгу страница 103,
        Примечание: в формуле 2.40 используется радиус r0, соответственно эквивалентный диаметр делим на 2.
        '''
        if tip_zazem == 'круглый прокат':
            return value * 0.5
        elif tip_zazem == 'уголок стальной':
            return value * 0.95 * 0.5
        elif tip_zazem == "полосовой прокат":
            return value * 0.5 * 0.5

    def get_P_ekviv_vert(self) -> None:
        '''Эквивалентное удельное сопротивление двухслойной земли для вертикальных заземлмтелей'''
        k = 1 if self.p1 > self.p2 else 1.2
        self.P_ekviv = round((self.p1 * self.p2 * k * self.l_vert) / (
                self.p1 * (self.t + k * self.l_vert - self.h) + self.p2 * (self.h - self.t)), self.znak)

    def get_R_vert(self):
        '''Сопротивление/проводимость одного вертикального заземлителя'''
        d_vert = self.get_ikviv_diametr(self.tip_vert_zazem, self.d_vert)
        self.R_vert = round((self.P_ekviv / (2 * pi * self.l_vert ** 2)) * (
                self.l_vert * log(2 * self.l_vert / d_vert) + (self.l_vert + self.t) * log(
            (self.l_vert + self.t) / (self.l_vert + 2 * self.t)) + self.t * log(
            2 * self.t / (self.l_vert + 2 * self.t)) - 0.307 * self.l_vert), self.znak)
        self.g_vert = round(1 / self.R_vert, self.znak)

    def get_R_gor(self, a):
        '''Эквивалентное удельное сопротивление/сопротивление/проводимость горизонтального заземлителя.
        В формуле 2.45а 2*r0*t а в примере r0*t'''
        d_g = self.get_ikviv_diametr(self.tip_gor_zazem, self.b)
        K_ekv_g = get_P_gor(self.p1, self.p2, self.h, self.t).get_tab(a)
        P_gor = round(K_ekv_g * self.p2, self.znak)
        R_gor = round((P_gor / (2 * pi * a)) * (
                log((a ** 2) / (d_g * self.t)) + (2 * self.t / a) - 0.5 * ((2 * self.t / a) ** 2) - 0.61),
                      self.znak)
        g_gor = round(1 / R_gor, 4)
        return P_gor, R_gor, g_gor

    def get_resist_for_contur(self):
        self.get_P_ekviv_vert()
        self.get_R_vert()
        P_gor1, R_gor1, g_gor1 = self.get_R_gor(self.a1)
        P_gor2, R_gor2, g_gor2 = self.get_R_gor(self.a2)
        K = K_isp_contur(self.p1, self.p2, self.h, self.l_vert, self.a1, self.a2)
        K.get_tabl()
        l_total = (self.a1 + self.a2) * 2
        if self.calc == False:
            K_isp = K.get_interpol_for_m(self.m)
            self.R = round(1 / (K_isp * (self.m * self.g_vert + 2 * g_gor1 + 2 * g_gor2)), self.znak)
            conditions, error = self.conditions_for_contur(self.m)
            if conditions:
                return True, [self.P_ekviv, self.R_vert, K_isp, P_gor1, R_gor1, P_gor2, R_gor2, self.m, self.R,
                              round(l_total / self.m, 2), l_total]
            else:
                return False, error
        elif self.calc == True:
            for m in range(2, 13):
                K_isp_c = K.get_interpol_for_m(m)
                R = round(1 / (K_isp_c * (m * self.g_vert + 2 * g_gor1 + 2 * g_gor2)), self.znak)
                conditions, error = self.conditions_for_contur(m)
                if R * self.zapas < self.R_norm and conditions:
                    return True, [self.P_ekviv, self.R_vert, K_isp_c, P_gor1, R_gor1, P_gor2, R_gor2, m, R,
                                  round(l_total / m, 2), l_total]
                elif m > 12 and not conditions:
                    return False, error
                else:
                    return False, 'error'

    def get_resist_for_rayd(self):
        self.get_P_ekviv_vert()
        self.get_R_vert()
        P_gor1, R_gor1, g_gor1 = self.get_R_gor(self.a1)
        if self.calc == False:
            K_isp = K_isp_ryad(self.p1, self.p2, self.m).get_K_isp()
            R = round(1 / (K_isp * (self.m * self.g_vert + g_gor1)), self.znak)
            conditions, error = self.conditions_for_rayd(self.m)
            if conditions:
                return True, [self.P_ekviv, self.R_vert, K_isp, P_gor1, R_gor1, '*', '*', self.m, R,
                              round(self.a1 / (self.m - 1), 2), self.a1]
            else:
                return False, error
        elif self.calc == True:
            for m in range(2, 15):
                conditions, error = self.conditions_for_rayd(m)
                K_isp = K_isp_ryad(self.p1, self.p2, m).get_K_isp()
                R = round(1 / (K_isp * (m * self.g_vert + g_gor1)), self.znak)
                if R * self.zapas < self.R_norm and conditions:
                    return True, [self.P_ekviv, self.R_vert, K_isp, P_gor1, R_gor1, '*', '*', m, R,
                                  round(self.a1 / (m - 1), 2), self.a1]
                elif m > 14 and not conditions:
                    return False, error
                else:
                    print(error, m, not conditions)
                    # return False, error




    def conditions_for_rayd(self, m):
        '''Проверка условий, см. стр. 238'''
        error = f'''Условие, 2 <= m <= 14:\t\t{2 <= m <= 14}\nУсловие, 0.5 <= (a1/m-1)/l_в <= 2:\t{0.5 <= (self.a1 / m - 1) / self.l_vert <= 2}\nУсловие, 0.05 <= t/l_в <= 0.1:\t\t{0.05 <= self.t / self.l_vert <= 0.1}\nУсловие, 0.1 <= h/l_в <= 1:\t\t{0.1 <= self.h / self.l_vert <= 1}'''
        if (2 <= m <= 14 and 0.5 <= (self.a1 / (m - 1)) / self.l_vert <= 2 and 0.05 <= self.t / self.l_vert <= 0.1 and 0.1 <= self.h / self.l_vert <= 1):
            return True, ''
        else:
            return False, error

    def conditions_for_contur(self, m):
        '''Проверка условий, см. стр. 238'''
        a_middle = (self.a1 + self.a2) * 2 / m
        error = f'Условие, 2 <= m <= 12:\t\t{2 <= m <= 12}\nУсловие, 0.2 <= h / l_в <= 1:\t\t{0.2 <= self.h / self.l_vert <= 1}\nУсловие, 0.5 <= a_ср / l_в <= 2:\t{0.5 <= a_middle / self.l_vert <= 2}'
        if 2 <= m <= 12 and 0.2 <= self.h / self.l_vert <= 1 and 0.5 <= a_middle / self.l_vert <= 2:
            return True, ''
        else:
            return False, error

    def calc_zazem(self):
        if self.rasp_zazem == "по контуру":
            return self.get_resist_for_contur()
        else:
            return self.get_resist_for_rayd()


if __name__ == '__main__':
    res = Book(250, 30, 2.5, 10, 0.012, 8, 14, 0.040, 0.8, 1, 6, 'круглый прокат', "полосовой прокат", "по контуру",
               False)
    print(res.calc_zazem())
