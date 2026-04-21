import streamlit as st
import pandas as pd
from statements import (
    generate_income_statement,
    generate_balance_sheet,
    generate_cash_flow,
    generate_appropriation_account,
    RATIOS_DB
)
from portfolio_manager import save_report

st.set_page_config(page_title="DGP Finance", layout="wide", page_icon="💰")

# Initialize session state
if 'lang' not in st.session_state: 
    st.session_state.lang = 'en'
if 'business_type' not in st.session_state: 
    st.session_state.business_type = 'Sole Trader'

# 1. FIRST: Define current_lang from session state
current_lang = st.session_state.lang

# 2. SECOND: Define get_ai_translation BEFORE using it
translate_mode = st.sidebar.toggle("🌐 Enable AI Translation", value=True)
if translate_mode:
    from translator import get_ai_translation
else:
    def get_ai_translation(text, lang):
        return text

# 3. NOW you can safely use get_ai_translation for the language selector
lang_options = {
    "en": "English", "ar": "العربية", "fr": "Français", "es": "Español", 
    "pt": "Português", "ru": "Русский", "de": "Deutsch", "sw": "Kiswahili", "zh": "中文"
}

selected_lang = st.sidebar.selectbox(
    get_ai_translation("Language", current_lang),
    options=list(lang_options.keys()),
    format_func=lambda x: lang_options[x],
    index=list(lang_options.keys()).index(st.session_state.lang),
    key="lang_selector"
)

if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()

# Update current_lang after potential rerun
current_lang = st.session_state.lang

# Organization Type Selector
business_types = ["Sole Trader", "Partnership", "Private Limited Company (Ltd)", "Public Limited Company (PLC)", "Public Sector", "Non-Profit Organization"]
st.session_state.business_type = st.sidebar.selectbox(
    get_ai_translation("Organization Type", current_lang),
    options=business_types,
    index=business_types.index(st.session_state.business_type),
    key="org_type_selector"
)

# Ratio Category Selector - Moved to main sidebar
st.sidebar.markdown("---")
st.sidebar.header(get_ai_translation("Select Ratio Category", current_lang))
selected_category = st.sidebar.selectbox(
    get_ai_translation("Choose a ratio category:", current_lang), 
    list(RATIOS_DB.keys()),
    key="ratio_category"
)

# Check if Non-Profit
is_nonprofit = st.session_state.business_type == "Non-Profit Organization"

# Check if Public Sector
is_public_sector = st.session_state.business_type == "Public Sector"

# RTL Support
if current_lang == "ar":
    st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# MAIN CONTENT
st.title(get_ai_translation("DGP Finance", current_lang))
st.subheader(get_ai_translation("Financial Statement Generator", current_lang))

# TABS - Dynamic titles based on organization type
if is_nonprofit:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        get_ai_translation("📊 Statement of Activities", current_lang),
        get_ai_translation("📋 Statement of Financial Position", current_lang),
        get_ai_translation("💵 Statement of Cash Flows", current_lang),
        get_ai_translation("👥 Appropriation Account", current_lang),
        get_ai_translation("📈 Financial Ratios", current_lang)
    ])
elif is_public_sector:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        get_ai_translation("📊 Statement of Financial Performance", current_lang),
        get_ai_translation("📋 Statement of Financial Position", current_lang),
        get_ai_translation("💵 Statement of Cash Flows", current_lang),
        get_ai_translation("👥 Appropriation Account", current_lang),
        get_ai_translation("📈 Financial Ratios", current_lang)
    ])
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        get_ai_translation("📊 Income Statement / Profit & Loss (P&L)", current_lang),
        get_ai_translation("📋 Statement of Financial Position (Balance Sheet)", current_lang),
        get_ai_translation("💵 Cash Flow Statement", current_lang),
        get_ai_translation("👥 Appropriation Account", current_lang),
        get_ai_translation("📈 Financial Ratios", current_lang)
    ])

# ============================================================================
# TAB 1: INCOME STATEMENT / STATEMENT OF ACTIVITIES
# ============================================================================
with tab1:
    if is_public_sector:
        st.subheader(get_ai_translation("Statement of Financial Performance", current_lang))
        
        with st.expander(get_ai_translation("📝 Enter Statement of Financial Performance Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Revenue", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                period = st.text_input(get_ai_translation("Reporting Period", current_lang), get_ai_translation("Year Ended 31 March 2025", current_lang), key="ps_period")
                government_grants = st.number_input(get_ai_translation("Government Grants / Funding", current_lang), min_value=0.0, step=10000.0, key="ps_grants")
                tax_revenue = st.number_input(get_ai_translation("Tax Revenue (if applicable)", current_lang), min_value=0.0, step=10000.0, key="ps_tax")
            with col2:
                currency = st.selectbox(get_ai_translation("Currency", current_lang), ["AED", "USD", "EUR", "GBP"], index=0, key="ps_currency")
                service_revenue = st.number_input(get_ai_translation("Service Revenue (fees, licenses)", current_lang), min_value=0.0, step=1000.0, key="ps_service")
                other_income = st.number_input(get_ai_translation("Other Income", current_lang), min_value=0.0, step=1000.0, key="ps_other_income")

            st.subheader(get_ai_translation("Expenses", current_lang))
            col3, col4, col5 = st.columns(3)
            with col3:
                employee_costs = st.number_input(get_ai_translation("Employee Costs (Wages & Salaries)", current_lang), min_value=0.0, step=1000.0, key="ps_employee")
                admin_expenses = st.number_input(get_ai_translation("Administrative Expenses", current_lang), min_value=0.0, step=1000.0, key="ps_admin")
                utilities = st.number_input(get_ai_translation("Utilities", current_lang), min_value=0.0, step=1000.0, key="ps_utilities")
            with col4:
                repairs_maintenance = st.number_input(get_ai_translation("Repairs & Maintenance", current_lang), min_value=0.0, step=1000.0, key="ps_repairs")
                depreciation = st.number_input(get_ai_translation("Depreciation", current_lang), min_value=0.0, step=1000.0, key="ps_depreciation")
                interest_expense = st.number_input(get_ai_translation("Interest Expense", current_lang), min_value=0.0, step=1000.0, key="ps_interest")
            with col5:
                program_costs = st.number_input(get_ai_translation("Program / Service Delivery Costs", current_lang), min_value=0.0, step=1000.0, key="ps_program")
                other_expenses = st.number_input(get_ai_translation("Other Operating Expenses", current_lang), min_value=0.0, step=1000.0, key="ps_other_exp")

            if st.button(get_ai_translation("📊 Generate Statement of Financial Performance", current_lang), type="primary", key="btn_ps_performance"):
                st.session_state.income_statement = {
                    "type": "public_sector_performance", "period": period, "currency": currency,
                    "government_grants": government_grants, "tax_revenue": tax_revenue,
                    "service_revenue": service_revenue, "other_income": other_income,
                    "employee_costs": employee_costs, "admin_expenses": admin_expenses,
                    "utilities": utilities, "repairs_maintenance": repairs_maintenance,
                    "depreciation": depreciation, "interest_expense": interest_expense,
                    "program_costs": program_costs, "other_expenses": other_expenses
                }
                st.success(get_ai_translation("✅ Statement of Financial Performance data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Statement of Financial Performance - {period}",
                    report_type="Statement of Financial Performance (Public Sector)",
                    org_type=st.session_state.business_type,
                    data=st.session_state.income_statement
                )

        cfg = st.session_state.get("income_statement")
        if cfg and cfg.get("type") == "public_sector_performance":
            currency = cfg.get('currency', 'AED')
            period = cfg.get('period', 'Year Ended 31 March 2025')
            
            total_revenue = cfg['government_grants'] + cfg['tax_revenue'] + cfg['service_revenue'] + cfg['other_income']
            total_expenses = (cfg['employee_costs'] + cfg['admin_expenses'] + cfg['utilities'] +
                            cfg['repairs_maintenance'] + cfg['depreciation'] + cfg['interest_expense'] +
                            cfg['program_costs'] + cfg['other_expenses'])
            surplus_deficit = total_revenue - total_expenses
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Statement of Financial Performance", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Revenue", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation(" Government Grants / Funding", current_lang), f"{cfg['government_grants']:,.2f}", ''])
            rows.append([get_ai_translation("Tax Revenue (if applicable)", current_lang), f"{cfg['tax_revenue']:,.2f}", ''])
            rows.append([get_ai_translation("Service Revenue (fees, licenses)", current_lang), f"{cfg['service_revenue']:,.2f}", ''])
            rows.append([get_ai_translation("Other Income", current_lang), f"{cfg['other_income']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Revenue", current_lang), '', f"{total_revenue:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Expenses", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Employee Costs (Wages & Salaries)", current_lang), f"{cfg['employee_costs']:,.2f}", ''])
            rows.append([get_ai_translation("Administrative Expenses", current_lang), f"{cfg['admin_expenses']:,.2f}", ''])
            rows.append([get_ai_translation("Utilities", current_lang), f"{cfg['utilities']:,.2f}", ''])
            rows.append([get_ai_translation("Repairs & Maintenance", current_lang), f"{cfg['repairs_maintenance']:,.2f}", ''])
            rows.append([get_ai_translation("Depreciation", current_lang), f"{cfg['depreciation']:,.2f}", ''])
            rows.append([get_ai_translation("Interest Expense", current_lang), f"{cfg['interest_expense']:,.2f}", ''])
            rows.append([get_ai_translation("Program / Service Delivery Costs", current_lang), f"{cfg['program_costs']:,.2f}", ''])
            rows.append([get_ai_translation("Other Operating Expenses", current_lang), f"{cfg['other_expenses']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Expenses", current_lang), '', f"({total_expenses:,.2f})"])
            rows.append(['', '', ''])
            
            result_label = get_ai_translation("Surplus", current_lang) if surplus_deficit >= 0 else get_ai_translation("Deficit", current_lang)
            rows.append([result_label, '', f"{surplus_deficit:,.2f}" if surplus_deficit >= 0 else f"-{abs(surplus_deficit):,.2f}"])

            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    elif is_nonprofit:
        st.subheader(get_ai_translation("Statement of Activities", current_lang))
        
        with st.expander(get_ai_translation("📝 Enter Statement of Activities Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Income / Inflows", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                period = st.text_input(get_ai_translation("Reporting Period", current_lang), get_ai_translation("Year Ended 31 December 2024", current_lang), key="np_period")
                donations = st.number_input(get_ai_translation("Donations", current_lang), min_value=0.0, step=1000.0, key="np_donations")
                grants = st.number_input(get_ai_translation("Grants", current_lang), min_value=0.0, step=1000.0, key="np_grants")
            with col2:
                membership_fees = st.number_input(get_ai_translation("Membership fees", current_lang), min_value=0.0, step=1000.0, key="np_membership")
                fundraising_income = st.number_input(get_ai_translation("Fundraising income", current_lang), min_value=0.0, step=1000.0, key="np_fundraising")
                currency = st.selectbox(get_ai_translation("Currency", current_lang), ["AED", "USD", "EUR", "GBP"], index=0, key="np_currency")                

            st.subheader(get_ai_translation("Expenses", current_lang))
            col3, col4, col5 = st.columns(3)
            with col3:
                program_expenses = st.number_input(get_ai_translation("Program expenses (core mission activities)", current_lang), min_value=0.0, step=1000.0, key="np_program")
            with col4:
                admin_expenses = st.number_input(get_ai_translation("Administrative expenses", current_lang), min_value=0.0, step=1000.0, key="np_admin")
            with col5:
                fundraising_costs = st.number_input(get_ai_translation("Fundraising costs", current_lang), min_value=0.0, step=1000.0, key="np_fundraising_costs")

            if st.button(get_ai_translation("📊 Generate Statement of Activities", current_lang), type="primary", key="btn_np_activities"):
                st.session_state.income_statement = {
                    "type": "nonprofit_activities", "period": period, "currency": currency,
                    "donations": donations, "grants": grants,
                    "membership_fees": membership_fees, "fundraising_income": fundraising_income,
                    "program_expenses": program_expenses, "admin_expenses": admin_expenses,
                    "fundraising_costs": fundraising_costs
                }
                st.success(get_ai_translation("✅ Statement of Activities data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Statement of Activities - {period}",
                    report_type="Statement of Activities (Non-Profit)",
                    org_type=st.session_state.business_type,
                    data=st.session_state.income_statement
                )

        cfg = st.session_state.get("income_statement")
        if cfg and cfg.get("type") == "nonprofit_activities":
            currency = cfg.get('currency', 'AED')
            period = cfg.get('period', 'Year Ended 31 December 2024')
            
            total_income = cfg['donations'] + cfg['grants'] + cfg['membership_fees'] + cfg['fundraising_income']
            total_expenses = cfg['program_expenses'] + cfg['admin_expenses'] + cfg['fundraising_costs']
            surplus_deficit = total_income - total_expenses
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Statement of Activities", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Income / Inflows", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Donations", current_lang), f"{cfg['donations']:,.2f}", ''])
            rows.append([get_ai_translation("Grants", current_lang), f"{cfg['grants']:,.2f}", ''])
            rows.append([get_ai_translation("Membership fees", current_lang), f"{cfg['membership_fees']:,.2f}", ''])
            rows.append([get_ai_translation("Fundraising income", current_lang), f"{cfg['fundraising_income']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Income", current_lang), '', f"{total_income:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Expenses", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Program expenses", current_lang), f"{cfg['program_expenses']:,.2f}", ''])
            rows.append([get_ai_translation("Administrative expenses", current_lang), f"{cfg['admin_expenses']:,.2f}", ''])
            rows.append([get_ai_translation("Fundraising costs", current_lang), f"{cfg['fundraising_costs']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Expenses", current_lang), '', f"({total_expenses:,.2f})"])
            
            result_label = get_ai_translation("Net Surplus", current_lang) if surplus_deficit >= 0 else get_ai_translation("Net Deficit", current_lang)
            rows.append([result_label, '', f"{surplus_deficit:,.2f}" if surplus_deficit >= 0 else f"-{abs(surplus_deficit):,.2f}"])

            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)            
    
    else:
        st.subheader(get_ai_translation("Income Statement / Profit & Loss (P&L)", current_lang))
        
        with st.expander(get_ai_translation("📝 Enter Income Statement Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Revenue / Trading", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                sales = st.number_input(get_ai_translation("Sales Revenue", current_lang), min_value=0.0, step=1000.0, key="is_sales")
                sales_returns = st.number_input(get_ai_translation("Less: Returns (if any)", current_lang), min_value=0.0, step=100.0, key="is_returns")
                opening_stock = st.number_input(get_ai_translation("Opening Stock", current_lang), min_value=0.0, step=1000.0, key="is_opening_stock")
                purchases = st.number_input(get_ai_translation("Purchases", current_lang), min_value=0.0, step=1000.0, key="is_purchases")
                carriage_in = st.number_input(get_ai_translation("Carriage Inwards", current_lang), min_value=0.0, step=100.0, key="is_carriage")
                closing_stock = st.number_input(get_ai_translation("– Closing Stock", current_lang), min_value=0.0, step=1000.0, key="is_closing_stock")
            with col2:
                period = st.text_input(get_ai_translation("Reporting Period", current_lang), get_ai_translation("Year Ended 31 March 2025", current_lang), key="is_period")
                currency = st.selectbox(get_ai_translation("Currency", current_lang), ["AED", "USD", "EUR", "GBP"], index=0, key="is_currency")
                rent_income = st.number_input(get_ai_translation("Rent income", current_lang), min_value=0.0, step=100.0, key="is_rent_income")
                interest_received = st.number_input(get_ai_translation("Interest received", current_lang), min_value=0.0, step=100.0, key="is_interest_received")
                misc_income = st.number_input(get_ai_translation("Miscellaneous income", current_lang), min_value=0.0, step=100.0, key="is_misc_income")

            st.subheader(get_ai_translation("Expenses", current_lang))
            col3, col4, col5 = st.columns(3)
            with col3:
                wages_salaries = st.number_input(get_ai_translation("Wages & Salaries", current_lang), min_value=0.0, step=100.0, key="is_wages")
                rent_paid = st.number_input(get_ai_translation("Rent Paid", current_lang), min_value=0.0, step=100.0, key="is_rent_paid")
                rent_prepaid = st.number_input(get_ai_translation("Rent Prepaid", current_lang), min_value=0.0, step=100.0, key="is_rent_prepaid")
                rent_accrued = st.number_input(get_ai_translation("Rent Accrued", current_lang), min_value=0.0, step=100.0, key="is_rent_accrued")
                insurance_paid = st.number_input(get_ai_translation("Insurance Paid", current_lang), min_value=0.0, step=100.0, key="is_ins_paid")
                insurance_prepaid = st.number_input(get_ai_translation("Insurance Prepaid", current_lang), min_value=0.0, step=100.0, key="is_ins_prepaid")
            with col4:
                utilities = st.number_input(get_ai_translation("Utilities (lighting, etc.)", current_lang), min_value=0.0, step=100.0, key="is_utilities")
                postage = st.number_input(get_ai_translation("Postage", current_lang), min_value=0.0, step=100.0, key="is_postage")
                printing = st.number_input(get_ai_translation("Office expenses (printing)", current_lang), min_value=0.0, step=100.0, key="is_printing")
                discount_allowed = st.number_input(get_ai_translation("Discount Allowed", current_lang), min_value=0.0, step=100.0, key="is_discount")
                bad_debts = st.number_input(get_ai_translation("Bad Debts", current_lang), min_value=0.0, step=100.0, key="is_bad_debts")
                prov_doubtful_debts = st.number_input(get_ai_translation("Provision for Doubtful Debts", current_lang), min_value=0.0, step=100.0, key="is_prov_debts")
            with col5:
                repairs = st.number_input(get_ai_translation("Repairs & Maintenance", current_lang), min_value=0.0, step=100.0, key="is_repairs")
                depreciation = st.number_input(get_ai_translation("Depreciation (non-cash expense)", current_lang), min_value=0.0, step=100.0, key="is_depreciation")
                interest_expense = st.number_input(get_ai_translation("Interest Expense", current_lang), min_value=0.0, step=100.0, key="is_interest_exp")
                general_expenses = st.number_input(get_ai_translation("General expenses", current_lang), min_value=0.0, step=100.0, key="is_general_exp")

            if st.button(get_ai_translation("📊 Generate Income Statement", current_lang), type="primary", key="btn_is"):
                st.session_state.income_statement = {
                    "type": "income_statement", "period": period, "currency": currency,
                    "sales": sales, "sales_returns": sales_returns,
                    "opening_stock": opening_stock, "purchases": purchases,
                    "closing_stock": closing_stock, "carriage_in": carriage_in,
                    "rent_income": rent_income, "interest_received": interest_received,
                    "misc_income": misc_income,
                    "rent_paid": rent_paid, "rent_prepaid": rent_prepaid, "rent_accrued": rent_accrued,
                    "insurance_paid": insurance_paid, "insurance_prepaid": insurance_prepaid,
                    "wages_salaries": wages_salaries, "utilities": utilities,
                    "postage": postage, "printing": printing, "discount_allowed": discount_allowed,
                    "bad_debts": bad_debts, "prov_doubtful_debts": prov_doubtful_debts,
                    "repairs": repairs, "depreciation": depreciation,
                    "interest_expense": interest_expense, "general_expenses": general_expenses
                }
                st.success(get_ai_translation("✅ Income Statement data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Income Statement - {period}",
                    report_type="Income Statement / P&L",
                    org_type=st.session_state.business_type,
                    data=st.session_state.income_statement
                )
        
        cfg = st.session_state.get("income_statement")
        if cfg and cfg.get("type") == "income_statement":
            currency = cfg.get('currency', 'AED')
            period = cfg.get('period', 'Year Ended 31 March 2025')
            
            net_sales = cfg['sales'] - cfg['sales_returns']
            cogs = cfg['opening_stock'] + cfg['purchases'] + cfg['carriage_in'] - cfg['closing_stock']
            gross_profit = net_sales - cogs
            other_income_total = cfg['rent_income'] + cfg['interest_received'] + cfg['misc_income']
            rent_exp = cfg['rent_paid'] + cfg['rent_accrued'] - cfg['rent_prepaid']
            insurance_exp = cfg['insurance_paid'] - cfg['insurance_prepaid']
            
            expenses_list = [
                (get_ai_translation("Wages & Salaries", current_lang), cfg['wages_salaries']),
                (get_ai_translation("Rent & Insurance (adjusted)", current_lang), rent_exp + insurance_exp),
                (get_ai_translation("Utilities (lighting, etc.)", current_lang), cfg['utilities']),
                (get_ai_translation("Office expenses (printing, postage)", current_lang), cfg['printing'] + cfg['postage']),
                (get_ai_translation("Discount Allowed", current_lang), cfg['discount_allowed']),
                (get_ai_translation("Bad Debts + Provision", current_lang), cfg['bad_debts'] + cfg['prov_doubtful_debts']),
                (get_ai_translation("Repairs & Maintenance", current_lang), cfg['repairs']),
                (get_ai_translation("Depreciation (non-cash expense)", current_lang), cfg['depreciation']),
                (get_ai_translation("Interest Expense", current_lang), cfg['interest_expense']),
                (get_ai_translation("General expenses", current_lang), cfg['general_expenses'])
            ]
            total_expenses = sum(x[1] for x in expenses_list)
            net_profit = gross_profit + other_income_total - total_expenses
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Income Statement / Profit & Loss (P&L)", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Revenue", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Sales Revenue", current_lang), f"{cfg['sales']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Less: Returns", current_lang), f"({cfg['sales_returns']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Sales", current_lang), '', f"{net_sales:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cost of Sales", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Opening Stock", current_lang), f"{cfg['opening_stock']:,.2f}", ''])
            rows.append([get_ai_translation("Purchases", current_lang), f"{cfg['purchases']:,.2f}", ''])
            rows.append([get_ai_translation("Carriage Inwards", current_lang), f"{cfg['carriage_in']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Less: Closing Stock", current_lang), f"({cfg['closing_stock']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Cost of Sales", current_lang), '', f"({cogs:,.2f})"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Gross Profit", current_lang), '', f"{gross_profit:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Other Income", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Rent income", current_lang), f"{cfg['rent_income']:,.2f}", ''])
            rows.append([get_ai_translation("Interest received", current_lang), f"{cfg['interest_received']:,.2f}", ''])
            rows.append([get_ai_translation("Miscellaneous income", current_lang), f"{cfg['misc_income']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Other Income", current_lang), '', f"{other_income_total:,.2f}"])
            rows.append(['', '', ''])
            
            pbe = gross_profit + other_income_total
            rows.append([get_ai_translation("Profit Before Expenses", current_lang), '', f"{pbe:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Expenses", current_lang), '', ''])
            rows.append(['', '', ''])
            for item_name, item_value in expenses_list:
                rows.append([item_name, f"{item_value:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Expenses", current_lang), '', f"({total_expenses:,.2f})"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Net Profit", current_lang), '', f"{net_profit:,.2f}" if net_profit >= 0 else f"-{abs(net_profit):,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 2: STATEMENT OF FINANCIAL POSITION
# ============================================================================
with tab2:
    if is_public_sector:
        st.subheader(get_ai_translation("Statement of Financial Position", current_lang))
        
        auto_import_data = {}
        is_data = st.session_state.get("income_statement")

        if is_data and is_data.get("type") == "public_sector_performance":
            total_revenue = is_data['government_grants'] + is_data['tax_revenue'] + is_data['service_revenue'] + is_data['other_income']
            total_expenses = (is_data['employee_costs'] + is_data['admin_expenses'] + is_data['utilities'] +
                            is_data['repairs_maintenance'] + is_data['depreciation'] + is_data['interest_expense'] +
                            is_data['program_costs'] + is_data['other_expenses'])
            auto_import_data['surplus_deficit'] = total_revenue - total_expenses
            auto_import_data['currency'] = is_data.get('currency', 'AED')

        with st.expander(get_ai_translation("📝 Enter Statement of Financial Position Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Assets", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                land_building = st.number_input(get_ai_translation("Land & Buildings", current_lang), min_value=0.0, step=10000.0, key="ps_bs_land")
                equipment = st.number_input(get_ai_translation("Equipment / Machinery", current_lang), min_value=0.0, step=10000.0, key="ps_bs_equipment")
                furniture = st.number_input(get_ai_translation("Furniture", current_lang), min_value=0.0, step=1000.0, key="ps_bs_furniture")
            with col2:
                accumulated_depreciation = st.number_input(get_ai_translation("Less: Accumulated Depreciation", current_lang), min_value=0.0, step=1000.0, key="ps_bs_acc_dep")

            st.subheader(get_ai_translation("Current Assets", current_lang))
            col3, col4 = st.columns(2)
            with col3:
                receivables = st.number_input(get_ai_translation("Receivables", current_lang), min_value=0.0, step=1000.0, key="ps_bs_receivables")
            with col4:
                cash_equivalents = st.number_input(get_ai_translation("Cash and Cash Equivalents", current_lang), min_value=0.0, step=1000.0, key="ps_bs_cash")
                
            st.subheader(get_ai_translation("Liabilities", current_lang))
            col5, col6 = st.columns(2)
            with col5:
                payables = st.number_input(get_ai_translation("Payables", current_lang), min_value=0.0, step=1000.0, key="ps_bs_payables")
            with col6:
                accrued_expenses = st.number_input(get_ai_translation("Accrued Expenses", current_lang), min_value=0.0, step=100.0, key="ps_bs_accrued")

            st.subheader(get_ai_translation("Non-Current Liabilities", current_lang))
            col7, col8 = st.columns(2)
            with col7:
                loans = st.number_input(get_ai_translation("Loans / Borrowings", current_lang), min_value=0.0, step=10000.0, key="ps_bs_loans")

            st.subheader(get_ai_translation("Net Assets", current_lang))
            col9, col10 = st.columns(2)
            with col9:
                accumulated_surplus = st.number_input(get_ai_translation("Opening Accumulated Surplus / (Deficit)", current_lang), min_value=0.0, step=10000.0, key="ps_bs_open_surplus")
            with col10:
                pass

            if st.button(get_ai_translation("📊 Generate Statement of Financial Position", current_lang), type="primary", key="btn_ps_bs"):
                st.session_state.balance_sheet = {
                    "type": "public_sector_bs",
                    "land_building": land_building, "equipment": equipment, "furniture": furniture,
                    "accumulated_depreciation": accumulated_depreciation,
                    "receivables": receivables, "cash_equivalents": cash_equivalents,
                    "payables": payables, "accrued_expenses": accrued_expenses,
                    "loans": loans, "accumulated_surplus": accumulated_surplus
                }
                st.success(get_ai_translation("✅ Statement of Financial Position data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Statement of Financial Position - {period}",
                    report_type="Statement of Financial Position (Public Sector)",
                    org_type=st.session_state.business_type,
                    data=st.session_state.balance_sheet
                )

        cfg = st.session_state.get("balance_sheet")
        if cfg:
            currency = cfg.get('currency', 'AED') if 'currency' in cfg else 'AED'
            period = 'As of 31 March 2025'
            
            nca_net = cfg.get('land_building', 0) + cfg.get('equipment', 0) + cfg.get('furniture', 0) - cfg.get('accumulated_depreciation', 0)
            current_assets = cfg.get('receivables', 0) + cfg.get('cash_equivalents', 0)
            total_assets = nca_net + current_assets
            
            current_liabilities = cfg.get('payables', 0) + cfg.get('accrued_expenses', 0)
            ncl_total = cfg.get('loans', 0)
            
            surplus_for_year = auto_import_data.get('surplus_deficit', 0)
            closing_net_assets = cfg.get('accumulated_surplus', 0) + surplus_for_year
            
            total_liabilities_equity = closing_net_assets + current_liabilities + ncl_total
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Statement of Financial Position", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Assets", current_lang), '', ''])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Non-Current Assets", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Land & Buildings", current_lang), f"{cfg.get('land_building', 0):,.2f}", ''])
            rows.append([get_ai_translation("Equipment / Machinery", current_lang), f"{cfg.get('equipment', 0):,.2f}", ''])
            rows.append([get_ai_translation("Furniture", current_lang), f"{cfg.get('furniture', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Less: Accumulated Depreciation", current_lang), f"({cfg.get('accumulated_depreciation', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Non-Current Assets", current_lang), '', f"{nca_net:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Current Assets", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Receivables", current_lang), f"{cfg.get('receivables', 0):,.2f}", ''])
            rows.append([get_ai_translation("Cash and Cash Equivalents", current_lang), f"{cfg.get('cash_equivalents', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Current Assets", current_lang), '', f"{current_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("TOTAL ASSETS", current_lang), '', f"{total_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Net Assets / Equity", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Opening Accumulated Surplus", current_lang), f"{cfg.get('accumulated_surplus', 0):,.2f}", ''])
            rows.append([get_ai_translation("Surplus / (Deficit) for the Year", current_lang), f"{surplus_for_year:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Closing Accumulated Surplus", current_lang), '', f"{closing_net_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Liabilities", current_lang), '', ''])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Non-Current Liabilities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Loans / Borrowings", current_lang), f"{cfg.get('loans', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Non-Current Liabilities", current_lang), '', f"{ncl_total:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Current Liabilities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Payables", current_lang), f"{cfg.get('payables', 0):,.2f}", ''])
            rows.append([get_ai_translation("Accrued Expenses", current_lang), f"{cfg.get('accrued_expenses', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Current Liabilities", current_lang), '', f"{current_liabilities:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("TOTAL NET ASSETS & LIABILITIES", current_lang), '', f"{total_liabilities_equity:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if abs(total_assets - total_liabilities_equity) < 0.01:
                st.success(get_ai_translation("✅ Statement balances correctly!", current_lang))
            else:
                st.warning(get_ai_translation(f"⚠️ Statement imbalance: {abs(total_assets - total_liabilities_equity):,.2f} {currency} difference", current_lang))

    elif is_nonprofit:
        st.subheader(get_ai_translation("Statement of Financial Position", current_lang))
        
        auto_import_data = {}
        is_data = st.session_state.get("income_statement")
        
        if is_data and is_data.get("type") == "nonprofit_activities":
            total_income = is_data['donations'] + is_data['grants'] + is_data['membership_fees'] + is_data['fundraising_income']
            total_expenses = is_data['program_expenses'] + is_data['admin_expenses'] + is_data['fundraising_costs']
            auto_import_data['net_profit'] = total_income - total_expenses

        with st.expander(get_ai_translation("📝 Enter Statement of Financial Position Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Non-Current Assets", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                land_building = st.number_input(get_ai_translation("Land & Buildings", current_lang), min_value=0.0, step=10000.0, key="np_bs_land")
                machinery = st.number_input(get_ai_translation("Machinery", current_lang), min_value=0.0, step=10000.0, key="np_bs_machinery")
                furniture = st.number_input(get_ai_translation("Furniture", current_lang), min_value=0.0, step=1000.0, key="np_bs_furniture")
            with col2:
                accumulated_depreciation = st.number_input(get_ai_translation("Less: Accumulated Depreciation", current_lang), min_value=0.0, step=1000.0, key="np_bs_acc_dep")

            st.subheader(get_ai_translation("Current Assets", current_lang))
            col3, col4 = st.columns(2)
            with col3:
                inventory = st.number_input(get_ai_translation("Inventory", current_lang), min_value=0.0, step=1000.0, key="np_bs_inventory")
                debtors = st.number_input(get_ai_translation("Debtors", current_lang), min_value=0.0, step=1000.0, key="np_bs_debtors")
                bills_receivable = st.number_input(get_ai_translation("Bills Receivable", current_lang), min_value=0.0, step=1000.0, key="np_bs_bills_rec")
            with col4:
                cash_hand = st.number_input(get_ai_translation("Cash in Hand", current_lang), min_value=0.0, step=100.0, key="np_bs_cash_hand")
                cash_bank = st.number_input(get_ai_translation("Cash at Bank", current_lang), min_value=0.0, step=1000.0, key="np_bs_cash_bank")
                
            st.subheader(get_ai_translation("Current Liabilities", current_lang))
            col5, col6 = st.columns(2)
            with col5:
                creditors = st.number_input(get_ai_translation("Creditors", current_lang), min_value=0.0, step=1000.0, key="np_bs_creditors")
                bills_payable = st.number_input(get_ai_translation("Bills Payable", current_lang), min_value=0.0, step=1000.0, key="np_bs_bills_pay")
            with col6:
                bank_overdraft = st.number_input(get_ai_translation("Bank Overdraft", current_lang), min_value=0.0, step=1000.0, key="np_bs_overdraft")
                accrued_expenses = st.number_input(get_ai_translation("Accrued Expenses", current_lang), min_value=0.0, step=100.0, key="np_bs_accrued")

            st.subheader(get_ai_translation("Non-Current Liabilities", current_lang))
            col7, col8 = st.columns(2)
            with col7:
                bank_loan = st.number_input(get_ai_translation("Bank Loans", current_lang), min_value=0.0, step=10000.0, key="np_bs_bank_loan")
            with col8:
                loan_notes = st.number_input(get_ai_translation("Loan Notes", current_lang), min_value=0.0, step=10000.0, key="np_bs_loan_notes")

            st.subheader(get_ai_translation("Equity (Capital)", current_lang))
            col9, col10 = st.columns(2)
            with col9:
                opening_capital = st.number_input(get_ai_translation("Opening Capital", current_lang), min_value=0.0, step=10000.0, key="np_bs_open_cap")
                additional_capital = st.number_input(get_ai_translation("Additional Capital", current_lang), min_value=0.0, step=10000.0, key="np_bs_add_cap")
            with col10:
                drawings = st.number_input(get_ai_translation("– Drawings", current_lang), min_value=0.0, step=1000.0, key="np_bs_drawings")

            if st.button(get_ai_translation("📊 Generate Statement of Financial Position", current_lang), type="primary", key="btn_np_bs"):
                st.session_state.balance_sheet = {
                    "land_building": land_building, "machinery": machinery, "furniture": furniture,
                    "accumulated_depreciation": accumulated_depreciation,
                    "inventory": inventory, "debtors": debtors, "bills_receivable": bills_receivable,
                    "cash_hand": cash_hand, "cash_bank": cash_bank,
                    "creditors": creditors, "bills_payable": bills_payable,
                    "bank_overdraft": bank_overdraft, "accrued_expenses": accrued_expenses,
                    "bank_loan": bank_loan, "loan_notes": loan_notes,
                    "opening_capital": opening_capital, "additional_capital": additional_capital,
                    "drawings": drawings
                }
                st.success(get_ai_translation("✅ Statement of Financial Position data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Statement of Financial Position - {period}",
                    report_type="Statement of Financial Position",
                    org_type=st.session_state.business_type,
                    data=st.session_state.balance_sheet
                )

        cfg = st.session_state.get("balance_sheet")
        if cfg:
            currency = cfg.get('currency', 'AED') if 'currency' in cfg else 'AED'
            period = 'As of 31 March 2025'
            
            nca_net = cfg.get('land_building', 0) + cfg.get('machinery', 0) + cfg.get('furniture', 0) - cfg.get('accumulated_depreciation', 0)
            current_assets = cfg.get('inventory', 0) + cfg.get('debtors', 0) + cfg.get('bills_receivable', 0) + cfg.get('cash_hand', 0) + cfg.get('cash_bank', 0)
            current_liabilities = cfg.get('creditors', 0) + cfg.get('bills_payable', 0) + cfg.get('bank_overdraft', 0) + cfg.get('accrued_expenses', 0)
            ncl_total = cfg.get('bank_loan', 0) + cfg.get('loan_notes', 0)
            net_profit_for_equity = auto_import_data.get('net_profit', 0)
            closing_capital = cfg.get('opening_capital', 0) + cfg.get('additional_capital', 0) + net_profit_for_equity - cfg.get('drawings', 0)
            total_assets = nca_net + current_assets
            total_liabilities_equity = closing_capital + current_liabilities + ncl_total
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Statement of Financial Position", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("ASSETS", current_lang), '', ''])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Non-Current Assets", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Land & Buildings", current_lang), f"{cfg.get('land_building', 0):,.2f}", ''])
            rows.append([get_ai_translation("Machinery", current_lang), f"{cfg.get('machinery', 0):,.2f}", ''])
            rows.append([get_ai_translation("Furniture", current_lang), f"{cfg.get('furniture', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Less: Accumulated Depreciation", current_lang), f"({cfg.get('accumulated_depreciation', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Non-Current Assets", current_lang), '', f"{nca_net:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Current Assets", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Inventory", current_lang), f"{cfg.get('inventory', 0):,.2f}", ''])
            rows.append([get_ai_translation("Debtors", current_lang), f"{cfg.get('debtors', 0):,.2f}", ''])
            rows.append([get_ai_translation("Bills Receivable", current_lang), f"{cfg.get('bills_receivable', 0):,.2f}", ''])
            rows.append([get_ai_translation("Cash in Hand", current_lang), f"{cfg.get('cash_hand', 0):,.2f}", ''])
            rows.append([get_ai_translation("Cash at Bank", current_lang), f"{cfg.get('cash_bank', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Current Assets", current_lang), '', f"{current_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("TOTAL ASSETS", current_lang), '', f"{total_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("EQUITY & LIABILITIES", current_lang), '', ''])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Capital", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Opening Capital", current_lang), f"{cfg.get('opening_capital', 0):,.2f}", ''])
            rows.append([get_ai_translation("Additional Capital", current_lang), f"{cfg.get('additional_capital', 0):,.2f}", ''])
            rows.append([get_ai_translation("Net Profit", current_lang), f"{net_profit_for_equity:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Less: Drawings", current_lang), f"({cfg.get('drawings', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Closing Capital", current_lang), '', f"{closing_capital:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Non-Current Liabilities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Bank Loans", current_lang), f"{cfg.get('bank_loan', 0):,.2f}", ''])
            rows.append([get_ai_translation("Loan Notes", current_lang), f"{cfg.get('loan_notes', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Non-Current Liabilities", current_lang), '', f"{ncl_total:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Current Liabilities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Creditors", current_lang), f"{cfg.get('creditors', 0):,.2f}", ''])
            rows.append([get_ai_translation("Bills Payable", current_lang), f"{cfg.get('bills_payable', 0):,.2f}", ''])
            rows.append([get_ai_translation("Bank Overdraft", current_lang), f"{cfg.get('bank_overdraft', 0):,.2f}", ''])
            rows.append([get_ai_translation("Accrued Expenses", current_lang), f"{cfg.get('accrued_expenses', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Current Liabilities", current_lang), '', f"{current_liabilities:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("TOTAL CAPITAL & LIABILITIES", current_lang), '', f"{total_liabilities_equity:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if abs(total_assets - total_liabilities_equity) < 0.01:
                st.success(get_ai_translation("✅ Statement balances correctly!", current_lang))
            else:
                st.warning(get_ai_translation(f"⚠️ Statement imbalance: {abs(total_assets - total_liabilities_equity):,.2f} {currency} difference", current_lang))

    else:
        st.subheader(get_ai_translation("Statement of Financial Position (Balance Sheet)", current_lang))
        
        auto_import_data = {}
        is_data = st.session_state.get("income_statement")

        if is_data and isinstance(is_data, dict):
            try:
                if is_data.get("type") == "income_statement":
                    net_sales = is_data['sales'] - is_data['sales_returns']
                    cogs = is_data['opening_stock'] + is_data['purchases'] + is_data['carriage_in'] - is_data['closing_stock']
                    gross_profit = net_sales - cogs
                    other_income_total = is_data['rent_income'] + is_data['interest_received'] + is_data['misc_income']
                    rent_exp = is_data['rent_paid'] + is_data['rent_accrued'] - is_data['rent_prepaid']
                    insurance_exp = is_data['insurance_paid'] - is_data['insurance_prepaid']
                    expenses_list = [is_data['wages_salaries'], rent_exp + insurance_exp, is_data['utilities'],
                                    is_data['printing'] + is_data['postage'], is_data['discount_allowed'],
                                    is_data['bad_debts'] + is_data['prov_doubtful_debts'], is_data['repairs'],
                                    is_data['depreciation'], is_data['interest_expense'], is_data['general_expenses']]
                    total_expenses = sum(expenses_list)
                    auto_import_data['net_profit'] = gross_profit + other_income_total - total_expenses
                    auto_import_data['inventory'] = is_data['closing_stock']
            except KeyError as e:
                st.error(f"Auto-import error: Missing key {e} in financial data")

        with st.expander(get_ai_translation("📝 Enter Balance Sheet Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Non-Current Assets", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                land_building = st.number_input(get_ai_translation("Land & Buildings", current_lang), min_value=0.0, step=10000.0, key="bs_land")
                machinery = st.number_input(get_ai_translation("Machinery", current_lang), min_value=0.0, step=10000.0, key="bs_machinery")
                furniture = st.number_input(get_ai_translation("Furniture", current_lang), min_value=0.0, step=1000.0, key="bs_furniture")
            with col2:
                accumulated_depreciation = st.number_input(get_ai_translation("Less: Accumulated Depreciation", current_lang), min_value=0.0, step=1000.0, key="bs_acc_dep")

            st.subheader(get_ai_translation("Current Assets", current_lang))
            col3, col4 = st.columns(2)
            with col3:
                inventory = st.number_input(get_ai_translation("Inventory (Closing Stock)", current_lang), min_value=0.0, step=1000.0, key="bs_inventory")
                debtors = st.number_input(get_ai_translation("Debtors (Accounts Receivable)", current_lang), min_value=0.0, step=1000.0, key="bs_debtors")
                bills_receivable = st.number_input(get_ai_translation("Bills Receivable", current_lang), min_value=0.0, step=1000.0, key="bs_bills_rec")
            with col4:
                cash_hand = st.number_input(get_ai_translation("Cash in Hand", current_lang), min_value=0.0, step=100.0, key="bs_cash_hand")
                cash_bank = st.number_input(get_ai_translation("Cash at Bank", current_lang), min_value=0.0, step=1000.0, key="bs_cash_bank")
                
            st.subheader(get_ai_translation("Current Liabilities", current_lang))
            col5, col6 = st.columns(2)
            with col5:
                creditors = st.number_input(get_ai_translation("Creditors (Accounts Payable)", current_lang), min_value=0.0, step=1000.0, key="bs_creditors")
                bills_payable = st.number_input(get_ai_translation("Bills Payable", current_lang), min_value=0.0, step=1000.0, key="bs_bills_pay")
            with col6:
                bank_overdraft = st.number_input(get_ai_translation("Bank Overdraft", current_lang), min_value=0.0, step=1000.0, key="bs_overdraft")
                accrued_expenses = st.number_input(get_ai_translation("Accrued Expenses", current_lang), min_value=0.0, step=100.0, key="bs_accrued")

            st.subheader(get_ai_translation("Non-Current Liabilities", current_lang))
            col7, col8 = st.columns(2)
            with col7:
                bank_loan = st.number_input(get_ai_translation("Bank Loans", current_lang), min_value=0.0, step=10000.0, key="bs_bank_loan")
            with col8:
                loan_notes = st.number_input(get_ai_translation("Loan Notes", current_lang), min_value=0.0, step=10000.0, key="bs_loan_notes")

            st.subheader(get_ai_translation("Equity (Capital)", current_lang))
            col9, col10 = st.columns(2)
            with col9:
                opening_capital = st.number_input(get_ai_translation("Opening Capital", current_lang), min_value=0.0, step=10000.0, key="bs_open_cap")
                additional_capital = st.number_input(get_ai_translation("Additional Capital", current_lang), min_value=0.0, step=10000.0, key="bs_add_cap")
            with col10:
                drawings = st.number_input(get_ai_translation("– Drawings", current_lang), min_value=0.0, step=1000.0, key="bs_drawings")

            if st.button(get_ai_translation("📊 Generate Balance Sheet", current_lang), type="primary", key="btn_bs"):
                st.session_state.balance_sheet = {
                    "land_building": land_building, "machinery": machinery, "furniture": furniture,
                    "accumulated_depreciation": accumulated_depreciation,
                    "inventory": inventory, "debtors": debtors, "bills_receivable": bills_receivable,
                    "cash_hand": cash_hand, "cash_bank": cash_bank,
                    "creditors": creditors, "bills_payable": bills_payable,
                    "bank_overdraft": bank_overdraft, "accrued_expenses": accrued_expenses,
                    "bank_loan": bank_loan, "loan_notes": loan_notes,
                    "opening_capital": opening_capital, "additional_capital": additional_capital,
                    "drawings": drawings
                }
                st.success(get_ai_translation("✅ Balance Sheet data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Statement of Financial Position - {period}",
                    report_type="Statement of Financial Position",
                    org_type=st.session_state.business_type,
                    data=st.session_state.balance_sheet
                )

        cfg = st.session_state.get("balance_sheet")
        if cfg:
            currency = cfg.get('currency', 'AED') if 'currency' in cfg else 'AED'
            period = 'As of 31 March 2025'
            
            nca_net = cfg.get('land_building', 0) + cfg.get('machinery', 0) + cfg.get('furniture', 0) - cfg.get('accumulated_depreciation', 0)
            current_assets = cfg.get('inventory', 0) + cfg.get('debtors', 0) + cfg.get('bills_receivable', 0) + cfg.get('cash_hand', 0) + cfg.get('cash_bank', 0)
            current_liabilities = cfg.get('creditors', 0) + cfg.get('bills_payable', 0) + cfg.get('bank_overdraft', 0) + cfg.get('accrued_expenses', 0)
            ncl_total = cfg.get('bank_loan', 0) + cfg.get('loan_notes', 0)
            net_profit_for_equity = auto_import_data.get('net_profit', 0)
            closing_capital = cfg.get('opening_capital', 0) + cfg.get('additional_capital', 0) + net_profit_for_equity - cfg.get('drawings', 0)
            total_assets = nca_net + current_assets
            total_liabilities_equity = closing_capital + current_liabilities + ncl_total
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Statement of Financial Position", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("ASSETS", current_lang), '', ''])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Non-Current Assets", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Land & Buildings", current_lang), f"{cfg.get('land_building', 0):,.2f}", ''])
            rows.append([get_ai_translation("Machinery", current_lang), f"{cfg.get('machinery', 0):,.2f}", ''])
            rows.append([get_ai_translation("Furniture", current_lang), f"{cfg.get('furniture', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Less: Accumulated Depreciation", current_lang), f"({cfg.get('accumulated_depreciation', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Non-Current Assets", current_lang), '', f"{nca_net:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Current Assets", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Inventory (Closing Stock)", current_lang), f"{cfg.get('inventory', 0):,.2f}", ''])
            rows.append([get_ai_translation("Debtors (Accounts Receivable)", current_lang), f"{cfg.get('debtors', 0):,.2f}", ''])
            rows.append([get_ai_translation("Bills Receivable", current_lang), f"{cfg.get('bills_receivable', 0):,.2f}", ''])
            rows.append([get_ai_translation("Cash in Hand", current_lang), f"{cfg.get('cash_hand', 0):,.2f}", ''])
            rows.append([get_ai_translation("Cash at Bank", current_lang), f"{cfg.get('cash_bank', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Current Assets", current_lang), '', f"{current_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("TOTAL ASSETS", current_lang), '', f"{total_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("EQUITY & LIABILITIES", current_lang), '', ''])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Capital", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Opening Capital", current_lang), f"{cfg.get('opening_capital', 0):,.2f}", ''])
            rows.append([get_ai_translation("Additional Capital", current_lang), f"{cfg.get('additional_capital', 0):,.2f}", ''])
            rows.append([get_ai_translation("Net Profit", current_lang), f"{net_profit_for_equity:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Less: Drawings", current_lang), f"({cfg.get('drawings', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Closing Capital", current_lang), '', f"{closing_capital:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Non-Current Liabilities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Bank Loans", current_lang), f"{cfg.get('bank_loan', 0):,.2f}", ''])
            rows.append([get_ai_translation("Loan Notes", current_lang), f"{cfg.get('loan_notes', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Non-Current Liabilities", current_lang), '', f"{ncl_total:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Current Liabilities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Creditors (Accounts Payable)", current_lang), f"{cfg.get('creditors', 0):,.2f}", ''])
            rows.append([get_ai_translation("Bills Payable", current_lang), f"{cfg.get('bills_payable', 0):,.2f}", ''])
            rows.append([get_ai_translation("Bank Overdraft", current_lang), f"{cfg.get('bank_overdraft', 0):,.2f}", ''])
            rows.append([get_ai_translation("Accrued Expenses", current_lang), f"{cfg.get('accrued_expenses', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Total Current Liabilities", current_lang), '', f"{current_liabilities:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("TOTAL CAPITAL & LIABILITIES", current_lang), '', f"{total_liabilities_equity:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if abs(total_assets - total_liabilities_equity) < 0.01:
                st.success(get_ai_translation("✅ Statement balances correctly!", current_lang))
            else:
                st.warning(get_ai_translation(f"⚠️ Statement imbalance: {abs(total_assets - total_liabilities_equity):,.2f} {currency} difference", current_lang))

# ============================================================================
# TAB 3: CASH FLOW STATEMENT
# ============================================================================
with tab3:
    if is_public_sector:
        st.subheader(get_ai_translation("Statement of Cash Flows", current_lang))
        
        with st.expander(get_ai_translation("📝 Enter Statement of Cash Flows Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Operating Activities", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                cash_from_grants = st.number_input(get_ai_translation("Cash received from government/grants", current_lang), min_value=0.0, step=10000.0, key="ps_cf_grants")
                cash_from_services = st.number_input(get_ai_translation("Cash received from services/fees", current_lang), min_value=0.0, step=1000.0, key="ps_cf_services")
            with col2:
                cash_to_employees = st.number_input(get_ai_translation("Cash paid to employees", current_lang), min_value=0.0, step=1000.0, key="ps_cf_employees")
                cash_to_suppliers = st.number_input(get_ai_translation("Cash paid to suppliers", current_lang), min_value=0.0, step=1000.0, key="ps_cf_suppliers")

            st.subheader(get_ai_translation("Investing Activities", current_lang))
            col3, col4 = st.columns(2)
            with col3:
                purchase_assets = st.number_input(get_ai_translation("Purchase of assets", current_lang), min_value=0.0, step=10000.0, key="ps_cf_purchase")
            with col4:
                sale_assets = st.number_input(get_ai_translation("Sale of assets", current_lang), min_value=0.0, step=1000.0, key="ps_cf_sale")

            st.subheader(get_ai_translation("Financing Activities", current_lang))
            col5, col6 = st.columns(2)
            with col5:
                government_funding = st.number_input(get_ai_translation("Government funding received", current_lang), min_value=0.0, step=10000.0, key="ps_cf_funding")
                loans_received = st.number_input(get_ai_translation("Loans received", current_lang), min_value=0.0, step=10000.0, key="ps_cf_loans_in")
            with col6:
                loans_repaid = st.number_input(get_ai_translation("Loans repaid", current_lang), min_value=0.0, step=10000.0, key="ps_cf_loans_out")
                interest_paid = st.number_input(get_ai_translation("Interest paid", current_lang), min_value=0.0, step=1000.0, key="ps_cf_interest")

            st.subheader(get_ai_translation("Opening Balance", current_lang))
            opening_cash = st.number_input(get_ai_translation("Opening cash balance", current_lang), min_value=0.0, step=1000.0, key="ps_cf_opening")

            currency = st.selectbox(get_ai_translation("Currency", current_lang), ["AED", "USD", "EUR", "GBP"], index=0, key="ps_cf_currency")
            
            if st.button(get_ai_translation("📊 Generate Statement of Cash Flows", current_lang), type="primary", key="btn_ps_cf"):
                st.session_state.cash_flow = {
                    "type": "public_sector_cf",
                    "currency": currency,
                    "cash_from_grants": cash_from_grants,
                    "cash_from_services": cash_from_services,
                    "cash_to_employees": cash_to_employees,
                    "cash_to_suppliers": cash_to_suppliers,
                    "purchase_assets": purchase_assets,
                    "sale_assets": sale_assets,
                    "government_funding": government_funding,
                    "loans_received": loans_received,
                    "loans_repaid": loans_repaid,
                    "interest_paid": interest_paid,
                    "opening_cash": opening_cash
                }
                st.success(get_ai_translation("✅ Statement of Cash Flows data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Statement of Cash Flows - {period}",
                    report_type="Statement of Cash Flows (Public Sector)",
                    org_type=st.session_state.business_type,
                    data=st.session_state.cash_flow
                )

        cfg = st.session_state.get("cash_flow")
        if cfg and cfg.get("type") == "public_sector_cf":
            currency = cfg.get('currency', 'AED')
            period = cfg.get('period', 'For the Year Ended 31 March 2025')
            
            cash_inflows_operating = cfg['cash_from_grants'] + cfg['cash_from_services']
            cash_outflows_operating = cfg['cash_to_employees'] + cfg['cash_to_suppliers']
            net_operating = cash_inflows_operating - cash_outflows_operating
            
            net_investing = cfg['sale_assets'] - cfg['purchase_assets']
            
            cash_inflows_financing = cfg['government_funding'] + cfg['loans_received']
            cash_outflows_financing = cfg['loans_repaid'] + cfg['interest_paid']
            net_financing = cash_inflows_financing - cash_outflows_financing
            
            net_change = net_operating + net_investing + net_financing
            closing_cash = net_change + cfg['opening_cash']
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Statement of Cash Flows", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Operating Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Cash received from government/grants", current_lang), f"{cfg['cash_from_grants']:,.2f}", ''])
            rows.append([get_ai_translation("Cash received from services/fees", current_lang), f"{cfg['cash_from_services']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Cash paid to employees", current_lang), f"({cfg['cash_to_employees']:,.2f})", ''])
            rows.append([get_ai_translation("Cash paid to suppliers", current_lang), f"({cfg['cash_to_suppliers']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Operating Activities", current_lang), '', f"{net_operating:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Investing Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Purchase of assets", current_lang), f"({cfg['purchase_assets']:,.2f})", ''])
            rows.append([get_ai_translation("Sale of assets", current_lang), f"{cfg['sale_assets']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Investing Activities", current_lang), '', f"{net_investing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Financing Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Government funding received", current_lang), f"{cfg['government_funding']:,.2f}", ''])
            rows.append([get_ai_translation("Loans received", current_lang), f"{cfg['loans_received']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Loans repaid", current_lang), f"({cfg['loans_repaid']:,.2f})", ''])
            rows.append([get_ai_translation("Interest paid", current_lang), f"({cfg['interest_paid']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Financing Activities", current_lang), '', f"{net_financing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Net Increase / (Decrease) in Cash", current_lang), '', f"{net_change:,.2f}" if net_change >= 0 else f"-{abs(net_change):,.2f}"])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Add: Opening Cash Balance", current_lang), '', f"{cfg['opening_cash']:,.2f}"])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Closing Cash Balance", current_lang), '', f"{closing_cash:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    elif is_nonprofit:
        st.subheader(get_ai_translation("Statement of Cash Flows", current_lang))
        
        with st.expander(get_ai_translation("📝 Enter Statement of Cash Flows Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Operating activities", current_lang))
            operating_receipts = st.number_input(get_ai_translation("Cash receipts from operations", current_lang), min_value=0.0, step=1000.0, key="np_cf_operating_receipts")
            operating_payments = st.number_input(get_ai_translation("Cash payments for operations", current_lang), min_value=0.0, step=1000.0, key="np_cf_operating_payments")
            
            st.subheader(get_ai_translation("Investing activities", current_lang))
            investing_inflows = st.number_input(get_ai_translation("Cash inflows from investing", current_lang), min_value=0.0, step=1000.0, key="np_cf_investing_in")
            investing_outflows = st.number_input(get_ai_translation("Cash outflows for investing", current_lang), min_value=0.0, step=1000.0, key="np_cf_investing_out")
            
            st.subheader(get_ai_translation("Financing activities", current_lang))
            financing_inflows = st.number_input(get_ai_translation("Cash inflows from financing", current_lang), min_value=0.0, step=1000.0, key="np_cf_financing_in")
            financing_outflows = st.number_input(get_ai_translation("Cash outflows for financing", current_lang), min_value=0.0, step=1000.0, key="np_cf_financing_out")
            
            opening_cash = st.number_input(get_ai_translation("Opening cash balance", current_lang), min_value=0.0, step=1000.0, key="np_cf_opening")

            currency = st.selectbox(get_ai_translation("Currency", current_lang), ["AED", "USD", "EUR", "GBP"], index=0, key="np_cf_currency")
            
            if st.button(get_ai_translation("📊 Generate Statement of Cash Flows", current_lang), type="primary", key="btn_np_cf"):
                st.session_state.cash_flow = {
                    "type": "nonprofit_cf",
                    "currency": currency,
                    "operating_receipts": operating_receipts, "operating_payments": operating_payments,
                    "investing_inflows": investing_inflows, "investing_outflows": investing_outflows,
                    "financing_inflows": financing_inflows, "financing_outflows": financing_outflows,
                    "opening_cash": opening_cash
                }
                st.success(get_ai_translation("✅ Statement of Cash Flows data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Statement of Cash Flows - {period}",
                    report_type="Statement of Cash Flows (Non-Profit)",
                    org_type=st.session_state.business_type,
                    data=st.session_state.cash_flow
                )

        cfg = st.session_state.get("cash_flow")
        if cfg and cfg.get("type") == "nonprofit_cf":
            currency = cfg.get('currency', 'AED')
            period = cfg.get('period', 'For the Year Ended 31 December 2024')
            
            net_operating = cfg['operating_receipts'] - cfg['operating_payments']
            net_investing = cfg['investing_inflows'] - cfg['investing_outflows']
            net_financing = cfg['financing_inflows'] - cfg['financing_outflows']
            net_change = net_operating + net_investing + net_financing
            closing_cash = net_change + cfg['opening_cash']
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Statement of Cash Flows", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Operating Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Cash receipts from operations", current_lang), f"{cfg['operating_receipts']:,.2f}", ''])
            rows.append([get_ai_translation("Cash payments for operations", current_lang), f"({cfg['operating_payments']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Operating Activities", current_lang), '', f"{net_operating:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Investing Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Cash inflows from investing", current_lang), f"{cfg['investing_inflows']:,.2f}", ''])
            rows.append([get_ai_translation("Cash outflows for investing", current_lang), f"({cfg['investing_outflows']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Investing Activities", current_lang), '', f"{net_investing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Financing Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Cash inflows from financing", current_lang), f"{cfg['financing_inflows']:,.2f}", ''])
            rows.append([get_ai_translation("Cash outflows for financing", current_lang), f"({cfg['financing_outflows']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Financing Activities", current_lang), '', f"{net_financing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Net Increase / (Decrease) in Cash", current_lang), '', f"{net_change:,.2f}" if net_change >= 0 else f"-{abs(net_change):,.2f}"])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Add: Opening Cash Balance", current_lang), '', f"{cfg['opening_cash']:,.2f}"])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Closing Cash Balance", current_lang), '', f"{closing_cash:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    else:
        st.subheader(get_ai_translation("Cash Flow Statement", current_lang))
        
        is_data = st.session_state.get("income_statement")
        bs_data = st.session_state.get("balance_sheet")
        cf_defaults = {}
        
        if is_data and is_data.get("type") == "income_statement":
            cf_defaults['depreciation_addback'] = is_data.get('depreciation', 0.0)
            net_sales = is_data['sales'] - is_data['sales_returns']
            cogs = is_data['opening_stock'] + is_data['purchases'] + is_data['carriage_in'] - is_data['closing_stock']
            gross_profit = net_sales - cogs
            other_income_total = is_data['rent_income'] + is_data['interest_received'] + is_data['misc_income']
            rent_exp = is_data['rent_paid'] + is_data['rent_accrued'] - is_data['rent_prepaid']
            insurance_exp = is_data['insurance_paid'] - is_data['insurance_prepaid']
            expenses_list = [is_data['wages_salaries'], rent_exp + insurance_exp, is_data['utilities'],
                            is_data['printing'] + is_data['postage'], is_data['discount_allowed'],
                            is_data['bad_debts'] + is_data['prov_doubtful_debts'], is_data['repairs'],
                            is_data['depreciation'], is_data['interest_expense'], is_data['general_expenses']]
            total_expenses = sum(expenses_list)
            cf_defaults['net_profit'] = gross_profit + other_income_total - total_expenses
            
        if bs_data:
            cf_defaults['opening_cash'] = bs_data.get('cash_bank', 0.0) + bs_data.get('cash_hand', 0.0)
        
        if cf_defaults.get('depreciation_addback'):
           st.session_state.cf_depreciation = cf_defaults['depreciation_addback']
        if cf_defaults.get('opening_cash'):
           st.session_state.cf_opening = cf_defaults['opening_cash']
        
        with st.expander(get_ai_translation("📝 Enter Cash Flow Data", current_lang), expanded=True):
            st.subheader(get_ai_translation("Operating Activities", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                cash_from_customers = st.number_input(get_ai_translation("Cash received from customers", current_lang), min_value=0.0, step=1000.0, key="cf_customers")
                cash_to_suppliers = st.number_input(get_ai_translation("Cash paid to suppliers", current_lang), min_value=0.0, step=1000.0, key="cf_suppliers")
                wages_paid = st.number_input(get_ai_translation("Wages paid", current_lang), min_value=0.0, step=100.0, key="cf_wages")
            with col2:
                rent_expenses_paid = st.number_input(get_ai_translation("Rent/expenses paid", current_lang), min_value=0.0, step=100.0, key="cf_rent")
                depreciation_addback = st.number_input(get_ai_translation("Adjustment: Depreciation (non-cash)", current_lang), min_value=0.0, step=100.0, key="cf_depreciation")
                wc_change = st.number_input(get_ai_translation("Adjustment: Working capital changes", current_lang), min_value=-1000000000.0, value=0.0, step=100.0, key="cf_wc")

            st.subheader(get_ai_translation("Investing Activities", current_lang))
            col3, col4 = st.columns(2)
            with col3:
                purchase_assets = st.number_input(get_ai_translation("Purchase of assets (machinery, land)", current_lang), min_value=0.0, step=10000.0, key="cf_purchase")
            with col4:
                sale_assets = st.number_input(get_ai_translation("Sale of assets", current_lang), min_value=0.0, step=1000.0, key="cf_sale")

            st.subheader(get_ai_translation("Financing Activities", current_lang))
            col5, col6 = st.columns(2)
            with col5:
                capital_introduced = st.number_input(get_ai_translation("Owner capital introduced", current_lang), min_value=0.0, step=10000.0, key="cf_capital")
                loan_received = st.number_input(get_ai_translation("Loan received/repayment", current_lang), min_value=-1000000000.0, value=0.0, step=1000.0, key="cf_loan")
            with col6:
                drawings_cf = st.number_input(get_ai_translation("Drawings", current_lang), min_value=0.0, step=1000.0, key="cf_drawings")
                interest_paid = st.number_input(get_ai_translation("Interest paid", current_lang), min_value=0.0, step=100.0, key="cf_interest")

            st.subheader(get_ai_translation("Final Output", current_lang))
            col7, col8 = st.columns(2)
            with col7:
                opening_cash = st.number_input(get_ai_translation("→ Opening cash balance", current_lang), min_value=0.0, step=1000.0, key="cf_opening")
            with col8:
                pass

            if st.button(get_ai_translation("📊 Generate Cash Flow Statement", current_lang), type="primary", key="btn_cf"):
                st.session_state.cash_flow = {
                    "cash_from_customers": cash_from_customers, "cash_to_suppliers": cash_to_suppliers,
                    "wages_paid": wages_paid, "rent_expenses_paid": rent_expenses_paid,
                    "depreciation_addback": depreciation_addback, "wc_change": wc_change,
                    "purchase_assets": purchase_assets, "sale_assets": sale_assets,
                    "capital_introduced": capital_introduced, "loan_received": loan_received,
                    "drawings_cf": drawings_cf, "interest_paid": interest_paid,
                    "opening_cash": opening_cash
                }
                st.success(get_ai_translation("✅ Cash Flow data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Cash Flow Statement - {period}",
                    report_type="Cash Flow Statement",
                    org_type=st.session_state.business_type,
                    data=st.session_state.cash_flow
                )
        
        cfg = st.session_state.get("cash_flow")
        if cfg:
            currency = 'AED'
            period = 'For the Year Ended 31 March 2025'
            
            net_operating = (cfg.get('cash_from_customers', 0) + cfg.get('cash_to_suppliers', 0) +
                           cfg.get('wages_paid', 0) + cfg.get('rent_expenses_paid', 0) +
                           cfg.get('depreciation_addback', 0) + cfg.get('wc_change', 0))
            net_investing = -cfg.get('purchase_assets', 0) + cfg.get('sale_assets', 0)
            net_financing = (cfg.get('capital_introduced', 0) + cfg.get('loan_received', 0) -
                           cfg.get('drawings_cf', 0) - cfg.get('interest_paid', 0))
            net_change = net_operating + net_investing + net_financing
            closing_cash = net_change + cfg.get('opening_cash', 0)
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Cash Flow Statement", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Operating Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Cash received from customers", current_lang), f"{cfg.get('cash_from_customers', 0):,.2f}", ''])
            rows.append([get_ai_translation("Cash paid to suppliers", current_lang), f"({abs(cfg.get('cash_to_suppliers', 0)):,.2f})" if cfg.get('cash_to_suppliers', 0) < 0 else f"{cfg.get('cash_to_suppliers', 0):,.2f}", ''])
            rows.append([get_ai_translation("Wages paid", current_lang), f"({abs(cfg.get('wages_paid', 0)):,.2f})" if cfg.get('wages_paid', 0) < 0 else f"{cfg.get('wages_paid', 0):,.2f}", ''])
            rows.append([get_ai_translation("Rent/expenses paid", current_lang), f"({abs(cfg.get('rent_expenses_paid', 0)):,.2f})" if cfg.get('rent_expenses_paid', 0) < 0 else f"{cfg.get('rent_expenses_paid', 0):,.2f}", ''])
            rows.append([get_ai_translation("Adjustment: Depreciation (non-cash)", current_lang), f"{cfg.get('depreciation_addback', 0):,.2f}", ''])
            rows.append([get_ai_translation("Adjustment: Working capital changes", current_lang), f"{cfg.get('wc_change', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Operating Activities", current_lang), '', f"{net_operating:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Investing Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Purchase of assets (machinery, land)", current_lang), f"({cfg.get('purchase_assets', 0):,.2f})", ''])
            rows.append([get_ai_translation("Sale of assets", current_lang), f"{cfg.get('sale_assets', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Investing Activities", current_lang), '', f"{net_investing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Cash Flow from Financing Activities", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Owner capital introduced", current_lang), f"{cfg.get('capital_introduced', 0):,.2f}", ''])
            rows.append([get_ai_translation("Loan received/repayment", current_lang), f"{cfg.get('loan_received', 0):,.2f}", ''])
            rows.append([get_ai_translation("Drawings", current_lang), f"({cfg.get('drawings_cf', 0):,.2f})", ''])
            rows.append([get_ai_translation("Interest paid", current_lang), f"({cfg.get('interest_paid', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Net Cash from Financing Activities", current_lang), '', f"{net_financing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Net Increase / (Decrease) in Cash", current_lang), '', f"{net_change:,.2f}" if net_change >= 0 else f"-{abs(net_change):,.2f}"])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Add: Opening Cash Balance", current_lang), '', f"{cfg.get('opening_cash', 0):,.2f}"])
            rows.append(['', '', ''])
            rows.append([get_ai_translation("Closing Cash Balance", current_lang), '', f"{closing_cash:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 4: APPROPRIATION ACCOUNT
# ============================================================================
with tab4:
    st.subheader(get_ai_translation("Appropriation Account", current_lang))
    
    if st.session_state.business_type != "Partnership":
        st.info(get_ai_translation("👥 Appropriation Account is only available for Partnerships. Select 'Partnership' in Organization Type in the sidebar.", current_lang))
    else:
        is_data = st.session_state.get("income_statement")
        net_profit_default = 0.0
        
        if is_data and is_data.get("type") == "income_statement":
            net_sales = is_data['sales'] - is_data['sales_returns']
            cogs = is_data['opening_stock'] + is_data['purchases'] + is_data['carriage_in'] - is_data['closing_stock']
            gross_profit = net_sales - cogs
            other_income_total = is_data['rent_income'] + is_data['interest_received'] + is_data['misc_income']
            rent_exp = is_data['rent_paid'] + is_data['rent_accrued'] - is_data['rent_prepaid']
            insurance_exp = is_data['insurance_paid'] - is_data['insurance_prepaid']
            expenses_list = [is_data['wages_salaries'], rent_exp + insurance_exp, is_data['utilities'],
                            is_data['printing'] + is_data['postage'], is_data['discount_allowed'],
                            is_data['bad_debts'] + is_data['prov_doubtful_debts'], is_data['repairs'],
                            is_data['depreciation'], is_data['interest_expense'], is_data['general_expenses']]
            total_expenses = sum(expenses_list)
            net_profit_default = gross_profit + other_income_total - total_expenses
        
        if net_profit_default:
            st.session_state.app_net_profit = net_profit_default

        with st.expander(get_ai_translation("📝 Enter Appropriation Account Data", current_lang), expanded=True):
            net_profit = st.number_input(get_ai_translation("Net Profit (from Income Statement)", current_lang), min_value=-1000000000.0, value=0.00, step=100.0, key="app_net_profit")
            
            st.subheader(get_ai_translation("Partnership Details", current_lang))
            col1, col2 = st.columns(2)
            with col1:
                p1_name = st.text_input(get_ai_translation("Partner 1 Name", current_lang), "Partner A", key="app_p1_name")
                p1_capital = st.number_input(get_ai_translation(f"{p1_name} Capital", current_lang), min_value=0.0, step=10000.0, key="app_p1_cap")
                p1_drawings = st.number_input(get_ai_translation(f"{p1_name} Drawings", current_lang), min_value=0.0, step=1000.0, key="app_p1_draw")
                p1_salary = st.number_input(get_ai_translation(f"{p1_name} Salary", current_lang), min_value=0.0, step=1000.0, key="app_p1_salary")
                p1_int_cap_rate = st.number_input(get_ai_translation(f"{p1_name} Interest on Capital %", current_lang), min_value=0.0, step=0.5, key="app_p1_int_rate")
            with col2:
                p2_name = st.text_input(get_ai_translation("Partner 2 Name", current_lang), "Partner B", key="app_p2_name")
                p2_capital = st.number_input(get_ai_translation(f"{p2_name} Capital", current_lang), min_value=0.0, step=10000.0, key="app_p2_cap")
                p2_drawings = st.number_input(get_ai_translation(f"{p2_name} Drawings", current_lang), min_value=0.0, step=1000.0, key="app_p2_draw")
                p2_salary = st.number_input(get_ai_translation(f"{p2_name} Salary", current_lang), min_value=0.0, step=1000.0, key="app_p2_salary")
                p2_int_cap_rate = st.number_input(get_ai_translation(f"{p2_name} Interest on Capital %", current_lang), min_value=0.0, step=0.5, key="app_p2_int_rate")
            
            drawings_interest_rate = st.number_input(
                get_ai_translation("Interest rate on drawings (%)", current_lang),
                min_value=0.0,
                max_value=20.0,
                value=5.0,
                step=0.5,
                key="app_drawings_rate"
            )
            
            profit_ratio = st.selectbox(get_ai_translation("Profit Sharing Ratio", current_lang), ["50:50", "60:40", "40:60", "70:30", "30:70"], key="app_ratio")
            
            if st.button(get_ai_translation("📊 Generate Appropriation Account", current_lang), type="primary", key="btn_app"):
                st.session_state.appropriation = {
                    "net_profit": net_profit,
                    "p1": {"name": p1_name, "capital": p1_capital, "drawings": p1_drawings, "salary": p1_salary, "int_cap_rate": p1_int_cap_rate},
                    "p2": {"name": p2_name, "capital": p2_capital, "drawings": p2_drawings, "salary": p2_salary, "int_cap_rate": p2_int_cap_rate},
                    "ratio": profit_ratio,
                    "drawings_rate": drawings_interest_rate
                }
                st.success(get_ai_translation("✅ Appropriation Account data saved!", current_lang))
                st.balloons()
                
                save_report(
                    report_name=f"Appropriation Account - {period}",
                    report_type="Appropriation Account",
                    org_type=st.session_state.business_type,
                    data=st.session_state.appropriation
                )
                        
        cfg = st.session_state.get("appropriation")
        if cfg:
            currency = 'AED'
            period = 'For the Year Ended 31 March 2025'
            
            p1 = cfg['p1']
            p2 = cfg['p2']
            
            drawings_rate = cfg.get('drawings_rate', 5.0)
            
            p1_int_cap = p1['capital'] * (p1['int_cap_rate'] / 100)
            p2_int_cap = p2['capital'] * (p2['int_cap_rate'] / 100)
            total_int_cap = p1_int_cap + p2_int_cap
            
            p1_sal = p1['salary']
            p2_sal = p2['salary']
            total_sal = p1_sal + p2_sal
            
            p1_int_draw = p1['drawings'] * (drawings_rate / 100)
            p2_int_draw = p2['drawings'] * (drawings_rate / 100)
            total_int_draw = p1_int_draw + p2_int_draw
            
            remaining = cfg['net_profit'] - total_int_cap - total_sal + total_int_draw
            
            ratio = cfg['ratio']
            r_parts = ratio.split(':')
            r1, r2 = int(r_parts[0]), int(r_parts[1])
            total_ratio = r1 + r2
            p1_share = remaining * (r1 / total_ratio)
            p2_share = remaining * (r2 / total_ratio)
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([get_ai_translation("Appropriation Account", current_lang), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Net Profit for the Year", current_lang), '', f"{cfg['net_profit']:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Less: Appropriations", current_lang), '', ''])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Partner Salaries", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([f"{p1['name']}", f"{p1_sal:,.2f}", ''])
            rows.append([f"{p2['name']}", f"{p2_sal:,.2f}", ''])
            rows.append([get_ai_translation("Total Salaries", current_lang), '', f"({total_sal:,.2f})"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Interest on Capital", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([f"{p1['name']}", f"{p1_int_cap:,.2f}", ''])
            rows.append([f"{p2['name']}", f"{p2_int_cap:,.2f}", ''])
            rows.append([get_ai_translation("Total Interest on Capital", current_lang), '', f"({total_int_cap:,.2f})"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Add: Interest on Drawings", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([f"{p1['name']}", f"{p1_int_draw:,.2f}", ''])
            rows.append([f"{p2['name']}", f"{p2_int_draw:,.2f}", ''])
            rows.append([get_ai_translation("Total Interest on Drawings", current_lang), '', f"{total_int_draw:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation("Residual Profit", current_lang), '', f"{remaining:,.2f}" if remaining >= 0 else f"-{abs(remaining):,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([get_ai_translation(f"Shared in Ratio {ratio}", current_lang), '', ''])
            rows.append(['', '', ''])
            rows.append([f"{p1['name']}", f"{abs(p1_share):,.2f}", ''])
            rows.append([f"{p2['name']}", f"{abs(p2_share):,.2f}", ''])
            
            rows.append([get_ai_translation("Total Appropriated", current_lang), '', f"{cfg['net_profit']:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 5: FINANCIAL RATIOS
# ============================================================================
with tab5:
    st.subheader(get_ai_translation("📈 Financial Ratios Calculator", current_lang))
    
    st.write(f"**{get_ai_translation('Category:', current_lang)}** {selected_category}")
    st.write("---")
    
    ratios = RATIOS_DB[selected_category]
    
    for ratio_name, ratio_info in ratios.items():
        with st.expander(f"📐 {get_ai_translation(ratio_name, current_lang)}", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(get_ai_translation("Formula", current_lang))
                st.markdown(f"""
                <div style="background-color: #2d2d2d; padding: 15px; border-radius: 5px; text-align: center; font-size: 1.1em; border-left: 4px solid #4CAF50;">
                    {get_ai_translation(ratio_info['formula'], current_lang)}
                </div>
                """, unsafe_allow_html=True)
                st.markdown(get_ai_translation("### Input Values", current_lang))
                input_values = {}
                cols = st.columns(min(len(ratio_info['inputs']), 3))
                for idx, input_name in enumerate(ratio_info['inputs']):
                    with cols[idx % 3]:
                        input_values[input_name] = st.number_input(
                            get_ai_translation(input_name, current_lang), min_value=0.0, step=100.0,
                            key=f"{ratio_name}_{input_name}"
                        )
                if st.button(get_ai_translation("🔢 Calculate", current_lang), key=f"calc_{ratio_name}"):
                    try:
                        values = [input_values[input_name] for input_name in ratio_info['inputs']]
                        result = ratio_info['calculation'](*values)
                        st.markdown(get_ai_translation("### Result", current_lang))
                        unit_str = ""
                        if ratio_info['unit'] == 'percentage': unit_str = "%"
                        elif ratio_info['unit'] == 'days': unit_str = get_ai_translation(" days", current_lang)
                        elif ratio_info['unit'] == 'times': unit_str = "x"
                        st.markdown(f"""
                        <div style="background-color: #4CAF50; color: white; padding: 15px; border-radius: 5px; text-align: center; font-size: 1.3em; font-weight: bold;">
                            {result:.2f}{unit_str}
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(get_ai_translation(f"Error: {str(e)}", current_lang))
            with col2:
                st.subheader(get_ai_translation("Information", current_lang))
                st.markdown(f"""
                **{get_ai_translation('Inputs:', current_lang)}** {len(ratio_info['inputs'])}
                
                **{get_ai_translation('Output:', current_lang)}** {ratio_info['unit'].title()}
                
                **{get_ai_translation('Required:', current_lang)}**
                """)
                for input_name in ratio_info['inputs']:
                    st.write(f"• {get_ai_translation(input_name, current_lang)}")

st.markdown("---")
st.caption(get_ai_translation("DGP Finance • Offline • Python • Streamlit • © 2024", current_lang))