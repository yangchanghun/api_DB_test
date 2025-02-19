import psycopg2

import requests
import time
from multiprocessing.dummy import Pool as ThreadPool

session = requests.Session()
access_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
access_headers = {"content-Type": "application/x-www-form-urlencoded"}
access_data = {
                'grant_type': 'amandues client id',
                'client_id': 'amandues client id',
                'client_secret': 'hiIgDXRmkdSQyQfs'
            }
access_response = session.post(url = access_url,data = access_data,headers = access_headers)
print(access_response)
print(access_response.json()["access_token"])
access_token = access_response.json()["access_token"]

search_url = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
originLocationCode = 'GMP'
destinationLocationCode = 'KWJ'
# date = "2025-02-07"함
date= []
for i in range(1, 29):
    date.append(f"2025-03-{i:02d}")  # ✅ 두 자리 숫자로 포맷팅


A = time.time()

for i in date:
  data = {
        "currencyCode": "USD",
    "originDestinations": [
      {
        "id": "1",
        "originLocationCode": originLocationCode,
        "destinationLocationCode": destinationLocationCode,
        "departureDateTimeRange": {
          "date": i
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
        ],
        "connectionRestriction":{
          "maxNumberOfConnections":0
        }
      }
    },
  }


  headers = {
      'Authorization':'Bearer ' + access_token,
      "content-Type": "application/json"
  }

  start_time = time.time()

  try:
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
  except KeyError:
    pass


  try:
    conn = psycopg2.connect(host='localhost', dbname='flights', user='postgres', password='password', port=5432)
    cursor = conn.cursor()
    try:
      for i in range(len(flight_data)):
          sql = """
          INSERT INTO kimpo_jeju (departure_time, arrival_time, price, seats_available, departure_airport, arrival_airport, airline_codes)
          VALUES (%s, %s, %s, %s, %s, %s, %s)
          """
          cursor.execute(sql, (
              departure_time[i], 
              arrival_time[i], 
              float(price[i]),   # 가격이 실수형일 가능성 있음
              int(seats_available[i]),  # 좌석 수는 정수형
              departure_airport[i], 
              arrival_airport[i], 
              airline_codes[i]
          ))
      conn.commit()  # ✅ 모든 데이터가 성공적으로 삽입되면 커밋
    except:
          conn.rollback()  # ❌ 오류 발생 시 롤백
  finally:
    conn.close()

B = time.time()
print(B-A)