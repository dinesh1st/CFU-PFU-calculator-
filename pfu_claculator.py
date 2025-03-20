import streamlit as st
import math

# Sidebar for navigation
st.sidebar.title("Choose a Calculator")
panel = st.sidebar.radio("Select:", ["Volumetric Calculation", "Bacteria-Phage density", "MOI Calculator", "CFU/PFU Calculator"])

# Panel 1: Volumetric Calculation
if panel == "Volumetric Calculation":
    st.title("Volumetric Calculation")
    st.markdown(r"Equation: $\text{Vol}_1 \times \text{Conc}_1 = \text{Vol}_2 \times \text{Conc}_2$")
    vol1 = st.number_input("Enter Vol1 (μL):", value=0.0, step=1.0)
    conc1 = st.number_input("Enter Conc1:", value=0.0, step=0.1)
    vol2 = st.number_input("Enter Vol2 (μL):", value=0.0, step=1.0)
    conc2 = st.number_input("Enter Conc2:", value=0.0, step=0.1)

    # Calculate missing value
    if st.button("Calculate Missing Value"):
        if vol1 == 0:
            vol1 = (vol2 * conc2) / conc1
            st.success(f"Vol1 = {vol1:.2f} μL")
        elif conc1 == 0:
            conc1 = (vol2 * conc2) / vol1
            st.success(f"Conc1 = {conc1:.2f}")
        elif vol2 == 0:
            vol2 = (vol1 * conc1) / conc2
            st.success(f"Vol2 = {vol2:.2f} μL")
        elif conc2 == 0:
            conc2 = (vol1 * conc1) / vol2
            st.success(f"Conc2 = {conc2:.2f}")
        else:
            st.warning("Please leave one field blank to calculate its value.")

# Panel 2: Bacteria-Phage density
elif panel == "Bacteria-Phage density":
    st.title("Bacteria-Phage density")
    st.markdown(r"Equation: $\text{Vol}_1 \times 10^{\text{density}_1} = \text{Vol}_2 \times 10^{\text{density}_2}$")
    vol1 = st.number_input("Enter Vol1 (μL):", value=0.0, step=1.0)
    density1 = st.number_input("Enter density1 (e.g., 5 for 10^5):", value=0.0, step=1.0)
    vol2 = st.number_input("Enter Vol2 (μL):", value=0.0, step=1.0)
    density2 = st.number_input("Enter density2 (e.g., 5 for 10^5):", value=0.0, step=1.0)

    # Calculate missing value
    if st.button("Calculate Missing Value"):
        if vol1 == 0:
            vol1 = (vol2 * (10 ** conc2)) / (10 ** conc1)
            st.success(f"Vol1 = {vol1:.2f} μL")
        elif density1 == 0:
            density1 = st.log10((vol2 * (10 ** density2)) / vol1)
            st.success(f"Conc1 = {conc1:.2f}")
        elif vol2 == 0:
            vol2 = (vol1 * (10 ** density1)) / (10 ** density2)
            st.success(f"Vol2 = {vol2:.2f} μL")
        elif density2 == 0:
            density2 = st.log10((vol1 * (10 ** density1)) / vol2)
            st.success(f"density2 = {density2:.2f}")
        else:
            st.warning("Please leave one field blank to calculate its value.")

# Panel 3: MOI Calculator
elif panel == "MOI Calculator":
    st.title("MOI Calculator")
    st.markdown(r"**Equation: $\text{MOI} = \frac{\text{PFU/mL (phage)}}{\text{CFU/mL (bacteria)}}$**")

    # User inputs in logarithmic form
    moi = st.number_input("Enter MOI (leave blank if unknown, set to 0.0):", value=0.0, step=0.1)
    log_pfu_per_ml = st.number_input("Enter log(PFU/mL) (e.g., 5 for 10^5, leave blank if unknown, set to 0.0):", value=0.0, step=1.0)
    log_cfu_per_ml = st.number_input("Enter log(CFU/mL) (e.g., 5 for 10^5, leave blank if unknown, set to 0.0):", value=0.0, step=1.0)

    # Convert log values to standard numbers (only if not zero)
    pfu_per_ml = 10 ** log_pfu_per_ml if log_pfu_per_ml > 0 else 0.0
    cfu_per_ml = 10 ** log_cfu_per_ml if log_cfu_per_ml > 0 else 0.0

    # Calculate missing value
    if st.button("Calculate Missing Value"):
        # Check if exactly one field is missing
        num_missing = sum([moi == 0, pfu_per_ml == 0, cfu_per_ml == 0])
        
        if num_missing == 1:  # Ensure only one field is blank
            if moi == 0:  # Calculate MOI
                if cfu_per_ml > 0:
                    moi = pfu_per_ml / cfu_per_ml
                    st.success(f"MOI = {moi:.2f}")
                else:
                    st.error("CFU/mL must be greater than 0 to calculate MOI.")
            elif cfu_per_ml == 0:  # Calculate CFU/mL
                if moi > 0:
                    cfu_per_ml = pfu_per_ml / moi
                    if cfu_per_ml > 0:
                        st.success(f"CFU/mL = {cfu_per_ml:.2e} (Logarithmic: {math.log10(cfu_per_ml):.2f})")
                    else:
                        st.error("CFU/mL cannot be 0 or negative.")
                else:
                    st.error("MOI must be greater than 0 to calculate CFU/mL.")
            elif pfu_per_ml == 0:  # Calculate PFU/mL
                if moi > 0:
                    pfu_per_ml = moi * cfu_per_ml
                    if pfu_per_ml > 0:
                        st.success(f"PFU/mL = {pfu_per_ml:.2e} (Logarithmic: {math.log10(pfu_per_ml):.2f})")
                    else:
                        st.error("PFU/mL cannot be 0 or negative.")
                else:
                    st.error("MOI must be greater than 0 to calculate PFU/mL.")
        else:
            st.warning("Please leave exactly one field blank to calculate its value.")
            
# Panel 4: Original CFU/PFU Calculator
elif panel == "CFU/PFU Calculator":
    st.title("CFU/PFU Calculator")
    # Input fields
    counted_colonies = st.number_input("Counted Colonies (CFUs):", min_value=0.0, step=1.0, format="%.0f")
    dilution_factor = st.number_input("Dilution Factor (e.g., enter 5 for 10^5):", min_value=0.0, step=1.0, format="%.0f")
    volume_microliters = st.number_input("Volume Used (μL):", min_value=0.0, step=1.0, format="%.0f")

    # Convert dilution factor (e.g., 5) to 10^5
    if dilution_factor > 0:
        dilution = 10 ** dilution_factor
    else:
        dilution = 1

    # Convert microliters to milliliters for calculation
    volume_milliliters = volume_microliters / 1000.0

    # Calculate button
    if st.button("Calculate CFU/mL"):
        if volume_microliters == 0:
            st.error("Volume cannot be zero.")
        else:
            cfu_per_ml = (counted_colonies * dilution) / volume_milliliters
            scientific_notation = "{:.2e}".format(cfu_per_ml)  # Convert to scientific notation
            st.success(f"CFU/mL: {scientific_notation}")
        
st.markdown("---")
st.markdown("**Credit: Dinesh Subedi**")
