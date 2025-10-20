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

# Fixed origin address
ORIGIN_NAME = "3PLWinner"
ORIGIN_ADDRESS = "1224 Exposition Way"
ORIGIN_CITY = "San Diego"
ORIGIN_STATE = "CA"
ORIGIN_POSTAL = "92154"
ORIGIN_COUNTRY = "US"

# Page config
st.set_page_config(page_title="ShipWise Rate Quote", page_icon="📦", layout="wide")

# Title
st.title("📦 International Shipping Rate Quote")
st.write("Get instant quotes for international shipments from San Diego")

# Show origin address
with st.expander("📤 Shipping From (Origin)", expanded=False):
    st.info(f"""
    **{ORIGIN_NAME}**  
    {ORIGIN_ADDRESS}  
    {ORIGIN_CITY}, {ORIGIN_STATE} {ORIGIN_POSTAL}  
    {ORIGIN_COUNTRY}
    """)

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
st.header("📍 Destination Address")
col1, col2 = st.columns(2)
with col1:
    to_name = st.text_input("Recipient Name*", key="to_name")
    to_address1 = st.text_input("Street Address*", key="to_address1")
    to_address2 = st.text_input("Apt/Suite/Floor (optional)", key="to_address2")
    to_city = st.text_input("City*", key="to_city")
with col2:
    to_company = st.text_input("Company (optional)", key="to_company")
    to_country = st.text_input("Country Code* (e.g., GB, DE, AU, JP)", key="to_country", 
                               help="2-letter ISO country code")
    to_state = st.text_input("State/Province (if applicable)", key="to_state",
                            help="Leave blank if country doesn't use states/provinces")
    to_postal = st.text_input("Postal/Zip Code*", key="to_postal")

# Phone (optional but recommended)
to_phone = st.text_input("Phone Number (recommended)", key="to_phone", 
                        help="Helps carriers contact recipient if needed")

# Check if international (always true since origin is US)
is_international = to_country.upper() != ORIGIN_COUNTRY

# Customs Information
st.header("🌍 Customs Information")
col1, col2 = st.columns(2)
with col1:
    customs_description = st.text_input("Contents Description*", 
                                       placeholder="e.g., Electronics, Clothing, Books",
                                       help="Brief description of what's being shipped")
    customs_tag = st.selectbox("Shipment Type*", 
        ["Merchandise", "Gift", "Sample", "Documents", "Return Goods", "Other"])
with col2:
    customs_signer = st.text_input("Customs Signer Name*", 
                                   placeholder="Your name or authorized person",
                                   help="Person responsible for customs declaration")

# Packages Section
st.header("📦 Package Details")

for pkg_idx, package in enumerate(st.session_state.packages):
    with st.expander(f"Package {pkg_idx + 1}", expanded=True):
        col1, col2 = st.columns([6, 1])
        with col2:
            if len(st.session_state.packages) > 1:
                if st.button("🗑️ Remove", key=f"remove_pkg_{pkg_idx}"):
                    remove_package(pkg_idx)
                    st.rerun()
        
        st.subheader("📏 Dimensions & Weight")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            package['length'] = st.number_input("Length (in)*", min_value=0.0, step=0.1, key=f"length_{pkg_idx}")
        with col2:
            package['width'] = st.number_input("Width (in)*", min_value=0.0, step=0.1, key=f"width_{pkg_idx}")
        with col3:
            package['height'] = st.number_input("Height (in)*", min_value=0.0, step=0.1, key=f"height_{pkg_idx}")
        with col4:
            package['total_weight'] = st.number_input("Weight (lbs)*", min_value=0.0, step=0.1, key=f"total_weight_{pkg_idx}")
        
        package['value'] = st.number_input("Total Package Value ($)*", min_value=0.0, step=0.01, key=f"value_{pkg_idx}", 
                                          help="Total declared value for insurance and customs")
        
        # Items in package
        st.subheader("📋 Items in This Package")
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
                                                       placeholder="e.g., Cotton T-Shirt, size M")
                    item['harmonized_code'] = st.text_input("HS Code*", key=f"hs_{pkg_idx}_{item_idx}",
                                                            placeholder="e.g., 6109.10.00",
                                                            help="Required for customs clearance")
                with col2:
                    item['quantity'] = st.number_input("Quantity*", min_value=1, step=1, key=f"qty_{pkg_idx}_{item_idx}")
                    item['country_origin'] = st.text_input("Country of Origin*", value="US", 
                                                          key=f"origin_{pkg_idx}_{item_idx}",
                                                          help="Where the product was manufactured")
                with col3:
                    item['unit_price'] = st.number_input("Unit Price ($)*", min_value=0.0, step=0.01, key=f"price_{pkg_idx}_{item_idx}",
                                                         help="Price per single item")
                    item['weight'] = st.number_input("Weight per Item (lbs)*", min_value=0.0, step=0.01, key=f"weight_{pkg_idx}_{item_idx}")
                
                st.divider()
        
        if st.button(f"➕ Add Item to Package {pkg_idx + 1}", key=f"add_item_{pkg_idx}"):
            add_item(pkg_idx)
            st.rerun()

if st.button("➕ Add Another Package", key="add_package"):
    add_package()
    st.rerun()

st.divider()

# Generate payload and get rates
if st.button("🚀 Get Shipping Rates", type="primary", use_container_width=True):
    # Validation
    if not all([to_name, to_address1, to_city, to_postal, to_country]):
        st.error("❌ Please fill in all required destination address fields (Name, Address, City, Postal Code, Country)")
    elif not all([customs_description, customs_signer]):
        st.error("❌ Please fill in all required customs information")
    elif not SHIPWISE_API_ENDPOINT or not SHIPWISE_API_TOKEN or not SHIPWISE_CLIENT_ID or not SHIPWISE_PROFILE_ID:
        st.error("❌ API credentials not configured. Please check your .env file.")
    else:
        # Validate package items
        valid = True
        for pkg_idx, package in enumerate(st.session_state.packages):
            if not package.get('length') or not package.get('width') or not package.get('height') or not package.get('total_weight'):
                st.error(f"❌ Package {pkg_idx + 1}: Please fill in all dimensions and weight")
                valid = False
                break
            for item_idx, item in enumerate(package['items']):
                if not item.get('description') or not item.get('harmonized_code') or not item.get('quantity') or not item.get('unit_price'):
                    st.error(f"❌ Package {pkg_idx + 1}, Item {item_idx + 1}: Please fill in all required item fields")
                    valid = False
                    break
        
        if valid:
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
                    "state": to_state if to_state else "",
                    "countryCode": to_country.upper(),
                    "phone": to_phone
                },
                "from": {
                    "name": ORIGIN_NAME,
                    "company": ORIGIN_NAME,
                    "address1": ORIGIN_ADDRESS,
                    "city": ORIGIN_CITY,
                    "postalCode": ORIGIN_POSTAL,
                    "state": ORIGIN_STATE,
                    "countryCode": ORIGIN_COUNTRY
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
                    "items": [],
                    "customs": {
                        "contentsDescription": customs_description,
                        "originCountry": ORIGIN_COUNTRY,
                        "signer": customs_signer,
                        "customsTag": customs_tag,
                        "items": []
                    }
                }
                
                # Add items
                for item in package['items']:
                    item_data = {
                        "sku": f"ITEM-{item.get('id', '')}",
                        "quantityToShip": item.get('quantity', 0),
                        "unitPrice": item.get('unit_price', 0),
                        "harmonizedCode": item.get('harmonized_code', ''),
                        "countryOfOrigin": item.get('country_origin', ORIGIN_COUNTRY).upper(),
                        "customsDescription": item.get('description', ''),
                        "customsDeclaredValue": item.get('unit_price', 0),
                        "weight": item.get('weight', 0)
                    }
                    pkg_data["items"].append(item_data)
                    
                    # Add to customs items
                    customs_item = {
                        "sku": f"ITEM-{item.get('id', '')}",
                        "description": item.get('description', ''),
                        "qty": item.get('quantity', 0),
                        "value": item.get('unit_price', 0),
                        "weight": item.get('weight', 0),
                        "countryOfMfg": item.get('country_origin', ORIGIN_COUNTRY).upper(),
                        "harmCode": item.get('harmonized_code', '')
                    }
                    pkg_data["customs"]["items"].append(customs_item)
                
                payload["packages"].append(pkg_data)
            
            # Display payload in debug mode
            with st.expander("🔍 Debug: View Request Payload"):
                st.json(payload)
            
            # Make API call
            with st.spinner("🔄 Fetching rates from international carriers..."):
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
                    st.success("✅ Rates retrieved successfully!")
                    
                    # Calculate total weight and value
                    total_weight = sum([pkg.get('total_weight', 0) for pkg in st.session_state.packages])
                    total_value = sum([pkg.get('value', 0) for pkg in st.session_state.packages])
                    
                    # Show shipment summary
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Packages", len(st.session_state.packages))
                    with col2:
                        st.metric("Total Weight", f"{total_weight} lbs")
                    with col3:
                        st.metric("Total Value", f"${total_value:.2f}")
                    
                    st.header("💰 Available Shipping Options")
                    st.write(f"Shipping from **{ORIGIN_CITY}, {ORIGIN_STATE}** to **{to_city}, {to_country.upper()}**")
                    
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
                                        st.write(f"⏱️ **{delivery_days}** business days")
                                    elif delivery_date:
                                        st.write(f"📅 By **{delivery_date}**")
                                    else:
                                        st.write("📦 Delivery time varies")
                                
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
                        st.info(f"📊 Found **{len(rates)}** shipping options")
                        
                    else:
                        st.warning("⚠️ No rates found. Response format:")
                        st.json(rate_data)
                    
                    # Full response in expandable section
                    with st.expander("🔍 View Full API Response"):
                        st.json(rate_data)
                    
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ API Error: {str(e)}")
                    if hasattr(e, 'response') and hasattr(e.response, 'text'):
                        with st.expander("View Error Details"):
                            st.code(e.response.text)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.caption("💡 Tip: HS codes are required for customs clearance. Make sure they're accurate!")
st.caption("📞 Questions? Contact 3PLWinner for assistance with your international shipments.")