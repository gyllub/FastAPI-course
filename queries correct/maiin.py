
# from fastapi.openapi.docs import get_swagger_ui_html
# import uvicorn

from fastapi import FastAPI, Query, Body
from starlette.authentication import requires

app = FastAPI()

our_hotels = [
    {"id":1, "name":"Dubai", "location":"UAE"},
    {"id":2, "name":"Sochi", "location":"RF"},
    {"id":4, "name":"Sochi", "location":"RF"},
    {"id":3, "name":"Milan", "location":"Spain"}
]

@app.get("/")
def get_hotels(
        hotel_name: str | None =Query (default=None, description="Hotels town"),
        hotel_id: int | None = Query(default=None, description="ID")
    ):
    hotels_ = []
    r_id = []
    for i in our_hotels:
        if hotel_id and i["id"] != hotel_id:
            r_id.append(i["id"])
            continue
        if hotel_name and i["name"] != hotel_name:
            continue
        hotels_.append(i)
    return hotels_


@app.delete("/{hotel_id}")
def hotel_delete(hotel_id: int):
    global our_hotels
    our_hotels = [i for i in our_hotels if i["id"] != hotel_id]
    return our_hotels


#body
@app.post("/hotels")
def hotel_create(        title: str = Body(embed=True)    ):
    global  our_hotels
    our_hotels.append(
        {"id": our_hotels[-1]["id"] + 4,
        "title": title
         }

    )
    return our_hotels



@app.put("/hotels/{hotel_id}",
         summary="Это метод PUT",
         description="Надо забивать все необходимые данные")
def hotel_put(hotel_id: int,
              hotel_name: str = Body(embed=True),
              hotel_location: str = Body(embed=True)
              ):
    global our_hotels
    for i in our_hotels:
        if hotel_id == i["id"] and hotel_name and hotel_location:
            i["name"] = hotel_name
            i["location"] = hotel_location

    # Здесь ретерном тащим список отелей, чтобы в гет не лазить лишний раз (лень)
    return our_hotels

@app.patch("/hotels/{hotel_id}",
           summary="Это метод PATCH",
           description="Можно забивать не все данные")
def hotel_patch(hotel_id: int,
              hotel_name: str | None = Body(None),
              hotel_location: str | None = Body(None)
              ):
    global our_hotels
    for i in our_hotels:
        if hotel_id == i["id"]:
            if hotel_name:
                i["name"] = hotel_name
            if hotel_location:
                i["location"] = hotel_location

    # Здесь ретерном тащим список отелей, чтобы в гет не лазить лишний раз (лень)
    return our_hotels

# uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
