import streamlit as st
import requests

API_ENDPOINT = "https://api.shipwise.com/api/v1/Rate"
TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50aWQiOiI5MDEzNTQ1IiwiaWF0IjoxNzYxNTk1MzQxLCJpc3MiOiJEZXNrdG9wU2hpcHBlckNsb3VkIiwiYXVkIjoiRFNDQVBJIn0.ZjNPRwA8HNxSWqxx8HMtLX86aLCQiG3Gc9jm0ve0J_zk1H751rDeUn7J2N83_Wur1_pxVTRyHmPw0GQdAPmn1w"

SERVICE_IDS = {
    "DHL Packet International": "D72",
    "DHL Parcel Intl Standard": "D86",
    "USPS First Class Intl": "P60",
    "USPS Priority Mail Intl": "P63",
    "UPS Worldwide Expedited": "U80"
}

st.title("📦 International Quoting Tool")

#ADDRESS
st.header("Destination Address")

to_address1 = st.text_input("Address", "")
to_city = st.text_input("City", "")
to_state = st.text_input("State / Province (ISO Code)", "")
to_postal = st.text_input("Postal Code", "")
to_country = st.text_input("Country Code", "")

#PACKAGES
st.header("Package Details (Same For All Packages)")

package_count = st.number_input("Number of Packages", min_value=1, value=1, step=1)
total_weight = st.number_input(f"Weight In Total", min_value=0.1, value=1.0)
length = st.number_input(f"Length (in)", min_value=0.1)
width = st.number_input(f"Width (in)", min_value=0.1)
height = st.number_input(f"Height (in)", min_value=0.1)


#CUSTOMS
st.header("Customs Information")

customs_value = st.number_input(f"Declared Value (USD)", min_value=0.1, value=10.0)
country_of_mfg = st.text_input(f"Country of Manufacture", "US")

def build_packages():
    package_template = {
        "totalWeight": total_weight,
        "packaging": {
            "length": length,
            "width": width,
            "height": height,
            "weight": 0.1,
            "cost": 1.0
        },
        "customs": {
            "contentsDescription": "Merchandise",
            "originCountry": "US",
            "customsTag": "Merchandise",
            "items": [
                {
                    "sku": "SKU123",
                    "description": "Merchandise",
                    "qty": 1,
                    "value": customs_value,
                    "weight": 0.1,
                    "harmCode": "4901.04",
                    "countryOfMfg": country_of_mfg
                }
            ]
        },
        "items": [
            {
                "marketSku": "SKU-ITEM",
                "marketTitle": "Merchandise",
                "orderedQty": 1,
                "unitPrice": customs_value,
                "weight": total_weight - 0.1, #-----
                "originCountry": "US",
                "harmCode": "4901.04",
                "customsDescription": "Merchandise",
                "customsDeclaredValue": customs_value,
                "length": length,
                "width": width,
                "height": height
            }
        ],
        "value": customs_value
    }
    return [package_template for _ in range(package_count)]


#QUOTES
if st.button("Get Quotes"):

    if not to_address1 or not to_city or not to_postal or not to_country:
        st.error("Please fill in all destination address fields.")
        st.stop()

    st.write("Fetching quotes...")

    packages_data = build_packages()

    headers = {"Authorization": f"Bearer {TOKEN}", "accept": "application/json"}

    #QUOTES RESULTS
    st.header("🚚 Quotes Results")

    for label, rate_id in SERVICE_IDS.items():
        payload = {
            "clientId": 307439,
            "ratingOptionId": rate_id,
            "addressVerification": True,
            "avsType": 0,
            "profileId": 7006216,
            "from": {
                "name": "Test",
                "company": "",
                "address1": "1224 Exposition Way",
                "city": "San Diego",
                "postalCode": "92154",
                "state": "CA",
                "countryCode": "US",
                "countryName": "United States",
                "phone": "5033314000",
                "email": "testEmployee@bigals.com"
            },
            "to": {
                "name": "TEST",
                "company": "QUOTE",
                "address1": to_address1,
                "city": to_city,
                "postalCode": to_postal,
                "state": to_state,
                "countryCode": to_country,
                "phone": " ",
                "email": "testEmployee@bigals.com"
            },
            "packages": packages_data
        }
        
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)

        try:
            data = response.json()
        except:
            continue

        try:
            shipment = data["shipmentItems"][0]
            selected = shipment["selectedRate"]
            price = selected["tertiaryRateType"]["value"]
            business_days = selected["transitTime"]["businessDays"]
            delivery_days = selected["transitTime"]["estimatedDelivery"]

            st.subheader(f" {label} ({rate_id})")
            st.write(f"**Rate:** ${price}")

            if rate_id == "D86":
                st.write("**Europe & Canada:** 4–8 business days")
                st.write("**Rest of World:** 8–14 business days")
            elif rate_id == "D72":
                st.write("**Business Days:** 4–8")
            else:
                st.write(f"**Business Days:** {business_days}")
                st.write(f"**Estimated Delivery:** {delivery_days}")

            st.write("---")

        except:
            continue