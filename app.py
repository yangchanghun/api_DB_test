import requests
import time
session = requests.Session()
access_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
access_headers = {"content-Type": "application/x-www-form-urlencoded"}
access_data = {
                'grant_type': 'client_credentials',
                'client_id': 'amandues client id',
                'client_secret': 'amandues secret id'
            }
access_response = session.post(url = access_url,data = access_data,headers = access_headers)
print(access_response)
print(access_response.json()["access_token"])
access_token = access_response.json()["access_token"]

A = time.time()


search_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
originLocationCode = 'GMP'
destinationLocationCode = 'CJU'
date = "2025-02-20"


data = {
      "currencyCode": "USD",
  "originDestinations": [
    {
      "id": "1",
      "originLocationCode": originLocationCode,
      "destinationLocationCode": destinationLocationCode,
      "departureDateTimeRange": {
        "date": date
      }
    }
  ],
  "travelers": [
    {
      "id": "1",
      "travelerType": "ADULT"
    }
  ],
  "sources": [
    "GDS"
  ],
  "searchCriteria": {
    "maxFlightOffers": 50,
    "flightFilters": {
      "cabinRestrictions": [
        {
          "cabin": "ECONOMY",
          "coverage": "MOST_SEGMENTS",
          "originDestinationIds": [
            "1"
          ]
        }
      ]
    }
  },
}


headers = {
    'Authorization':'Bearer ' + access_token,
    "content-Type": "application/json"
}

start_time = time.time()
response = session.post(search_url,json=data,headers=headers)
end_time = time.time()
print(response.json())
print("소요시간:",end_time - start_time)
print(response.json())

# JSON 데이터에서 항공편 정보 추출
flight_data = response.json()["data"]

# 데이터 저장을 위한 리스트 초기화
price = []
seats_available = []
airline_codes = []
departure_time = []
arrival_time = []
departure_airport = []
arrival_airport = []

# 데이터 파싱
for i in range(len(flight_data)):
    flight = flight_data[i]

    # 가격 정보
    price.append(flight["price"]["base"])

    # 예약 가능 좌석 수
    seats_available.append(flight["numberOfBookableSeats"])

    # 항공사 코드
    airline_codes.append(flight["validatingAirlineCodes"][0])  # 리스트이므로 첫 번째 값 사용

    # 경로 정보 (itineraries > segments)
    segment = flight["itineraries"][0]["segments"][0]  # 첫 번째 여정 & 첫 번째 구간

    departure_time.append(segment["departure"]["at"])
    arrival_time.append(segment["arrival"]["at"])
    departure_airport.append(segment["departure"]["iataCode"])
    arrival_airport.append(segment["arrival"]["iataCode"])
B = time.time()
print(B-A)

# 결과 출력
# print("가격:", price)
# print("예약 가능 좌석:", seats_available)
# print("항공사 코드:", airline_codes)
# print("출발 시간:", departure_time)
# print("도착 시간:", arrival_time)
# print("출발 공항:", departure_airport)
# print("도착 공항:", arrival_airport)

