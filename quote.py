import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

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

st.header("Destination Address")

to_address1 = st.text_input("Address", "")
to_city = st.text_input("City", "")
to_state = st.text_input("State / Province (ISO Code)", "")
to_postal = st.text_input("Postal Code", "")
to_country = st.text_input("Country Code", "")

st.header("Package Details")

total_weight = st.number_input("Total Weight (lbs)", min_value=0.1, value=1.0)
length = st.number_input("Length (inches)", min_value=0.1, value=4.0)
width = st.number_input("Width (inches)", min_value=0.1, value=4.0)
height = st.number_input("Height (inches)", min_value=0.1, value=6.0)

st.header("Customs Information")

harm_code = st.text_input("HS Code", "4901.04")
customs_value = st.number_input("Declared Value", min_value=0.1, value=10.0)
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
                #"countryName": "Canada",
                "phone": " ",
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
                            "length": length,
                            "width": width,
                            "height": height
                        }
                    ],
                    "value": customs_value
                }
            ]
        }

    headers = {"Authorization": f"Bearer {TOKEN}", "accept": "application/json"}

    st.header("🚚 Quotes Results")

    results = {}

    for label, rate_id in SERVICE_IDS.items():
        payload = make_payload(rate_id)
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)

        try:
            data = response.json()
        except:
            #results[label] = "❌ Invalid JSON response"
            continue

        try:
            shipment = data["shipmentItems"][0]
            selected = shipment["selectedRate"]
            price = selected["tertiaryRateType"]["value"]
            business_days = selected["transitTime"]["businessDays"]
            delivery_days = selected["transitTime"]["estimatedDelivery"]

            if rate_id == "D86": #DHL Parcel Intl Standard
                canada_business_days = "4-8 business days"
                world_business_days = "8-14 business days"
                st.subheader(f" {label} ({rate_id})")
                st.write(f"**Rate:** ${price}")
                st.write(f"**Delivering to Europe & Canada:** {canada_business_days}")
                st.write(f"**Delivering to rest of World:** {world_business_days}")
                st.write("---")
                

            elif rate_id == "D72": #DHL Packet International
                business_days = "4-8 business days"
                st.subheader(f" {label} ({rate_id})")
                st.write(f"**Rate:** ${price}")
                st.write(f"**Business Days:** {business_days}")
                st.write("---")

            else:
                st.subheader(f" {label} ({rate_id})")
                st.write(f"**Rate:** ${price}")
                st.write(f"**Business Days:** {business_days}")
                st.write(f"**Estimated Delivery:** {delivery_days}")
                st.write("---")

            #results[label] = price

        except Exception as e:
            results[label] = f"Carrier Not Applicable"
            #results[label] = f"❌ Could not extract rate: {e}"

    #st.header("📊 Shipping Quotes")

    #for carrier, quote in results.items():
    #    st.write(f"**{carrier}:** {quote}")



