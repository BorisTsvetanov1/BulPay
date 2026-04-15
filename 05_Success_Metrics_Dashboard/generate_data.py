"""
BulPay Dashboard Data Generator v2
Realistic simulated data for a fintech product showing healthy growth
over 2 years (Apr 2024 – Mar 2026).

~750 users, ~16k sessions, monthly balances and ops data.
Growth narrative: slow early traction → accelerating adoption driven
by word-of-mouth in the 45-65 primary demographic.
"""
import csv
import random
import math
from datetime import datetime, timedelta
from collections import Counter, defaultdict

random.seed(42)

# ── Constants ─────────────────────────────────────────────────────────────────
START = datetime(2024, 4, 1)
END   = datetime(2026, 3, 31, 23, 59, 59)

MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
DAYS_ORDER  = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

AGE_COHORTS = ['18-30', '30-45', '45-65', '65+']

# S-curve monthly registration targets (healthy, accelerating growth)
MONTHLY_REGS = [
    10, 12, 14, 16, 15, 18, 22, 25, 20,   # Apr 2024 – Dec 2024
    28, 30, 33, 36, 38, 40, 38, 36, 42,   # Jan 2025 – Sep 2025
    46, 50, 42, 52, 55, 58,               # Oct 2025 – Mar 2026
]

TIERS = ['power', 'regular', 'casual', 'dormant', 'churned']

TIER_WEIGHTS = {
    '18-30': [14, 24, 30, 17, 15],
    '30-45': [13, 33, 33, 13, 8],
    '45-65': [12, 37, 36, 10, 5],
    '65+':   [8,  28, 35, 18, 11],
}

PAYMENT_TYPES  = ['p2p', 'bill_payment', 'merchant_grocery',
                  'merchant_retail', 'merchant_restaurant']
PT_WEIGHTS     = [42, 25, 17, 11, 5]

AMOUNT_RANGES = {
    'p2p':                 (10, 200),
    'bill_payment':        (20, 150),
    'merchant_grocery':    (15, 80),
    'merchant_retail':     (20, 300),
    'merchant_restaurant': (10, 60),
}

CHANNELS = ['referral', 'organic', 'paid', 'app_store']

# ── Utility functions ─────────────────────────────────────────────────────────

def next_month(dt):
    return datetime(dt.year + (1 if dt.month == 12 else 0),
                    (dt.month % 12) + 1, 1)

def lerp(a, b, t):
    return a + (b - a) * min(1, max(0, t))

def rand_dt_in_range(lo, hi):
    delta = (hi - lo).total_seconds()
    if delta <= 0:
        return lo
    return lo + timedelta(seconds=random.uniform(0, delta))

def rand_hour():
    weights = [
        0.3, 0.2, 0.1, 0.1, 0.2, 0.5,   # 0-5   night
        1.0, 3.0, 4.5, 3.8, 3.5, 3.8,   # 6-11  morning
        4.2, 3.8, 3.2, 3.5, 4.5, 6.0,   # 12-17 afternoon
        7.0, 7.5, 6.5, 5.0, 3.5, 2.0,   # 18-23 evening
    ]
    return random.choices(range(24), weights=weights)[0]

# ═══════════════════════════════════════════════════════════════════════════════
#  1. USERS
# ═══════════════════════════════════════════════════════════════════════════════

def _age_weights(month_idx):
    """45-65 share grows from ~36% to ~46% via word-of-mouth."""
    t = month_idx / 23
    w4565 = 0.36 + 0.10 * t
    rem   = 1 - w4565
    return [rem * 0.33, rem * 0.35, w4565, rem * 0.32]

def _channel_weights(cohort, t):
    early = {'18-30': [18,35,32,15], '30-45': [30,30,28,12],
             '45-65': [42,30,18,10], '65+':   [45,28,17,10]}
    late  = {'18-30': [28,32,27,13], '30-45': [40,28,22,10],
             '45-65': [58,24,12,6],  '65+':   [60,22,12,6]}
    return [lerp(e, l, t) for e, l in zip(early[cohort], late[cohort])]

def generate_users():
    users = []
    idx = 1

    for mi, target in enumerate(MONTHLY_REGS):
        y = 2024 + (3 + mi) // 12
        m = (3 + mi) % 12 + 1
        ms = datetime(y, m, 1)
        me = next_month(ms) - timedelta(seconds=1)
        t  = mi / 23

        count = target + random.randint(-2, 2)
        count = max(5, count)
        aw = _age_weights(mi)

        for _ in range(count):
            cohort = random.choices(AGE_COHORTS, weights=aw)[0]

            os_w = {'18-30':[62,38],'30-45':[55,45],
                    '45-65':[48,52],'65+':[42,58]}[cohort]
            device = random.choices(['Android', 'iOS'], weights=os_w)[0]

            if cohort in ('45-65', '65+'):
                nc = random.choices([1,2,3,4], weights=[48,32,14,6])[0]
            else:
                nc = random.choices([1,2,3,4], weights=[38,30,22,10])[0]
            sources = ['bulpay_balance'] + [f'card_{k}' for k in range(1, nc+1)]

            channel = random.choices(CHANNELS, weights=_channel_weights(cohort, t))[0]

            tw = list(TIER_WEIGHTS[cohort])
            if t > 0.4 and random.random() < 0.12:
                tw[3] -= 3; tw[1] += 3
            if t > 0.6 and random.random() < 0.18:
                tw[4] -= 3; tw[2] += 3
            tier = random.choices(TIERS, weights=tw)[0]

            reg_dt = rand_dt_in_range(ms, me)
            users.append({
                'user_id': f'u{idx:04d}',
                'registered_at': reg_dt.strftime('%Y-%m-%dT%H:%M:%S'),
                'age_cohort': cohort,
                'device_os': device,
                'num_linked_cards': nc,
                'default_payment_source': random.choice(sources),
                'acquisition_channel': channel,
                '_tier': tier,
                '_mi': mi,
                '_reg_dt': reg_dt,
            })
            idx += 1

    users.sort(key=lambda u: u['_reg_dt'])
    for i, u in enumerate(users):
        u['user_id'] = f'u{i+1:04d}'
    return users


# ═══════════════════════════════════════════════════════════════════════════════
#  2. SESSIONS
# ═══════════════════════════════════════════════════════════════════════════════

# First-login delay (hours) cumulative probability by tier
_FLD = {
    'power':   [(2, 0.55), (8, 0.80), (24, 0.96), (72, 1.0)],
    'regular': [(4, 0.30), (12, 0.52), (24, 0.72), (72, 0.90), (168, 0.98), (720, 1.0)],
    'casual':  [(6, 0.18), (24, 0.42), (72, 0.68), (168, 0.88), (720, 1.0)],
    'dormant': [(12, 0.12), (24, 0.28), (72, 0.50), (168, 0.72), (720, 1.0)],
    'churned': [(12, 0.20), (24, 0.42), (72, 0.65), (168, 0.85), (720, 1.0)],
}

def _first_login_hours(tier, product_t):
    """Delay in hours; later cohorts activate faster due to better onboarding."""
    r = random.random()
    bonus = product_t * 0.10
    r = min(r + bonus, 0.9999)
    bands = _FLD[tier]
    prev_h, prev_p = 0, 0
    for h, p in bands:
        if r <= p:
            frac = (r - prev_p) / (p - prev_p) if p > prev_p else 0
            return prev_h + frac * (h - prev_h)
        prev_h, prev_p = h, p
    return bands[-1][0]

SESS_PER_MONTH = {
    'power':   (3, 8),
    'regular': (2, 4),
    'casual':  (0, 2),
    'dormant': (0, 1),
    'churned': (1, 3),
}

ACTION_W = {
    'power':   [62, 24, 10, 4],
    'regular': [53, 30, 13, 4],
    'casual':  [40, 40, 15, 5],
    'dormant': [30, 50, 15, 5],
    'churned': [45, 35, 15, 5],
}
ACTIONS = ['send', 'view_balance', 'add_card', 'freeze_card']


def generate_sessions(users):
    sessions = []
    sid = 1

    reg_dates = {u['user_id']: u['_reg_dt'] for u in users}
    all_uids  = [u['user_id'] for u in users]

    for u in users:
        uid    = u['user_id']
        reg    = u['_reg_dt']
        tier   = u['_tier']
        cohort = u['age_cohort']
        mi     = u['_mi']
        t      = mi / 23
        nc     = int(u['num_linked_cards'])
        sources = ['bulpay_balance'] + [f'card_{k}' for k in range(1, nc+1)]

        churn_after = None
        if tier == 'churned':
            churn_after = random.randint(1, 4)

        delay_h    = _first_login_hours(tier, t)
        first_dt   = reg + timedelta(hours=delay_h)
        if first_dt > END:
            first_dt = reg + timedelta(minutes=random.randint(30, 240))

        user_sess_dts = [first_dt]

        cur = datetime(reg.year, reg.month, 1)
        months_active = 0
        while cur <= datetime(2026, 3, 1):
            ms = max(cur, reg)
            me = min(next_month(cur), END + timedelta(seconds=1))
            if ms >= me:
                cur = next_month(cur); months_active += 1; continue

            if tier == 'churned' and churn_after and months_active > churn_after:
                cur = next_month(cur); months_active += 1; continue
            if tier == 'dormant' and months_active > 0 and random.random() < 0.45:
                cur = next_month(cur); months_active += 1; continue

            lo, hi = SESS_PER_MONTH[tier]
            bonus  = int(t * 1.5)
            n = random.randint(lo, hi) + bonus

            if months_active == 0:
                frac = max(0.15, (me - first_dt).total_seconds() /
                           (me - ms).total_seconds()) if (me - ms).total_seconds() > 0 else 0.15
                n = max(0, int(n * frac))

            for _ in range(n):
                sd = rand_dt_in_range(max(ms, first_dt + timedelta(minutes=30)), me)
                if sd <= first_dt or sd > END:
                    continue
                user_sess_dts.append(sd)

            cur = next_month(cur)
            months_active += 1

        user_sess_dts.sort()

        for si, sdt in enumerate(user_sess_dts):
            is_first = (si == 0)
            dow = DAYS_ORDER[sdt.weekday()]

            if is_first:
                action = random.choices(
                    ['view_balance', 'send', 'add_card'], weights=[35, 45, 20])[0]
            else:
                action = random.choices(ACTIONS, weights=ACTION_W[tier])[0]

            pt = ''; step = ''; amt = ''; dur = ''; pin = ''; recip = ''

            if action == 'send':
                pt = random.choices(PAYMENT_TYPES, weights=PT_WEIGHTS)[0]

                completion = 0.62 + t * 0.18
                if random.random() < completion:
                    step = 6
                else:
                    step = random.choices([1,2,3,4,5],
                                          weights=[6,8,25,32,29])[0]

                if step >= 3:
                    lo_a, hi_a = AMOUNT_RANGES[pt]
                    if cohort in ('45-65', '65+'):
                        lo_a *= 1.3; hi_a *= 1.4
                    amt = round(random.uniform(lo_a, hi_a), 2)
                    if random.random() < 0.018:
                        amt = round(random.uniform(500, 2500), 2)

                if step == 6:
                    base_dur = lerp(48, 20, t)
                    dur = max(4, int(random.gauss(base_dur, base_dur * 0.35)))
                    dur = min(dur, 360)

                if step and int(step) >= 5:
                    pin = random.choices([1,2,3], weights=[83,13,4])[0]

                if step == 6 and pt == 'p2p':
                    eligible = [x for x in all_uids
                                if x != uid and reg_dates[x] < sdt]
                    if eligible:
                        recip = random.choice(eligible)

            src = random.choice(sources)
            sw_w = {'18-30':[20,80],'30-45':[18,82],
                    '45-65':[12,88],'65+':[8,92]}[cohort]
            switched = random.choices(['true','false'], weights=sw_w)[0]
            tech = 'true' if random.random() < lerp(0.955, 0.993, t) else 'false'

            sessions.append({
                'session_id': f's{sid:05d}',
                'user_id':    uid,
                'started_at': sdt.strftime('%Y-%m-%dT%H:%M:%S'),
                'hour_of_day': sdt.hour,
                'day_of_week': dow,
                'is_first_session': 'true' if is_first else 'false',
                'core_action_performed': action,
                'payment_type':             pt,
                'funnel_step_reached':      step,
                'amount_eur':               amt,
                'payment_duration_seconds': dur,
                'pin_attempts':             pin,
                'payment_source':           src,
                'switched_source':          switched,
                'technical_success':        tech,
                'recipient_user_id':        recip,
            })
            sid += 1

    sessions.sort(key=lambda s: s['started_at'])
    for i, s in enumerate(sessions):
        s['session_id'] = f's{i+1:05d}'
    return sessions


# ═══════════════════════════════════════════════════════════════════════════════
#  3. BALANCES
# ═══════════════════════════════════════════════════════════════════════════════

_BAL_INIT = {
    'power':   {'18-30':(30,150),'30-45':(80,300),'45-65':(120,500),'65+':(100,400)},
    'regular': {'18-30':(15,80), '30-45':(40,180),'45-65':(60,250), '65+':(50,200)},
    'casual':  {'18-30':(5,40),  '30-45':(15,80), '45-65':(30,120), '65+':(20,90)},
    'dormant': {'18-30':(5,20),  '30-45':(10,40), '45-65':(15,60),  '65+':(10,40)},
    'churned': {'18-30':(5,30),  '30-45':(10,50), '45-65':(15,70),  '65+':(10,40)},
}
_BAL_GROWTH = {
    'power':(0.06,0.18), 'regular':(0.03,0.10),
    'casual':(0.01,0.05), 'dormant':(-0.02,0.02), 'churned':(-0.04,0.01),
}

def generate_balances(users, sessions):
    sess_activity = defaultdict(lambda: defaultdict(int))
    for s in sessions:
        d = datetime.strptime(s['started_at'], '%Y-%m-%dT%H:%M:%S')
        sess_activity[s['user_id']][f'{d.year}-{d.month:02d}'] += 1

    balances = []
    for u in users:
        uid    = u['user_id']
        tier   = u['_tier']
        cohort = u['age_cohort']
        reg    = u['_reg_dt']

        lo, hi = _BAL_INIT[tier][cohort]
        bal = round(random.uniform(lo, hi), 2)
        if tier == 'power' and random.random() < 0.025:
            bal = round(random.uniform(2000, 8000), 2)

        glo, ghi = _BAL_GROWTH[tier]
        base_g   = random.uniform(glo, ghi)

        cur = datetime(reg.year, reg.month, 1)
        is_gone = False
        while cur <= datetime(2026, 3, 1):
            ym = f'{cur.year}-{cur.month:02d}'
            act = sess_activity[uid].get(ym, 0)

            if act == 0 and is_gone:
                bal = max(0, bal * random.uniform(0.55, 0.82))
            elif act == 0 and cur > datetime(reg.year, reg.month, 1):
                bal = max(0, bal * random.uniform(0.90, 1.02))
                if tier == 'churned':
                    is_gone = True
            else:
                mg = base_g + random.uniform(-0.03, 0.04)
                bal = max(0.5, bal * (1 + mg))
                if act >= 4 and random.random() < 0.18:
                    bal += random.uniform(40, 350)

            balances.append({
                'user_id': uid,
                'year_month': ym,
                'balance_eur': round(bal, 2),
            })
            cur = next_month(cur)
    return balances


# ═══════════════════════════════════════════════════════════════════════════════
#  4. OPS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_ops(users):
    reg_by_month = defaultdict(int)
    for u in users:
        rd = u['_reg_dt']
        reg_by_month[f'{rd.year}-{rd.month:02d}'] += 1

    ops = []
    cur = datetime(2024, 4, 1)
    mi = 0
    while cur <= datetime(2026, 3, 1):
        ym = f'{cur.year}-{cur.month:02d}'
        t  = mi / 23

        approved = reg_by_month.get(ym, 0)
        kp = lerp(0.72, 0.85, t) + random.uniform(-0.012, 0.012)
        kp = min(max(kp, 0.70), 0.87)
        started  = round(approved / kp) if kp > 0 else approved
        ik = lerp(0.78, 0.86, t) + random.uniform(-0.02, 0.02)
        installs = round(started / ik)

        cr = 3.5 * (1 - t * 0.83) + random.uniform(-0.12, 0.12)
        if mi == 6:                        # Oct 2024 bad deploy
            cr += 1.1
        cr = round(max(cr, 0.40), 2)

        up = lerp(98.0, 99.85, t) + random.uniform(-0.10, 0.08)
        if mi == 6:
            up -= 0.70
        up = round(min(max(up, 97.0), 99.97), 2)

        inc = 0
        if mi == 3:  inc = 1               # early compliance finding
        if mi == 14: inc = 1               # annual audit item

        ops.append({
            'year_month': ym,
            'app_installs': installs,
            'kyc_started':  started,
            'kyc_approved': approved,
            'crash_rate_per_1000':  cr,
            'uptime_pct':           up,
            'regulatory_incidents': inc,
        })
        cur = next_month(cur)
        mi += 1
    return ops


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

print("Generating users …")
USERS = generate_users()
print(f"  Users: {len(USERS)}")

print("Generating sessions …")
SESSIONS = generate_sessions(USERS)
print(f"  Sessions: {len(SESSIONS)}")

print("Generating balances …")
BALANCES = generate_balances(USERS, SESSIONS)
print(f"  Balance records: {len(BALANCES)}")

print("Generating ops …")
OPS = generate_ops(USERS)
print(f"  Ops records: {len(OPS)}")

# ── Write CSV ─────────────────────────────────────────────────────────────────

def write_csv(path, rows, fields):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)

write_csv('bulpay_users.csv', USERS,
    ['user_id','registered_at','age_cohort','device_os',
     'num_linked_cards','default_payment_source','acquisition_channel'])

write_csv('bulpay_sessions.csv', SESSIONS,
    ['session_id','user_id','started_at','hour_of_day','day_of_week',
     'is_first_session','core_action_performed','payment_type',
     'funnel_step_reached','amount_eur','payment_duration_seconds',
     'pin_attempts','payment_source','switched_source','technical_success',
     'recipient_user_id'])

write_csv('bulpay_balances.csv', BALANCES,
    ['user_id','year_month','balance_eur'])

write_csv('bulpay_ops.csv', OPS,
    ['year_month','app_installs','kyc_started','kyc_approved',
     'crash_rate_per_1000','uptime_pct','regulatory_incidents'])

print("\n✓ All CSV files written.")

# ── Diagnostics ───────────────────────────────────────────────────────────────

print(f"\nAge cohorts:   {dict(Counter(u['age_cohort'] for u in USERS))}")
print(f"Device OS:     {dict(Counter(u['device_os'] for u in USERS))}")
print(f"Tiers:         {dict(Counter(u['_tier'] for u in USERS))}")
print(f"Channels:      {dict(Counter(u['acquisition_channel'] for u in USERS))}")

first_by_user = {}
for s in SESSIONS:
    if s['user_id'] not in first_by_user:
        first_by_user[s['user_id']] = datetime.strptime(s['started_at'],
                                                         '%Y-%m-%dT%H:%M:%S')
n = len(USERS)
w24 = sum(1 for u in USERS
          if u['user_id'] in first_by_user
          and (first_by_user[u['user_id']] - u['_reg_dt'])
              .total_seconds() <= 86400)
w72 = sum(1 for u in USERS
          if u['user_id'] in first_by_user
          and (first_by_user[u['user_id']] - u['_reg_dt'])
              .total_seconds() <= 259200)
w7d = sum(1 for u in USERS
          if u['user_id'] in first_by_user
          and (first_by_user[u['user_id']] - u['_reg_dt'])
              .total_seconds() <= 604800)

print(f"\nActivation:")
print(f"  Login ≤24 h: {w24}/{n} ({w24/n*100:.1f}%)")
print(f"  Login ≤72 h: {w72}/{n} ({w72/n*100:.1f}%)")
print(f"  Login ≤ 7 d: {w7d}/{n} ({w7d/n*100:.1f}%)")
