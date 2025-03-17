import streamlit as st
# Inject meta tags
st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
    <meta name="description" content="CFU Calculator - Calculate CFU/mL with dilution and volume inputs. Designed for microbiologists!">
    <meta name="keywords" content="CFU, microbiology, scientific calculator, dilution factor">
    <meta name="author" content="Dinesh Subedi">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFU Calculator</title>
</head>
</html>
""", height=0)
    
     

st.title("CFU Calculator")

# Input fields
counted_colonies = st.number_input("Counted Colonies (CFUs):", min_value=0.0, step=1.0, format="%.0f")
dilution_factor = st.number_input("Dilution Factor (e.g., enter 5 for 10^-5):", min_value=0.0, step=1.0, format="%.0f")
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

# Add credits
st.markdown("---")
st.markdown("**Credit: Dinesh Subedi**")
