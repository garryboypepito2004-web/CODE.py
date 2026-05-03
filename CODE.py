import streamlit as st
import smtplib
import pandas as pd
from datetime import datetime
from email.message import EmailMessage

# ═════════════════ SYSTEM SETTINGS ═════════════════
SENDER_EMAIL = "garryboypepito71@gmail.com"
SENDER_PASSWORD = "fhyv cimp gync wjmj" 
# ══════════════════════════════════════════════════

st.set_page_config(page_title="AILYN PRO V5.4", layout="centered")

# --- EMERALD GLASS UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    .stApp { 
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center; background-attachment: fixed; 
    }
    [data-testid="stVerticalBlock"] > div > [data-testid="stVerticalBlock"] { 
        background: rgba(16, 45, 30, 0.25) !important; 
        backdrop-filter: blur(25px) saturate(180%); border-radius: 40px; padding: 45px;
        border: 1px solid rgba(52, 211, 153, 0.25) !important; 
        max-width: 950px; margin: auto;
    }
    .stats-container { 
        display: flex; justify-content: space-between; 
        background: rgba(255, 255, 255, 0.04); 
        padding: 40px 50px; border-radius: 35px; 
        margin-bottom: 35px; border: 1px solid rgba(52, 211, 153, 0.2);
        min-height: 180px; align-items: center;
    }
    .stat-label { font-size: 11px; color: #34d399; letter-spacing: 4px; font-weight: 700; text-transform: uppercase; }
    .stat-value { font-weight: 900; font-size: 30px; font-family: 'Inter', sans-serif; }
    .stButton>button { 
        background: rgba(52, 211, 153, 0.1) !important; color: #34d399 !important; 
        border: 1px solid rgba(52, 211, 153, 0.4) !important;
        height: 55px !important; border-radius: 15px !important;
        font-size: 13px !important; letter-spacing: 2px !important; font-weight: 900 !important;
        transition: 0.15s ease-in-out;
    }
    .stButton>button:hover { background: rgba(52, 211, 153, 0.25) !important; border: 1px solid #34d399 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION INITIALIZATION ---
if 'access' not in st.session_state: st.session_state.access = False
if 'records' not in st.session_state: st.session_state.records = []
if 'budget' not in st.session_state: st.session_state.budget = 0.0
if 'mode' not in st.session_state: st.session_state.mode = "menu"
if 'emails' not in st.session_state: 
    st.session_state.emails = ["garryboypepito2004@gmail.com", "ailyn_peps0678@yahoo.com"]

def get_bal_ui(val):
    abs_v = abs(val)
    if val > 0: return f"₱ {abs_v:,.2f}", "#34d399"
    if val < 0: return f"- ₱ {abs_v:,.2f}", "#ff4b4b"
    return f"₱ {abs_v:,.2f}", "#ffffff"

def send_report():
    spent = sum(r['Total'] for r in st.session_state.records)
    bal = st.session_state.budget - spent
    b_txt, b_col = get_bal_ui(bal)
    today = datetime.now().strftime('%Y-%m-%d')
    
    msg = EmailMessage()
    msg["Subject"] = f"AILYN CONSTRUCTION RECEIPT: {datetime.now().strftime('%b %d, %Y')}"
    msg["From"] = f"AILYN PRO SYSTEM <{SENDER_EMAIL}>"
    msg["To"] = ", ".join(st.session_state.emails)
    
    # Matching the Photo Layout exactly
    rows = "".join([f"""
        <tr>
            <td style='padding:12px; border-bottom:1px solid #eee; font-size:12px;'>{today}</td>
            <td style='padding:12px; border-bottom:1px solid #eee; font-size:12px; text-align:center;'>1</td>
            <td style='padding:12px; border-bottom:1px solid #eee; font-size:12px; color:#1a5d2a; font-weight:bold;'>[{r['Category']}] {r['Description']}</td>
            <td style='padding:12px; border-bottom:1px solid #eee; font-size:12px; text-align:right;'>{r['Total']:,.2f}</td>
            <td style='padding:12px; border-bottom:1px solid #eee; font-size:12px; text-align:right; font-weight:bold;'>PHP {r['Total']:,.2f}</td>
        </tr>
    """ for r in st.session_state.records])
    
    html = f"""
    <div style="background-color: #e9ecef; padding: 40px; font-family: 'Helvetica', sans-serif;">
        <div style="max-width: 800px; margin: auto; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            <!-- Header -->
            <div style="background-color: #215423; color: white; padding: 40px 20px; text-align: center;">
                <h1 style="margin: 0; font-size: 32px; letter-spacing: 2px;">AILYN CONSTRUCTION</h1>
                <p style="margin: 10px 0 0; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Official Inventory System</p>
            </div>
            
            <!-- Table Container -->
            <div style="padding: 30px;">
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <thead>
                        <tr style="border-bottom: 2px solid #215423; text-transform: uppercase; font-size: 10px; color: #666;">
                            <th style="text-align: left; padding: 10px;">Date</th>
                            <th style="text-align: center; padding: 10px;">Qty</th>
                            <th style="text-align: left; padding: 10px;">Description</th>
                            <th style="text-align: right; padding: 10px;">Price</th>
                            <th style="text-align: right; padding: 10px;">Total</th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>

                <!-- Summary Box -->
                <div style="float: right; width: 300px; background-color: #1a3d20; color: white; border-radius: 6px; padding: 20px; margin-top: 20px;">
                    <p style="margin: 0; font-size: 12px;">Material Total: PHP {spent:,.2f}</p>
                    <p style="margin: 5px 0 10px; font-size: 12px;">Allocation: PHP {st.session_state.budget:,.2f}</p>
                    <div style="border-top: 1px dotted #ffffff; padding-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 18px; font-weight: bold;">BALANCE:</span>
                        <span style="font-size: 18px; font-weight: bold;">PHP {bal:,.2f}</span>
                    </div>
                </div>
                <div style="clear: both;"></div>

                <!-- Greeting Footer -->
                <div style="text-align: center; margin-top: 50px; color: #215423; font-weight: bold; font-size: 13px; text-transform: uppercase;">
                    THANK YOU FOR YOUR TIME TO SEE THIS EMAIL TAYLIN ❤️
                </div>
            </div>
        </div>
    </div>
    """
    msg.add_alternative(html, subtype="html")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(SENDER_EMAIL, SENDER_PASSWORD)
            s.send_message(msg)
        st.success("✅ RECEIPT SENT TO BOTH EMAILS")
    except Exception as e: st.error(f"Error: {e}")

# --- LOGIN SCREEN ---
if not st.session_state.access:
    st.markdown("<h1 style='text-align:center; color:#34d399; margin-top:150px; letter-spacing:15px; font-weight:900;'>AILYN</h1>", unsafe_allow_html=True)
    if st.button("LAUNCH V5.4"): st.session_state.access = True; st.rerun()
    st.stop()

# --- CALCULATIONS ---
spent = sum(r['Total'] for r in st.session_state.records)
bal = st.session_state.budget - spent
b_text, b_color = get_bal_ui(bal)

st.markdown('<h2 style="text-align:center; color:white; font-weight:900; letter-spacing:5px; margin-bottom:35px;">AILYN CONSTRUCTION <span style="color:#34d399;">PRO</span></h2>', unsafe_allow_html=True)

# --- DASHBOARD STATS ---
st.markdown(f"""<div class="stats-container">
    <div><div class="stat-label">Capital</div><div class="stat-value" style="color:white;">₱ {st.session_state.budget:,.2f}</div></div>
    <div><div class="stat-label">Spent</div><div class="stat-value" style="color:#fbbf24;">₱ {spent:,.2f}</div></div>
    <div><div class="stat-label">Balance</div><div class="stat-value" style="color:{b_color};">{b_text}</div></div>
</div>""", unsafe_allow_html=True)

# --- NAVIGATION MENU ---
if st.session_state.mode == "menu":
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("➕ MATERIAL"): st.session_state.mode = "MAT"; st.rerun()
    with c2: 
        if st.button("🚚 DELIVERY"): st.session_state.mode = "DEL"; st.rerun()
    with c3: 
        if st.button("📦 OTHERS"): st.session_state.mode = "OTH"; st.rerun()

    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("💰 CAPITAL"): st.session_state.mode = "FUND"; st.rerun()
    with c5:
        if st.button("⚙️ EMAILS"): st.session_state.mode = "MAIL"; st.rerun()
    with c6:
        if st.button("🔄 RESET"): st.session_state.records = []; st.session_state.budget = 0.0; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✉️ DISPATCH GMAIL REPORT"): send_report()

    if st.session_state.records:
        st.markdown("### RECENT LOGS")
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df[['Category', 'Description', 'Total']], use_container_width=True)
    else:
        st.info("System Ready. No records to display yet.")

# --- DATA ENTRY MODES ---
elif st.session_state.mode == "MAT":
    with st.form("mat_form", clear_on_submit=True):
        st.subheader("ADD MATERIAL")
        d = st.text_input("ITEM NAME").upper()
        col_q, col_p = st.columns(2)
        q = col_q.number_input("QUANTITY", min_value=1, step=1)
        p = col_p.number_input("PRICE/UNIT", min_value=0.0)
        if st.form_submit_button("SAVE"):
            st.session_state.records.append({"Category": "MATERIAL", "Description": f"{q}X {d}", "Total": (q * p)})
            st.session_state.mode = "menu"; st.rerun()
    if st.button("CANCEL"): st.session_state.mode = "menu"; st.rerun()

elif st.session_state.mode in ["DEL", "OTH"]:
    with st.form("simple_form", clear_on_submit=True):
        st.subheader(f"ADD {st.session_state.mode}")
        d = st.text_input("DESCRIPTION").upper()
        a = st.number_input("TOTAL AMOUNT", min_value=0.0)
        if st.form_submit_button("SAVE"):
            st.session_state.records.append({"Category": st.session_state.mode, "Description": d, "Total": a})
            st.session_state.mode = "menu"; st.rerun()
    if st.button("CANCEL"): st.session_state.mode = "menu"; st.rerun()

elif st.session_state.mode == "FUND":
    st.session_state.budget = st.number_input("UPDATE CAPITAL", value=st.session_state.budget)
    if st.button("SAVE CHANGES"): st.session_state.mode = "menu"; st.rerun()

elif st.session_state.mode == "MAIL":
    st.markdown("### 📧 RECIPIENTS")
    for e in st.session_state.emails: st.write(f"✔ {e}")
    if st.button("BACK"): st.session_state.mode = "menu"; st.rerun()