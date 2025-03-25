import streamlit as st

# Page setup
st.set_page_config(page_title="Payroll Demo", page_icon="💸")
st.title("🏦 Simulate Paycheck")
st.write("Simulate payroll processing and see where every penny goes.")

# Move annual view outside the form so it works after submission
annual_view = st.checkbox("📅 Show Annual Pay Summary")

# Input form
st.subheader("👤 Employee Details")

with st.form("payroll_form"):
    name = st.text_input("Employee Name", value="John Doe")
    hours_worked = st.number_input("Hours Worked", min_value=0, value=40, step=1)
    hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=25.00, step=0.50)

    st.markdown("### 🧾 Pre-tax Deductions")
    k401_percent = st.slider("401(k) Contribution (%)", min_value=0, max_value=15, value=5, step=1)
    health_insurance = st.number_input("Health Insurance ($)", min_value=0.0, value=25.00, step=1.00)

    st.markdown("### 💰 Taxes")
    federal_tax_rate = st.slider("Federal Tax Rate (%)", min_value=0, max_value=30, value=12, step=1)
    state = st.selectbox("State", options=["CA", "TX", "NY", "FL", "Other"], index=0)

    st.markdown("### 🐞 Underpay")
    underpay_toggle = st.checkbox("Intentionally underpay by 1¢")

    submitted = st.form_submit_button("Generate Paycheck")

if submitted:
    st.subheader("📊 Payroll Summary")

    # Calculations
    gross_pay = hours_worked * hourly_rate
    k401_deduction = gross_pay * (k401_percent / 100)
    taxable_income = gross_pay - k401_deduction - health_insurance

    # Tax calculations
    federal_tax = taxable_income * (federal_tax_rate / 100)
    state_tax_rates = {
        "CA": 0.02,
        "NY": 0.03,
        "TX": 0.00,
        "FL": 0.00,
        "Other": 0.01
    }
    state_tax = taxable_income * state_tax_rates[state]
    total_taxes = federal_tax + state_tax

    # Expected Net Pay (used for penny test)
    expected_net = gross_pay - k401_deduction - health_insurance - total_taxes

    # Simulate optional underpayment
    net_pay = expected_net
    if underpay_toggle:
        net_pay -= 0.01  # Intentionally short by 1¢

    # Output breakdown
    st.write(f"**Gross Pay:** ${gross_pay:,.2f}")
    st.write(f"- 401(k) Deduction ({k401_percent}%): -${k401_deduction:,.2f}")
    st.write(f"- Health Insurance: -${health_insurance:,.2f}")
    st.write(f"**Taxable Income:** ${taxable_income:,.2f}")
    st.write(f"- Federal Tax ({federal_tax_rate}%): -${federal_tax:,.2f}")
    st.write(f"- {state} State Tax ({state_tax_rates[state]*100:.1f}%): -${state_tax:,.2f}")
    st.markdown("---")
    st.write(f"### ✅ Net Pay: ${net_pay:,.2f}")

    # Penny test
    difference = round(net_pay - expected_net, 2)

    if underpay_toggle:
        if difference == -0.01:
            st.error("❌ Penny Test Failed — You underpaid by 1¢")
        else:
            st.warning(f"⚠️ Unexpected difference: {difference}")
    else:
        if abs(difference) <= 0.005:
            st.success("🪙 Penny Check Passed!")
        else:
            st.error(f"❌ Penny Test Failed — Off by ${difference:.2f}")

    # Annual Pay Summary
    if annual_view:
        st.subheader("📅 Annual Pay Summary")
        st.write(f"**Annual Gross Pay:** ${gross_pay * 52:,.2f}")
        st.write(f"**Annual 401(k) Contribution:** ${k401_deduction * 52:,.2f}")
        st.write(f"**Annual Taxes (Federal + State):** ${total_taxes * 52:,.2f}")
        st.write(f"**Annual Net Pay:** ${net_pay * 52:,.2f}")
