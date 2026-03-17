APP_CSS = """
    <style>
    .main {
        background-color: #F8FAFC;
    }
    .metric-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1);
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }
    .invoice-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    .invoice-info {
        display: flex;
        flex-direction: column;
    }
    .invoice-value {
        font-size: 2.5em; /* Matches stMetricValue */
        font-weight: 700;
        color: #0F172A;
        margin: 8px 0;
    }
    .invoice-label {
        font-size: 0.875rem; /* Matches stMetricLabel (14px) */
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .invoice-period {
        font-size: 0.85em;
        color: #94A3B8;
    }
    /* Mobile First Adjustments */
    @media (max-width: 640px) {
        .invoice-card {
            flex-direction: column;
            align-items: flex-start;
        }
        .invoice-logo {
            margin-top: 16px;
            align-self: flex-end;
        }
    }
    .stTable {
        background-color: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1);
    }
    h1, h2, h3 {
        color: #0F172A;
        font-weight: 600;
    }
    p {
        color: #334155;
    }
    .stMetric {
        background-color: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1) !important;
        border: 1px solid #E2E8F0;
    }
    [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 2.5em !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        border-bottom-color: #1D4ED8;
        font-weight: 700;
    }
    /* --- Global Limit Bar --- */
    .global-limit-card {
        background-color: white;
        padding: 20px 24px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1);
        border: 1px solid #E2E8F0;
        margin-bottom: 24px;
    }
    .limit-label {
        font-size: 0.875rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .limit-value {
        font-size: 1rem;
        font-weight: 700;
    }
    .limit-bar-container-global {
        width: 100%;
        height: 8px; /* Thicker than before */
        background: #F1F5F9;
        border-radius: 4px;
        margin: 8px 0;
        overflow: hidden;
    }
    .limit-bar-fill {
        height: 100%;
        border-radius: 4px;
        transition: width 0.4s ease;
    }
    .limit-available {
        font-size: 0.85rem;
        color: #475569;
        font-weight: 500;
        display: block;
    }
    /* --- Tooltip on card hover --- */
    .invoice-card {
        position: relative;
    }
    .tooltip-content {
        display: none;
        position: absolute;
        bottom: calc(100% + 8px);
        left: 50%;
        transform: translateX(-50%);
        background: #1E293B;
        color: #F1F5F9;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 0.8rem;
        white-space: nowrap;
        z-index: 10;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        flex-direction: column;
        gap: 4px;
    }
    .tooltip-content::after {
        content: '';
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        border: 6px solid transparent;
        border-top-color: #1E293B;
    }
    .invoice-card:hover .tooltip-content {
        display: flex;
    }
    </style>
"""
