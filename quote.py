import streamlit as st
import requests
import json

API_ENDPOINT = "https://api.shipwise.com/api/v1/Rate"
TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50aWQiOiI5MDEzNTQ1IiwiaWF0IjoxNzYxNTk1MzQxLCJpc3MiOiJEZXNrdG9wU2hpcHBlckNsb3VkIiwiYXVkIjoiRFNDQVBJIn0.ZjNPRwA8HNxSWqxx8HMtLX86aLCQiG3Gc9jm0ve0J_zk1H751rDeUn7J2N83_Wur1_pxVTRyHmPw0GQdAPmn1w"

SERVICE_IDS = {
    "USPS First Class Intl (P60)": "P60",
    "USPS Priority Mail Intl (P63)": "P63",
    "UPS Worldwide Expedited (U80)": "U80",
    "DHL Packet International (D72)": "D72",
    "DHL Parcel Intl Standard (D86)": "D86",
}

st.title("📦 International Quoting Tool")

st.header("Destination Address")

to_address1 = st.text_input("Address", "845 Sherbrooke Street West")
to_city = st.text_input("City", "Montreal")
to_state = st.text_input("State / Province (ISO Code)", "QC")
to_postal = st.text_input("Postal Code", "H3A 0G4")
to_country = st.text_input("Country Code", "CA")

st.header("Package Details")

total_weight = st.number_input("Total Weight (lbs)", value=1.0)
length = st.number_input("Length (inches)", value=4.0)
width = st.number_input("Width (inches)", value=4.0)
height = st.number_input("Height (inches)", value=6.0)

st.header("Customs Information")

harm_code = st.text_input("HS Code", "4901.04")
customs_value = st.number_input("Declared Value", value=10.0)
country_of_mfg = st.text_input("Country of Manufacture", "US")

if st.button("Get Quotes"):

    if not to_address1 or not to_city or not to_postal or not to_country:
        st.error("Please fill in all destination address fields.")
        st.stop()
    
    st.write("Fetching quotes...")

    def make_payload(rating_id):
        return {
            "clientId": 307439,
            "ratingOptionId": rating_id,
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
                "countryName": "Canada",
                "phone": "5033314000",
                "email": "testEmployee@bigals.com"
            },
            "packages": [
                {
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
                                "harmCode": harm_code,
                                "countryOfMfg": country_of_mfg
                            }
                        ]
                    },
                    "items": [
                        {
                            "marketSku": "SKU-TEST",
                            "marketTitle": "Merchandise",
                            "orderedQty": 1,
                            "unitPrice": customs_value,
                            "weight": total_weight - 0.1,
                            "originCountry": "US",
                            "harmCode": harm_code,
                            "customsDescription": "Merchandise",
                            "customsDeclaredValue": customs_value,
                            "length": 2,
                            "width": 2,
                            "height": 3
                        }
                    ],
                    "value": customs_value
                }
            ]
        }

    headers = {"Authorization": f"Bearer {TOKEN}", "accept": "application/json"}

    results = {}

    for label, rate_id in SERVICE_IDS.items():
        payload = make_payload(rate_id)
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)

        try:
            data = response.json()
        except:
            results[label] = "❌ Invalid JSON response"
            continue

        try:
            shipment = data["shipmentItems"][0]
            selected = shipment["selectedRate"]
            tertiary = selected["tertiaryRateType"]["value"]

            results[label] = tertiary

        except Exception as e:
            results[label] = f"❌ Could not extract rate: {e}"

    st.header("📊 Shipping Quotes")

    for carrier, quote in results.items():
        st.write(f"**{carrier}:** {quote}")



