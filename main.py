import streamlit as st

# command to run: streamlit run main.py
#
if __name__ == "__main__":
    # title and description of website
    st.title("Energy Efficiency Calculator")
    st.write("This will calculate your energy savings using some questions. Results will be immediately shown.")

    # Fields(aka Questions for the webapp)
    house_area = st.number_input("Enter square footage of the house")
    kwh_comsumption = st.number_input(
        "What is the average total monthly energy consumption in your house in Kilowatt Hour(KWH)?")

    dollar_kwh_comsumption = st.number_input("What is the average total monthly energy cost in your house, in dollars?")
    windows_replacement = st.selectbox(
        "Have the windows in your house been replaced with high efficiency ones in the last 15yrs?", ["Yes", "No"])
    num_conv_bulb = st.number_input("Enter the number of conventional light bulbs in the house.")
    num_led_bulb = st.number_input("Enter the number of LED lightbulbs in the house.")
    thermostat = st.selectbox("Do you have learning thermostat in the house?(Google Nest or Ecobee are examples)",
                              ["Yes", "No"])
    heating = st.selectbox("Does your home use electricity for heating?", ["Yes", "No"])
    air_conditioning = st.selectbox("Does your home use electricity for air conditioning?", ["Yes", "No"])
    hot_water = st.selectbox("Does your house use electricity for hot water?", ["Yes", "No"])
    st.write("Which of the following appliances are energy efficient? (Energy Star)")
    oven_stovetop = st.selectbox("Oven/Stovetop", ["Yes", "No"])
    washer = st.selectbox("Washer", ["Yes", "No"])
    dryer = st.selectbox("Dryer", ["Yes", "No"])
    refridgerator = st.selectbox("Refridgerator", ["Yes", "No"])
    # Avg or User Input
    # variables for kWh will be appliancekWh and vars for hours/month will be appliance_hPm
    st.write(
        "For these next few questions, I will ask you the energy rating & hours per month usage for the non-energy efficient appliances that you own. You have a choice to either write in the exact kwh rating of the appliance and the exact hours of usage per month or select the option 'average' from the drop-down menu where we will use an average value of kwh rating of the appliance and average usage per month.\n")
    st.write("Note: if you selected average for energy rating and hours of usage per month, then skip the next question. Only reply to the appliances that are not energy efficient in your house.")
    # Oven/Stovetop
    # Oven/Stovetopkwhhpm
    ovenStoveTop_input = st.selectbox(
        "Would you like your energy rating for your Oven/Stovetop an Average value or an actual value?",
        ["Actual", "Average"])
    userOvenkWh = st.number_input(
        "Please enter in the kWh/energy rating for your oven/stovetop(ONLY IF YOU SELECTED 'ACTUAL'): ")
    if ovenStoveTop_input == "Actual":

        ovenkWh = userOvenkWh

    else:
        ovenkWh = 2350.00

    ovenStoveTop_input_hPm = st.selectbox(
        "Would you like your hours per month for your Oven/Stovetop an Average value or an actual value?",
        ["Actual", "Average"])
    userOvenhPm = st.number_input(
        "Please enter in the hours per month for your oven/stovetop(ONLY IF YOU SELECTED 'ACTUAL'): ")
    if ovenStoveTop_input_hPm == "Actual":
        ovenhPm = userOvenhPm
    else:
        ovenhPm = 25

    # Washerkwhhpm
    washer_input = st.selectbox(
        "Would you like your energy rating for your Washer an Average value or an actual value?",
        ["Actual", "Average"])
    userwasherkWh = st.number_input(
        "Please enter in the kWh/energy rating for your washer(ONLY IF YOU SELECTED 'ACTUAL'): ")
    if washer_input == "Actual":

        washerkWh = userwasherkWh

    else:
        washerkWh = 2000
    washer_input_hPm = st.selectbox(
        "Would you like your hours per month for your Washer an Average value or an actual value?",
        ["Actual", "Average"])
    userwasherhPm = st.number_input(
        "Please enter in the hours per month for your washer(ONLY IF YOU SELECTED 'ACTUAL'): ")
    if washer_input_hPm == "Actual":
        washerhPm = userwasherhPm
    else:
        washerhPm = 24
    # Dryerkwhhpm
    dryer_input = st.selectbox("Would you like your energy rating for your Dryer an Average value or an actual value?",
                               ["Actual", "Average"])
    userdryerkWh = st.number_input(
        "Please enter in the kWh/energy rating for your dryer(ONLY OF YOU SELECTED 'ACTUAL'): ")
    if dryer_input == "Actual":

        dryerkWh = userdryerkWh

    else:
        dryerkWh = 2800
    dryer_input_hPm = st.selectbox(
        "Would you like your hours per month for your Dryer an Average value or an actual value?",
        ["Actual", "Average"])
    userdryerhPm = st.number_input(
        "Please enter in the hours per month for your dryer(ONLY IF YOU SELECTED 'ACTUAL'): ")
    if dryer_input_hPm == "Actual":
        dryerhPm = userdryerhPm
    else:
        dryerhPm = 30
    # FridgekWhHPm

    refridgerator_input = st.selectbox(
        "Would you like your energy rating for your Fridge an Average value or an actual value?",
        ["Average", "Actual"])
    userrefridgeratorkWh = st.number_input(
        "Please enter in the kWh/energy rating for your refridgerator(ONLY OF YOU SELECTED 'ACTUAL'): ")
    if refridgerator_input == "Actual":

        refridgeratorkWh = userrefridgeratorkWh

    else:
        refridgeratorkWh = 2000
    refridgerator_input_hPm = st.selectbox(
        "Would you like your hours per month for your Fridge an Average value or an actual value?",
        ["Average", "Actual"])
    userrefridgeratorhPm = st.number_input(
        "Please enter in the hours per month for your refridgerator(ONLY IF YOU SELECTED 'ACTUAL'): ")
    if refridgerator_input_hPm == "Actual":
        refridgeratorhPm = userrefridgeratorhPm
    else:
        refridgeratorhPm = 24
    # More Questions:

    ev = st.selectbox("Do you currently own a electric vehicle?", ["Yes", "No"])

    # All Calculations & New Variables

    kwhsaved = 0
    num_bulb = num_conv_bulb
    watt_savings = 52
    hours_per_day = 1.6
    days_in_a_month = 30
    watt_to_kwh = 1000
    bulb_savings = num_bulb * watt_savings * hours_per_day * days_in_a_month / watt_to_kwh
    kwhsaved += bulb_savings
    tesla_kwhPm = 153.33
    num_notEnergyStar = 0
    energy_star_savings = 0.3
    money_converter = 0.20
    thermostat_savings = 0.11
    windows_savings = 0.12
    washerS = 0
    dryerS = 0
    oven_stovetopS = 0
    refridgeratorS = 0
    # If statements
    if windows_replacement == "Yes":
        kwhsaved += 113.40
        windowsY = "was"
    if windows_replacement == "No":
        windowsY = "was not"
    if thermostat == "Yes":
        kwhsaved += 103.95
        thermostatY = "was"
    if thermostat == "No":
        thermostatY = "was not"
    # Washer/Dryer(if statements)
    washerS += washerkWh*washerhPm/1000 * energy_star_savings
    dryerS += dryerkWh*dryerhPm/1000 * energy_star_savings
    if dryer == "Yes":
        dryerY = "was"
    if washer == "Yes":
        washerY = "was"
    if washer == "No":
        kwhsaved += 14.40
        num_notEnergyStar += 1
        washerY = "was not"
    if dryer == "No":
        num_notEnergyStar += 1
        kwhsaved += 25.20
        dryerY = "was not"
    #washerdryerS = washerS + dryerS
    #washerdryer_totalS = dryerkWh - dryerS + washerkWh - washerS
    # Oven/Stovetop(if statements)
    oven_stovetopS += ovenkWh*ovenhPm/1000 * energy_star_savings
    if oven_stovetop == "No":
        kwhsaved += 17.63
        ovenStovetopY = "was not"
        num_notEnergyStar += 1
    if oven_stovetop == "Yes":
        ovenStovetopY = "was"
    #oven_totalS = ovenkWh - oven_stovetopS
    # Fridge(if statements)
    refridgeratorS = refridgeratorkWh *refridgeratorhPm/1000* energy_star_savings
    if refridgerator == "No":
        kwhsaved += 17.82
        refridgeratorY = "was not"
        num_notEnergyStar += 1
    if refridgerator == "Yes":
        refridgeratorY = "was"
    #refridgerator_totalS = refridgeratorkWh - refridgeratorS

    # Results
    st.write("Your individualized report is as follows:\n")
    if kwhsaved >= 153.33:
        st.write(
            "There is room to save enough energy in your housesold to buy a electric vehicle! You can save up to " + "%.2f" %
                kwhsaved + " kwh! \n")
    else:
        st.write(
            "There is room to save enough energy in your housesold to buy a electric vehicle! You can save up to " + "%.2f" %
                kwhsaved + " kwh! \n")

    # Bulbs
    bulb_savings_string = "%.2f" % bulb_savings
    bulb_savings_m = bulb_savings*money_converter
    bulb_savings_money  = "%.2f" % bulb_savings_m
    st.write("You currently have " + str(
        num_conv_bulb) + " conventional bulbs in your home. If you were to switch to LED Bulbs, then you would save " + "%.2f" % bulb_savings + " kwh in your household just by switching to LED bulbs. You would save $" +
        str(bulb_savings_money) + " on doing this action.")
    # Smart Thermostat
    if thermostatY == "was not":
        st.write(
            "You do not have a smart thermostat installed in your home. If you do switch to using one, then you will save 11% of your total kwh energy consumtion for the month, which is " + str(
                thermostat_savings * kwh_comsumption) + " kwh per month. You will also save $" + str(
                thermostat_savings * kwh_comsumption * money_converter) + " per month in doing this. \n")
    # Washer & Dryer
    if washerY == "was not":
        st.write(
            "Your washer was not energy star rated. If you were to make this energy star rated, you will save " + str(
                washerS) + " kwh per month and $" + str(washerS * money_converter))
    if dryerY == "was not":
        st.write(
            "Your dryer was not energy star rated. If you were to make this energy star rated, you will save " + str(
                dryerS) + " kwh per month and $" + str(dryerS * money_converter))
    if refridgeratorY == "was not":
        st.write(
            "Your refridgerator was not energy star rated. If you were to make this energy star rated, you will save " + str(
                refridgeratorS) + " kwh per month and $" + str(refridgeratorS * money_converter))
    if ovenStovetopY == "was not":
        st.write("Your oven/stovetop was not energy star rated. To make this energy star rated, you will save " + str(
            oven_stovetopS) + " kwh per month and $" + str(oven_stovetopS * money_converter))
    # Windows
    if windowsY == "was not":
        st.write(
            "You do not have windows installed in your home. If you do install one, then you will save 12% of your total kwh energy consumtion for the month, which is " + str(
                windows_savings * kwh_comsumption) + " kwh per month. You will also save $" + str(
                windows_savings * kwh_comsumption * money_converter) + " per month in doing this. \n")

st.write(
    "I hope this helps you save energy. None of your answers are stored and you are the only person able to see these results.\n")
st.write("Have a nice day!")

# WHATS DONE SO FAR:
# oven/stovetop
# fridge
# washer/dryerr
