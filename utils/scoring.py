def calculate_risk(sleep_hours, stress_level, sleep_quality,
                   work_study_hours=0, physical_activity=50,
                   social_support=5, enjoy_activities=5,
                   feel_hopeless=False, stress_temporary=True,
                   anxiety=False, depression_hist=False,
                   family_history=False, dietary_habits="Moderate",
                   suicidal_thoughts=False):

    score = 0
    factors = []

    # ── SLEEP HOURS ──────────────────────────────────
    # Good sleep alone doesn't mean low risk
    # Bad sleep alone doesn't mean high risk
    if sleep_hours < 4:
        score += 3
        factors.append("🔴 Very low sleep ({:.1f}h) — consistent lack of sleep affects mental health".format(sleep_hours))
    elif sleep_hours < 5.5:
        score += 2
        factors.append("🟠 Low sleep ({:.1f}h) — try to improve gradually".format(sleep_hours))
    elif sleep_hours < 6.5:
        score += 1
        factors.append("🟡 Slightly low sleep ({:.1f}h) — not critical but worth improving".format(sleep_hours))
    elif sleep_hours > 10:
        score += 1
        factors.append("🟡 Oversleeping ({:.1f}h) — too much sleep can also indicate low mood".format(sleep_hours))
    else:
        factors.append("🟢 Sleep hours are healthy ({:.1f}h)".format(sleep_hours))

    # ── STRESS LEVEL ─────────────────────────────────
    # Stress alone is normal — everyone has stress
    # Only counts if combined with other factors
    if stress_level >= 8:
        if stress_temporary:
            score += 1  # Temporary high stress is manageable
            factors.append("🟡 High stress ({}/10) but temporary — manageable with support".format(stress_level))
        else:
            score += 3  # Chronic high stress is serious
            factors.append("🔴 Chronic high stress ({}/10) — ongoing for long time, major concern".format(stress_level))
    elif stress_level >= 6:
        if stress_temporary:
            score += 0  # Moderate temporary stress is normal
            factors.append("🟢 Moderate stress ({}/10) — normal for busy periods, temporary".format(stress_level))
        else:
            score += 2
            factors.append("🟠 Ongoing moderate stress ({}/10) — has been lasting a while".format(stress_level))
    elif stress_level >= 4:
        score += 0
        factors.append("🟢 Low-moderate stress ({}/10) — within normal range".format(stress_level))
    else:
        score += 0
        factors.append("🟢 Stress is well managed ({}/10)".format(stress_level))

    # ── SOCIAL SUPPORT ───────────────────────────────
    # This is the BIGGEST protective factor
    # Strong support can offset many other risks
    if social_support <= 2:
        score += 4
        factors.append("🔴 Very low social support — feeling isolated is one of the biggest risk factors")
    elif social_support <= 4:
        score += 2
        factors.append("🟠 Low social support — having someone to talk to makes a big difference")
    elif social_support <= 6:
        score += 0
        factors.append("🟡 Moderate social support — could be stronger but not a concern")
    else:
        score -= 1  # Strong support REDUCES risk
        factors.append("🟢 Strong social support — this significantly protects your mental health")

    # ── ENJOYMENT OF ACTIVITIES ───────────────────────
    # Loss of interest/pleasure is a key depression indicator
    if enjoy_activities <= 2:
        score += 3
        factors.append("🔴 Lost interest in most activities — this is a significant warning sign")
    elif enjoy_activities <= 4:
        score += 2
        factors.append("🟠 Reduced enjoyment in activities — worth paying attention to")
    elif enjoy_activities <= 6:
        score += 0
        factors.append("🟡 Moderate enjoyment — some days better than others, which is normal")
    else:
        score -= 1  # Still enjoying life REDUCES risk
        factors.append("🟢 Still enjoying activities — this is a strong positive sign")

    # ── HOPELESSNESS ─────────────────────────────────
    # Feeling hopeless is one of the strongest risk indicators
    if feel_hopeless:
        score += 4
        factors.append("🔴 Feeling hopeless about future — this is the most important factor to address")
    else:
        score -= 1
        factors.append("🟢 Not feeling hopeless — positive outlook is very protective")

    # ── WORK/STUDY HOURS ──────────────────────────────
    # Only a risk if combined with stress and no recovery time
    if work_study_hours > 12:
        score += 2
        factors.append("🔴 Very high work/study hours ({}h) — leaves no time for recovery".format(int(work_study_hours)))
    elif work_study_hours > 9:
        score += 1
        factors.append("🟠 High work/study hours ({}h) — make sure to take breaks".format(int(work_study_hours)))
    else:
        factors.append("🟢 Work/study hours are balanced ({}h)".format(int(work_study_hours)))

    # ── PHYSICAL ACTIVITY ─────────────────────────────
    # Exercise is protective — lack of it adds small risk
    if physical_activity < 20:
        score += 2
        factors.append("🔴 Very low physical activity — exercise is one of the best natural stress relievers")
    elif physical_activity < 40:
        score += 1
        factors.append("🟠 Low physical activity — even a short daily walk helps significantly")
    elif physical_activity >= 70:
        score -= 1  # High activity REDUCES risk
        factors.append("🟢 High physical activity — great protective factor for mental health")
    else:
        factors.append("🟢 Moderate physical activity — keep it up")

    # ── MENTAL HEALTH HISTORY ────────────────────────
    if depression_hist:
        score += 2
        factors.append("🟠 History of depression — past episodes can recur, worth monitoring")
    if anxiety:
        score += 1
        factors.append("🟠 Anxiety present — manageable with right support and techniques")
    if suicidal_thoughts:
        score += 4
        factors.append("🔴 History of suicidal thoughts — please speak to a professional")
    if family_history:
        score += 1
        factors.append("🟡 Family history of mental illness — slight genetic predisposition")

    # ── DIETARY HABITS ───────────────────────────────
    if dietary_habits == "Unhealthy":
        score += 1
        factors.append("🟡 Unhealthy diet — nutrition directly affects mood and energy")
    elif dietary_habits == "Healthy":
        score -= 1
        factors.append("🟢 Healthy diet — good nutrition supports mental wellbeing")

    # ── SLEEP QUALITY ────────────────────────────────
    # Quality matters more than quantity sometimes
    if sleep_quality <= 3:
        score += 2
        factors.append("🔴 Very poor sleep quality — waking up unrefreshed affects everything")
    elif sleep_quality <= 5:
        score += 1
        factors.append("🟠 Below average sleep quality — try improving sleep environment")
    elif sleep_quality >= 8:
        score -= 1
        factors.append("🟢 Great sleep quality — waking up refreshed is very important")
    else:
        factors.append("🟢 Decent sleep quality")

    # ── MINIMUM SCORE ────────────────────────────────
    # Score can't go below 0
    score = max(0, score)

    # ── REALISTIC RISK LEVELS ────────────────────────
    # Thresholds are higher now — not easy to hit High
    if score >= 10:
        risk_level = "High"
    elif score >= 5:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # Sort factors — most critical first
    factors_sorted = (
        [f for f in factors if "🔴" in f] +
        [f for f in factors if "🟠" in f] +
        [f for f in factors if "🟡" in f] +
        [f for f in factors if "🟢" in f]
    )

    return score, risk_level, factors_sorted
