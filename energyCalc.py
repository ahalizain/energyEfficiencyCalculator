import streamlit as st
import time
import plotly.express as px  # For interactive charts

if __name__ == "__main__":
    st.title("Energy Efficiency Calculator")
    st.subheader("An easy, user-friendly application created by Zain Ahmad")
    st.subheader("This will calculate your energy savings using some questions.")
    st.subheader("You will need your energy bill handy for some of the questions presented.")

    st.header("General Information About Your Home")
    house_area = st.number_input("Enter square footage of the house", min_value=0)
    kwh_consumption = st.number_input("What is the average total monthly energy consumption in your house in Kilowatt Hour (kWh)?", min_value=0.0)
    dollar_kwh_consumption = st.number_input("What is the average total monthly energy cost in your house, in dollars?", min_value=0.0)
    windows_replacement = st.selectbox("Have the windows in your house been replaced with high efficiency ones in the last 15 years?", ["Yes", "No"])
    num_conv_bulb = st.number_input("Enter the number of conventional light bulbs in the house.", min_value=0)
    num_led_bulb = st.number_input("Enter the number of LED lightbulbs in the house.", min_value=0)
    thermostat = st.selectbox("Do you have a learning thermostat in the house? (Google Nest or Ecobee are examples)", ["Yes", "No"])
    heating = st.selectbox("Does your home use electricity for heating?", ["Yes", "No"])
    air_conditioning = st.selectbox("Does your home use electricity for air conditioning?", ["Yes", "No"])
    hot_water = st.selectbox("Does your house use electricity for hot water?", ["Yes", "No"])

    st.header("Energy Efficient Appliances")
    st.write("Which of the following appliances are energy efficient? (Energy Star)")
    oven_stovetop = st.selectbox("Oven/Stovetop", ["Yes", "No"])
    washer = st.selectbox("Washer", ["Yes", "No"])
    dryer = st.selectbox("Dryer", ["Yes", "No"])
    refrigerator = st.selectbox("Refrigerator", ["Yes", "No"])

    confirm1 = st.checkbox("Confirm answers for this section")
    if confirm1:
        bar1 = st.progress(0)
        for p in [25,50,65,75,95,100]:
            time.sleep(0.5)
            bar1.progress(p)

        st.header("Detailed Appliance Information")
        oven_power_mode = st.selectbox("Energy rating mode for Oven/Stovetop", ["Actual","Average"])
        oven_watts = st.number_input("Enter Oven/Stovetop power (watts)", min_value=0.0) if oven_power_mode=="Actual" else 2350.0
        oven_usage_mode = st.selectbox("Usage mode for Oven/Stovetop (hours/month)", ["Actual","Average"])
        oven_hours = st.number_input("Enter Oven/Stovetop usage (hours/month)", min_value=0.0) if oven_usage_mode=="Actual" else 25

        washer_power_mode = st.selectbox("Energy rating mode for Washer", ["Actual","Average"])
        washer_watts = st.number_input("Enter Washer power (watts)", min_value=0.0) if washer_power_mode=="Actual" else 2000.0
        washer_usage_mode = st.selectbox("Usage mode for Washer (hours/month)", ["Actual","Average"])
        washer_hours = st.number_input("Enter Washer usage (hours/month)", min_value=0.0) if washer_usage_mode=="Actual" else 24

        dryer_power_mode = st.selectbox("Energy rating mode for Dryer", ["Actual","Average"])
        dryer_watts = st.number_input("Enter Dryer power (watts)", min_value=0.0) if dryer_power_mode=="Actual" else 2800.0
        dryer_usage_mode = st.selectbox("Usage mode for Dryer (hours/month)", ["Actual","Average"])
        dryer_hours = st.number_input("Enter Dryer usage (hours/month)", min_value=0.0) if dryer_usage_mode=="Actual" else 30

        refrigerator_power_mode = st.selectbox("Energy rating mode for Refrigerator", ["Actual","Average"])
        refrigerator_watts = st.number_input("Enter Refrigerator power (watts)", min_value=0.0) if refrigerator_power_mode=="Actual" else 2000.0
        refrigerator_usage_mode = st.selectbox("Usage mode for Refrigerator (hours/month)", ["Actual","Average"])
        refrigerator_hours = st.number_input("Enter Refrigerator usage (hours/month)", min_value=0.0) if refrigerator_usage_mode=="Actual" else 24

        st.header("Additional Questions")
        ev = st.selectbox("Do you currently own an electric vehicle?", ["Yes","No"])

        confirm2 = st.checkbox("Confirm all inputs and calculate results")
        if confirm2:
            bar2 = st.progress(0)
            for p in [20,50,75,100]:
                time.sleep(0.5)
                bar2.progress(p)

            energy_star_savings = 0.3
            thermostat_savings = 0.11
            windows_savings = 0.12
            money_converter = dollar_kwh_consumption / kwh_consumption if kwh_consumption > 0 else 0.20
            tesla_kwh_pm = 153.33

            if kwh_consumption == 0:
                st.warning("Warning: Monthly kWh consumption is zero. Savings calculations may be incomplete.")

            bulb_savings = num_conv_bulb * 52 * 1.6 * 30 / 1000
            thermostat_kwh = thermostat_savings * kwh_consumption if thermostat=="No" and kwh_consumption > 0 else 0
            windows_kwh = windows_savings * kwh_consumption if windows_replacement=="No" and kwh_consumption > 0 else 0
            washer_kwh = (washer_watts * washer_hours / 1000 * energy_star_savings) if washer=="No" else 0
            dryer_kwh = (dryer_watts * dryer_hours / 1000 * energy_star_savings) if dryer=="No" else 0
            oven_kwh = (oven_watts * oven_hours / 1000 * energy_star_savings) if oven_stovetop=="No" else 0
            refrigerator_kwh = (refrigerator_watts * refrigerator_hours / 1000 * energy_star_savings) if refrigerator=="No" else 0

            items = {
                "Bulbs": bulb_savings,
                "Thermostat": thermostat_kwh,
                "Windows": windows_kwh,
                "Washer": washer_kwh,
                "Dryer": dryer_kwh,
                "Oven/Stovetop": oven_kwh,
                "Refrigerator": refrigerator_kwh
            }
            total_kwh_saved = sum(items.values())
            total_money_saved = total_kwh_saved * money_converter

            st.header("Your Individualized Report")
            st.write(f"You have potential to save **{total_kwh_saved:.2f} kWh** and **${total_money_saved:.2f}** per month!")
            
            # --- ADDED VISUALIZATIONS ---
            if total_kwh_saved > 0:
                # 1. Savings Breakdown Bar Chart
                st.subheader("Savings Breakdown (kWh)")
                st.bar_chart(
                    {k: v for k, v in items.items() if v > 0},
                    x_label="Upgrade Category",  # Label for the X-axis
                    y_label="Potential Monthly Savings (kWh)", # Label for the Y-axis
                    color="#4CAF50"  # Green for energy savings
                    )
                
                # 2. Money Saved vs Energy Saved Scatter Plot
                st.subheader("Money Saved vs Energy Saved")
                fig = px.scatter(
                    x=list(items.keys()),
                    y=list(items.values()),
                    labels={"x": "Category", "y": "kWh Saved"},
                    size=[v * money_converter for v in items.values()],
                    color=list(items.keys()),
                    title="Size represents dollar savings"
                )
                st.plotly_chart(fig)

            if total_kwh_saved >= tesla_kwh_pm:
                st.success("You can save enough energy monthly to charge an electric vehicle!")

            for name, kwh in items.items():
                if kwh > 0:
                    st.write(f"{name}: saves {kwh:.2f} kWh → ${kwh*money_converter:.2f}")

            if st.button("View Credits / Sources"):
                st.header("Credits & Sources")
                st.write("- ENERGY STAR-qualified appliances reduce energy use by at least 30% of baseline usage (EPA / ENERGY STAR program)")
                st.link_button("View ENERGY STAR Appliance Info", "https://www.energystar.gov/products/energy_choices_count")
                st.write("- Smart learning thermostats reduce total energy consumption ~11% based on EPA estimates (10-12% HVAC savings, ~11% total)")
                st.link_button("View ENERGY STAR Smart Thermostat FAQ", "https://www.energystar.gov/products/heating_cooling/smart_thermostats/smart_thermostat_faq")
                st.write("- Efficient window upgrades can cut household energy bills by approximately 12%, within EPA-reported typical 7–15% range")
                st.link_button("View ENERGY STAR Windows, Doors, and Skylights", "https://www.energystar.gov/products/res_windows_doors_skylights")
                st.write("- Bulb wattage savings (52W per conventional bulb replaced with LED) based on typical incandescent vs LED averages")
                st.link_button("View Lighting Efficiency Article", "https://voltaelectricinc.com/blog/energy-efficient-lighting-how-to-lower-your-electricity-bill")
                st.write("- Tesla comparison: 153.33 kWh/month assumes 1,000 miles driven at ~300 Wh/mile (Tesla Model 3 average)")
                st.link_button("View Tesla Model 3 Energy Data", "https://ev-database.org/imp/car/1322/Tesla-Model-3-Performance")
        else:
            st.warning("Please confirm all inputs to proceed.")
    else:
        st.warning("Please confirm answers to proceed.")

    st.write("I hope this helps you save energy. None of your answers are stored.")
