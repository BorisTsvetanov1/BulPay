"""
BulPay Dashboard Data Generator
Generates 500+ users over 2 years (Apr 2024 – Mar 2026)
with age cohort, device OS, payment type, and monthly balances.
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# ── Age cohort targets ─────────────────────────────────────────────────────────
# 45-65 is the PRIMARY target demo → biggest slice
AGE_COHORTS   = ['18-30', '30-45', '45-65', '65+']
AGE_COUNTS    = [72,      118,     240,      70]   # 500 total

# ── Date range ─────────────────────────────────────────────────────────────────
START = datetime(2024, 4, 1)
END   = datetime(2026, 3, 31, 23, 59, 59)

MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
DAYS_ORDER  = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

def next_month(dt):
    if dt.month == 12:
        return datetime(dt.year + 1, 1, 1)
    return datetime(dt.year, dt.month + 1, 1)

def rand_hour():
    # Peak usage: morning commute 7-9, lunch 12-13, evening 17-21
    hour_weights = [
        0.3, 0.2, 0.2, 0.2, 0.3, 0.6,   # 0-5
        1.2, 3.5, 4.5, 3.8, 3.5, 3.8,   # 6-11
        4.2, 3.8, 3.2, 3.5, 4.5, 6.0,   # 12-17
        7.0, 7.5, 6.5, 5.0, 3.5, 2.0,   # 18-23
    ]
    return random.choices(range(24), weights=hour_weights)[0]

def rand_reg_date(cohort_idx):
    """
    Registration curve: slow start → acceleration.
    Later cohort months have slightly more 45-65 users (word-of-mouth).
    """
    total_days = (END - START).days
    # beta(1.4, 1.2) gives mild left-skew → earlier months slightly denser
    t = random.betavariate(1.4, 1.2)
    days = int(t * total_days)
    h = random.randint(7, 21)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return START + timedelta(days=days, hours=h, minutes=m, seconds=s)

def device_os(cohort):
    weights = {
        '18-30': [62, 38],
        '30-45': [56, 44],
        '45-65': [50, 50],
        '65+':   [44, 56],
    }
    return random.choices(['Android', 'iOS'], weights=weights[cohort])[0]

# ─── USERS ────────────────────────────────────────────────────────────────────
all_cohorts = []
for cohort, count in zip(AGE_COHORTS, AGE_COUNTS):
    all_cohorts.extend([cohort] * count)
random.shuffle(all_cohorts)

users_raw = []
for idx, cohort in enumerate(all_cohorts):
    reg = rand_reg_date(idx)
    os_ = device_os(cohort)
    if cohort in ('45-65', '65+'):
        nc = random.choices([1, 2, 3, 4], weights=[50, 30, 13, 7])[0]
    else:
        nc = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]
    sources = ['bulpay_balance'] + [f'card_{k}' for k in range(1, nc + 1)]
    users_raw.append({
        'reg': reg,
        'age_cohort': cohort,
        'device_os': os_,
        'num_linked_cards': nc,
        'default_payment_source': random.choice(sources),
    })

# Sort by registration date and assign IDs
users_raw.sort(key=lambda u: u['reg'])
USERS = []
for i, ur in enumerate(users_raw):
    USERS.append({
        'user_id':              f'u{i+1:03d}',
        'registered_at':        ur['reg'].strftime('%Y-%m-%dT%H:%M:%S'),
        'age_cohort':           ur['age_cohort'],
        'device_os':            ur['device_os'],
        'num_linked_cards':     ur['num_linked_cards'],
        'default_payment_source': ur['default_payment_source'],
    })

print(f"Users generated: {len(USERS)}")

# ─── SESSIONS ─────────────────────────────────────────────────────────────────
CORE_ACTIONS   = ['send', 'send', 'send', 'send', 'send', 'send', 'send',
                  'add_card', 'freeze_card', 'view_balance']

PAYMENT_TYPES  = ['p2p', 'bill_payment', 'merchant_grocery',
                  'merchant_retail', 'merchant_restaurant']
PT_WEIGHTS     = [45, 25, 15, 10, 5]

def num_sessions(cohort):
    # 45-65 and 65+ have slightly fewer but very focused sessions
    r = {
        '18-30': (8, 38),
        '30-45': (10, 42),
        '45-65': (6, 32),
        '65+':   (4, 22),
    }[cohort]
    return random.randint(*r)

def funnel_step():
    return random.choices([1,2,3,4,5,6], weights=[3,4,8,5,5,75])[0]

def duration(step):
    if step != 6:
        return ''
    b = random.choices([0,1,2,3,4], weights=[5,25,35,25,10])[0]
    ranges = [(3,10),(11,30),(31,60),(61,120),(121,350)]
    return random.randint(*ranges[b])

SESSIONS = []
sid = 1

for user in USERS:
    uid     = user['user_id']
    cohort  = user['age_cohort']
    reg_dt  = datetime.strptime(user['registered_at'], '%Y-%m-%dT%H:%M:%S')
    nc      = int(user['num_linked_cards'])
    sources = ['bulpay_balance'] + [f'card_{k}' for k in range(1, nc + 1)]

    period_days = max(1, (END - reg_dt).days)
    n_sess = num_sessions(cohort)

    # Build time offsets (spread over user's lifetime, no duplicates within a minute)
    offsets_used = set()
    first = True
    for _ in range(n_sess):
        for attempt in range(20):   # retry if collision
            od = random.randint(0, period_days)
            oh = rand_hour()
            om = random.randint(0, 59)
            os_s = random.randint(0, 59)
            key = (od, oh, om)
            if key not in offsets_used:
                offsets_used.add(key)
                break

        sdt = reg_dt + timedelta(days=od)
        sdt = sdt.replace(hour=oh, minute=om, second=os_s)
        if sdt < reg_dt:
            sdt = reg_dt + timedelta(minutes=random.randint(15, 600))
        if sdt > END:
            sdt = END - timedelta(hours=random.randint(1, 24))

        dow = DAYS_ORDER[sdt.weekday()]
        action = random.choice(CORE_ACTIONS)

        pt    = ''
        step  = ''
        amt   = ''
        dur   = ''
        pin   = ''

        if action == 'send':
            pt   = random.choices(PAYMENT_TYPES, weights=PT_WEIGHTS)[0]
            step = funnel_step()
            if step >= 3:
                if cohort in ('45-65', '65+'):
                    amt = round(random.uniform(20, 250), 2)
                else:
                    amt = round(random.uniform(10, 160), 2)
            dur = duration(step)
            if step >= 5:
                pin = random.choices([1, 2, 3], weights=[80, 15, 5])[0]

        src     = random.choice(sources)
        # Switching probability
        sw_w = {'18-30':[20,80], '30-45':[18,82], '45-65':[12,88], '65+':[8,92]}[cohort]
        switched = random.choices(['true','false'], weights=sw_w)[0]
        tech     = random.choices(['true','false'], weights=[97, 3])[0]

        SESSIONS.append({
            'session_id':               f's{sid:04d}',
            'user_id':                  uid,
            'started_at':               sdt.strftime('%Y-%m-%dT%H:%M:%S'),
            'hour_of_day':              sdt.hour,
            'day_of_week':              dow,
            'is_first_session':         'true' if first else 'false',
            'core_action_performed':    action,
            'payment_type':             pt,
            'funnel_step_reached':      step,
            'amount_eur':               amt,
            'payment_duration_seconds': dur,
            'pin_attempts':             pin,
            'payment_source':           src,
            'switched_source':          switched,
            'technical_success':        tech,
        })
        sid += 1
        first = False

# Sort by date and re-ID
SESSIONS.sort(key=lambda s: s['started_at'])
for i, s in enumerate(SESSIONS):
    s['session_id'] = f's{i+1:04d}'

print(f"Sessions generated: {len(SESSIONS)}")

# ─── BALANCES ─────────────────────────────────────────────────────────────────
BALANCES = []

for user in USERS:
    uid    = user['user_id']
    cohort = user['age_cohort']
    reg_dt = datetime.strptime(user['registered_at'], '%Y-%m-%dT%H:%M:%S')

    # Starting balance and monthly growth vary by age cohort
    params = {
        '18-30': (5,  50,  5, 22),
        '30-45': (20, 110, 8, 40),
        '45-65': (50, 220, 12, 65),
        '65+':   (40, 170, 10, 55),
    }[cohort]
    bal = round(random.uniform(params[0], params[1]), 2)
    monthly_base = random.uniform(params[2], params[3])

    # Start from first day of registration month
    cur_month = datetime(reg_dt.year, reg_dt.month, 1)
    while cur_month <= datetime(2026, 3, 1):
        ym = cur_month.strftime('%Y-%m')
        BALANCES.append({
            'user_id':    uid,
            'year_month': ym,
            'balance_eur': round(bal, 2),
        })
        variation = random.uniform(-0.2, 0.55)
        bal = max(0.5, bal + monthly_base * (1 + variation))
        cur_month = next_month(cur_month)

print(f"Balance records: {len(BALANCES)}")

# ─── WRITE CSV ─────────────────────────────────────────────────────────────────
def write_csv(path, rows, fields):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

write_csv('bulpay_users.csv', USERS,
    ['user_id','registered_at','age_cohort','device_os',
     'num_linked_cards','default_payment_source'])

write_csv('bulpay_sessions.csv', SESSIONS,
    ['session_id','user_id','started_at','hour_of_day','day_of_week',
     'is_first_session','core_action_performed','payment_type',
     'funnel_step_reached','amount_eur','payment_duration_seconds',
     'pin_attempts','payment_source','switched_source','technical_success'])

write_csv('bulpay_balances.csv', BALANCES,
    ['user_id','year_month','balance_eur'])

print("✓ All CSV files written.")

# Quick stats
from collections import Counter
cohort_counts = Counter(u['age_cohort'] for u in USERS)
os_counts     = Counter(u['device_os'] for u in USERS)
pt_counts     = Counter(s['payment_type'] for s in SESSIONS if s['payment_type'])
print("\nAge cohort distribution:", dict(cohort_counts))
print("Device OS distribution:", dict(os_counts))
print("Payment type distribution:", dict(pt_counts))
