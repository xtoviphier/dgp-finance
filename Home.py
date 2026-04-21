import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime

# Import translator
try:
    from translator import get_ai_translation
except ImportError:
    def get_ai_translation(text, lang):
        return text

# Page config
st.set_page_config(
    page_title="DGP Finance • Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = None
if 'translate_mode' not in st.session_state:
    st.session_state.translate_mode = True

# Helper function to conditionally translate
def t(text):
    return get_ai_translation(text, st.session_state.lang) if st.session_state.translate_mode else text

# Sidebar with consistent UI
with st.sidebar:
    # Enable AI Translation toggle (matching Financial Reports)
    st.session_state.translate_mode = st.toggle(
        t("🌐 Enable AI Translation"), 
        value=st.session_state.translate_mode
    )
    
    # Language selector
    st.markdown(t("### Language"))
    lang_options = {
        "en": "English", "ar": "العربية", "fr": "Français", "es": "Español",
        "pt": "Português", "ru": "Русский", "de": "Deutsch", "sw": "Kiswahili", "zh": "中文"
    }
    selected_lang = st.selectbox(
        t("Select Language"),
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(st.session_state.lang),
        key="lang_selector_home"
    )
    
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()
    
    current_lang = st.session_state.lang
    
    # RTL support for Arabic
    if current_lang == "ar":
        st.markdown("""
        <style>
        .stApp { direction: rtl; text-align: right; }
        </style>
        """, unsafe_allow_html=True)

# Branding: DGP Finance at top right
st.markdown(f"""
<div style="position: fixed; top: 10px; right: 20px; z-index: 1000; font-weight: bold; font-size: 1.2em; color: #1f77b4;">
    {t("DGP Finance")} 💰
</div>
""", unsafe_allow_html=True)

# Main title
current_time = datetime.now().strftime('%H:%M:%S')
current_date = datetime.now().strftime('%B %d, %Y')
st.title(f"📊 {t('DGP Finance Dashboard')}")
st.markdown(f"*{t('Live Global Market Data')} • {current_date} • {t('Last Updated')}: {current_time}*")

# ============================================================================
# RIGHT-TO-LEFT STOCK TICKER - ALL GLOBAL MARKETS
# ============================================================================
st.markdown(f"### 🔄 {t('Live Market Ticker')}")

# UPDATED TICKERS - COMPREHENSIVE GLOBAL MARKETS
TICKERS = {
    "UAE": [
        "DFM.AE",
    ],
    "EU": [
        "ASML.AS", "SAP.DE", "MC.PA", "OR.PA", "NESN.SW", "ROG.SW", "NOVN.SW",
        "SHEL.L", "BP.L", "HSBA.L", "BARC.L", "BNP.PA", "SAN.PA", "AIR.PA",
        "DTE.DE", "VOW3.DE", "BMW.DE", "MBG.DE", "ADS.DE", "BAS.DE", "BAYN.DE", "SIE.DE", "IFX.DE",
        "ENEL.MI", "ENI.MI", "ISP.MI", "UCG.MI", "RACE.MI", "STLA.MI",
        "KER.PA", "SU.PA", "DG.PA", "AI.PA", "ORA.PA", "CAP.PA", "RI.PA",
        "ABI.BR", "ULVR.L", "NG.L", "GLEN.L", "RIO.L", "AAL.L", "PRU.L", "LSEG.L", "EXPN.L", "REL.L", "IMB.L", "VOD.L", "TSCO.L"
    ],
    "Asia": [
        "BABA", "TCEHY", "JD", "PDD", "NTES", "BIDU",
        "TSM", "SSNLF", "SONY", "HMC", "TM", "MUFG", "SMFG",
        "INFY", "TCS.NS", "RELIANCE.NS", "ICICIBANK.NS", "HDB",
        "SE", "GRAB"
    ],
    "US": [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "NFLX", "INTC", "NOK", "AAL", "SNAP", "SOFI", "MARA", "MRVL", "ARM", "TTD", "DJT", "LCID", "DUOL", "TEAM", "PL",
        "CAR", "MXL", "BLD", "LEGN", "NKTR", "ERAS", "USAR", "LWLG", "HPP", "BB", "WIX", "ACLS", "SGML", "BLLN", "VECO", "CRDO", "MP", "YSS", "HIMS", "BBWI", "AEHR", "KVYO", "COHU", "PLUG", "ONDS", "FRMI", "QXO", "IONQ", "ASTS", "QBTS", "BTG", "RGTI", "BMNR", "IREN", "NRG", "FCEL", "BSX", "POET", "ENV", "CMND", "HPE", "CHTR", "STLD", "BW", "AXTI", "RGC", "TERN", "TNGX", "ABVX", "LITE", "AAOI", "KOD", "BE", "HYMC", "CELC", "WDC", "LASR", "PRAX", "WULF", "AMPX", "CIEN", "FIG", "BULL", "MNDY", "FISV", "STUB", "VERX", "KLAR", "SRPT", "IT", "GPK", "HUBS", "NTSK", "EMAT", "FMC", "SPSC", "SFM", "GLOB", "DOCS"
    ]
}

@st.cache_data(ttl=120, show_spinner=False)
def fetch_market_data():
    data = []
    errors = []
    
    for region, symbols in TICKERS.items():
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                
                if current_price:
                    prev_close = info.get('previousClose', current_price)
                    change = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
                    currency = info.get('currency', 'USD')
                    
                    data.append({
                        'symbol': symbol,
                        'region': region,
                        'price': float(current_price),
                        'change': float(change),
                        'currency': currency
                    })
            except Exception as e:
                errors.append(f"{symbol}")
                continue
    
    return pd.DataFrame(data) if data else None, errors

# Fetch the data
df, fetch_errors = fetch_market_data()

# Show ticker or simple message
if df is not None and not df.empty:
    if fetch_errors:
        st.warning(f"⚠️ {t('Partial data')}: {len(fetch_errors)} {t('symbols failed')}.")
    
    ticker_items = []
    for _, row in df.iterrows():
        color = "#2ecc71" if row['change'] >= 0 else "#e74c3c"
        arrow = "▲" if row['change'] >= 0 else "▼"
        ticker_items.append(
            f"<span style='margin: 0 20px; color: {color}; font-weight: bold; font-family: monospace;'>"
            f"{row['symbol']} {row['price']:,.2f} {row['currency']} "
            f"{arrow} {abs(row['change']):.2f}%</span>"
        )
    
    ticker_html = f"""
    <div style="overflow: hidden; white-space: nowrap; width: 100%; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 12px 0; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
        <div id="ticker" style="display: inline-block; animation: scroll-left 3480s linear infinite;">
            {''.join(ticker_items * 8)}
        </div>
    </div>
    <style>
    @keyframes scroll-left {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}
    </style>
    """
    st.markdown(ticker_html, unsafe_allow_html=True)
else:
    st.info(t("⚠️ Market data unavailable. Check your internet connection or refresh the page."))

# ============================================================================
# LIVE CHARTS & GLOBAL MARKET OVERVIEW
# ============================================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 🌍 {t('Global Indices Performance')}")
    
    indices = ["^GSPC", "^IXIC", "^DJI", "^FTSE", "^GDAXI", "^N225", "^HSI"]
    index_data = []
    
    for idx in indices:
        try:
            ticker = yf.Ticker(idx)
            hist = ticker.history(period="1d", interval="1m")
            
            if not hist.empty and len(hist) > 0:
                current = hist['Close'].iloc[-1]
                opening = hist['Open'].iloc[0]
                change = ((current - opening) / opening * 100) if opening else 0
                
                index_data.append({
                    'name': idx,
                    'price': current,
                    'change': change
                })
        except Exception as e:
            continue
    
    if index_data:
        idx_df = pd.DataFrame(index_data)
        
        fig = px.bar(
            idx_df, 
            x='name', 
            y='change',
            color='change',
            color_continuous_scale=['#e74c3c', '#f1c40f', '#2ecc71'],
            title=t("Today's Performance (%)"),
            labels={'name': t('Index'), 'change': t('Change %')}
        )
        fig.update_layout(
            height=350, 
            margin=dict(t=40, b=40, l=40, r=40),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(t("Loading index data..."))

with col2:
    st.markdown(f"### 📊 {t('Biggest Movers')}")
    
    if df is not None and not df.empty:
        df_sorted = df.reindex(df['change'].abs().sort_values(ascending=False).index)
        top5 = df_sorted.head(5)
        
        for _, row in top5.iterrows():
            color = "#2ecc71" if row['change'] >= 0 else "#e74c3c"
            arrow = "▲" if row['change'] >= 0 else "▼"
            st.markdown(f"""
            <div style="padding: 12px; margin: 8px 0; border-left: 4px solid {color}; background: rgba(255,255,255,0.05); border-radius: 5px;">
                <strong style="font-size: 1.1em;">{row['symbol']}</strong><br>
                <span style="color: {color}; font-weight: bold; font-size: 1.2em;">
                    {row['price']:,.2f} {row['currency']} {arrow} {abs(row['change']):.2f}%
                </span><br>
                <small style="opacity: 0.7;">{row['region']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(t("Loading top performers..."))

# ============================================================================
# INTERACTIVE CHART: Select any stock to view details
# ============================================================================
st.markdown("---")
st.markdown(f"### 🔍 {t('Explore Stocks')}")
col_a, col_b = st.columns([1, 2])

with col_a:
    all_symbols = [sym for symbols in TICKERS.values() for sym in symbols]
    selected_symbol = st.selectbox(
        t("Select Symbol"), 
        all_symbols, 
        key="symbol_selector"
    )
    
    if st.button(f"📈 {t('View Details')}", type="primary", use_container_width=True):
        st.session_state.selected_symbol = selected_symbol
        st.rerun()

with col_b:
    if st.session_state.selected_symbol:
        symbol = st.session_state.selected_symbol
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1mo")
            
            if not hist.empty:
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name=symbol,
                    increasing_line_color='#2ecc71',
                    decreasing_line_color='#e74c3c'
                )])
                fig.update_layout(
                    title=f"{symbol} - 1 Month Price Action",
                    yaxis_title="Price",
                    xaxis_title="Date",
                    height=400,
                    margin=dict(t=40, b=40, l=40, r=40),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                info = ticker.info
                current_price = info.get('currentPrice', 'N/A')
                prev_close = info.get('previousClose', 'N/A')
                day_high = info.get('dayHigh', 'N/A')
                day_low = info.get('dayLow', 'N/A')
                volume = info.get('volume')
                market_cap = info.get('marketCap')
                
                volume_str = f"{volume:,}" if volume is not None else 'N/A'
                market_cap_str = f"{market_cap:,}" if market_cap is not None else 'N/A'
                
                st.markdown(f"""
                **{t('Key Metrics')} for {symbol}**  
                • {t('Current Price')}: {current_price} {info.get('currency', 'USD')}  
                • {t('Previous Close')}: {prev_close}  
                • {t('Day High')}: {day_high}  
                • {t('Day Low')}: {day_low}  
                • {t('Volume')}: {volume_str}  
                • {t('Market Cap')}: {market_cap_str}
                """)
            else:
                st.warning(t("No historical data available"))
        except Exception as e:
            st.error(f"{t('Error loading data')}: {str(e)}")
    else:
        st.info(f"👈 {t('Select a symbol and click View Details to see charts')}")

# ============================================================================
# AUTO-REFRESH INDICATOR
# ============================================================================
st.markdown("---")
st.caption(f"🔄 {t('Dashboard auto-refreshes every 60 seconds')} • {t('Data source')}: Yahoo Finance • {t('Server time')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if st.button(f"🔄 {t('Refresh Data Now')}", type="secondary"):
    st.cache_data.clear()
    st.session_state.selected_symbol = None
    st.rerun()