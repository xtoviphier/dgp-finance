import pandas as pd

# ============================================================================
# COMPREHENSIVE FINANCIAL RATIOS DATABASE - ALL 12 CATEGORIES, 100+ RATIOS
# ============================================================================

RATIOS_DB = {
    # 1. LIQUIDITY RATIOS (Short-term solvency)
    "Liquidity Ratios": {
        "Current Ratio": {
            "formula": "Current Assets / Current Liabilities",
            "inputs": ["Current Assets", "Current Liabilities"],
            "calculation": lambda ca, cl: ca/cl if cl else 0,
            "unit": "ratio"
        },
        "Quick Ratio (Acid Test)": {
            "formula": "(Current Assets - Inventory) / Current Liabilities",
            "inputs": ["Current Assets", "Inventory", "Current Liabilities"],
            "calculation": lambda ca, inv, cl: (ca-inv)/cl if cl else 0,
            "unit": "ratio"
        },
        "Cash Ratio": {
            "formula": "(Cash + Marketable Securities) / Current Liabilities",
            "inputs": ["Cash", "Marketable Securities", "Current Liabilities"],
            "calculation": lambda c, ms, cl: (c+ms)/cl if cl else 0,
            "unit": "ratio"
        },
        "Operating Cash Flow Ratio": {
            "formula": "Operating Cash Flow / Current Liabilities",
            "inputs": ["Operating Cash Flow", "Current Liabilities"],
            "calculation": lambda ocf, cl: ocf/cl if cl else 0,
            "unit": "ratio"
        },
        "Defensive Interval Ratio": {
            "formula": "Current Assets / Daily Operating Expenses",
            "inputs": ["Current Assets", "Daily Operating Expenses"],
            "calculation": lambda ca, doe: ca/doe if doe else 0,
            "unit": "days"
        },
        "Working Capital Ratio": {
            "formula": "(Current Assets - Current Liabilities) / Total Assets",
            "inputs": ["Current Assets", "Current Liabilities", "Total Assets"],
            "calculation": lambda ca, cl, ta: (ca-cl)/ta if ta else 0,
            "unit": "ratio"
        },
        "Net Working Capital Turnover": {
            "formula": "Revenue / Net Working Capital",
            "inputs": ["Revenue", "Net Working Capital"],
            "calculation": lambda rev, nwc: rev/nwc if nwc else 0,
            "unit": "times"
        }
    },
    
    # 2. SOLVENCY/LEVERAGE RATIOS (Long-term financial stability)
    "Solvency/Leverage Ratios": {
        "Debt-to-Equity Ratio": {
            "formula": "Total Debt / Total Equity",
            "inputs": ["Total Debt", "Total Equity"],
            "calculation": lambda td, te: td/te if te else 0,
            "unit": "ratio"
        },
        "Debt-to-Assets Ratio": {
            "formula": "Total Debt / Total Assets",
            "inputs": ["Total Debt", "Total Assets"],
            "calculation": lambda td, ta: (td/ta*100) if ta else 0,
            "unit": "percentage"
        },
        "Equity Ratio": {
            "formula": "Total Equity / Total Assets",
            "inputs": ["Total Equity", "Total Assets"],
            "calculation": lambda te, ta: (te/ta*100) if ta else 0,
            "unit": "percentage"
        },
        "Debt Ratio": {
            "formula": "Total Liabilities / Total Assets",
            "inputs": ["Total Liabilities", "Total Assets"],
            "calculation": lambda tl, ta: (tl/ta*100) if ta else 0,
            "unit": "percentage"
        },
        "Equity Multiplier": {
            "formula": "Total Assets / Total Equity",
            "inputs": ["Total Assets", "Total Equity"],
            "calculation": lambda ta, te: ta/te if te else 0,
            "unit": "ratio"
        },
        "Long-term Debt to Capitalization": {
            "formula": "Long-term Debt / (Long-term Debt + Equity)",
            "inputs": ["Long-term Debt", "Equity"],
            "calculation": lambda ltd, eq: ltd/(ltd+eq)*100 if (ltd+eq) else 0,
            "unit": "percentage"
        },
        "Total Debt to Capitalization": {
            "formula": "Total Debt / (Total Debt + Equity)",
            "inputs": ["Total Debt", "Equity"],
            "calculation": lambda td, eq: td/(td+eq)*100 if (td+eq) else 0,
            "unit": "percentage"
        },
        "Interest Coverage Ratio": {
            "formula": "EBIT / Interest Expense",
            "inputs": ["EBIT", "Interest Expense"],
            "calculation": lambda ebit, ie: ebit/ie if ie else 0,
            "unit": "times"
        },
        "Debt Service Coverage Ratio": {
            "formula": "Net Operating Income / Total Debt Service",
            "inputs": ["Net Operating Income", "Total Debt Service"],
            "calculation": lambda noi, tds: noi/tds if tds else 0,
            "unit": "ratio"
        },
        "Fixed Charge Coverage Ratio": {
            "formula": "(EBIT + Lease Payments) / (Interest + Lease Payments)",
            "inputs": ["EBIT", "Lease Payments", "Interest"],
            "calculation": lambda ebit, lp, ie: (ebit+lp)/(ie+lp) if (ie+lp) else 0,
            "unit": "times"
        },
        "Cash Flow to Debt Ratio": {
            "formula": "Operating Cash Flow / Total Debt",
            "inputs": ["Operating Cash Flow", "Total Debt"],
            "calculation": lambda ocf, td: ocf/td if td else 0,
            "unit": "ratio"
        },
        "Capitalization Ratio": {
            "formula": "Total Debt / (Total Debt + Shareholders' Equity)",
            "inputs": ["Total Debt", "Shareholders' Equity"],
            "calculation": lambda td, se: td/(td+se)*100 if (td+se) else 0,
            "unit": "percentage"
        }
    },
    
    # 3. PROFITABILITY RATIOS (Ability to generate profit)
    "Profitability Ratios": {
        "Gross Profit Margin": {
            "formula": "(Gross Profit / Revenue) × 100",
            "inputs": ["Gross Profit", "Revenue"],
            "calculation": lambda gp, rev: (gp/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "Operating Profit Margin": {
            "formula": "(Operating Income / Revenue) × 100",
            "inputs": ["Operating Income", "Revenue"],
            "calculation": lambda oi, rev: (oi/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "Net Profit Margin": {
            "formula": "(Net Income / Revenue) × 100",
            "inputs": ["Net Income", "Revenue"],
            "calculation": lambda ni, rev: (ni/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "EBITDA Margin": {
            "formula": "(EBITDA / Revenue) × 100",
            "inputs": ["EBITDA", "Revenue"],
            "calculation": lambda ebitda, rev: (ebitda/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "Return on Assets (ROA)": {
            "formula": "(Net Income / Total Assets) × 100",
            "inputs": ["Net Income", "Total Assets"],
            "calculation": lambda ni, ta: (ni/ta*100) if ta else 0,
            "unit": "percentage"
        },
        "Return on Equity (ROE)": {
            "formula": "(Net Income / Shareholders' Equity) × 100",
            "inputs": ["Net Income", "Shareholders' Equity"],
            "calculation": lambda ni, se: (ni/se*100) if se else 0,
            "unit": "percentage"
        },
        "Return on Capital Employed (ROCE)": {
            "formula": "(EBIT / Capital Employed) × 100",
            "inputs": ["EBIT", "Capital Employed"],
            "calculation": lambda ebit, ce: (ebit/ce*100) if ce else 0,
            "unit": "percentage"
        },
        "Return on Invested Capital (ROIC)": {
            "formula": "(NOPAT / Invested Capital) × 100",
            "inputs": ["NOPAT", "Invested Capital"],
            "calculation": lambda nopat, ic: (nopat/ic*100) if ic else 0,
            "unit": "percentage"
        },
        "Return on Tangible Assets": {
            "formula": "(Net Income / Tangible Assets) × 100",
            "inputs": ["Net Income", "Tangible Assets"],
            "calculation": lambda ni, ta: (ni/ta*100) if ta else 0,
            "unit": "percentage"
        },
        "Return on Common Equity": {
            "formula": "((Net Income - Preferred Dividends) / Common Equity) × 100",
            "inputs": ["Net Income", "Preferred Dividends", "Common Equity"],
            "calculation": lambda ni, pd, ce: ((ni-pd)/ce*100) if ce else 0,
            "unit": "percentage"
        },
        "EBIT Margin": {
            "formula": "(EBIT / Revenue) × 100",
            "inputs": ["EBIT", "Revenue"],
            "calculation": lambda ebit, rev: (ebit/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "EBT Margin": {
            "formula": "(EBT / Revenue) × 100",
            "inputs": ["EBT", "Revenue"],
            "calculation": lambda ebt, rev: (ebt/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "Pretax Margin": {
            "formula": "(Pretax Income / Revenue) × 100",
            "inputs": ["Pretax Income", "Revenue"],
            "calculation": lambda pti, rev: (pti/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "Effective Tax Rate": {
            "formula": "(Tax Expense / Pretax Income) × 100",
            "inputs": ["Tax Expense", "Pretax Income"],
            "calculation": lambda te, pti: (te/pti*100) if pti else 0,
            "unit": "percentage"
        }
    },
    
    # 4. EFFICIENCY/ACTIVITY RATIOS (Asset utilization)
    "Efficiency/Activity Ratios": {
        "Asset Turnover Ratio": {
            "formula": "Revenue / Total Assets",
            "inputs": ["Revenue", "Total Assets"],
            "calculation": lambda rev, ta: rev/ta if ta else 0,
            "unit": "times"
        },
        "Fixed Asset Turnover": {
            "formula": "Revenue / Net Fixed Assets",
            "inputs": ["Revenue", "Net Fixed Assets"],
            "calculation": lambda rev, nfa: rev/nfa if nfa else 0,
            "unit": "times"
        },
        "Current Asset Turnover": {
            "formula": "Revenue / Current Assets",
            "inputs": ["Revenue", "Current Assets"],
            "calculation": lambda rev, ca: rev/ca if ca else 0,
            "unit": "times"
        },
        "Working Capital Turnover": {
            "formula": "Revenue / Working Capital",
            "inputs": ["Revenue", "Working Capital"],
            "calculation": lambda rev, wc: rev/wc if wc else 0,
            "unit": "times"
        },
        "Inventory Turnover": {
            "formula": "Cost of Goods Sold / Average Inventory",
            "inputs": ["Cost of Goods Sold", "Average Inventory"],
            "calculation": lambda cogs, ai: cogs/ai if ai else 0,
            "unit": "times"
        },
        "Days Inventory Outstanding (DIO)": {
            "formula": "365 / Inventory Turnover",
            "inputs": ["Inventory Turnover"],
            "calculation": lambda it: 365/it if it else 0,
            "unit": "days"
        },
        "Receivables Turnover": {
            "formula": "Revenue / Average Accounts Receivable",
            "inputs": ["Revenue", "Average Accounts Receivable"],
            "calculation": lambda rev, aar: rev/aar if aar else 0,
            "unit": "times"
        },
        "Days Sales Outstanding (DSO)": {
            "formula": "365 / Receivables Turnover",
            "inputs": ["Receivables Turnover"],
            "calculation": lambda rt: 365/rt if rt else 0,
            "unit": "days"
        },
        "Payables Turnover": {
            "formula": "Cost of Goods Sold / Average Accounts Payable",
            "inputs": ["Cost of Goods Sold", "Average Accounts Payable"],
            "calculation": lambda cogs, aap: cogs/aap if aap else 0,
            "unit": "times"
        },
        "Days Payable Outstanding (DPO)": {
            "formula": "365 / Payables Turnover",
            "inputs": ["Payables Turnover"],
            "calculation": lambda pt: 365/pt if pt else 0,
            "unit": "days"
        },
        "Cash Conversion Cycle": {
            "formula": "DIO + DSO - DPO",
            "inputs": ["DIO", "DSO", "DPO"],
            "calculation": lambda dio, dso, dpo: dio+dso-dpo,
            "unit": "days"
        },
        "Total Asset Turnover": {
            "formula": "Net Sales / Average Total Assets",
            "inputs": ["Net Sales", "Average Total Assets"],
            "calculation": lambda ns, ata: ns/ata if ata else 0,
            "unit": "times"
        },
        "Equity Turnover": {
            "formula": "Revenue / Shareholders' Equity",
            "inputs": ["Revenue", "Shareholders' Equity"],
            "calculation": lambda rev, se: rev/se if se else 0,
            "unit": "times"
        },
        "Capital Employed Turnover": {
            "formula": "Revenue / Capital Employed",
            "inputs": ["Revenue", "Capital Employed"],
            "calculation": lambda rev, ce: rev/ce if ce else 0,
            "unit": "times"
        }
    },
    
    # 5. MARKET VALUE RATIOS (Stock market performance)
    "Market Value Ratios": {
        "Earnings Per Share (EPS)": {
            "formula": "Net Income / Number of Outstanding Shares",
            "inputs": ["Net Income", "Number of Outstanding Shares"],
            "calculation": lambda ni, shares: ni/shares if shares else 0,
            "unit": "currency"
        },
        "Price-to-Earnings Ratio (P/E)": {
            "formula": "Market Price per Share / EPS",
            "inputs": ["Market Price per Share", "EPS"],
            "calculation": lambda mps, eps: mps/eps if eps else 0,
            "unit": "ratio"
        },
        "Price-to-Book Ratio (P/B)": {
            "formula": "Market Price per Share / Book Value per Share",
            "inputs": ["Market Price per Share", "Book Value per Share"],
            "calculation": lambda mps, bvps: mps/bvps if bvps else 0,
            "unit": "ratio"
        },
        "Price-to-Sales Ratio (P/S)": {
            "formula": "Market Cap / Revenue",
            "inputs": ["Market Cap", "Revenue"],
            "calculation": lambda mc, rev: mc/rev if rev else 0,
            "unit": "ratio"
        },
        "Price-to-Cash Flow Ratio": {
            "formula": "Market Price per Share / Cash Flow per Share",
            "inputs": ["Market Price per Share", "Cash Flow per Share"],
            "calculation": lambda mps, cfps: mps/cfps if cfps else 0,
            "unit": "ratio"
        },
        "Enterprise Value to EBITDA (EV/EBITDA)": {
            "formula": "Enterprise Value / EBITDA",
            "inputs": ["Enterprise Value", "EBITDA"],
            "calculation": lambda ev, ebitda: ev/ebitda if ebitda else 0,
            "unit": "ratio"
        },
        "Enterprise Value to Revenue (EV/Revenue)": {
            "formula": "Enterprise Value / Revenue",
            "inputs": ["Enterprise Value", "Revenue"],
            "calculation": lambda ev, rev: ev/rev if rev else 0,
            "unit": "ratio"
        },
        "Dividend Yield": {
            "formula": "(Annual Dividend per Share / Market Price per Share) × 100",
            "inputs": ["Annual Dividend per Share", "Market Price per Share"],
            "calculation": lambda adps, mps: (adps/mps*100) if mps else 0,
            "unit": "percentage"
        },
        "Dividend Payout Ratio": {
            "formula": "(Dividends / Net Income) × 100",
            "inputs": ["Dividends", "Net Income"],
            "calculation": lambda div, ni: (div/ni*100) if ni else 0,
            "unit": "percentage"
        },
        "Retention Ratio": {
            "formula": "((Net Income - Dividends) / Net Income) × 100",
            "inputs": ["Net Income", "Dividends"],
            "calculation": lambda ni, div: ((ni-div)/ni*100) if ni else 0,
            "unit": "percentage"
        },
        "Book Value per Share": {
            "formula": "Shareholders' Equity / Number of Shares",
            "inputs": ["Shareholders' Equity", "Number of Shares"],
            "calculation": lambda se, shares: se/shares if shares else 0,
            "unit": "currency"
        },
        "Market-to-Book Ratio": {
            "formula": "Market Value of Equity / Book Value of Equity",
            "inputs": ["Market Value of Equity", "Book Value of Equity"],
            "calculation": lambda mve, bve: mve/bve if bve else 0,
            "unit": "ratio"
        },
        "PEG Ratio": {
            "formula": "P/E Ratio / Earnings Growth Rate",
            "inputs": ["P/E Ratio", "Earnings Growth Rate"],
            "calculation": lambda pe, egr: pe/egr if egr else 0,
            "unit": "ratio"
        },
        "EV/EBIT": {
            "formula": "Enterprise Value / EBIT",
            "inputs": ["Enterprise Value", "EBIT"],
            "calculation": lambda ev, ebit: ev/ebit if ebit else 0,
            "unit": "ratio"
        },
        "EV/FCF": {
            "formula": "Enterprise Value / Free Cash Flow",
            "inputs": ["Enterprise Value", "Free Cash Flow"],
            "calculation": lambda ev, fcf: ev/fcf if fcf else 0,
            "unit": "ratio"
        }
    },
    
    # 6. COVERAGE RATIOS (Ability to meet obligations)
    "Coverage Ratios": {
        "Interest Coverage Ratio": {
            "formula": "EBIT / Interest Expense",
            "inputs": ["EBIT", "Interest Expense"],
            "calculation": lambda ebit, ie: ebit/ie if ie else 0,
            "unit": "times"
        },
        "Debt Service Coverage Ratio": {
            "formula": "Net Operating Income / Debt Service",
            "inputs": ["Net Operating Income", "Debt Service"],
            "calculation": lambda noi, ds: noi/ds if ds else 0,
            "unit": "ratio"
        },
        "Fixed Charge Coverage": {
            "formula": "(EBIT + Fixed Charges before tax) / (Fixed Charges + Interest)",
            "inputs": ["EBIT", "Fixed Charges", "Interest"],
            "calculation": lambda ebit, fc, ie: (ebit+fc)/(fc+ie) if (fc+ie) else 0,
            "unit": "times"
        },
        "Cash Coverage Ratio": {
            "formula": "(EBIT + Depreciation) / Interest Expense",
            "inputs": ["EBIT", "Depreciation", "Interest Expense"],
            "calculation": lambda ebit, dep, ie: (ebit+dep)/ie if ie else 0,
            "unit": "times"
        },
        "Asset Coverage Ratio": {
            "formula": "(Total Assets - Current Liabilities) / Total Debt",
            "inputs": ["Total Assets", "Current Liabilities", "Total Debt"],
            "calculation": lambda ta, cl, td: (ta-cl)/td if td else 0,
            "unit": "ratio"
        },
        "Cash Flow Coverage Ratio": {
            "formula": "Operating Cash Flow / Total Debt",
            "inputs": ["Operating Cash Flow", "Total Debt"],
            "calculation": lambda ocf, td: ocf/td if td else 0,
            "unit": "ratio"
        },
        "Dividend Coverage Ratio": {
            "formula": "Net Income / Dividends Paid",
            "inputs": ["Net Income", "Dividends Paid"],
            "calculation": lambda ni, dp: ni/dp if dp else 0,
            "unit": "times"
        }
    },
    
    # 7. CASH FLOW RATIOS (Cash generation and quality)
    "Cash Flow Ratios": {
        "Operating Cash Flow Ratio": {
            "formula": "Operating Cash Flow / Current Liabilities",
            "inputs": ["Operating Cash Flow", "Current Liabilities"],
            "calculation": lambda ocf, cl: ocf/cl if cl else 0,
            "unit": "ratio"
        },
        "Cash Flow to Net Income": {
            "formula": "Operating Cash Flow / Net Income",
            "inputs": ["Operating Cash Flow", "Net Income"],
            "calculation": lambda ocf, ni: ocf/ni if ni else 0,
            "unit": "ratio"
        },
        "Free Cash Flow to Equity": {
            "formula": "Operating Cash Flow - Capital Expenditures + Net Borrowing",
            "inputs": ["Operating Cash Flow", "Capital Expenditures", "Net Borrowing"],
            "calculation": lambda ocf, capex, nb: ocf-capex+nb,
            "unit": "currency"
        },
        "Free Cash Flow to Firm": {
            "formula": "Operating Cash Flow - Capital Expenditures",
            "inputs": ["Operating Cash Flow", "Capital Expenditures"],
            "calculation": lambda ocf, capex: ocf-capex,
            "unit": "currency"
        },
        "Cash Flow Margin": {
            "formula": "(Operating Cash Flow / Revenue) × 100",
            "inputs": ["Operating Cash Flow", "Revenue"],
            "calculation": lambda ocf, rev: (ocf/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "Cash Flow Return on Assets": {
            "formula": "(Operating Cash Flow / Total Assets) × 100",
            "inputs": ["Operating Cash Flow", "Total Assets"],
            "calculation": lambda ocf, ta: (ocf/ta*100) if ta else 0,
            "unit": "percentage"
        },
        "Cash Flow Return on Equity": {
            "formula": "(Operating Cash Flow / Shareholders' Equity) × 100",
            "inputs": ["Operating Cash Flow", "Shareholders' Equity"],
            "calculation": lambda ocf, se: (ocf/se*100) if se else 0,
            "unit": "percentage"
        },
        "Cash Flow to Debt": {
            "formula": "Operating Cash Flow / Total Debt",
            "inputs": ["Operating Cash Flow", "Total Debt"],
            "calculation": lambda ocf, td: ocf/td if td else 0,
            "unit": "ratio"
        },
        "Cash Flow Coverage Ratio": {
            "formula": "Operating Cash Flow / Total Debt Service",
            "inputs": ["Operating Cash Flow", "Total Debt Service"],
            "calculation": lambda ocf, tds: ocf/tds if tds else 0,
            "unit": "ratio"
        },
        "Quality of Income Ratio": {
            "formula": "Operating Cash Flow / Net Income",
            "inputs": ["Operating Cash Flow", "Net Income"],
            "calculation": lambda ocf, ni: ocf/ni if ni else 0,
            "unit": "ratio"
        },
        "Cash Flow to Sales": {
            "formula": "Operating Cash Flow / Revenue",
            "inputs": ["Operating Cash Flow", "Revenue"],
            "calculation": lambda ocf, rev: ocf/rev if rev else 0,
            "unit": "ratio"
        },
        "Reinvestment Ratio": {
            "formula": "Capital Expenditures / Operating Cash Flow",
            "inputs": ["Capital Expenditures", "Operating Cash Flow"],
            "calculation": lambda capex, ocf: capex/ocf if ocf else 0,
            "unit": "ratio"
        }
    },
    
    # 8. VALUATION RATIOS
    "Valuation Ratios": {
        "Enterprise Value (EV)": {
            "formula": "Market Cap + Debt - Cash",
            "inputs": ["Market Cap", "Debt", "Cash"],
            "calculation": lambda mc, d, c: mc+d-c,
            "unit": "currency"
        },
        "EV/EBITDA": {
            "formula": "Enterprise Value / EBITDA",
            "inputs": ["Enterprise Value", "EBITDA"],
            "calculation": lambda ev, ebitda: ev/ebitda if ebitda else 0,
            "unit": "ratio"
        },
        "EV/EBIT": {
            "formula": "Enterprise Value / EBIT",
            "inputs": ["Enterprise Value", "EBIT"],
            "calculation": lambda ev, ebit: ev/ebit if ebit else 0,
            "unit": "ratio"
        },
        "EV/Sales": {
            "formula": "Enterprise Value / Revenue",
            "inputs": ["Enterprise Value", "Revenue"],
            "calculation": lambda ev, rev: ev/rev if rev else 0,
            "unit": "ratio"
        },
        "EV/FCF": {
            "formula": "Enterprise Value / Free Cash Flow",
            "inputs": ["Enterprise Value", "Free Cash Flow"],
            "calculation": lambda ev, fcf: ev/fcf if fcf else 0,
            "unit": "ratio"
        },
        "Price/Earnings to Growth (PEG)": {
            "formula": "P/E Ratio / Earnings Growth Rate",
            "inputs": ["P/E Ratio", "Earnings Growth Rate"],
            "calculation": lambda pe, egr: pe/egr if egr else 0,
            "unit": "ratio"
        },
        "Price/Cash Flow": {
            "formula": "Market Price per Share / Cash Flow per Share",
            "inputs": ["Market Price per Share", "Cash Flow per Share"],
            "calculation": lambda mps, cfps: mps/cfps if cfps else 0,
            "unit": "ratio"
        },
        "Price/Book": {
            "formula": "Market Price per Share / Book Value per Share",
            "inputs": ["Market Price per Share", "Book Value per Share"],
            "calculation": lambda mps, bvps: mps/bvps if bvps else 0,
            "unit": "ratio"
        },
        "Price/Sales": {
            "formula": "Market Cap / Revenue",
            "inputs": ["Market Cap", "Revenue"],
            "calculation": lambda mc, rev: mc/rev if rev else 0,
            "unit": "ratio"
        },
        "Price/Tangible Book": {
            "formula": "Market Price per Share / Tangible Book Value per Share",
            "inputs": ["Market Price per Share", "Tangible Book Value per Share"],
            "calculation": lambda mps, tbvps: mps/tbvps if tbvps else 0,
            "unit": "ratio"
        },
        "EV/Invested Capital": {
            "formula": "Enterprise Value / Invested Capital",
            "inputs": ["Enterprise Value", "Invested Capital"],
            "calculation": lambda ev, ic: ev/ic if ic else 0,
            "unit": "ratio"
        }
    },
    
    # 9. DUPONT ANALYSIS COMPONENTS
    "DuPont Analysis Components": {
        "Net Profit Margin (DuPont)": {
            "formula": "Net Income / Revenue",
            "inputs": ["Net Income", "Revenue"],
            "calculation": lambda ni, rev: (ni/rev*100) if rev else 0,
            "unit": "percentage"
        },
        "Asset Turnover (DuPont)": {
            "formula": "Revenue / Total Assets",
            "inputs": ["Revenue", "Total Assets"],
            "calculation": lambda rev, ta: rev/ta if ta else 0,
            "unit": "times"
        },
        "Equity Multiplier (DuPont)": {
            "formula": "Total Assets / Total Equity",
            "inputs": ["Total Assets", "Total Equity"],
            "calculation": lambda ta, te: ta/te if te else 0,
            "unit": "ratio"
        },
        "ROE (3-step DuPont)": {
            "formula": "Net Profit Margin × Asset Turnover × Equity Multiplier",
            "inputs": ["Net Profit Margin", "Asset Turnover", "Equity Multiplier"],
            "calculation": lambda npm, at, em: (npm/100)*at*em*100,
            "unit": "percentage"
        },
        "ROE (5-step DuPont)": {
            "formula": "Tax Burden × Interest Burden × EBIT Margin × Asset Turnover × Equity Multiplier",
            "inputs": ["Tax Burden", "Interest Burden", "EBIT Margin", "Asset Turnover", "Equity Multiplier"],
            "calculation": lambda tb, ib, ebitm, at, em: tb*ib*ebitm*at*em*100,
            "unit": "percentage"
        }
    },
    
    # 10. BANKING-SPECIFIC RATIOS
    "Banking-Specific Ratios": {
        "Capital Adequacy Ratio (CAR)": {
            "formula": "(Tier 1 Capital + Tier 2 Capital) / Risk-Weighted Assets",
            "inputs": ["Tier 1 Capital", "Tier 2 Capital", "Risk-Weighted Assets"],
            "calculation": lambda t1, t2, rwa: ((t1+t2)/rwa*100) if rwa else 0,
            "unit": "percentage"
        },
        "Tier 1 Capital Ratio": {
            "formula": "Tier 1 Capital / Risk-Weighted Assets",
            "inputs": ["Tier 1 Capital", "Risk-Weighted Assets"],
            "calculation": lambda t1, rwa: (t1/rwa*100) if rwa else 0,
            "unit": "percentage"
        },
        "Loan-to-Deposit Ratio": {
            "formula": "Total Loans / Total Deposits",
            "inputs": ["Total Loans", "Total Deposits"],
            "calculation": lambda tl, td: (tl/td*100) if td else 0,
            "unit": "percentage"
        },
        "Non-Performing Loan Ratio": {
            "formula": "Non-Performing Loans / Total Loans",
            "inputs": ["Non-Performing Loans", "Total Loans"],
            "calculation": lambda npl, tl: (npl/tl*100) if tl else 0,
            "unit": "percentage"
        },
        "Provision Coverage Ratio": {
            "formula": "Loan Loss Provisions / Non-Performing Loans",
            "inputs": ["Loan Loss Provisions", "Non-Performing Loans"],
            "calculation": lambda llp, npl: (llp/npl*100) if npl else 0,
            "unit": "percentage"
        },
        "Net Interest Margin": {
            "formula": "(Interest Income - Interest Expense) / Average Earning Assets",
            "inputs": ["Interest Income", "Interest Expense", "Average Earning Assets"],
            "calculation": lambda ii, ie, aea: ((ii-ie)/aea*100) if aea else 0,
            "unit": "percentage"
        }
    },
    
    # 11. INSURANCE-SPECIFIC RATIOS
    "Insurance-Specific Ratios": {
        "Combined Ratio": {
            "formula": "(Loss Ratio + Expense Ratio)",
            "inputs": ["Loss Ratio", "Expense Ratio"],
            "calculation": lambda lr, er: lr+er,
            "unit": "percentage"
        },
        "Loss Ratio": {
            "formula": "(Incurred Losses + Loss Adjustment Expenses) / Earned Premiums",
            "inputs": ["Incurred Losses", "Loss Adjustment Expenses", "Earned Premiums"],
            "calculation": lambda il, lae, ep: ((il+lae)/ep*100) if ep else 0,
            "unit": "percentage"
        },
        "Expense Ratio": {
            "formula": "Underwriting Expenses / Earned Premiums",
            "inputs": ["Underwriting Expenses", "Earned Premiums"],
            "calculation": lambda ue, ep: (ue/ep*100) if ep else 0,
            "unit": "percentage"
        },
        "Solvency Ratio": {
            "formula": "Net Written Premiums / Policyholders' Surplus",
            "inputs": ["Net Written Premiums", "Policyholders' Surplus"],
            "calculation": lambda nwp, ps: (nwp/ps*100) if ps else 0,
            "unit": "percentage"
        }
    },
    
    # 12. RETAIL-SPECIFIC RATIOS
    "Retail-Specific Ratios": {
        "Same-Store Sales Growth": {
            "formula": "((Current Period Sales - Prior Period Sales) / Prior Period Sales) × 100",
            "inputs": ["Current Period Sales", "Prior Period Sales"],
            "calculation": lambda cps, pps: ((cps-pps)/pps*100) if pps else 0,
            "unit": "percentage"
        },
        "Sales per Square Foot": {
            "formula": "Net Sales / Total Square Footage",
            "inputs": ["Net Sales", "Total Square Footage"],
            "calculation": lambda ns, tsf: ns/tsf if tsf else 0,
            "unit": "currency"
        },
        "Inventory to Sales Ratio": {
            "formula": "Average Inventory / Net Sales",
            "inputs": ["Average Inventory", "Net Sales"],
            "calculation": lambda ai, ns: ai/ns if ns else 0,
            "unit": "ratio"
        },
        "Gross Margin Return on Investment (GMROI)": {
            "formula": "Gross Margin / Average Inventory Cost",
            "inputs": ["Gross Margin", "Average Inventory Cost"],
            "calculation": lambda gm, aic: gm/aic if aic else 0,
            "unit": "ratio"
        }
    }
}

# ============================================================================
# FINANCIAL STATEMENT GENERATION FUNCTIONS (Keep existing logic)
# ============================================================================

def calculate_expense(paid, accrued=0, prepaid=0):
    """Calculate expense with accruals and prepayments"""
    return paid + accrued - prepaid

def generate_income_statement(data):
    statements = {}
    
    # Trading Account
    cost_of_sales = (data['opening_stock'] + data['purchases'] + 
                     data['carriage_in'] - data['closing_stock'])
    gross_profit = (data['sales'] - data['sales_returns']) - cost_of_sales
    
    trading_data = {
        'Item': ['Revenue/Sales', 'Less: Returns', 'Net Sales', 'Opening Stock', 'Purchases', 
                 'Carriage Inwards', 'Less: Closing Stock', 'Cost of Goods Sold', 'Gross Profit'],
        'Amount': [data['sales'], -data['sales_returns'], data['sales']-data['sales_returns'],
                   data['opening_stock'], data['purchases'], data['carriage_in'], 
                   -data['closing_stock'], -cost_of_sales, gross_profit]
    }
    statements['Trading Account'] = pd.DataFrame(trading_data)
    
    # Operating Expenses with adjustments
    rent_exp = calculate_expense(data['rent_paid'], data['rent_accrued'], data['rent_prepaid'])
    insurance_exp = calculate_expense(data['insurance_paid'], 0, data['insurance_prepaid'])
    loan_interest = data['loan_notes'] * (data['loan_notes_rate'] / 100) if data.get('loan_notes') else 0
    
    expenses_list = [
        ("Wages & Salaries", data['wages_salaries'] + data['salaries_accrued']),
        ("Rent & Insurance (adjusted)", rent_exp + insurance_exp),
        ("Utilities", data['utilities']),
        ("Office expenses", data['printing'] + data['postage']),
        ("Discount Allowed", data['discount_allowed']),
        ("Bad Debts + Provision", data['bad_debts'] + data['prov_doubtful_debts']),
        ("Repairs & Maintenance", data['repairs']),
        ("Depreciation", data['depreciation']),
        ("Interest Expense", data['interest_expense'] + loan_interest),
        ("General expenses", data['general_expenses'])
    ]
    
    items = [x[0] for x in expenses_list]
    amounts = [x[1] for x in expenses_list]
    total_expenses = sum(amounts)
    
    other_income = data['rent_income'] + data['interest_received'] + data['misc_income']
    net_profit = gross_profit + other_income - total_expenses
    
    items.extend(["Total Operating Expenses", "Other Income", "NET PROFIT/(LOSS)"])
    amounts.extend([-total_expenses, other_income, net_profit])
    
    statements['Profit & Loss Account'] = pd.DataFrame({'Item': items, 'Amount': amounts})
    return statements

def generate_balance_sheet(data):
    statements = {}
    
    # Non-Current Assets
    nca_net = data['land_building'] + data['machinery'] + data['furniture'] - data['accumulated_depreciation']
    nca_data = {
        'Item': ['Land & Buildings', 'Machinery', 'Furniture', 'Less: Accumulated Depreciation', 'Total Non-Current Assets'],
        'Amount': [data['land_building'], data['machinery'], data['furniture'], -data['accumulated_depreciation'], nca_net]
    }
    statements['Non-Current Assets'] = pd.DataFrame(nca_data)
    
    # Current Assets
    current_assets = data['inventory'] + data['debtors'] + data['bills_receivable'] + data['cash_hand'] + data['cash_bank']
    ca_data = {
        'Item': ['Inventory (Closing Stock)', 'Debtors (Accounts Receivable)', 'Bills Receivable', 
                'Cash in Hand', 'Cash at Bank', 'Total Current Assets'],
        'Amount': [data['inventory'], data['debtors'], data['bills_receivable'], 
                  data['cash_hand'], data['cash_bank'], current_assets]
    }
    statements['Current Assets'] = pd.DataFrame(ca_data)
    
    # Current Liabilities
    current_liabilities = data['creditors'] + data['bills_payable'] + data['bank_overdraft'] + data['accrued_expenses']
    cl_data = {
        'Item': ['Creditors (Accounts Payable)', 'Bills Payable', 'Bank Overdraft', 
                'Accrued Expenses', 'Total Current Liabilities'],
        'Amount': [data['creditors'], data['bills_payable'], data['bank_overdraft'], 
                  data['accrued_expenses'], current_liabilities]
    }
    statements['Current Liabilities'] = pd.DataFrame(cl_data)
    
    # Non-Current Liabilities
    ncl_total = data['bank_loan'] + data['loan_notes']
    ncl_data = {
        'Item': ['Bank Loans', 'Loan Notes', 'Total Non-Current Liabilities'],
        'Amount': [data['bank_loan'], data['loan_notes'], ncl_total]
    }
    statements['Non-Current Liabilities'] = pd.DataFrame(ncl_data)
    
    # Capital Section
    net_sales = data['sales'] - data['sales_returns']
    cogs = data['opening_stock'] + data['purchases'] + data['carriage_in'] - data['closing_stock']
    gross_profit = net_sales - cogs
    other_income = data['rent_income'] + data['interest_received'] + data['misc_income']
    rent_exp = calculate_expense(data['rent_paid'], data['rent_accrued'], data['rent_prepaid'])
    insurance_exp = calculate_expense(data['insurance_paid'], 0, data['insurance_prepaid'])
    loan_interest = data['loan_notes'] * (data['loan_notes_rate'] / 100) if data.get('loan_notes') else 0
    total_exp = ((data['wages_salaries'] + data['salaries_accrued']) + 
                 (rent_exp + insurance_exp) + data['utilities'] + 
                 (data['printing'] + data['postage']) + data['discount_allowed'] + 
                 (data['bad_debts'] + data['prov_doubtful_debts']) + data['repairs'] + 
                 data['depreciation'] + (data['interest_expense'] + loan_interest) + 
                 data['general_expenses'])
    net_profit = gross_profit + other_income - total_exp
    
    closing_capital = data['opening_capital'] + data['additional_capital'] + net_profit - data['drawings']
    cap_data = {
        'Item': ['Opening Capital', 'Additional Capital', 'Net Profit', '– Drawings', '→ Closing Capital'],
        'Amount': [data['opening_capital'], data['additional_capital'], net_profit, -data['drawings'], closing_capital]
    }
    statements['Capital'] = pd.DataFrame(cap_data)
    
    # Summary
    total_assets = nca_net + current_assets
    total_liab_equity = closing_capital + current_liabilities + ncl_total
    summary_data = {
        'Item': ['Total Assets', 'Total Capital & Liabilities'],
        'Amount': [total_assets, total_liab_equity]
    }
    statements['Summary'] = pd.DataFrame(summary_data)
    return statements

def generate_cash_flow(data):
    # Simplified cash flow based on receipts and payments
    net_sales = data['sales'] - data['sales_returns']
    net_profit = generate_income_statement(data)['Profit & Loss Account']['Amount'].iloc[-1]
    
    items = [
        ("Net Profit", net_profit),
        ("Add: Depreciation (non-cash)", data['depreciation']),
        ("Net Cash from Operating Activities", net_profit + data['depreciation']),
        ("Purchase of assets (machinery, land)", -(data['machinery'] + data['land_building'])),
        ("Net Cash from Investing Activities", -(data['machinery'] + data['land_building'])),
        ("Owner capital introduced", data['additional_capital']),
        ("Loan received/repayment", data['bank_loan']),
        ("Less: Drawings", -data['drawings']),
        ("Interest paid", -data['interest_expense']),
        ("Net Cash from Financing Activities", data['additional_capital'] + data['bank_loan'] - data['drawings'] - data['interest_expense']),
        ("→ Net increase/decrease in cash", net_profit + data['depreciation'] - (data['machinery'] + data['land_building']) + data['additional_capital'] + data['bank_loan'] - data['drawings'] - data['interest_expense']),
        ("→ Opening cash balance", data['cash_hand'] + data['cash_bank']),
        ("→ Closing cash balance", net_profit + data['depreciation'] - (data['machinery'] + data['land_building']) + data['additional_capital'] + data['bank_loan'] - data['drawings'] - data['interest_expense'] + data['cash_hand'] + data['cash_bank'])
    ]
    return pd.DataFrame(items, columns=["Item", "Amount"])

def generate_appropriation_account(data):
    if data['business_type'] != "Partnership" or not data.get('partners'):
        return pd.DataFrame()
    
    # Recalculate net profit
    net_sales = data['sales'] - data['sales_returns']
    cogs = data['opening_stock'] + data['purchases'] + data['carriage_in'] - data['closing_stock']
    gross_profit = net_sales - cogs
    other_income = data['rent_income'] + data['interest_received'] + data['misc_income']
    rent_exp = calculate_expense(data['rent_paid'], data['rent_accrued'], data['rent_prepaid'])
    insurance_exp = calculate_expense(data['insurance_paid'], 0, data['insurance_prepaid'])
    loan_interest = data['loan_notes'] * (data['loan_notes_rate'] / 100) if data.get('loan_notes') else 0
    total_exp = ((data['wages_salaries'] + data['salaries_accrued']) + 
                 (rent_exp + insurance_exp) + data['utilities'] + 
                 (data['printing'] + data['postage']) + data['discount_allowed'] + 
                 (data['bad_debts'] + data['prov_doubtful_debts']) + data['repairs'] + 
                 data['depreciation'] + (data['interest_expense'] + loan_interest) + 
                 data['general_expenses'])
    net_profit = gross_profit + other_income - total_exp
    
    p1 = data['partners']['p1']
    p2 = data['partners']['p2']
    
    # Interest on Capital
    p1_int_cap = p1['capital'] * (p1['int_cap_rate'] / 100)
    p2_int_cap = p2['capital'] * (p2['int_cap_rate'] / 100)
    total_int_cap = p1_int_cap + p2_int_cap
    
    # Salaries to Partners
    p1_sal = p1['salary']
    p2_sal = p2['salary']
    total_sal = p1_sal + p2_sal
    
    # Interest on Drawings (example 5%)
    p1_int_draw = p1['drawings'] * 0.05
    p2_int_draw = p2['drawings'] * 0.05
    total_int_draw = p1_int_draw + p2_int_draw
    
    # Remaining Profit
    remaining = net_profit - total_int_cap - total_sal + total_int_draw
    
    # Split according to ratio
    ratio = data['partners']['ratio']
    r_parts = ratio.split(':')
    r1, r2 = int(r_parts[0]), int(r_parts[1])
    total_ratio = r1 + r2
    p1_share = remaining * (r1 / total_ratio)
    p2_share = remaining * (r2 / total_ratio)
    
    items = [
        ("Net Profit (from Income Statement)", net_profit),
        ("ADD: Interest on Capital", total_int_cap),
        (f"  - {p1['name']}", p1_int_cap),
        (f"  - {p2['name']}", p2_int_cap),
        ("ADD: Salaries to Partners", total_sal),
        (f"  - {p1['name']}", p1_sal),
        (f"  - {p2['name']}", p2_sal),
        ("LESS: Interest on Drawings", -total_int_draw),
        (f"  - {p1['name']}", -p1_int_draw),
        (f"  - {p2['name']}", -p2_int_draw),
        ("Remaining Profit shared in agreed ratio", remaining),
        (f"  - {p1['name']} ({ratio})", p1_share),
        (f"  - {p2['name']} ({ratio})", p2_share)
    ]
    return pd.DataFrame(items, columns=["Item", "Amount"])