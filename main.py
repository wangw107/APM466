import csv
import math
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.interpolate import interp1d
last_coupon=[5/12, 1/6, 1/3, 1/12, 5/12, 1/3, 1/3, 1/12, 1/3, 1/3]
number_of_future_coupons=[1, 1, 3, 3, 5, 6, 7, 9, 10, 11]
coupon_rate = []
acc_i = []
dirty_p_jan10=[]
dirty_p_jan11=[]
dirty_p_jan12=[]
dirty_p_jan13=[]
dirty_p_jan14=[]
dirty_p_jan17=[]
dirty_p_jan18=[]
dirty_p_jan19=[]
dirty_p_jan20=[]
dirty_p_jan21=[]
p_series = (dirty_p_jan10, dirty_p_jan11, dirty_p_jan12, dirty_p_jan13, dirty_p_jan14, dirty_p_jan17, dirty_p_jan18, dirty_p_jan19, dirty_p_jan20, dirty_p_jan21)
i=0
with open('bonds_selected.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        coupon_rate.append(float(row['coupon']))
        acc_i.append(float(row['coupon'])*100*last_coupon[i])
        dirty_p_jan10.append(float(row['close_price_jan10'])+acc_i[i])
        dirty_p_jan11.append(float(row['close_price_jan11'])+acc_i[i])
        dirty_p_jan12.append(float(row['close_price_jan12'])+acc_i[i])
        dirty_p_jan13.append(float(row['close_price_jan13'])+acc_i[i])
        dirty_p_jan14.append(float(row['close_price_jan14'])+acc_i[i])
        dirty_p_jan17.append(float(row['close_price_jan17'])+acc_i[i])
        dirty_p_jan18.append(float(row['close_price_jan18'])+acc_i[i])
        dirty_p_jan19.append(float(row['close_price_jan19'])+acc_i[i])
        dirty_p_jan20.append(float(row['close_price_jan20'])+acc_i[i])
        dirty_p_jan21.append(float(row['close_price_jan21'])+acc_i[i])
        i+=1

def coupon(couponrate):
    return 100*couponrate

t0 = []
for i in range(10):
    if number_of_future_coupons[i] == 0:
        t0.append(0)
    else:
        t0.append(1/2-last_coupon[i])

def r0(dirty_p, t0):
    r0 = -math.log(dirty_p/100)/(t0)
    return r0

r_series = []
t_list = []
for h in range(10):
    r_list = []
    for i in range(10):
        p = p_series[h][i]
        t_0 = t0[i]
        if t_0 == 0:
            r_0 = 0
        else:
            r_0 = r0(p, t_0)
        c = coupon(coupon_rate[i])
        j = 0                
        future_c = c*math.exp(-r_0*t_0)
        if number_of_future_coupons[i] == 1:
            r = r_0
            r_list.append(r)
        else:
            r = -1/(t_0+0.5) * math.log((p-c*math.exp(-r_0*t_0))/(c+100))#r1
            while j < number_of_future_coupons[i] - 2:
                j += 1
                t = t_0 + 0.5 * j
                future_c += c * math.exp(-r*t)
                r = -1/(t+0.5) * math.log((p-future_c)/(c+100))
            r_list.append(r)
    r_series.append(r_list)
print(r_series)
m_times = [datetime(2022, 1, 31), datetime(2022, 4, 30), datetime(2023, 2, 28), datetime(2023, 5, 31), datetime(2024, 1, 31), datetime(2024, 8, 31), datetime(2025, 2, 28), datetime(2026, 5, 31), datetime(2026, 8, 31), datetime(2027, 2, 28)]
date_list = ['Jan 10', 'Jan 11', 'Jan12', 'Jan13', 'Jan 14', 'Jan 17', 'Jan 18', 'Jan 19', 'Jan 20', 'Jan 21']
for i in range(10):
    plt.plot_date(m_times, r_series[i], '-')
plt.legend(date_list)
plt.show()


