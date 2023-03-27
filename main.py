import streamlit as st

# command to run: streamlit run main.py
#
if __name__ == "__main__":
    # title and description of website
    st.title("Energy Efficiency Calculator")
    st.write("An easy, user-friendly application created by Zain Ahmad \n")
    
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
        ["Actual", "Average"])
    userrefridgeratorkWh = st.number_input(
        "Please enter in the kWh/energy rating for your refridgerator(ONLY OF YOU SELECTED 'ACTUAL'): ")
    if refridgerator_input == "Actual":

        refridgeratorkWh = userrefridgeratorkWh

    else:
        refridgeratorkWh = 2000
    refridgerator_input_hPm = st.selectbox(
        "Would you like your hours per month for your Fridge an Average value or an actual value?",
        ["Actual", "Average"])
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
    thermostat_savings = 0.11*0.53
    windows_savings = 0.12*0.53
    washerS = 0
    dryerS = 0
    oven_stovetopS = 0
    refridgeratorS = 0
    # If statements
    if windows_replacement == "Yes":
        windowsY = "was"
    if windows_replacement == "No":
        kwhsaved += 113.40
        windowsY = "was not"
    if thermostat == "Yes":
        thermostatY = "was"
    if thermostat == "No":
        kwhsaved += 103.95
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
            "There is room to save enough energy in your housesold to buy a electric vehicle! You have potential to save " + "%.2f" %
                kwhsaved + " kwh! \n")
    else:
        st.write(
            "There is not enough room to save energy in your housesold to buy a electric vehicle. You have potential to save up to " + "%.2f" %
                kwhsaved + " kwh! \n")

    # Bulbs
    bulb_savings_string = "%.2f" % bulb_savings
    bulb_savings_m = bulb_savings*money_converter
    bulb_savings_money  = "%.2f" % bulb_savings_m
    st.write("You currently have " + str(
        num_conv_bulb) + " conventional bulbs in your home. If you were to switch to LED Bulbs, then you would save " + "%.2f" % bulb_savings + " kwh in your household just by switching to LED bulbs. You would save $" +
        str(bulb_savings_money) + " on doing this action.")
    # Smart Thermostat
    thermo_savings_string = "%.2f" % thermostat_savings
    thermo_savings_m = thermostat_savings*money_converter
    thermo_savings_money  = "%.2f" % thermo_savings_m
    if thermostatY == "was not":
        st.write(
            "You do not have a smart thermostat installed in your home. If you do switch to using one, then you will save 11% of about half of your total kwh energy consumtion for the month, which is " + str(
                thermo_savings_string*kwh_consumption) + " kwh per month. You will also save $" + str(
                thermo_savings_money * kwh_comsumption) + " per month in doing this. \n")
    # Washer & Dryer
    washer_savings_m= washerS * money_converter
    washer_savings_money = "%.2f" % washer_savings_m
    if washerY == "was not":
        st.write(
            "Your washer was not energy star rated. If you were to make this energy star rated, you will save " + "%.2f" %
                washerS + " kwh per month and $" + str(washer_savings_money))
    dryer_savings_m = dryerS * money_converter
    dryer_savings_money = "%.2f" % dryer_savings_m
    if dryerY == "was not":
        st.write(
            "Your dryer was not energy star rated. If you were to make this energy star rated, you will save " + "%.2f" %
                dryerS + " kwh per month and $" + str(dryer_savings_money))
    refridgerator_savings_m = refridgeratorS * money_converter
    refridgerator_savings_money = "%.2f" % refridgerator_savings_m
    if refridgeratorY == "was not":
        st.write(
            "Your refridgerator was not energy star rated. If you 5were to make this energy star rated, you will save " + "%.2f" %
                refridgeratorS + " kwh per month and $" + str(refridgerator_savings_money))
    oven_savings_m = oven_stovetopS * money_converter
    oven_savings_money = "%.2f" % oven_savings_m
    if ovenStovetopY == "was not":
        st.write("Your oven/stovetop was not energy star rated. To make this energy star rated, you will save " + "%.2f" %
            oven_stovetopS + " kwh per month and $" + str(oven_savings_money))
    # Windows
    windowsS = windows_savings * kwh_comsumption
    windows_money = windowsS * money_converter
    windows_money_m = "%.2f" % windows_money
    if windowsY == "was not":
        st.write(
            "You do not have energy efficient windows installed in your home. If you do install one, then you will save 12% of your total kwh energy consumtion for the month, which is " + "%.2f" %
                 windowsS + " kwh per month. You will also save $" + str(
                windows_money_m) + " per month in doing this. \n")

st.write(
    "I hope this helps you save energy. None of your answers are stored and you are the only person able to see these results.\n")
st.write("Have a nice day!")

# WHATS DONE SO FAR:
# oven/stovetop
# fridge
# washer/dryer
