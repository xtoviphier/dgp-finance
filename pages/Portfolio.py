import streamlit as st
import pandas as pd
import os
import json  # ✅ ADD THIS LINE
from portfolio_manager import load_all_reports, get_report_data, REPORTS_DIR
from datetime import datetime

# Import translator (matching Financial Reports)
try:
    from translator import get_ai_translation
except ImportError:
    def get_ai_translation(text, lang):
        return text

st.set_page_config(page_title="Portfolio • DGP Finance", page_icon="📁", layout="wide")

# Initialize session state for translation
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'translate_mode' not in st.session_state:
    st.session_state.translate_mode = True

# Helper function to conditionally translate
def t(text):
    return get_ai_translation(text, st.session_state.lang) if st.session_state.translate_mode else text

# Sidebar with translation (matching Financial Reports)
with st.sidebar:
    # Enable AI Translation toggle
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
        key="lang_selector_portfolio"
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

# ============================================================================
# HELPER FUNCTIONS FOR DELETE/RENAME
# ============================================================================
def delete_report(filename: str):
    """Delete a report file"""
    filepath = REPORTS_DIR / filename
    if filepath.exists():
        filepath.unlink()
        return True
    return False

def rename_report(filename: str, new_name: str):
    """Update the report name in metadata (keeps same filename)"""
    filepath = REPORTS_DIR / filename
    if not filepath.exists():
        return False
    
    with open(filepath, "r", encoding="utf-8") as f:
        report = json.load(f)
    
    report["name"] = new_name
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return True

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.title(f"📁 {t('Financial Portfolio')}")
st.markdown(f"*{t('All your generated reports, stored locally and ready for download.')}*")

# Load reports
reports = load_all_reports()

if not reports:
    st.info(f"📭 {t('No reports yet. Generate a financial statement to see it here.')}")
    st.stop()

# Display as editable dataframe with actions
st.subheader(f"📋 {t('Saved Reports')}")

for i, report in enumerate(reports):
    with st.expander(f"📄 {report['name']} ({report['created_at']})", expanded=False):
        col_meta, col_actions = st.columns([3, 1])
        
        with col_meta:
            st.markdown(f"""
            **{t('Type')}:** {report['type']}  
            **{t('Organization')}:** {report['org_type']}  
            **{t('Created')}:** {report['created_at']}  
            **{t('File')}:** `{report['filename']}`
            """)
        
        with col_actions:
            # ✅ RENAME BUTTON
            new_name = st.text_input(
                t("Rename"), 
                value=report['name'], 
                key=f"rename_{report['filename']}",
                label_visibility="collapsed"
            )
            if st.button(t("💾 Save"), key=f"save_rename_{report['filename']}"):
                if new_name and new_name != report['name']:
                    if rename_report(report['filename'], new_name):
                        st.success(f"✅ {t('Renamed!')}")
                        st.rerun()
                    else:
                        st.error(f"❌ {t('Failed to rename')}")
            
            # ✅ DELETE BUTTON (FIXED WITH SESSION STATE)
            delete_key = f"delete_confirm_{report['filename']}"
            
            # Check if we're waiting for delete confirmation
            if st.session_state.get(delete_key):
                col_del1, col_del2 = st.columns(2)
                with col_del1:
                    if st.button(f"⚠️ {t('Confirm Delete')}", key=f"confirm_{report['filename']}", type="primary"):
                        if delete_report(report['filename']):
                            st.success(f"✅ {t('Deleted!')}")
                            st.session_state[delete_key] = False
                            st.rerun()
                        else:
                            st.error(f"❌ {t('Failed to delete')}")
                with col_del2:
                    if st.button(t("Cancel"), key=f"cancel_{report['filename']}"):
                        st.session_state[delete_key] = False
                        st.rerun()
            else:
                # Normal state: show Delete button
                if st.button(t("🗑️ Delete"), key=f"delete_{report['filename']}", type="secondary"):
                    st.session_state[delete_key] = True
                    st.rerun()
        
        # ✅ DOWNLOAD BUTTON
        st.markdown("---")
        if st.button(f"⬇️ {t('Download as CSV')}", key=f"download_{report['filename']}", type="primary"):
            data = report.get("data", {})
            rows = []
            
            # Add document headers
            rows.append(['DGP Finance Client', '', ''])
            rows.append([report['type'], '', ''])
            rows.append([report.get('name', '').replace(f"{report['type']} - ", ""), '', ''])
            rows.append(['', '', ''])
            currency = data.get('currency', 'AED')
            rows.append(['', currency, currency])
            rows.append(['', '', ''])
            
            # Format CSV based on report type
            if report["type"] == "Statement of Activities (Non-Profit)":
                # Non-Profit Statement of Activities
                total_income = data.get('donations', 0) + data.get('grants', 0) + data.get('membership_fees', 0) + data.get('fundraising_income', 0)
                total_expenses = data.get('program_expenses', 0) + data.get('admin_expenses', 0) + data.get('fundraising_costs', 0)
                surplus_deficit = total_income - total_expenses
                
                rows.append([t("Income / Inflows"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Donations"), f"{data.get('donations', 0):,.2f}", ''])
                rows.append([t("Grants"), f"{data.get('grants', 0):,.2f}", ''])
                rows.append([t("Membership fees"), f"{data.get('membership_fees', 0):,.2f}", ''])
                rows.append([t("Fundraising income"), f"{data.get('fundraising_income', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Income"), '', f"{total_income:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Expenses"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Program expenses"), f"{data.get('program_expenses', 0):,.2f}", ''])
                rows.append([t("Administrative expenses"), f"{data.get('admin_expenses', 0):,.2f}", ''])
                rows.append([t("Fundraising costs"), f"{data.get('fundraising_costs', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Expenses"), '', f"({total_expenses:,.2f})"])
                
                result_label = "Net Surplus" if surplus_deficit >= 0 else "Net Deficit"
                rows.append([result_label, '', f"{surplus_deficit:,.2f}" if surplus_deficit >= 0 else f"-{abs(surplus_deficit):,.2f}"])

            elif report["type"] == "Statement of Financial Performance (Public Sector)":
                # Public Sector Statement of Financial Performance
                total_revenue = data.get('government_grants', 0) + data.get('tax_revenue', 0) + data.get('service_revenue', 0) + data.get('other_income', 0)
                total_expenses = (data.get('employee_costs', 0) + data.get('admin_expenses', 0) + data.get('utilities', 0) + 
                                data.get('repairs_maintenance', 0) + data.get('depreciation', 0) + data.get('interest_expense', 0) + 
                                data.get('program_costs', 0) + data.get('other_expenses', 0))
                surplus_deficit = total_revenue - total_expenses
                
                rows.append([t("Revenue"), '', ''])
                rows.append(['', '', ''])
                rows.append([t(" Government Grants / Funding"), f"{data.get('government_grants', 0):,.2f}", ''])
                rows.append([t("Tax Revenue (if applicable)"), f"{data.get('tax_revenue', 0):,.2f}", ''])
                rows.append([t("Service Revenue (fees, licenses)"), f"{data.get('service_revenue', 0):,.2f}", ''])
                rows.append([t("Other Income"), f"{data.get('other_income', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Revenue"), '', f"{total_revenue:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Expenses"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Employee Costs (Wages & Salaries)"), f"{data.get('employee_costs', 0):,.2f}", ''])
                rows.append([t("Administrative Expenses"), f"{data.get('admin_expenses', 0):,.2f}", ''])
                rows.append([t("Utilities"), f"{data.get('utilities', 0):,.2f}", ''])
                rows.append([t("Repairs & Maintenance"), f"{data.get('repairs_maintenance', 0):,.2f}", ''])
                rows.append([t("Depreciation"), f"{data.get('depreciation', 0):,.2f}", ''])
                rows.append([t("Interest Expense"), f"{data.get('interest_expense', 0):,.2f}", ''])
                rows.append([t("Program / Service Delivery Costs"), f"{data.get('program_costs', 0):,.2f}", ''])
                rows.append([t("Other Operating Expenses"), f"{data.get('other_expenses', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Expenses"), '', f"({total_expenses:,.2f})"])
                rows.append(['', '', ''])
                
                result_label = "Surplus" if surplus_deficit >= 0 else "Deficit"
                rows.append([result_label, '', f"{surplus_deficit:,.2f}" if surplus_deficit >= 0 else f"-{abs(surplus_deficit):,.2f}"])

            elif report["type"] == "Statement of Cash Flows (Public Sector)":
                # Public Sector Statement of Cash Flows
                net_operating = (data.get('cash_from_grants', 0) + data.get('cash_from_services', 0) - 
                               data.get('cash_to_employees', 0) - data.get('cash_to_suppliers', 0))
                net_investing = data.get('sale_assets', 0) - data.get('purchase_assets', 0)
                net_financing = (data.get('government_funding', 0) + data.get('loans_received', 0) - 
                               data.get('loans_repaid', 0) - data.get('interest_paid', 0))
                net_change = net_operating + net_investing + net_financing
                closing_cash = net_change + data.get('opening_cash', 0)
                
                rows.append([t("Cash Flow from Operating Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Cash received from government/grants"), f"{data.get('cash_from_grants', 0):,.2f}", ''])
                rows.append([t("Cash received from services/fees"), f"{data.get('cash_from_services', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Cash paid to employees"), f"({data.get('cash_to_employees', 0):,.2f})", ''])
                rows.append([t("Cash paid to suppliers"), f"({data.get('cash_to_suppliers', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Operating Activities"), '', f"{net_operating:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Cash Flow from Investing Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Purchase of assets"), f"({data.get('purchase_assets', 0):,.2f})", ''])
                rows.append([t("Sale of assets"), f"{data.get('sale_assets', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Investing Activities"), '', f"{net_investing:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Cash Flow from Financing Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Government funding received"), f"{data.get('government_funding', 0):,.2f}", ''])
                rows.append([t("Loans received"), f"{data.get('loans_received', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Loans repaid"), f"({data.get('loans_repaid', 0):,.2f})", ''])
                rows.append([t("Interest paid"), f"({data.get('interest_paid', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Financing Activities"), '', f"{net_financing:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Net Increase / (Decrease) in Cash"), '', f"{net_change:,.2f}" if net_change >= 0 else f"-{abs(net_change):,.2f}"])
                rows.append(['', '', ''])
                rows.append([t("Add: Opening Cash Balance"), '', f"{data.get('opening_cash', 0):,.2f}"])
                rows.append(['', '', ''])
                rows.append([t("Closing Cash Balance"), '', f"{closing_cash:,.2f}"])

            elif report["type"] == "Statement of Financial Position (Public Sector)":
                # Public Sector Statement of Financial Position
                nca_net = data.get('land_building', 0) + data.get('equipment', 0) + data.get('furniture', 0) - data.get('accumulated_depreciation', 0)
                current_assets = data.get('receivables', 0) + data.get('cash_equivalents', 0)
                total_assets = nca_net + current_assets
                
                current_liabilities = data.get('payables', 0) + data.get('accrued_expenses', 0)
                ncl_total = data.get('loans', 0)
                
                surplus_for_year = data.get('surplus_for_year', 0) 
                closing_net_assets = data.get('accumulated_surplus', 0) + surplus_for_year
                total_liabilities_equity = closing_net_assets + current_liabilities + ncl_total

                rows.append([t("Assets"), '', ''])
                rows.append(['', '', ''])
                
                rows.append([t("Non-Current Assets"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Land & Buildings"), f"{data.get('land_building', 0):,.2f}", ''])
                rows.append([t("Equipment / Machinery"), f"{data.get('equipment', 0):,.2f}", ''])
                rows.append([t("Furniture"), f"{data.get('furniture', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Less: Accumulated Depreciation"), f"({data.get('accumulated_depreciation', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Non-Current Assets"), '', f"{nca_net:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Current Assets"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Receivables"), f"{data.get('receivables', 0):,.2f}", ''])
                rows.append([t("Cash and Cash Equivalents"), f"{data.get('cash_equivalents', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Current Assets"), '', f"{current_assets:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("TOTAL ASSETS"), '', f"{total_assets:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Net Assets / Equity"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Opening Accumulated Surplus"), f"{data.get('accumulated_surplus', 0):,.2f}", ''])
                rows.append([t("Surplus / (Deficit) for the Year"), f"{surplus_for_year:,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Closing Accumulated Surplus"), '', f"{closing_net_assets:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Liabilities"), '', ''])
                rows.append(['', '', ''])
                
                rows.append([t("Non-Current Liabilities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Loans / Borrowings"), f"{data.get('loans', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Non-Current Liabilities"), '', f"{ncl_total:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Current Liabilities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Payables"), f"{data.get('payables', 0):,.2f}", ''])
                rows.append([t("Accrued Expenses"), f"{data.get('accrued_expenses', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Current Liabilities"), '', f"{current_liabilities:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("TOTAL NET ASSETS & LIABILITIES"), '', f"{total_liabilities_equity:,.2f}"])
            
            elif report["type"] == "Statement of Financial Position":
                # Non-Profit Statement of Financial Position
                nca_net = data.get('land_building', 0) + data.get('machinery', 0) + data.get('furniture', 0) - data.get('accumulated_depreciation', 0)
                current_assets = data.get('inventory', 0) + data.get('debtors', 0) + data.get('bills_receivable', 0) + data.get('cash_hand', 0) + data.get('cash_bank', 0)
                total_assets = nca_net + current_assets
                
                current_liabilities = data.get('creditors', 0) + data.get('bills_payable', 0) + data.get('bank_overdraft', 0) + data.get('accrued_expenses', 0)
                ncl_total = data.get('bank_loan', 0) + data.get('loan_notes', 0)
                
                net_profit_for_equity = 0  # Would need to calculate from Statement of Activities
                closing_capital = data.get('opening_capital', 0) + data.get('additional_capital', 0) + net_profit_for_equity - data.get('drawings', 0)
                total_liabilities_equity = closing_capital + current_liabilities + ncl_total
                
                rows.append([t("ASSETS"), '', ''])
                rows.append(['', '', ''])
                
                rows.append([t("Non-Current Assets"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Land & Buildings"), f"{data.get('land_building', 0):,.2f}", ''])
                rows.append([t("Machinery"), f"{data.get('machinery', 0):,.2f}", ''])
                rows.append([t("Furniture"), f"{data.get('furniture', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Less: Accumulated Depreciation"), f"({data.get('accumulated_depreciation', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Non-Current Assets"), '', f"{nca_net:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Current Assets"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Inventory"), f"{data.get('inventory', 0):,.2f}", ''])
                rows.append([t("Debtors"), f"{data.get('debtors', 0):,.2f}", ''])
                rows.append([t("Bills Receivable"), f"{data.get('bills_receivable', 0):,.2f}", ''])
                rows.append([t("Cash in Hand"), f"{data.get('cash_hand', 0):,.2f}", ''])
                rows.append([t("Cash at Bank"), f"{data.get('cash_bank', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Current Assets"), '', f"{current_assets:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("TOTAL ASSETS"), '', f"{total_assets:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("EQUITY & LIABILITIES"), '', ''])
                rows.append(['', '', ''])
                
                rows.append([t("Capital"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Opening Capital"), f"{data.get('opening_capital', 0):,.2f}", ''])
                rows.append([t("Additional Capital"), f"{data.get('additional_capital', 0):,.2f}", ''])
                rows.append([t("Net Profit"), f"{net_profit_for_equity:,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Less: Drawings"), f"({data.get('drawings', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Closing Capital"), '', f"{closing_capital:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Non-Current Liabilities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Bank Loans"), f"{data.get('bank_loan', 0):,.2f}", ''])
                rows.append([t("Loan Notes"), f"{data.get('loan_notes', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Non-Current Liabilities"), '', f"{ncl_total:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Current Liabilities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Creditors"), f"{data.get('creditors', 0):,.2f}", ''])
                rows.append([t("Bills Payable"), f"{data.get('bills_payable', 0):,.2f}", ''])
                rows.append([t("Bank Overdraft"), f"{data.get('bank_overdraft', 0):,.2f}", ''])
                rows.append([t("Accrued Expenses"), f"{data.get('accrued_expenses', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Current Liabilities"), '', f"{current_liabilities:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("TOTAL CAPITAL & LIABILITIES"), '', f"{total_liabilities_equity:,.2f}"])
            
            elif report["type"] == "Statement of Cash Flows (Non-Profit)":
                # Non-Profit Statement of Cash Flows
                net_operating = data.get('operating_receipts', 0) - data.get('operating_payments', 0)
                net_investing = data.get('investing_inflows', 0) - data.get('investing_outflows', 0)
                net_financing = data.get('financing_inflows', 0) - data.get('financing_outflows', 0)
                net_change = net_operating + net_investing + net_financing
                closing_cash = net_change + data.get('opening_cash', 0)
                
                rows.append([t("Cash Flow from Operating Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Cash receipts from operations"), f"{data.get('operating_receipts', 0):,.2f}", ''])
                rows.append([t("Cash payments for operations"), f"({data.get('operating_payments', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Operating Activities"), '', f"{net_operating:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Cash Flow from Investing Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Cash inflows from investing"), f"{data.get('investing_inflows', 0):,.2f}", ''])
                rows.append([t("Cash outflows for investing"), f"({data.get('investing_outflows', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Investing Activities"), '', f"{net_investing:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Cash Flow from Financing Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Cash inflows from financing"), f"{data.get('financing_inflows', 0):,.2f}", ''])
                rows.append([t("Cash outflows for financing"), f"({data.get('financing_outflows', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Financing Activities"), '', f"{net_financing:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Net Increase / (Decrease) in Cash"), '', f"{net_change:,.2f}" if net_change >= 0 else f"-{abs(net_change):,.2f}"])
                rows.append(['', '', ''])
                rows.append([t("Add: Opening Cash Balance"), '', f"{data.get('opening_cash', 0):,.2f}"])
                rows.append(['', '', ''])
                rows.append([t("Closing Cash Balance"), '', f"{closing_cash:,.2f}"])
            
            elif report["type"] == "Income Statement / P&L":
                # === CALCULATIONS ===
                net_sales = data.get('sales', 0) - data.get('sales_returns', 0)
                cogs = (data.get('opening_stock', 0) + data.get('purchases', 0) + 
                       data.get('carriage_in', 0) - data.get('closing_stock', 0))
                gross_profit = net_sales - cogs
                
                other_income = (data.get('rent_income', 0) + data.get('interest_received', 0) + 
                               data.get('misc_income', 0))
                pbe = gross_profit + other_income
                
                # Expense calculations
                rent_exp = (data.get('rent_paid', 0) + data.get('rent_accrued', 0) - 
                           data.get('rent_prepaid', 0))
                insurance_exp = (data.get('insurance_paid', 0) - data.get('insurance_prepaid', 0))
                total_expenses = (data.get('wages_salaries', 0) + rent_exp + insurance_exp + 
                                 data.get('utilities', 0) + data.get('printing', 0) + 
                                 data.get('postage', 0) + data.get('discount_allowed', 0) + 
                                 data.get('bad_debts', 0) + data.get('prov_doubtful_debts', 0) + 
                                 data.get('repairs', 0) + data.get('depreciation', 0) + 
                                 data.get('interest_expense', 0) + data.get('general_expenses', 0))
                net_profit = pbe - total_expenses

                # === CSV ROWS ===
                # Revenue
                rows.append([t("Revenue"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Sales Revenue"), f"{data.get('sales', 0):,.2f}", ''])
                rows.append([t("Less: Returns"), f"({data.get('sales_returns', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Sales"), '', f"{net_sales:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Cost of Sales"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Opening Stock"), f"{data.get('opening_stock', 0):,.2f}", ''])
                rows.append([t("Purchases"), f"{data.get('purchases', 0):,.2f}", ''])
                rows.append([t("Carriage Inwards"), f"{data.get('carriage_in', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Less: Closing Stock"), f"({data.get('closing_stock', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Cost of Sales"), '', f"({cogs:,.2f})"])
                rows.append(['', '', ''])
                
                rows.append([t("Gross Profit"), '', f"{gross_profit:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Other Income"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Rent income"), f"{data.get('rent_income', 0):,.2f}", ''])
                rows.append([t("Interest received"), f"{data.get('interest_received', 0):,.2f}", ''])
                rows.append([t("Miscellaneous income"), f"{data.get('misc_income', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Other Income"), '', f"{other_income:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Profit Before Expenses"), '', f"{pbe:,.2f}"])
                rows.append(['', '', ''])
                
                rows.append([t("Expenses"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Wages & Salaries"), f"{data.get('wages_salaries', 0):,.2f}", ''])
                rows.append([t("Rent & Insurance (adjusted)"), f"{rent_exp + insurance_exp:,.2f}", ''])
                rows.append([t("Utilities (lighting, etc.)"), f"{data.get('utilities', 0):,.2f}", ''])
                rows.append([t("Office expenses (printing, postage)"), f"{data.get('printing', 0) + data.get('postage', 0):,.2f}", ''])
                rows.append([t("Discount Allowed"), f"{data.get('discount_allowed', 0):,.2f}", ''])
                rows.append([t("Bad Debts + Provision"), f"{data.get('bad_debts', 0) + data.get('prov_doubtful_debts', 0):,.2f}", ''])
                rows.append([t("Repairs & Maintenance"), f"{data.get('repairs', 0):,.2f}", ''])
                rows.append([t("Depreciation (non-cash expense)"), f"{data.get('depreciation', 0):,.2f}", ''])
                rows.append([t("Interest Expense"), f"{data.get('interest_expense', 0):,.2f}", ''])
                rows.append([t("General expenses"), f"{data.get('general_expenses', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Total Expenses"), '', f"({total_expenses:,.2f})"])
                rows.append(['', '', ''])
                rows.append([t("Net Profit"), '', f"{net_profit:,.2f}" if net_profit >= 0 else f"-{abs(net_profit):,.2f}"])
            
            elif report["type"] == "Cash Flow Statement":
                # For-Profit Cash Flow Statement CSV Export
                net_operating = (data.get('cash_from_customers', 0) + data.get('cash_to_suppliers', 0) +
                                data.get('wages_paid', 0) + data.get('rent_expenses_paid', 0) +
                                data.get('depreciation_addback', 0) + data.get('wc_change', 0))
                net_investing = (-data.get('purchase_assets', 0) + data.get('sale_assets', 0))
                net_financing = (data.get('capital_introduced', 0) + data.get('loan_received', 0) -
                                data.get('drawings_cf', 0) - data.get('interest_paid', 0))
                net_change = net_operating + net_investing + net_financing
                closing_cash = net_change + data.get('opening_cash', 0)
                
                # Operating Activities Section
                rows.append([t("Cash Flow from Operating Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Cash received from customers"), f"{data.get('cash_from_customers', 0):,.2f}", ''])
                rows.append([t("Cash paid to suppliers"), f"({abs(data.get('cash_to_suppliers', 0)):,.2f})", ''])
                rows.append([t("Wages paid"), f"({abs(data.get('wages_paid', 0)):,.2f})", ''])
                rows.append([t("Rent/expenses paid"), f"({abs(data.get('rent_expenses_paid', 0)):,.2f})", ''])
                rows.append([t("Adjustment: Depreciation (non-cash)"), f"{data.get('depreciation_addback', 0):,.2f}", ''])
                rows.append([t("Adjustment: Working capital changes"), f"{data.get('wc_change', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Operating Activities"), '', f"{net_operating:,.2f}"])
                rows.append(['', '', ''])
                
                # Investing Activities Section
                rows.append([t("Cash Flow from Investing Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Purchase of assets (machinery, land)"), f"({data.get('purchase_assets', 0):,.2f})", ''])
                rows.append([t("Sale of assets"), f"{data.get('sale_assets', 0):,.2f}", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Investing Activities"), '', f"{net_investing:,.2f}"])
                rows.append(['', '', ''])
                
                # Financing Activities Section
                rows.append([t("Cash Flow from Financing Activities"), '', ''])
                rows.append(['', '', ''])
                rows.append([t("Owner capital introduced"), f"{data.get('capital_introduced', 0):,.2f}", ''])
                rows.append([t("Loan received/repayment"), f"{data.get('loan_received', 0):,.2f}", ''])
                rows.append([t("Drawings"), f"({data.get('drawings_cf', 0):,.2f})", ''])
                rows.append([t("Interest paid"), f"({data.get('interest_paid', 0):,.2f})", ''])
                rows.append(['', '', ''])
                rows.append([t("Net Cash from Financing Activities"), '', f"{net_financing:,.2f}"])
                rows.append(['', '', ''])
                
                # Summary Section
                rows.append([t("Net Increase / (Decrease) in Cash"), '', f"{net_change:,.2f}"])
                rows.append([t("Add: Opening Cash Balance"), '', f"{data.get('opening_cash', 0):,.2f}"])
                rows.append(['', '', ''])
                rows.append([t("Closing Cash Balance"), '', f"{closing_cash:,.2f}"])
            
            else:
                # Fallback for any other report types - create 3-column rows
                rows.append([t("Report Data"), '', ''])
                rows.append(['', '', ''])
                for k, v in data.items():
                    if isinstance(v, (int, float)):
                        rows.append([k, f"{v:,.2f}", ''])
                    else:
                        rows.append([k, str(v), ''])

            # Create CSV - Force every row to have exactly 3 columns
            safe_rows = []
            for row in rows:
                if len(row) == 1:
                    safe_rows.append([row[0], '', ''])
                elif len(row) == 2:
                    safe_rows.append([row[0], row[1], ''])
                elif len(row) >= 3:
                    safe_rows.append([row[0], row[1], row[2]])
                else:
                    safe_rows.append(['', '', ''])
            
            csv_df = pd.DataFrame(safe_rows, columns=['', '', ''])
            csv_data = csv_df.to_csv(index=False).encode("utf-8")
            
            st.download_button(
                label=f"📥 {t('Download')} {report['name']}.csv",
                data=csv_data,
                file_name=f"{report['name'].replace(' ', '_')}.csv",
                mime="text/csv",
                key=f"dl_btn_{report['filename']}"
            )
                        
st.markdown("---")
st.caption(f"💾 {t('Get your money up not your funny up')}")