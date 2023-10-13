from P_ikviv_gor import get_P_gor
from Сoefficient_isp import K_isp_contur, K_isp_ryad
from math import pi, log

class Book:
    def __init__(self, p1, p2, h, l_vert, d_v, b, t, a1, a2, R_norm, m, tip_vert_zazem, tip_gor_zazem,
                 rasp_zazem):
        '''
        p1 - удельное сопротивление верхнего слоя грунта, Ом*м;
        p2 - удельное сопротивление нижнего слоя грунта, Ом*м;
        h - толщина(мощность) верхнего слоя грунта, м.;
        l_vert - длинна вертикального заземлителя, м.;
        d_v - диаметр вертикального заземлителя, м.;
        t - глубина укладки горизонтального заземлителя, м.;
        a1 - длинна горизонтального заземлителя, сторона 1, м.;
        a2 - длинна горизонтального заземлителя, сторона 2, м.;
        R_norm - нормируемое сопротивление, Ом;
        m - число вертикальных заземлителей, шт. [2, 12];
        '''
        self.p1 = p1
        self.p2 = p2
        self.h = h
        self.l_vert = l_vert
        self.d_v = d_v
        self.b = b
        self.t = t
        self.a1 = a1
        self.a2 = a2
        self.R_norm = R_norm
        self.m = m
        self.tip_vert_zazem = tip_vert_zazem
        self.tip_gor_zazem = tip_gor_zazem
        self.rasp_zazem = rasp_zazem
        self.znak = 3

    @staticmethod
    def get_ikviv_diametr(tip_zazem: str, value: float) -> float:
        '''Расчет эквивалентного диаметра,
        Примечание: в формуле 2.40 используется радиус r0, соответственно эквивалентный диаметр делим на 2
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
        self.P_ekviv = round((self.p1 * self.p2 * k * self.l_vert) / (self.p1 * (self.t + k * self.l_vert - self.h) + self.p2 * (self.h - self.t)), self.znak)

    def get_R_vert(self):
        d_v = self.get_ikviv_diametr(self.tip_vert_zazem, self.d_v)
        self.R_vert = round((self.P_ekviv / (2 * pi * self.l_vert ** 2)) * (self.l_vert * log(2 * self.l_vert / d_v) + (self.l_vert + self.t) * log((self.l_vert + self.t) / (self.l_vert + 2 * self.t)) + self.t * log(2 * self.t / (self.l_vert + 2 * self.t)) - 0.307 * self.l_vert), self.znak)
        self.g_vert = round(1 / self.R_vert, self.znak)

    def get_R_gor(self, a):
        '''В формуле 2.45а 2*r0*t а в примере r0*t'''
        d_g = self.get_ikviv_diametr(self.tip_vert_zazem,  self.b)
        K_ekv_g = get_P_gor(self.p1, self.p2, self.h, self.t).get_tab(a)
        P_gor = round(K_ekv_g * self.p2, self.znak)
        R_gor = round((P_gor / (2 * pi * a)) * (
                log((a ** 2) / (d_g * self.t)) + (2 * self.t / a) - 0.5 * ((2 * self.t / a) ** 2) - 0.61), self.znak)
        g_gor = round(1 /R_gor, 4)
        return P_gor, R_gor, g_gor

    def get_resist_for_contur(self):
        self.get_P_ekviv_vert()
        self.get_R_vert()
        P_gor1, R_gor1, g_gor1 = self.get_R_gor(self.a1)
        P_gor2, R_gor2, g_gor2 = self.get_R_gor(self.a2)
        K = K_isp_contur(self.p1, self.p2, self.h, self.l_vert, self.a1, self.a2)
        K.get_tabl()
        K.get_interpol_for_m(self.m)
        K_isp_c = K.K_i
        R = 1 / (K_isp_c * (self.m * self.g_vert + 2 * g_gor1 + 2 * g_gor2))


        print(self.P_ekviv, self.R_vert, self.g_vert, R_gor1, R_gor2, K_isp_c, R)
if __name__ == '__main__':
    B = Book(250, 30, 2.5, 10, 0.012, 0.040, 0.8, 8, 14, 1, 6, 'круглый прокат', "полосовой прокат","по контуру")
    B.get_resist_for_contur()



