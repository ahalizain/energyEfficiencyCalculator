import streamlit as st
import time
import matplotlib.pyplot as plt
import matplotlib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

# Set matplotlib to use non-interactive backend for Streamlit
matplotlib.use('Agg')

def generate_pdf(total_kwh_saved, total_money_saved, items, money_converter, tesla_kwh_pm, fig_bar, fig_scatter):
    """Generate a PDF report with energy savings data"""
    # Create PDF in memory
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # 612 x 792 points
    
    current_y = height - 50  # Track vertical position
    
    # Add title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, current_y, "Energy Efficiency Report")
    current_y -= 40
    
    # Add main summary text
    pdf.setFont("Helvetica-Bold", 14)
    summary_text = f"You have potential to save {total_kwh_saved:.2f} kWh and ${total_money_saved:.2f} per month!"
    pdf.drawString(50, current_y, summary_text)
    current_y -= 30
    
    # Add EV message if applicable
    if total_kwh_saved >= tesla_kwh_pm:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColorRGB(0, 0.6, 0)  # Green color
        pdf.drawString(50, current_y, "You can save enough energy monthly to charge an electric vehicle!")
        pdf.setFillColorRGB(0, 0, 0)  # Reset to black
        current_y -= 35
    else:
        current_y -= 15
    
    # Add Bar Chart: Savings Breakdown
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, current_y, "Savings Breakdown (kWh)")
    current_y -= 10
    
    # Convert matplotlib bar chart to image
    img_buffer_bar = io.BytesIO()
    fig_bar.savefig(img_buffer_bar, format='png', dpi=100, bbox_inches='tight')
    img_buffer_bar.seek(0)
    pdf.drawImage(ImageReader(img_buffer_bar), 50, current_y - 300, width=500, height=300)
    current_y -= 320
    
    # Add Scatter Plot: Money Saved vs Energy Saved
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, current_y, "Money Saved vs Energy Saved")
    current_y -= 10
    
    # Convert matplotlib scatter plot to image
    img_buffer_scatter = io.BytesIO()
    fig_scatter.savefig(img_buffer_scatter, format='png', dpi=100, bbox_inches='tight')
    img_buffer_scatter.seek(0)
    pdf.drawImage(ImageReader(img_buffer_scatter), 50, current_y - 300, width=500, height=300)
    current_y -= 320
    
    # Add itemized savings list
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, current_y, "Itemized Savings Breakdown:")
    current_y -= 20
    
    pdf.setFont("Helvetica", 11)
    for name, kwh in items.items():
        if kwh > 0:
            savings_text = f"{name}: saves {kwh:.2f} kWh → ${kwh*money_converter:.2f}"
            pdf.drawString(70, current_y, savings_text)
            current_y -= 18
    
    # Add footer text
    current_y -= 20
    pdf.setFont("Helvetica-Italic", 9)
    pdf.drawString(50, current_y, "Created March 2023. Updated regularly. Last Update Nov 2025.")
    current_y -= 15
    pdf.drawString(50, current_y, "I hope this helps you save energy. None of your answers are stored.")
    
    # Save and return
    pdf.save()
    buffer.seek(0)
    return buffer

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
            
            # --- VISUALIZATIONS ---
            if total_kwh_saved > 0:
                # 1. Savings Breakdown Bar Chart (Streamlit display)
                st.subheader("Savings Breakdown (kWh)")
                filtered_items = {k: v for k, v in items.items() if v > 0}
                st.bar_chart(
                    filtered_items,
                    x_label="Upgrade Category",
                    y_label="Potential Monthly Savings (kWh)",
                    color="#4CAF50"
                )
                
                # Create matplotlib version of bar chart for PDF
                fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
                ax_bar.bar(list(filtered_items.keys()), list(filtered_items.values()), color='#4CAF50')
                ax_bar.set_xlabel('Upgrade Category', fontsize=12)
                ax_bar.set_ylabel('Potential Monthly Savings (kWh)', fontsize=12)
                ax_bar.set_title('Savings Breakdown (kWh)', fontsize=14, fontweight='bold')
                ax_bar.grid(axis='y', alpha=0.3)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                # 2. Money Saved vs Energy Saved Scatter Plot
                st.subheader("Money Saved vs Energy Saved")
                
                # Create matplotlib scatter plot
                fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
                
                # Calculate sizes based on dollar savings (scale up for visibility)
                sizes = [v * money_converter * 100 for v in items.values()]
                
                # Create color map for different categories
                colors = plt.cm.tab10(range(len(items)))
                
                # Create scatter plot
                scatter = ax_scatter.scatter(
                    range(len(items.keys())),
                    list(items.values()),
                    s=sizes,
                    c=colors,
                    alpha=0.6,
                    edgecolors='black',
                    linewidth=1.5
                )
                
                # Set x-axis labels
                ax_scatter.set_xticks(range(len(items.keys())))
                ax_scatter.set_xticklabels(list(items.keys()), rotation=45, ha='right')
                ax_scatter.set_xlabel('Category', fontsize=12)
                ax_scatter.set_ylabel('kWh Saved', fontsize=12)
                ax_scatter.set_title('Size represents dollar savings', fontsize=14, fontweight='bold')
                ax_scatter.grid(alpha=0.3)
                plt.tight_layout()
                
                # Display in Streamlit
                st.pyplot(fig_scatter)

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
            
            # --- PDF DOWNLOAD BUTTON ---
            st.divider()
            st.subheader("Download Your Report")
            
            # Generate PDF with all data (only if there are savings to report)
            if total_kwh_saved > 0:
                pdf_file = generate_pdf(
                    total_kwh_saved=total_kwh_saved,
                    total_money_saved=total_money_saved,
                    items=items,
                    money_converter=money_converter,
                    tesla_kwh_pm=tesla_kwh_pm,
                    fig_bar=fig_bar,
                    fig_scatter=fig_scatter
                )
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_file,
                    file_name="energy_efficiency_report.pdf",
                    mime="application/pdf",
                    help="Download your personalized energy efficiency report as a PDF"
                )
            else:
                st.info("Complete the form with potential savings to generate a PDF report.")
            
        else:
            st.warning("Please confirm all inputs to proceed.")
    else:
        st.warning("Please confirm answers to proceed.")
    st.write("Created March 2023. Updated regularly. Last Update Nov 2025.")
    st.write("I hope this helps you save energy. None of your answers are stored.")
