import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SHIPWISE_API_ENDPOINT = os.getenv('SHIPWISE_API_ENDPOINT')
SHIPWISE_API_TOKEN = os.getenv('SHIPWISE_API_TOKEN')
SHIPWISE_CLIENT_ID = os.getenv('SHIPWISE_CLIENT_ID')
SHIPWISE_PROFILE_ID = os.getenv('SHIPWISE_PROFILE_ID')

# Page config
st.set_page_config(page_title="ShipWise Rate Quote", layout="wide")

# Title
st.title("Get Shipping Rates")
st.write("Enter your shipment details to compare carrier rates")

# Initialize session state for packages
if 'packages' not in st.session_state:
    st.session_state.packages = [{'id': 1, 'items': [{'id': 1}]}]

def add_package():
    new_id = len(st.session_state.packages) + 1
    st.session_state.packages.append({'id': new_id, 'items': [{'id': 1}]})

def remove_package(index):
    if len(st.session_state.packages) > 1:
        st.session_state.packages.pop(index)

def add_item(pkg_index):
    new_id = len(st.session_state.packages[pkg_index]['items']) + 1
    st.session_state.packages[pkg_index]['items'].append({'id': new_id})

def remove_item(pkg_index, item_index):
    if len(st.session_state.packages[pkg_index]['items']) > 1:
        st.session_state.packages[pkg_index]['items'].pop(item_index)

# Ship To Address
st.header("Destination Address")
col1, col2 = st.columns(2)
with col1:
    to_name = st.text_input("Recipient Name*", key="to_name")
    to_address1 = st.text_input("Street Address*", key="to_address1")
    to_city = st.text_input("City*", key="to_city")
    to_country = st.text_input("Country Code* (e.g., US, CA, GB)", value="US", key="to_country")
with col2:
    to_company = st.text_input("Company (optional)", key="to_company")
    to_address2 = st.text_input("Apt/Suite (optional)", key="to_address2")
    to_state = st.text_input("State/Province*", key="to_state")
    to_postal = st.text_input("Postal/Zip Code*", key="to_postal")

# Ship From Address
st.header("Origin Address")
col1, col2 = st.columns(2)
with col1:
    from_name = st.text_input("Shipper Name*", key="from_name")
    from_address1 = st.text_input("Street Address*", key="from_address1")
    from_city = st.text_input("City*", key="from_city")
    from_country = st.text_input("Country Code*", value="US", key="from_country")
with col2:
    from_company = st.text_input("Company (optional)", key="from_company")
    from_address2 = st.text_input("Suite/Building (optional)", key="from_address2")
    from_state = st.text_input("State/Province*", key="from_state")
    from_postal = st.text_input("Postal/Zip Code*", key="from_postal")

# Check if international
is_international = to_country.upper() != from_country.upper()

# Customs Information (only for international)
if is_international:
    st.header("Customs Information")
    st.info("International shipment detected - please provide customs information")
    col1, col2 = st.columns(2)
    with col1:
        customs_description = st.text_input("Contents Description*", placeholder="e.g., Electronics, Clothing, Books")
        customs_signer = st.text_input("Customs Signer Name*", placeholder="Your name or shipping manager")
    with col2:
        customs_tag = st.selectbox("Shipment Type*", 
            ["Merchandise", "Gift", "Sample", "Documents", "Return Goods", "Other"])
        customs_origin = st.text_input("Origin Country Code*", value=from_country.upper())

# Packages Section
st.header("Package Details")

for pkg_idx, package in enumerate(st.session_state.packages):
    with st.expander(f"Package {pkg_idx + 1}", expanded=True):
        col1, col2 = st.columns([6, 1])
        with col2:
            if len(st.session_state.packages) > 1:
                if st.button("🗑️ Remove", key=f"remove_pkg_{pkg_idx}"):
                    remove_package(pkg_idx)
                    st.rerun()
        
        st.subheader("Package Dimensions & Weight")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            package['length'] = st.number_input("Length (inches)*", min_value=0.0, step=0.1, key=f"length_{pkg_idx}")
        with col2:
            package['width'] = st.number_input("Width (inches)*", min_value=0.0, step=0.1, key=f"width_{pkg_idx}")
        with col3:
            package['height'] = st.number_input("Height (inches)*", min_value=0.0, step=0.1, key=f"height_{pkg_idx}")
        with col4:
            package['total_weight'] = st.number_input("Total Weight (lbs)*", min_value=0.0, step=0.1, key=f"total_weight_{pkg_idx}")
        
        package['value'] = st.number_input("Package Value ($)*", min_value=0.0, step=0.01, key=f"value_{pkg_idx}", 
                                          help="Total declared value for insurance purposes")
        
        # Items in package
        st.subheader("Items in Package")
        for item_idx, item in enumerate(package['items']):
            with st.container():
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.markdown(f"**Item {item_idx + 1}**")
                with col2:
                    if len(package['items']) > 1:
                        if st.button("🗑️", key=f"remove_item_{pkg_idx}_{item_idx}"):
                            remove_item(pkg_idx, item_idx)
                            st.rerun()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    item['description'] = st.text_input("Product Description*", key=f"desc_{pkg_idx}_{item_idx}", 
                                                       placeholder="e.g., Cotton T-Shirt")
                    item['quantity'] = st.number_input("Quantity*", min_value=1, step=1, key=f"qty_{pkg_idx}_{item_idx}")
                with col2:
                    item['unit_price'] = st.number_input("Unit Price ($)*", min_value=0.0, step=0.01, key=f"price_{pkg_idx}_{item_idx}")
                    item['weight'] = st.number_input("Weight per Item (lbs)*", min_value=0.0, step=0.01, key=f"weight_{pkg_idx}_{item_idx}")
                with col3:
                    if is_international:
                        item['harmonized_code'] = st.text_input("HS Code*", key=f"hs_{pkg_idx}_{item_idx}",
                                                                placeholder="e.g., 6109.10.00")
                        item['country_origin'] = st.text_input("Country of Origin*", value=from_country.upper(), 
                                                              key=f"origin_{pkg_idx}_{item_idx}")
                    else:
                        item['harmonized_code'] = st.text_input("HS Code (optional)", key=f"hs_{pkg_idx}_{item_idx}",
                                                                placeholder="e.g., 6109.10.00")
                        item['country_origin'] = st.text_input("Country of Origin (optional)", value=from_country.upper(), 
                                                              key=f"origin_{pkg_idx}_{item_idx}")
                
                st.divider()
        
        if st.button(f"Add Item to Package {pkg_idx + 1}", key=f"add_item_{pkg_idx}"):
            add_item(pkg_idx)
            st.rerun()

if st.button("Add Another Package", key="add_package"):
    add_package()
    st.rerun()

st.divider()

# Generate payload and get rates
if st.button("Get Shipping Rates", type="primary", use_container_width=True):
    # Validation
    if not all([to_name, to_address1, to_city, to_state, to_postal, to_country]):
        st.error("Please fill in all required destination address fields")
    elif not all([from_name, from_address1, from_city, from_state, from_postal, from_country]):
        st.error("Please fill in all required origin address fields")
    elif is_international and not all([customs_description, customs_signer]):
        st.error("Please fill in all required customs information for international shipments")
    elif not SHIPWISE_API_ENDPOINT or not SHIPWISE_API_TOKEN or not SHIPWISE_CLIENT_ID or not SHIPWISE_PROFILE_ID:
        st.error("API credentials not configured. Please check your .env file.")
    else:
        # Build payload
        payload = {
            "clientId": SHIPWISE_CLIENT_ID,
            "profileId": SHIPWISE_PROFILE_ID,
            "to": {
                "name": to_name,
                "company": to_company,
                "address1": to_address1,
                "address2": to_address2,
                "city": to_city,
                "postalCode": to_postal,
                "state": to_state,
                "countryCode": to_country.upper()
            },
            "from": {
                "name": from_name,
                "company": from_company,
                "address1": from_address1,
                "address2": from_address2,
                "city": from_city,
                "postalCode": from_postal,
                "state": from_state,
                "countryCode": from_country.upper()
            },
            "packages": []
        }
        
        # Add packages
        for package in st.session_state.packages:
            pkg_data = {
                "weightUnit": "LB",
                "contentWeight": sum([item.get('weight', 0) * item.get('quantity', 0) for item in package['items']]),
                "totalWeight": package.get('total_weight', 0),
                "packaging": {
                    "length": package.get('length', 0),
                    "width": package.get('width', 0),
                    "height": package.get('height', 0)
                },
                "value": package.get('value', 0),
                "items": []
            }
            
            # Add customs for international
            if is_international:
                pkg_data["customs"] = {
                    "contentsDescription": customs_description,
                    "originCountry": customs_origin.upper(),
                    "signer": customs_signer,
                    "customsTag": customs_tag,
                    "items": []
                }
            
            # Add items
            for item in package['items']:
                item_data = {
                    "sku": f"ITEM-{item.get('id', '')}",
                    "quantityToShip": item.get('quantity', 0),
                    "unitPrice": item.get('unit_price', 0),
                    "harmonizedCode": item.get('harmonized_code', ''),
                    "countryOfOrigin": item.get('country_origin', from_country.upper()),
                    "customsDescription": item.get('description', ''),
                    "customsDeclaredValue": item.get('unit_price', 0),
                    "weight": item.get('weight', 0)
                }
                pkg_data["items"].append(item_data)
                
                # Add to customs items if international
                if is_international:
                    customs_item = {
                        "sku": f"ITEM-{item.get('id', '')}",
                        "description": item.get('description', ''),
                        "qty": item.get('quantity', 0),
                        "value": item.get('unit_price', 0),
                        "weight": item.get('weight', 0),
                        "countryOfMfg": item.get('country_origin', from_country.upper()),
                        "harmCode": item.get('harmonized_code', '')
                    }
                    pkg_data["customs"]["items"].append(customs_item)
            
            payload["packages"].append(pkg_data)
        
        # Display payload in debug mode
        with st.expander("Debug: View Request Payload"):
            st.json(payload)
        
        # Make API call
        with st.spinner("Fetching rates from carriers..."):
            try:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {SHIPWISE_API_TOKEN}'
                }
                
                response = requests.post(
                    SHIPWISE_API_ENDPOINT,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                response.raise_for_status()
                rate_data = response.json()
                
                # Display rates
                st.success("Rates retrieved successfully!")
                st.header("Available Shipping Options")
                
                # Try to parse common rate formats
                rates = None
                if 'rates' in rate_data and isinstance(rate_data['rates'], list):
                    rates = rate_data['rates']
                elif 'serviceRates' in rate_data:
                    rates = rate_data['serviceRates']
                elif 'services' in rate_data:
                    rates = rate_data['services']
                elif isinstance(rate_data, list):
                    rates = rate_data
                
                if rates and len(rates) > 0:
                    # Sort rates by price (lowest first)
                    def get_rate_cost(rate):
                        return float(rate.get('totalCharge') or rate.get('rate') or rate.get('cost') or rate.get('price') or 999999)
                    
                    sorted_rates = sorted(rates, key=get_rate_cost)
                    
                    for idx, rate in enumerate(sorted_rates):
                        # Determine if this is the cheapest option
                        is_cheapest = idx == 0
                        
                        with st.container():
                            col1, col2, col3 = st.columns([3, 2, 1])
                            
                            with col1:
                                carrier = rate.get('carrier') or rate.get('carrierName') or 'Unknown Carrier'
                                service = rate.get('serviceName') or rate.get('service') or rate.get('serviceType') or ''
                                
                                if is_cheapest:
                                    st.markdown(f"### 🏆 {carrier} - {service}")
                                    st.caption("💚 Best Value")
                                else:
                                    st.markdown(f"### {carrier} - {service}")
                                
                                service_code = rate.get('serviceCode')
                                if service_code:
                                    st.caption(f"Service Code: {service_code}")
                            
                            with col2:
                                delivery_days = rate.get('deliveryDays') or rate.get('transitDays')
                                delivery_date = rate.get('deliveryDate') or rate.get('estimatedDelivery')
                                
                                if delivery_days:
                                    st.write(f"**{delivery_days}** business days")
                                elif delivery_date:
                                    st.write(f"By **{delivery_date}**")
                                else:
                                    st.write("Delivery time varies")
                            
                            with col3:
                                cost = rate.get('totalCharge') or rate.get('rate') or rate.get('cost') or rate.get('price')
                                if cost:
                                    if is_cheapest:
                                        st.markdown(f"### :green[${float(cost):.2f}]")
                                    else:
                                        st.markdown(f"### ${float(cost):.2f}")
                                
                                currency = rate.get('currency')
                                if currency and currency != 'USD':
                                    st.caption(currency)
                            
                            # Show breakdown if available
                            if 'breakdown' in rate or 'charges' in rate:
                                breakdown = rate.get('breakdown') or rate.get('charges')
                                with st.expander("View Cost Breakdown"):
                                    if isinstance(breakdown, dict):
                                        for key, value in breakdown.items():
                                            st.write(f"**{key}:** ${value}")
                                    else:
                                        st.json(breakdown)
                            
                            st.divider()
                    
                    # Summary
                    st.info(f"Found **{len(rates)}** shipping options")
                    
                else:
                    st.warning("No rates found. Response format:")
                    st.json(rate_data)
                
                # Full response in expandable section
                with st.expander("View Full API Response"):
                    st.json(rate_data)
                
            except requests.exceptions.RequestException as e:
                st.error(f"API Error: {str(e)}")
                if hasattr(e.response, 'text'):
                    with st.expander("View Error Details"):
                        st.code(e.response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("Tip: All rates are estimates. Final costs may vary based on carrier terms and conditions.")