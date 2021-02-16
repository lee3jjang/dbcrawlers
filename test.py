# maturity = np.array([1, 3, 5, 10, 20, 30])
# rate = np.array([0.01301, 0.01325, 0.01415, 0.01600, 0.01625, 0.01604])
# alpha, ufr = 0.1, 0.052
# sw = SmithWilson(alpha, ufr, cp=60, eps=1e-4)
# sw.set_params(maturity, rate)

import numpy as np
from scipy.optimize import minimize_scalar

__all__ = ['SmithWilson', 'NelsonSiegel']

class SmithWilson:

    def __init__(self, ufr, alpha0=0.1, cp=60, eps=1e-4):
        self.ufr = np.log(1+ufr)
        self.alpha0 = alpha0
        self.cp = cp
        self.eps = eps

    def discount_factor(self, t, order=0):
        """
            Description
            -----------
            ㆍ할인요소(P(t))를 계산
            ㆍ2nd derivatives까지 계산 가능함
        """
        df = (-self.ufr)**order*np.exp(-self.ufr*t)+self._wilson(t[:, None], self.u, self._alpha, order)@self.zeta
        return df

    def set_interest_rate(self, maturity, interest_rate):
        """
            Description
            -----------
            ㆍα 및 UFR은 사전에 주어져야 함
            ㆍ관찰 금리 데이터를 이용해 ζ를 계산 후 u와 함께 객체 내에 저장

            Warning
            -------
            입력할 때 연단위금리(annually compounded annual rate)를 넣을 것
        """
        m = 1/(1+interest_rate)**maturity
        mu = np.exp(-self.ufr*maturity)
        W = self._wilson(maturity[:, None], maturity, self.alpha0)

        self.maturity = maturity
        self.interest_rate = interest_rate
        self.zeta = np.linalg.inv(W)@(m-mu)
        self.u = maturity.copy()

    def _wilson(self, t, u, alpha, order=0):
        if order == 0:
            W = np.exp(-self.ufr*(t+u))*(alpha*np.fmin(t,u) - np.exp(-alpha*np.fmax(t,u))*np.sinh(alpha*np.fmin(t,u)))
        elif order == 1:
            W = np.where(t < u, np.exp(-self.ufr*t-(alpha+self.ufr)*u)*(self.ufr*np.sinh(alpha*t)-alpha*np.cosh(alpha*t)-alpha*(self.ufr*t-1)*np.exp(alpha*u)), \
                    np.exp(-self.ufr*u-(alpha+self.ufr)*t)*((alpha+self.ufr)*np.sinh(alpha*u)-alpha*self.ufr*u*np.exp(alpha*t)))
        elif order == 2:
            W = np.where(t < u, np.exp(-self.ufr*t-(alpha+self.ufr)*u)*(-(alpha**2+self.ufr**2)*np.sinh(alpha*t)+2*alpha*self.ufr*np.cosh(alpha*t)+alpha*self.ufr*(self.ufr*t-2)*np.exp(alpha*u)), \
                    np.exp(-self.ufr*u-(alpha+self.ufr)*t)*(alpha*self.ufr**2*u*np.exp(alpha*t)-(alpha+self.ufr)**2*np.sinh(alpha*u)))
        else:
            raise OrderError
        return W

    def optimize_alpha(self):
        """
            Description
            -----------
            ㆍConvergence Point에서 오차(LTFR과 intantaneous forward rate (at CP)의 차이 절대값)가 ε가 되게 하는 α 설정
            ㆍLTFR와 intantaneous forward rate는 continuously compounded 기준으로 계산함
            ㆍinplace=True로 설정하면 parameter(u, ζ)이 객체 내에 설정됨

            Warning
            -------
            입력할 때 연단위금리(annually compounded annual rate)를 넣을 것
        """

        m = 1/(1+self.interest_rate)**self.maturity
        mu = np.exp(-self.ufr*self.maturity)
        
        def obj_fun(alpha):
            W = self._wilson(self.maturity[:, None], self.maturity, alpha)
            zeta = (m-mu)@np.linalg.inv(W)
            W_T = self._wilson(self.cp, self.maturity, alpha)
            derivW_T = self._wilson(self.cp, self.maturity, alpha, order=1)
            bond0_T = np.exp(-self.ufr*self.cp) + W_T@zeta
            bond1_T = -self.ufr*np.exp(-self.ufr*self.cp)+derivW_T@zeta
            forward_T = -bond1_T/bond0_T
            error = abs(self.eps-abs(self.ufr-forward_T)) # 금감원 optimizer 그대로 복제할 경우 수정 필요
            return error
        
        alpha = minimize_scalar(obj_fun, method='bounded', bounds=(1e-4,1), options={'disp':False}).x
        return alpha

    @property
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        m = 1/(1+self.interest_rate)**self.maturity
        mu = np.exp(-self.ufr*self.maturity)
        W = self._wilson(self.maturity[:, None], self.maturity, self._alpha)
        self.zeta = np.linalg.inv(W)@(m-mu)
        self.u = self.maturity.copy()

    def spot_rate(self, t, compounded='annually'):
        """
            Description
            -----------
            현물이자율(r(t))를 계산
        """

        t = np.fmax(t, 1e-6)
        P = np.exp(-self.ufr*t)+self._wilson(t[:, None], self.u, self._alpha)@self.zeta
        if compounded == 'annually':
            rate = (1/P)**(1/t) - 1
        elif compounded == 'continuously':
            rate = -np.log(P)/t
        else:
            raise CompoundedError
        return rate

    def forward_rate(self, t, s, compounded='annually'):
        """
            Description
            -----------
            선도이자율(f(t, t+s))를 계산
        """

        if s<0:
            raise Exception("s < 0 예외")
        if compounded == 'annually':
            rate = (self.discount_factor(t)/self.discount_factor(t+s))**(1/s)-1
        elif compounded == 'continuously':
            rate = 1/s*np.log(self.discount_factor(t)/self.discount_factor(t+s))
        else:
            raise CompoundedError
        return rate
    
    def instantaneous_forward_rate(self, t, order=0):
        """
            Description
            -----------
            ㆍ순간선도이자율(f(t))를 계산
            ㆍcontinuously compounded
            ㆍinstantaneous_forward_rate(t) ≒ forward_rate(t, 1e-6, compounded="continuously")
            ㆍ1st derivatives까지 계산 가능함
        """

        if order==0:
            rate = -self.discount_factor(t, 1)/self.discount_factor(t, 0)
        elif order==1:
            rate = 1/self.discount_factor(t, 0)*(-self.discount_factor(t, 1)**2/self.discount_factor(t, 0)+self.discount_factor(t, 2))
        else:
            raise OrderError
        return rate
    
    def _wilson(self, t, u, alpha, order=0):
        if order == 0:
            W = np.exp(-self.ufr*(t+u))*(alpha*np.fmin(t,u) - np.exp(-alpha*np.fmax(t,u))*np.sinh(alpha*np.fmin(t,u)))
        elif order == 1:
            W = np.where(t < u, np.exp(-self.ufr*t-(alpha+self.ufr)*u)*(self.ufr*np.sinh(alpha*t)-alpha*np.cosh(alpha*t)-alpha*(self.ufr*t-1)*np.exp(alpha*u)), \
                    np.exp(-self.ufr*u-(alpha+self.ufr)*t)*((alpha+self.ufr)*np.sinh(alpha*u)-alpha*self.ufr*u*np.exp(alpha*t)))
        elif order == 2:
            W = np.where(t < u, np.exp(-self.ufr*t-(alpha+self.ufr)*u)*(-(alpha**2+self.ufr**2)*np.sinh(alpha*t)+2*alpha*self.ufr*np.cosh(alpha*t)+alpha*self.ufr*(self.ufr*t-2)*np.exp(alpha*u)), \
                    np.exp(-self.ufr*u-(alpha+self.ufr)*t)*(alpha*self.ufr**2*u*np.exp(alpha*t)-(alpha+self.ufr)**2*np.sinh(alpha*u)))
        else:
            raise OrderError
        return W

class OrderError(ValueError):
    pass

class CompoundedError(ValueError):
    pass

