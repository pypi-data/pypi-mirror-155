import requests
import json

class Apiintercambiador:
    
    global app_url_sandbox
    app_url_sandbox = "https://sandbox.apiplataforma.online"
    # app_url_sandbox = "http://localhost:3000"
    global app_url_pro
    app_url_pro = "https://intercam.apiplataforma.online"

    def __init__(self, token, sandbox):
        self.token = token
        if sandbox:
            self.url = app_url_sandbox
        else:
            self.url = app_url_pro

    def getProperties(self):
        url = self.url + "/api-intercambiador"

        payload={}
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.text
    
    def addProperty(self, listProperties):
        url = self.url + "/properties"

        payload = json.dumps(listProperties)
        headers = {
            'x-access-token': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text

    def updateProperty(self, listProperties):
        url = self.url + "/properties"

        payload = json.dumps(listProperties)
        headers = {
            'x-access-token': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        return response.text

    def deleteProperty(self, listProperties):
        url = self.url + "/properties"

        payload = json.dumps(listProperties)
        headers = {
            'x-access-token': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("DELETE", url, headers=headers, data=payload)

        return response.text


# ai = Apiintercambiador("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0aW1lIjoiTW9uIE1heSAzMCAyMDIyIDE2OjQxOjA1IEdNVCswMjAwIChob3JhIGRlIHZlcmFubyBkZSBFdXJvcGEgY2VudHJhbCkiLCJ1c2VySWQiOiI2Mjk0YmM3ZGU1ODVlODhiODYxNzYzZDAiLCJpYXQiOjE2NTM5MjE2NjV9.pqFNn58pI4dlRQGkSQzqQD6CukiZWiX17KEcbFJV-Ew", True)

#####
#GET all properties
#####

#print(ai.getProperties())

#####
#POST properties
#####

# data = [
#     {
#         "fuente_origen": "1",
#         "agency_id": "123",
#         "propietario": "123",
#         "reference": "11905-OB TEST PYTHONTEST1",
#         "status_id": "1",
#         "status_property_id": "1",
#         "property_type_id": "8",
#         "property_subtype_id": "2",
#         "visibility_type_id": "2",
#         "cadastral_reference": "PYTHONTEST1",
#         "price_rent": 95,
#         "community_costs": "",
#         "ibi_costs": "",
#         "traspass": "",
#         "parking_place_included_in_price": "",
#         "parking_place_price": "",
#         "honorary_shared": "",
#         "honorary_seller": "",
#         "price_changes": []
#     },
#     {
#         "fuente_origen": "1",
#         "agency_id": "123",
#         "propietario": "123",
#         "reference": "11905-OB TEST PUT PYTHONTEST2",
#         "status_id": "1",
#         "status_property_id": "1",
#         "property_type_id": "8",
#         "property_subtype_id": "2",
#         "visibility_type_id": "2",
#         "cadastral_reference": "PYTHONTEST2",
#         "price_rent": 95,
#         "community_costs": "",
#         "ibi_costs": "",
#         "traspass": "",
#         "parking_place_included_in_price": "",
#         "parking_place_price": "",
#         "honorary_shared": "",
#         "honorary_seller": "",
#         "price_changes": []
#     }
# ]
# print(ai.addProperty(data))

#####
#PUT properties
#####

# data = [
#     {
#         "_id": "6299fbf85500288ed8a81cd7",
#         "fuente_origen": "1",
#         "agency_id": "123",
#         "propietario": "123",
#         "reference": "11905-OB TEST PYTHONTEST1 3",
#         "status_id": "1",
#         "status_property_id": "1",
#         "property_type_id": "8",
#         "property_subtype_id": "2",
#         "visibility_type_id": "2",
#         "cadastral_reference": "PYTHONTEST1",
#         "price_rent": 95,
#         "community_costs": "",
#         "ibi_costs": "",
#         "traspass": "",
#         "parking_place_included_in_price": "",
#         "parking_place_price": "",
#         "honorary_shared": "",
#         "honorary_seller": "",
#         "price_changes": []
#     },
#     {
#         "_id": "6299fbf85500288ed8a81cdb",
#         "fuente_origen": "1",
#         "agency_id": "123",
#         "propietario": "123",
#         "reference": "11905-OB TEST PUT PYTHONTEST2 3",
#         "status_id": "1",
#         "status_property_id": "1",
#         "property_type_id": "8",
#         "property_subtype_id": "2",
#         "visibility_type_id": "2",
#         "cadastral_reference": "PYTHONTEST2",
#         "price_rent": 95,
#         "community_costs": "",
#         "ibi_costs": "",
#         "traspass": "",
#         "parking_place_included_in_price": "",
#         "parking_place_price": "",
#         "honorary_shared": "",
#         "honorary_seller": "",
#         "price_changes": []
#     }
# ]
# print(ai.updateProperty(data))

#####
#DELETE properties
#####

# data = ["6299fbf85500288ed8a81cd7","6299fbf85500288ed8a81cdb"]

# print(ai.deleteProperty(data))

