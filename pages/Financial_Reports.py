import streamlit as st
import pandas as pd
from statements import (
    generate_income_statement,
    generate_balance_sheet,
    generate_cash_flow,
    generate_appropriation_account,
    RATIOS_DB
)
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

from portfolio_manager import save_report

st.set_page_config(page_title="DGP Finance", layout="wide", page_icon="💰")

# ================= TRANSLATION SYSTEM =================
from translation_ui import init_translation, render_translation_sidebar, t

# Initialize translation (handles lang + toggle)
init_translation()

# Keep ONLY non-translation session state
if 'business_type' not in st.session_state:
    st.session_state.business_type = 'Sole Trader'

# Sidebar
with st.sidebar:
    render_translation_sidebar()

# Organization Type Selector
business_types = [
    "Sole Trader",
    "Partnership",
    "Private Limited Company (Ltd)",
    "Public Limited Company (PLC)",
    "Public Sector",
    "Non-Profit Organization"
]

# Translate for display
translated_types = [t(bt) for bt in business_types]

# Select translated value
selected_translated = st.sidebar.selectbox(
    t("Organization Type"),
    options=translated_types,
    index=translated_types.index(t(st.session_state.business_type)),
    key="org_type_selector"
)

# Map back to original English value
st.session_state.business_type = business_types[
    translated_types.index(selected_translated)
]

st.sidebar.markdown("---")
st.sidebar.header(t("Select Ratio Category"))

# Translate options properly
ratio_keys = list(RATIOS_DB.keys())
translated_options = [t(k) for k in ratio_keys]

selected_translated = st.sidebar.selectbox(
    t("Choose a ratio category:"),
    options=translated_options,
    key="ratio_category"
)

# Map back to original key
selected_category = ratio_keys[translated_options.index(selected_translated)]

# Check if Non-Profit
is_nonprofit = st.session_state.business_type == "Non-Profit Organization"

# Check if Public Sector
is_public_sector = st.session_state.business_type == "Public Sector"

# MAIN CONTENT
st.title(t("DGP Finance"))
st.subheader(t("Financial Statement Generator"))

# TABS - Dynamic titles based on organization type
if is_nonprofit:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t("📊 Statement of Activities"),
        t("📋 Statement of Financial Position"),
        t("💵 Statement of Cash Flows"),
        t("👥 Appropriation Account"),
        t("📈 Financial Ratios")
    ])
elif is_public_sector:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t("📊 Statement of Financial Performance"),
        t("📋 Statement of Financial Position"),
        t("💵 Statement of Cash Flows"),
        t("👥 Appropriation Account"),
        t("📈 Financial Ratios")
    ])
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t("📊 Income Statement / Profit & Loss (P&L)"),
        t("📋 Statement of Financial Position (Balance Sheet)"),
        t("💵 Cash Flow Statement"),
        t("👥 Appropriation Account"),
        t("📈 Financial Ratios")
    ])

# ============================================================================
# TAB 1: INCOME STATEMENT / STATEMENT OF ACTIVITIES
# ============================================================================
with tab1:
    if is_public_sector:
        st.subheader(t("Statement of Financial Performance"))
        
        with st.expander(t("📝 Enter Statement of Financial Performance Data"), expanded=True):
            st.subheader(t("Revenue"))
            col1, col2 = st.columns(2)
            with col1:
                period = st.text_input(t("Reporting Period"), t("Year Ended 31 March 2025"), key="ps_period")
                government_grants = st.number_input(t("Government Grants / Funding"), min_value=0.0, step=10000.0, key="ps_grants")
                tax_revenue = st.number_input(t("Tax Revenue (if applicable)"), min_value=0.0, step=10000.0, key="ps_tax")
            with col2:
                currency = st.selectbox(t("Currency"), ["AED", "USD", "EUR", "GBP"], index=0, key="ps_currency")
                service_revenue = st.number_input(t("Service Revenue (fees, licenses)"), min_value=0.0, step=1000.0, key="ps_service")
                other_income = st.number_input(t("Other Income"), min_value=0.0, step=1000.0, key="ps_other_income")

            st.subheader(t("Expenses"))
            col3, col4, col5 = st.columns(3)
            with col3:
                employee_costs = st.number_input(t("Employee Costs (Wages & Salaries)"), min_value=0.0, step=1000.0, key="ps_employee")
                admin_expenses = st.number_input(t("Administrative Expenses"), min_value=0.0, step=1000.0, key="ps_admin")
                utilities = st.number_input(t("Utilities"), min_value=0.0, step=1000.0, key="ps_utilities")
            with col4:
                repairs_maintenance = st.number_input(t("Repairs & Maintenance"), min_value=0.0, step=1000.0, key="ps_repairs")
                depreciation = st.number_input(t("Depreciation"), min_value=0.0, step=1000.0, key="ps_depreciation")
                interest_expense = st.number_input(t("Interest Expense"), min_value=0.0, step=1000.0, key="ps_interest")
            with col5:
                program_costs = st.number_input(t("Program / Service Delivery Costs"), min_value=0.0, step=1000.0, key="ps_program")
                other_expenses = st.number_input(t("Other Operating Expenses"), min_value=0.0, step=1000.0, key="ps_other_exp")

            if st.button(t("📊 Generate Statement of Financial Performance"), type="primary", key="btn_ps_performance"):
                st.session_state.income_statement = {
                    "type": "public_sector_performance", "period": period, "currency": currency,
                    "government_grants": government_grants, "tax_revenue": tax_revenue,
                    "service_revenue": service_revenue, "other_income": other_income,
                    "employee_costs": employee_costs, "admin_expenses": admin_expenses,
                    "utilities": utilities, "repairs_maintenance": repairs_maintenance,
                    "depreciation": depreciation, "interest_expense": interest_expense,
                    "program_costs": program_costs, "other_expenses": other_expenses
                }
                st.success(t("✅ Statement of Financial Performance data saved!"))
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
            rows.append([t("Statement of Financial Performance"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("Revenue"), '', ''])
            rows.append(['', '', ''])
            rows.append([t(" Government Grants / Funding"), f"{cfg['government_grants']:,.2f}", ''])
            rows.append([t("Tax Revenue (if applicable)"), f"{cfg['tax_revenue']:,.2f}", ''])
            rows.append([t("Service Revenue (fees, licenses)"), f"{cfg['service_revenue']:,.2f}", ''])
            rows.append([t("Other Income"), f"{cfg['other_income']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Revenue"), '', f"{total_revenue:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Expenses"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Employee Costs (Wages & Salaries)"), f"{cfg['employee_costs']:,.2f}", ''])
            rows.append([t("Administrative Expenses"), f"{cfg['admin_expenses']:,.2f}", ''])
            rows.append([t("Utilities"), f"{cfg['utilities']:,.2f}", ''])
            rows.append([t("Repairs & Maintenance"), f"{cfg['repairs_maintenance']:,.2f}", ''])
            rows.append([t("Depreciation"), f"{cfg['depreciation']:,.2f}", ''])
            rows.append([t("Interest Expense"), f"{cfg['interest_expense']:,.2f}", ''])
            rows.append([t("Program / Service Delivery Costs"), f"{cfg['program_costs']:,.2f}", ''])
            rows.append([t("Other Operating Expenses"), f"{cfg['other_expenses']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Expenses"), '', f"({total_expenses:,.2f})"])
            rows.append(['', '', ''])
            
            result_label = t("Surplus") if surplus_deficit >= 0 else t("Deficit")
            rows.append([result_label, '', f"{surplus_deficit:,.2f}" if surplus_deficit >= 0 else f"-{abs(surplus_deficit):,.2f}"])

            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    elif is_nonprofit:
        st.subheader(t("Statement of Activities"))
        
        with st.expander(t("📝 Enter Statement of Activities Data"), expanded=True):
            st.subheader(t("Income / Inflows"))
            col1, col2 = st.columns(2)
            with col1:
                period = st.text_input(t("Reporting Period"), t("Year Ended 31 December 2024"), key="np_period")
                donations = st.number_input(t("Donations"), min_value=0.0, step=1000.0, key="np_donations")
                grants = st.number_input(t("Grants"), min_value=0.0, step=1000.0, key="np_grants")
            with col2:
                membership_fees = st.number_input(t("Membership fees"), min_value=0.0, step=1000.0, key="np_membership")
                fundraising_income = st.number_input(t("Fundraising income"), min_value=0.0, step=1000.0, key="np_fundraising")
                currency = st.selectbox(t("Currency"), ["AED", "USD", "EUR", "GBP"], index=0, key="np_currency")                

            st.subheader(t("Expenses"))
            col3, col4, col5 = st.columns(3)
            with col3:
                program_expenses = st.number_input(t("Program expenses (core mission activities)"), min_value=0.0, step=1000.0, key="np_program")
            with col4:
                admin_expenses = st.number_input(t("Administrative expenses"), min_value=0.0, step=1000.0, key="np_admin")
            with col5:
                fundraising_costs = st.number_input(t("Fundraising costs"), min_value=0.0, step=1000.0, key="np_fundraising_costs")

            if st.button(t("📊 Generate Statement of Activities"), type="primary", key="btn_np_activities"):
                st.session_state.income_statement = {
                    "type": "nonprofit_activities", "period": period, "currency": currency,
                    "donations": donations, "grants": grants,
                    "membership_fees": membership_fees, "fundraising_income": fundraising_income,
                    "program_expenses": program_expenses, "admin_expenses": admin_expenses,
                    "fundraising_costs": fundraising_costs
                }
                st.success(t("✅ Statement of Activities data saved!"))
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
            rows.append([t("Statement of Activities"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("Income / Inflows"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Donations"), f"{cfg['donations']:,.2f}", ''])
            rows.append([t("Grants"), f"{cfg['grants']:,.2f}", ''])
            rows.append([t("Membership fees"), f"{cfg['membership_fees']:,.2f}", ''])
            rows.append([t("Fundraising income"), f"{cfg['fundraising_income']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Income"), '', f"{total_income:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Expenses"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Program expenses"), f"{cfg['program_expenses']:,.2f}", ''])
            rows.append([t("Administrative expenses"), f"{cfg['admin_expenses']:,.2f}", ''])
            rows.append([t("Fundraising costs"), f"{cfg['fundraising_costs']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Expenses"), '', f"({total_expenses:,.2f})"])
            
            result_label = t("Net Surplus") if surplus_deficit >= 0 else t("Net Deficit")
            rows.append([result_label, '', f"{surplus_deficit:,.2f}" if surplus_deficit >= 0 else f"-{abs(surplus_deficit):,.2f}"])

            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)            
    
    else:
        st.subheader(t("Income Statement / Profit & Loss (P&L)"))
        
        with st.expander(t("📝 Enter Income Statement Data"), expanded=True):
            st.subheader(t("Revenue / Trading"))
            col1, col2 = st.columns(2)
            with col1:
                sales = st.number_input(t("Sales Revenue"), min_value=0.0, step=1000.0, key="is_sales")
                sales_returns = st.number_input(t("Less: Returns (if any)"), min_value=0.0, step=100.0, key="is_returns")
                opening_stock = st.number_input(t("Opening Stock"), min_value=0.0, step=1000.0, key="is_opening_stock")
                purchases = st.number_input(t("Purchases"), min_value=0.0, step=1000.0, key="is_purchases")
                carriage_in = st.number_input(t("Carriage Inwards"), min_value=0.0, step=100.0, key="is_carriage")
                closing_stock = st.number_input(t("– Closing Stock"), min_value=0.0, step=1000.0, key="is_closing_stock")
            with col2:
                period = st.text_input(t("Reporting Period"), t("Year Ended 31 March 2025"), key="is_period")
                currency = st.selectbox(t("Currency"), ["AED", "USD", "EUR", "GBP"], index=0, key="is_currency")
                rent_income = st.number_input(t("Rent income"), min_value=0.0, step=100.0, key="is_rent_income")
                interest_received = st.number_input(t("Interest received"), min_value=0.0, step=100.0, key="is_interest_received")
                misc_income = st.number_input(t("Miscellaneous income"), min_value=0.0, step=100.0, key="is_misc_income")

            st.subheader(t("Expenses"))
            col3, col4, col5 = st.columns(3)
            with col3:
                wages_salaries = st.number_input(t("Wages & Salaries"), min_value=0.0, step=100.0, key="is_wages")
                rent_paid = st.number_input(t("Rent Paid"), min_value=0.0, step=100.0, key="is_rent_paid")
                rent_prepaid = st.number_input(t("Rent Prepaid"), min_value=0.0, step=100.0, key="is_rent_prepaid")
                rent_accrued = st.number_input(t("Rent Accrued"), min_value=0.0, step=100.0, key="is_rent_accrued")
                insurance_paid = st.number_input(t("Insurance Paid"), min_value=0.0, step=100.0, key="is_ins_paid")
                insurance_prepaid = st.number_input(t("Insurance Prepaid"), min_value=0.0, step=100.0, key="is_ins_prepaid")
            with col4:
                utilities = st.number_input(t("Utilities (lighting, etc.)"), min_value=0.0, step=100.0, key="is_utilities")
                postage = st.number_input(t("Postage"), min_value=0.0, step=100.0, key="is_postage")
                printing = st.number_input(t("Office expenses (printing)"), min_value=0.0, step=100.0, key="is_printing")
                discount_allowed = st.number_input(t("Discount Allowed"), min_value=0.0, step=100.0, key="is_discount")
                bad_debts = st.number_input(t("Bad Debts"), min_value=0.0, step=100.0, key="is_bad_debts")
                prov_doubtful_debts = st.number_input(t("Provision for Doubtful Debts"), min_value=0.0, step=100.0, key="is_prov_debts")
            with col5:
                repairs = st.number_input(t("Repairs & Maintenance"), min_value=0.0, step=100.0, key="is_repairs")
                depreciation = st.number_input(t("Depreciation (non-cash expense)"), min_value=0.0, step=100.0, key="is_depreciation")
                interest_expense = st.number_input(t("Interest Expense"), min_value=0.0, step=100.0, key="is_interest_exp")
                general_expenses = st.number_input(t("General expenses"), min_value=0.0, step=100.0, key="is_general_exp")

            if st.button(t("📊 Generate Income Statement"), type="primary", key="btn_is"):
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
                st.success(t("✅ Income Statement data saved!"))
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
                (t("Wages & Salaries"), cfg['wages_salaries']),
                (t("Rent & Insurance (adjusted)"), rent_exp + insurance_exp),
                (t("Utilities (lighting, etc.)"), cfg['utilities']),
                (t("Office expenses (printing, postage)"), cfg['printing'] + cfg['postage']),
                (t("Discount Allowed"), cfg['discount_allowed']),
                (t("Bad Debts + Provision"), cfg['bad_debts'] + cfg['prov_doubtful_debts']),
                (t("Repairs & Maintenance"), cfg['repairs']),
                (t("Depreciation (non-cash expense)"), cfg['depreciation']),
                (t("Interest Expense"), cfg['interest_expense']),
                (t("General expenses"), cfg['general_expenses'])
            ]
            total_expenses = sum(x[1] for x in expenses_list)
            net_profit = gross_profit + other_income_total - total_expenses
            
            rows = []
            rows.append(['DGP Finance Client', '', ''])
            rows.append([t("Income Statement / Profit & Loss (P&L)"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("Revenue"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Sales Revenue"), f"{cfg['sales']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Less: Returns"), f"({cfg['sales_returns']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Sales"), '', f"{net_sales:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Cost of Sales"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Opening Stock"), f"{cfg['opening_stock']:,.2f}", ''])
            rows.append([t("Purchases"), f"{cfg['purchases']:,.2f}", ''])
            rows.append([t("Carriage Inwards"), f"{cfg['carriage_in']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Less: Closing Stock"), f"({cfg['closing_stock']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Cost of Sales"), '', f"({cogs:,.2f})"])
            rows.append(['', '', ''])
            
            rows.append([t("Gross Profit"), '', f"{gross_profit:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Other Income"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Rent income"), f"{cfg['rent_income']:,.2f}", ''])
            rows.append([t("Interest received"), f"{cfg['interest_received']:,.2f}", ''])
            rows.append([t("Miscellaneous income"), f"{cfg['misc_income']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Other Income"), '', f"{other_income_total:,.2f}"])
            rows.append(['', '', ''])
            
            pbe = gross_profit + other_income_total
            rows.append([t("Profit Before Expenses"), '', f"{pbe:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Expenses"), '', ''])
            rows.append(['', '', ''])
            for item_name, item_value in expenses_list:
                rows.append([item_name, f"{item_value:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Expenses"), '', f"({total_expenses:,.2f})"])
            rows.append(['', '', ''])
            
            rows.append([t("Net Profit"), '', f"{net_profit:,.2f}" if net_profit >= 0 else f"-{abs(net_profit):,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 2: STATEMENT OF FINANCIAL POSITION
# ============================================================================
with tab2:
    if is_public_sector:
        st.subheader(t("Statement of Financial Position"))
        
        auto_import_data = {}
        is_data = st.session_state.get("income_statement")

        if is_data and is_data.get("type") == "public_sector_performance":
            total_revenue = is_data['government_grants'] + is_data['tax_revenue'] + is_data['service_revenue'] + is_data['other_income']
            total_expenses = (is_data['employee_costs'] + is_data['admin_expenses'] + is_data['utilities'] +
                            is_data['repairs_maintenance'] + is_data['depreciation'] + is_data['interest_expense'] +
                            is_data['program_costs'] + is_data['other_expenses'])
            auto_import_data['surplus_deficit'] = total_revenue - total_expenses
            auto_import_data['currency'] = is_data.get('currency', 'AED')

        with st.expander(t("📝 Enter Statement of Financial Position Data"), expanded=True):
            st.subheader(t("Assets"))
            col1, col2 = st.columns(2)
            with col1:
                land_building = st.number_input(t("Land & Buildings"), min_value=0.0, step=10000.0, key="ps_bs_land")
                equipment = st.number_input(t("Equipment / Machinery"), min_value=0.0, step=10000.0, key="ps_bs_equipment")
                furniture = st.number_input(t("Furniture"), min_value=0.0, step=1000.0, key="ps_bs_furniture")
            with col2:
                accumulated_depreciation = st.number_input(t("Less: Accumulated Depreciation"), min_value=0.0, step=1000.0, key="ps_bs_acc_dep")

            st.subheader(t("Current Assets"))
            col3, col4 = st.columns(2)
            with col3:
                receivables = st.number_input(t("Receivables"), min_value=0.0, step=1000.0, key="ps_bs_receivables")
            with col4:
                cash_equivalents = st.number_input(t("Cash and Cash Equivalents"), min_value=0.0, step=1000.0, key="ps_bs_cash")
                
            st.subheader(t("Liabilities"))
            col5, col6 = st.columns(2)
            with col5:
                payables = st.number_input(t("Payables"), min_value=0.0, step=1000.0, key="ps_bs_payables")
            with col6:
                accrued_expenses = st.number_input(t("Accrued Expenses"), min_value=0.0, step=100.0, key="ps_bs_accrued")

            st.subheader(t("Non-Current Liabilities"))
            col7, col8 = st.columns(2)
            with col7:
                loans = st.number_input(t("Loans / Borrowings"), min_value=0.0, step=10000.0, key="ps_bs_loans")

            st.subheader(t("Net Assets"))
            col9, col10 = st.columns(2)
            with col9:
                accumulated_surplus = st.number_input(t("Opening Accumulated Surplus / (Deficit)"), min_value=0.0, step=10000.0, key="ps_bs_open_surplus")
            with col10:
                pass

            if st.button(t("📊 Generate Statement of Financial Position"), type="primary", key="btn_ps_bs"):
                st.session_state.balance_sheet = {
                    "type": "public_sector_bs",
                    "land_building": land_building, "equipment": equipment, "furniture": furniture,
                    "accumulated_depreciation": accumulated_depreciation,
                    "receivables": receivables, "cash_equivalents": cash_equivalents,
                    "payables": payables, "accrued_expenses": accrued_expenses,
                    "loans": loans, "accumulated_surplus": accumulated_surplus
                }
                st.success(t("✅ Statement of Financial Position data saved!"))
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
            rows.append([t("Statement of Financial Position"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("Assets"), '', ''])
            rows.append(['', '', ''])
            
            rows.append([t("Non-Current Assets"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Land & Buildings"), f"{cfg.get('land_building', 0):,.2f}", ''])
            rows.append([t("Equipment / Machinery"), f"{cfg.get('equipment', 0):,.2f}", ''])
            rows.append([t("Furniture"), f"{cfg.get('furniture', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Less: Accumulated Depreciation"), f"({cfg.get('accumulated_depreciation', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Non-Current Assets"), '', f"{nca_net:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Current Assets"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Receivables"), f"{cfg.get('receivables', 0):,.2f}", ''])
            rows.append([t("Cash and Cash Equivalents"), f"{cfg.get('cash_equivalents', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Current Assets"), '', f"{current_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("TOTAL ASSETS"), '', f"{total_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Net Assets / Equity"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Opening Accumulated Surplus"), f"{cfg.get('accumulated_surplus', 0):,.2f}", ''])
            rows.append([t("Surplus / (Deficit) for the Year"), f"{surplus_for_year:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Closing Accumulated Surplus"), '', f"{closing_net_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Liabilities"), '', ''])
            rows.append(['', '', ''])
            
            rows.append([t("Non-Current Liabilities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Loans / Borrowings"), f"{cfg.get('loans', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Non-Current Liabilities"), '', f"{ncl_total:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Current Liabilities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Payables"), f"{cfg.get('payables', 0):,.2f}", ''])
            rows.append([t("Accrued Expenses"), f"{cfg.get('accrued_expenses', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Current Liabilities"), '', f"{current_liabilities:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("TOTAL NET ASSETS & LIABILITIES"), '', f"{total_liabilities_equity:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if abs(total_assets - total_liabilities_equity) < 0.01:
                st.success(t("✅ Statement balances correctly!"))
            else:
                st.warning(t(f"⚠️ Statement imbalance: {abs(total_assets - total_liabilities_equity):,.2f} {currency} difference"))

    elif is_nonprofit:
        st.subheader(t("Statement of Financial Position"))
        
        auto_import_data = {}
        is_data = st.session_state.get("income_statement")
        
        if is_data and is_data.get("type") == "nonprofit_activities":
            total_income = is_data['donations'] + is_data['grants'] + is_data['membership_fees'] + is_data['fundraising_income']
            total_expenses = is_data['program_expenses'] + is_data['admin_expenses'] + is_data['fundraising_costs']
            auto_import_data['net_profit'] = total_income - total_expenses

        with st.expander(t("📝 Enter Statement of Financial Position Data"), expanded=True):
            st.subheader(t("Non-Current Assets"))
            col1, col2 = st.columns(2)
            with col1:
                land_building = st.number_input(t("Land & Buildings"), min_value=0.0, step=10000.0, key="np_bs_land")
                machinery = st.number_input(t("Machinery"), min_value=0.0, step=10000.0, key="np_bs_machinery")
                furniture = st.number_input(t("Furniture"), min_value=0.0, step=1000.0, key="np_bs_furniture")
            with col2:
                accumulated_depreciation = st.number_input(t("Less: Accumulated Depreciation"), min_value=0.0, step=1000.0, key="np_bs_acc_dep")

            st.subheader(t("Current Assets"))
            col3, col4 = st.columns(2)
            with col3:
                inventory = st.number_input(t("Inventory"), min_value=0.0, step=1000.0, key="np_bs_inventory")
                debtors = st.number_input(t("Debtors"), min_value=0.0, step=1000.0, key="np_bs_debtors")
                bills_receivable = st.number_input(t("Bills Receivable"), min_value=0.0, step=1000.0, key="np_bs_bills_rec")
            with col4:
                cash_hand = st.number_input(t("Cash in Hand"), min_value=0.0, step=100.0, key="np_bs_cash_hand")
                cash_bank = st.number_input(t("Cash at Bank"), min_value=0.0, step=1000.0, key="np_bs_cash_bank")
                
            st.subheader(t("Current Liabilities"))
            col5, col6 = st.columns(2)
            with col5:
                creditors = st.number_input(t("Creditors"), min_value=0.0, step=1000.0, key="np_bs_creditors")
                bills_payable = st.number_input(t("Bills Payable"), min_value=0.0, step=1000.0, key="np_bs_bills_pay")
            with col6:
                bank_overdraft = st.number_input(t("Bank Overdraft"), min_value=0.0, step=1000.0, key="np_bs_overdraft")
                accrued_expenses = st.number_input(t("Accrued Expenses"), min_value=0.0, step=100.0, key="np_bs_accrued")

            st.subheader(t("Non-Current Liabilities"))
            col7, col8 = st.columns(2)
            with col7:
                bank_loan = st.number_input(t("Bank Loans"), min_value=0.0, step=10000.0, key="np_bs_bank_loan")
            with col8:
                loan_notes = st.number_input(t("Loan Notes"), min_value=0.0, step=10000.0, key="np_bs_loan_notes")

            st.subheader(t("Equity (Capital)"))
            col9, col10 = st.columns(2)
            with col9:
                opening_capital = st.number_input(t("Opening Capital"), min_value=0.0, step=10000.0, key="np_bs_open_cap")
                additional_capital = st.number_input(t("Additional Capital"), min_value=0.0, step=10000.0, key="np_bs_add_cap")
            with col10:
                drawings = st.number_input(t("– Drawings"), min_value=0.0, step=1000.0, key="np_bs_drawings")

            if st.button(t("📊 Generate Statement of Financial Position"), type="primary", key="btn_np_bs"):
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
                st.success(t("✅ Statement of Financial Position data saved!"))
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
            rows.append([t("Statement of Financial Position"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("ASSETS"), '', ''])
            rows.append(['', '', ''])
            
            rows.append([t("Non-Current Assets"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Land & Buildings"), f"{cfg.get('land_building', 0):,.2f}", ''])
            rows.append([t("Machinery"), f"{cfg.get('machinery', 0):,.2f}", ''])
            rows.append([t("Furniture"), f"{cfg.get('furniture', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Less: Accumulated Depreciation"), f"({cfg.get('accumulated_depreciation', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Non-Current Assets"), '', f"{nca_net:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Current Assets"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Inventory"), f"{cfg.get('inventory', 0):,.2f}", ''])
            rows.append([t("Debtors"), f"{cfg.get('debtors', 0):,.2f}", ''])
            rows.append([t("Bills Receivable"), f"{cfg.get('bills_receivable', 0):,.2f}", ''])
            rows.append([t("Cash in Hand"), f"{cfg.get('cash_hand', 0):,.2f}", ''])
            rows.append([t("Cash at Bank"), f"{cfg.get('cash_bank', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Current Assets"), '', f"{current_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("TOTAL ASSETS"), '', f"{total_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("EQUITY & LIABILITIES"), '', ''])
            rows.append(['', '', ''])
            
            rows.append([t("Capital"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Opening Capital"), f"{cfg.get('opening_capital', 0):,.2f}", ''])
            rows.append([t("Additional Capital"), f"{cfg.get('additional_capital', 0):,.2f}", ''])
            rows.append([t("Net Profit"), f"{net_profit_for_equity:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Less: Drawings"), f"({cfg.get('drawings', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Closing Capital"), '', f"{closing_capital:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Non-Current Liabilities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Bank Loans"), f"{cfg.get('bank_loan', 0):,.2f}", ''])
            rows.append([t("Loan Notes"), f"{cfg.get('loan_notes', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Non-Current Liabilities"), '', f"{ncl_total:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Current Liabilities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Creditors"), f"{cfg.get('creditors', 0):,.2f}", ''])
            rows.append([t("Bills Payable"), f"{cfg.get('bills_payable', 0):,.2f}", ''])
            rows.append([t("Bank Overdraft"), f"{cfg.get('bank_overdraft', 0):,.2f}", ''])
            rows.append([t("Accrued Expenses"), f"{cfg.get('accrued_expenses', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Current Liabilities"), '', f"{current_liabilities:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("TOTAL CAPITAL & LIABILITIES"), '', f"{total_liabilities_equity:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if abs(total_assets - total_liabilities_equity) < 0.01:
                st.success(t("✅ Statement balances correctly!"))
            else:
                st.warning(t(f"⚠️ Statement imbalance: {abs(total_assets - total_liabilities_equity):,.2f} {currency} difference"))

    else:
        st.subheader(t("Statement of Financial Position (Balance Sheet)"))
        
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

        with st.expander(t("📝 Enter Balance Sheet Data"), expanded=True):
            st.subheader(t("Non-Current Assets"))
            col1, col2 = st.columns(2)
            with col1:
                land_building = st.number_input(t("Land & Buildings"), min_value=0.0, step=10000.0, key="bs_land")
                machinery = st.number_input(t("Machinery"), min_value=0.0, step=10000.0, key="bs_machinery")
                furniture = st.number_input(t("Furniture"), min_value=0.0, step=1000.0, key="bs_furniture")
            with col2:
                accumulated_depreciation = st.number_input(t("Less: Accumulated Depreciation"), min_value=0.0, step=1000.0, key="bs_acc_dep")

            st.subheader(t("Current Assets"))
            col3, col4 = st.columns(2)
            with col3:
                inventory = st.number_input(t("Inventory (Closing Stock)"), min_value=0.0, step=1000.0, key="bs_inventory")
                debtors = st.number_input(t("Debtors (Accounts Receivable)"), min_value=0.0, step=1000.0, key="bs_debtors")
                bills_receivable = st.number_input(t("Bills Receivable"), min_value=0.0, step=1000.0, key="bs_bills_rec")
            with col4:
                cash_hand = st.number_input(t("Cash in Hand"), min_value=0.0, step=100.0, key="bs_cash_hand")
                cash_bank = st.number_input(t("Cash at Bank"), min_value=0.0, step=1000.0, key="bs_cash_bank")
                
            st.subheader(t("Current Liabilities"))
            col5, col6 = st.columns(2)
            with col5:
                creditors = st.number_input(t("Creditors (Accounts Payable)"), min_value=0.0, step=1000.0, key="bs_creditors")
                bills_payable = st.number_input(t("Bills Payable"), min_value=0.0, step=1000.0, key="bs_bills_pay")
            with col6:
                bank_overdraft = st.number_input(t("Bank Overdraft"), min_value=0.0, step=1000.0, key="bs_overdraft")
                accrued_expenses = st.number_input(t("Accrued Expenses"), min_value=0.0, step=100.0, key="bs_accrued")

            st.subheader(t("Non-Current Liabilities"))
            col7, col8 = st.columns(2)
            with col7:
                bank_loan = st.number_input(t("Bank Loans"), min_value=0.0, step=10000.0, key="bs_bank_loan")
            with col8:
                loan_notes = st.number_input(t("Loan Notes"), min_value=0.0, step=10000.0, key="bs_loan_notes")

            st.subheader(t("Equity (Capital)"))
            col9, col10 = st.columns(2)
            with col9:
                opening_capital = st.number_input(t("Opening Capital"), min_value=0.0, step=10000.0, key="bs_open_cap")
                additional_capital = st.number_input(t("Additional Capital"), min_value=0.0, step=10000.0, key="bs_add_cap")
            with col10:
                drawings = st.number_input(t("– Drawings"), min_value=0.0, step=1000.0, key="bs_drawings")

            if st.button(t("📊 Generate Balance Sheet"), type="primary", key="btn_bs"):
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
                st.success(t("✅ Balance Sheet data saved!"))
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
            rows.append([t("Statement of Financial Position"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("ASSETS"), '', ''])
            rows.append(['', '', ''])
            
            rows.append([t("Non-Current Assets"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Land & Buildings"), f"{cfg.get('land_building', 0):,.2f}", ''])
            rows.append([t("Machinery"), f"{cfg.get('machinery', 0):,.2f}", ''])
            rows.append([t("Furniture"), f"{cfg.get('furniture', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Less: Accumulated Depreciation"), f"({cfg.get('accumulated_depreciation', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Non-Current Assets"), '', f"{nca_net:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Current Assets"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Inventory (Closing Stock)"), f"{cfg.get('inventory', 0):,.2f}", ''])
            rows.append([t("Debtors (Accounts Receivable)"), f"{cfg.get('debtors', 0):,.2f}", ''])
            rows.append([t("Bills Receivable"), f"{cfg.get('bills_receivable', 0):,.2f}", ''])
            rows.append([t("Cash in Hand"), f"{cfg.get('cash_hand', 0):,.2f}", ''])
            rows.append([t("Cash at Bank"), f"{cfg.get('cash_bank', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Current Assets"), '', f"{current_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("TOTAL ASSETS"), '', f"{total_assets:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("EQUITY & LIABILITIES"), '', ''])
            rows.append(['', '', ''])
            
            rows.append([t("Capital"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Opening Capital"), f"{cfg.get('opening_capital', 0):,.2f}", ''])
            rows.append([t("Additional Capital"), f"{cfg.get('additional_capital', 0):,.2f}", ''])
            rows.append([t("Net Profit"), f"{net_profit_for_equity:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Less: Drawings"), f"({cfg.get('drawings', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Closing Capital"), '', f"{closing_capital:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Non-Current Liabilities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Bank Loans"), f"{cfg.get('bank_loan', 0):,.2f}", ''])
            rows.append([t("Loan Notes"), f"{cfg.get('loan_notes', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Non-Current Liabilities"), '', f"{ncl_total:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Current Liabilities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Creditors (Accounts Payable)"), f"{cfg.get('creditors', 0):,.2f}", ''])
            rows.append([t("Bills Payable"), f"{cfg.get('bills_payable', 0):,.2f}", ''])
            rows.append([t("Bank Overdraft"), f"{cfg.get('bank_overdraft', 0):,.2f}", ''])
            rows.append([t("Accrued Expenses"), f"{cfg.get('accrued_expenses', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Total Current Liabilities"), '', f"{current_liabilities:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("TOTAL CAPITAL & LIABILITIES"), '', f"{total_liabilities_equity:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if abs(total_assets - total_liabilities_equity) < 0.01:
                st.success(t("✅ Statement balances correctly!"))
            else:
                st.warning(t(f"⚠️ Statement imbalance: {abs(total_assets - total_liabilities_equity):,.2f} {currency} difference"))

# ============================================================================
# TAB 3: CASH FLOW STATEMENT
# ============================================================================
with tab3:
    if is_public_sector:
        st.subheader(t("Statement of Cash Flows"))
        
        with st.expander(t("📝 Enter Statement of Cash Flows Data"), expanded=True):
            st.subheader(t("Operating Activities"))
            col1, col2 = st.columns(2)
            with col1:
                cash_from_grants = st.number_input(t("Cash received from government/grants"), min_value=0.0, step=10000.0, key="ps_cf_grants")
                cash_from_services = st.number_input(t("Cash received from services/fees"), min_value=0.0, step=1000.0, key="ps_cf_services")
            with col2:
                cash_to_employees = st.number_input(t("Cash paid to employees"), min_value=0.0, step=1000.0, key="ps_cf_employees")
                cash_to_suppliers = st.number_input(t("Cash paid to suppliers"), min_value=0.0, step=1000.0, key="ps_cf_suppliers")

            st.subheader(t("Investing Activities"))
            col3, col4 = st.columns(2)
            with col3:
                purchase_assets = st.number_input(t("Purchase of assets"), min_value=0.0, step=10000.0, key="ps_cf_purchase")
            with col4:
                sale_assets = st.number_input(t("Sale of assets"), min_value=0.0, step=1000.0, key="ps_cf_sale")

            st.subheader(t("Financing Activities"))
            col5, col6 = st.columns(2)
            with col5:
                government_funding = st.number_input(t("Government funding received"), min_value=0.0, step=10000.0, key="ps_cf_funding")
                loans_received = st.number_input(t("Loans received"), min_value=0.0, step=10000.0, key="ps_cf_loans_in")
            with col6:
                loans_repaid = st.number_input(t("Loans repaid"), min_value=0.0, step=10000.0, key="ps_cf_loans_out")
                interest_paid = st.number_input(t("Interest paid"), min_value=0.0, step=1000.0, key="ps_cf_interest")

            st.subheader(t("Opening Balance"))
            opening_cash = st.number_input(t("Opening cash balance"), min_value=0.0, step=1000.0, key="ps_cf_opening")

            currency = st.selectbox(t("Currency"), ["AED", "USD", "EUR", "GBP"], index=0, key="ps_cf_currency")
            
            if st.button(t("📊 Generate Statement of Cash Flows"), type="primary", key="btn_ps_cf"):
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
                st.success(t("✅ Statement of Cash Flows data saved!"))
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
            rows.append([t("Statement of Cash Flows"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Operating Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Cash received from government/grants"), f"{cfg['cash_from_grants']:,.2f}", ''])
            rows.append([t("Cash received from services/fees"), f"{cfg['cash_from_services']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Cash paid to employees"), f"({cfg['cash_to_employees']:,.2f})", ''])
            rows.append([t("Cash paid to suppliers"), f"({cfg['cash_to_suppliers']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Operating Activities"), '', f"{net_operating:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Investing Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Purchase of assets"), f"({cfg['purchase_assets']:,.2f})", ''])
            rows.append([t("Sale of assets"), f"{cfg['sale_assets']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Investing Activities"), '', f"{net_investing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Financing Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Government funding received"), f"{cfg['government_funding']:,.2f}", ''])
            rows.append([t("Loans received"), f"{cfg['loans_received']:,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Loans repaid"), f"({cfg['loans_repaid']:,.2f})", ''])
            rows.append([t("Interest paid"), f"({cfg['interest_paid']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Financing Activities"), '', f"{net_financing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Net Increase / (Decrease) in Cash"), '', f"{net_change:,.2f}" if net_change >= 0 else f"-{abs(net_change):,.2f}"])
            rows.append(['', '', ''])
            rows.append([t("Add: Opening Cash Balance"), '', f"{cfg['opening_cash']:,.2f}"])
            rows.append(['', '', ''])
            rows.append([t("Closing Cash Balance"), '', f"{closing_cash:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    elif is_nonprofit:
        st.subheader(t("Statement of Cash Flows"))
        
        with st.expander(t("📝 Enter Statement of Cash Flows Data"), expanded=True):
            st.subheader(t("Operating activities"))
            operating_receipts = st.number_input(t("Cash receipts from operations"), min_value=0.0, step=1000.0, key="np_cf_operating_receipts")
            operating_payments = st.number_input(t("Cash payments for operations"), min_value=0.0, step=1000.0, key="np_cf_operating_payments")
            
            st.subheader(t("Investing activities"))
            investing_inflows = st.number_input(t("Cash inflows from investing"), min_value=0.0, step=1000.0, key="np_cf_investing_in")
            investing_outflows = st.number_input(t("Cash outflows for investing"), min_value=0.0, step=1000.0, key="np_cf_investing_out")
            
            st.subheader(t("Financing activities"))
            financing_inflows = st.number_input(t("Cash inflows from financing"), min_value=0.0, step=1000.0, key="np_cf_financing_in")
            financing_outflows = st.number_input(t("Cash outflows for financing"), min_value=0.0, step=1000.0, key="np_cf_financing_out")
            
            opening_cash = st.number_input(t("Opening cash balance"), min_value=0.0, step=1000.0, key="np_cf_opening")

            currency = st.selectbox(t("Currency"), ["AED", "USD", "EUR", "GBP"], index=0, key="np_cf_currency")
            
            if st.button(t("📊 Generate Statement of Cash Flows"), type="primary", key="btn_np_cf"):
                st.session_state.cash_flow = {
                    "type": "nonprofit_cf",
                    "currency": currency,
                    "operating_receipts": operating_receipts, "operating_payments": operating_payments,
                    "investing_inflows": investing_inflows, "investing_outflows": investing_outflows,
                    "financing_inflows": financing_inflows, "financing_outflows": financing_outflows,
                    "opening_cash": opening_cash
                }
                st.success(t("✅ Statement of Cash Flows data saved!"))
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
            rows.append([t("Statement of Cash Flows"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Operating Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Cash receipts from operations"), f"{cfg['operating_receipts']:,.2f}", ''])
            rows.append([t("Cash payments for operations"), f"({cfg['operating_payments']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Operating Activities"), '', f"{net_operating:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Investing Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Cash inflows from investing"), f"{cfg['investing_inflows']:,.2f}", ''])
            rows.append([t("Cash outflows for investing"), f"({cfg['investing_outflows']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Investing Activities"), '', f"{net_investing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Financing Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Cash inflows from financing"), f"{cfg['financing_inflows']:,.2f}", ''])
            rows.append([t("Cash outflows for financing"), f"({cfg['financing_outflows']:,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Financing Activities"), '', f"{net_financing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Net Increase / (Decrease) in Cash"), '', f"{net_change:,.2f}" if net_change >= 0 else f"-{abs(net_change):,.2f}"])
            rows.append(['', '', ''])
            rows.append([t("Add: Opening Cash Balance"), '', f"{cfg['opening_cash']:,.2f}"])
            rows.append(['', '', ''])
            rows.append([t("Closing Cash Balance"), '', f"{closing_cash:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    else:
        st.subheader(t("Cash Flow Statement"))
        
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
        
        with st.expander(t("📝 Enter Cash Flow Data"), expanded=True):
            st.subheader(t("Operating Activities"))
            col1, col2 = st.columns(2)
            with col1:
                cash_from_customers = st.number_input(t("Cash received from customers"), min_value=0.0, step=1000.0, key="cf_customers")
                cash_to_suppliers = st.number_input(t("Cash paid to suppliers"), min_value=0.0, step=1000.0, key="cf_suppliers")
                wages_paid = st.number_input(t("Wages paid"), min_value=0.0, step=100.0, key="cf_wages")
            with col2:
                rent_expenses_paid = st.number_input(t("Rent/expenses paid"), min_value=0.0, step=100.0, key="cf_rent")
                depreciation_addback = st.number_input(t("Adjustment: Depreciation (non-cash)"), min_value=0.0, step=100.0, key="cf_depreciation")
                wc_change = st.number_input(t("Adjustment: Working capital changes"), min_value=-1000000000.0, value=0.0, step=100.0, key="cf_wc")

            st.subheader(t("Investing Activities"))
            col3, col4 = st.columns(2)
            with col3:
                purchase_assets = st.number_input(t("Purchase of assets (machinery, land)"), min_value=0.0, step=10000.0, key="cf_purchase")
            with col4:
                sale_assets = st.number_input(t("Sale of assets"), min_value=0.0, step=1000.0, key="cf_sale")

            st.subheader(t("Financing Activities"))
            col5, col6 = st.columns(2)
            with col5:
                capital_introduced = st.number_input(t("Owner capital introduced"), min_value=0.0, step=10000.0, key="cf_capital")
                loan_received = st.number_input(t("Loan received/repayment"), min_value=-1000000000.0, value=0.0, step=1000.0, key="cf_loan")
            with col6:
                drawings_cf = st.number_input(t("Drawings"), min_value=0.0, step=1000.0, key="cf_drawings")
                interest_paid = st.number_input(t("Interest paid"), min_value=0.0, step=100.0, key="cf_interest")

            st.subheader(t("Final Output"))
            col7, col8 = st.columns(2)
            with col7:
                opening_cash = st.number_input(t("→ Opening cash balance"), min_value=0.0, step=1000.0, key="cf_opening")
            with col8:
                pass

            if st.button(t("📊 Generate Cash Flow Statement"), type="primary", key="btn_cf"):
                st.session_state.cash_flow = {
                    "cash_from_customers": cash_from_customers, "cash_to_suppliers": cash_to_suppliers,
                    "wages_paid": wages_paid, "rent_expenses_paid": rent_expenses_paid,
                    "depreciation_addback": depreciation_addback, "wc_change": wc_change,
                    "purchase_assets": purchase_assets, "sale_assets": sale_assets,
                    "capital_introduced": capital_introduced, "loan_received": loan_received,
                    "drawings_cf": drawings_cf, "interest_paid": interest_paid,
                    "opening_cash": opening_cash
                }
                st.success(t("✅ Cash Flow data saved!"))
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
            rows.append([t("Cash Flow Statement"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Operating Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Cash received from customers"), f"{cfg.get('cash_from_customers', 0):,.2f}", ''])
            rows.append([t("Cash paid to suppliers"), f"({abs(cfg.get('cash_to_suppliers', 0)):,.2f})" if cfg.get('cash_to_suppliers', 0) < 0 else f"{cfg.get('cash_to_suppliers', 0):,.2f}", ''])
            rows.append([t("Wages paid"), f"({abs(cfg.get('wages_paid', 0)):,.2f})" if cfg.get('wages_paid', 0) < 0 else f"{cfg.get('wages_paid', 0):,.2f}", ''])
            rows.append([t("Rent/expenses paid"), f"({abs(cfg.get('rent_expenses_paid', 0)):,.2f})" if cfg.get('rent_expenses_paid', 0) < 0 else f"{cfg.get('rent_expenses_paid', 0):,.2f}", ''])
            rows.append([t("Adjustment: Depreciation (non-cash)"), f"{cfg.get('depreciation_addback', 0):,.2f}", ''])
            rows.append([t("Adjustment: Working capital changes"), f"{cfg.get('wc_change', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Operating Activities"), '', f"{net_operating:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Investing Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Purchase of assets (machinery, land)"), f"({cfg.get('purchase_assets', 0):,.2f})", ''])
            rows.append([t("Sale of assets"), f"{cfg.get('sale_assets', 0):,.2f}", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Investing Activities"), '', f"{net_investing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Cash Flow from Financing Activities"), '', ''])
            rows.append(['', '', ''])
            rows.append([t("Owner capital introduced"), f"{cfg.get('capital_introduced', 0):,.2f}", ''])
            rows.append([t("Loan received/repayment"), f"{cfg.get('loan_received', 0):,.2f}", ''])
            rows.append([t("Drawings"), f"({cfg.get('drawings_cf', 0):,.2f})", ''])
            rows.append([t("Interest paid"), f"({cfg.get('interest_paid', 0):,.2f})", ''])
            rows.append(['', '', ''])
            rows.append([t("Net Cash from Financing Activities"), '', f"{net_financing:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Net Increase / (Decrease) in Cash"), '', f"{net_change:,.2f}" if net_change >= 0 else f"-{abs(net_change):,.2f}"])
            rows.append(['', '', ''])
            rows.append([t("Add: Opening Cash Balance"), '', f"{cfg.get('opening_cash', 0):,.2f}"])
            rows.append(['', '', ''])
            rows.append([t("Closing Cash Balance"), '', f"{closing_cash:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 4: APPROPRIATION ACCOUNT
# ============================================================================
with tab4:
    st.subheader(t("Appropriation Account"))
    
    if st.session_state.business_type != "Partnership":
        st.info(t("👥 Appropriation Account is only available for Partnerships. Select 'Partnership' in Organization Type in the sidebar."))
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

        with st.expander(t("📝 Enter Appropriation Account Data"), expanded=True):
            net_profit = st.number_input(t("Net Profit (from Income Statement)"), min_value=-1000000000.0, value=0.00, step=100.0, key="app_net_profit")
            
            st.subheader(t("Partnership Details"))
            col1, col2 = st.columns(2)
            with col1:
                p1_name = st.text_input(t("Partner 1 Name"), "Partner A", key="app_p1_name")
                p1_capital = st.number_input(t(f"{p1_name} Capital"), min_value=0.0, step=10000.0, key="app_p1_cap")
                p1_drawings = st.number_input(t(f"{p1_name} Drawings"), min_value=0.0, step=1000.0, key="app_p1_draw")
                p1_salary = st.number_input(t(f"{p1_name} Salary"), min_value=0.0, step=1000.0, key="app_p1_salary")
                p1_int_cap_rate = st.number_input(t(f"{p1_name} Interest on Capital %"), min_value=0.0, step=0.5, key="app_p1_int_rate")
            with col2:
                p2_name = st.text_input(t("Partner 2 Name"), "Partner B", key="app_p2_name")
                p2_capital = st.number_input(t(f"{p2_name} Capital"), min_value=0.0, step=10000.0, key="app_p2_cap")
                p2_drawings = st.number_input(t(f"{p2_name} Drawings"), min_value=0.0, step=1000.0, key="app_p2_draw")
                p2_salary = st.number_input(t(f"{p2_name} Salary"), min_value=0.0, step=1000.0, key="app_p2_salary")
                p2_int_cap_rate = st.number_input(t(f"{p2_name} Interest on Capital %"), min_value=0.0, step=0.5, key="app_p2_int_rate")
            
            drawings_interest_rate = st.number_input(
                t("Interest rate on drawings (%)"),
                min_value=0.0,
                max_value=20.0,
                value=5.0,
                step=0.5,
                key="app_drawings_rate"
            )
            
            profit_ratio = st.selectbox(t("Profit Sharing Ratio"), ["50:50", "60:40", "40:60", "70:30", "30:70"], key="app_ratio")
            
            if st.button(t("📊 Generate Appropriation Account"), type="primary", key="btn_app"):
                st.session_state.appropriation = {
                    "net_profit": net_profit,
                    "p1": {"name": p1_name, "capital": p1_capital, "drawings": p1_drawings, "salary": p1_salary, "int_cap_rate": p1_int_cap_rate},
                    "p2": {"name": p2_name, "capital": p2_capital, "drawings": p2_drawings, "salary": p2_salary, "int_cap_rate": p2_int_cap_rate},
                    "ratio": profit_ratio,
                    "drawings_rate": drawings_interest_rate
                }
                st.success(t("✅ Appropriation Account data saved!"))
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
            rows.append([t("Appropriation Account"), '', ''])
            rows.append([period, '', ''])
            rows.append(['', '', ''])
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            rows.append([t("Net Profit for the Year"), '', f"{cfg['net_profit']:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Less: Appropriations"), '', ''])
            rows.append(['', '', ''])
            
            rows.append([t("Partner Salaries"), '', ''])
            rows.append(['', '', ''])
            rows.append([f"{p1['name']}", f"{p1_sal:,.2f}", ''])
            rows.append([f"{p2['name']}", f"{p2_sal:,.2f}", ''])
            rows.append([t("Total Salaries"), '', f"({total_sal:,.2f})"])
            rows.append(['', '', ''])
            
            rows.append([t("Interest on Capital"), '', ''])
            rows.append(['', '', ''])
            rows.append([f"{p1['name']}", f"{p1_int_cap:,.2f}", ''])
            rows.append([f"{p2['name']}", f"{p2_int_cap:,.2f}", ''])
            rows.append([t("Total Interest on Capital"), '', f"({total_int_cap:,.2f})"])
            rows.append(['', '', ''])
            
            rows.append([t("Add: Interest on Drawings"), '', ''])
            rows.append(['', '', ''])
            rows.append([f"{p1['name']}", f"{p1_int_draw:,.2f}", ''])
            rows.append([f"{p2['name']}", f"{p2_int_draw:,.2f}", ''])
            rows.append([t("Total Interest on Drawings"), '', f"{total_int_draw:,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t("Residual Profit"), '', f"{remaining:,.2f}" if remaining >= 0 else f"-{abs(remaining):,.2f}"])
            rows.append(['', '', ''])
            
            rows.append([t(f"Shared in Ratio {ratio}"), '', ''])
            rows.append(['', '', ''])
            rows.append([f"{p1['name']}", f"{abs(p1_share):,.2f}", ''])
            rows.append([f"{p2['name']}", f"{abs(p2_share):,.2f}", ''])
            
            rows.append([t("Total Appropriated"), '', f"{cfg['net_profit']:,.2f}"])
            
            df = pd.DataFrame(rows, columns=['', '\u200b' + currency, '\u200c' + currency])
            st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# TAB 5: FINANCIAL RATIOS
# ============================================================================
with tab5:
    st.subheader(t("📈 Financial Ratios Calculator"))
    
    st.write(f"**{t('Category:')}** {selected_category}")
    st.write("---")
    
    ratios = RATIOS_DB[selected_category]
    
    for ratio_name, ratio_info in ratios.items():
        with st.expander(f"📐 {t(ratio_name)}", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(t("Formula"))
                st.markdown(f"""
                <div style="background-color: #2d2d2d; padding: 15px; border-radius: 5px; text-align: center; font-size: 1.1em; border-left: 4px solid #4CAF50;">
                    {t(ratio_info['formula'])}
                </div>
                """, unsafe_allow_html=True)
                st.markdown(t("### Input Values"))
                input_values = {}
                cols = st.columns(min(len(ratio_info['inputs']), 3))
                for idx, input_name in enumerate(ratio_info['inputs']):
                    with cols[idx % 3]:
                        input_values[input_name] = st.number_input(
                            t(input_name), min_value=0.0, step=100.0,
                            key=f"{ratio_name}_{input_name}"
                        )
                if st.button(t("🔢 Calculate"), key=f"calc_{ratio_name}"):
                    try:
                        values = [input_values[input_name] for input_name in ratio_info['inputs']]
                        result = ratio_info['calculation'](*values)
                        st.markdown(t("### Result"))
                        unit_str = ""
                        if ratio_info['unit'] == 'percentage': unit_str = "%"
                        elif ratio_info['unit'] == 'days': unit_str = t(" days")
                        elif ratio_info['unit'] == 'times': unit_str = "x"
                        st.markdown(f"""
                        <div style="background-color: #4CAF50; color: white; padding: 15px; border-radius: 5px; text-align: center; font-size: 1.3em; font-weight: bold;">
                            {result:.2f}{unit_str}
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(t(f"Error: {str(e)}"))
            with col2:
                st.subheader(t("Information"))
                st.markdown(f"""
                **{t('Inputs:')}** {len(ratio_info['inputs'])}
                
                **{t('Output:')}** {ratio_info['unit'].title()}
                
                **{t('Required:')}**
                """)
                for input_name in ratio_info['inputs']:
                    st.write(f"• {t(input_name)}")

st.markdown("---")
st.caption(t("DGP Finance • Offline • Python • Streamlit • © 2024"))