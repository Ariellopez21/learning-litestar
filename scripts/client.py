import httpx 

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "ariel1"
PASSWORD = "ariel1"


def main():
    token = get_token()

    with httpx.Client(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {token}"}
        ) as client:
        #delete_item(client, 1013)
        #get_items(client)
        patch_item(
            client=client,
            item_id=1014, 
            title="Item actualizado", 
            #user_id=1, 
            tags=[{"id": 1}, {"id": 2}], 
            done=False
        )
        get_item(client, 1014)

def get_token() -> str:
    with httpx.Client(base_url=BASE_URL) as client:
        r = client.post("/auth/login", data={
            "username": USERNAME,
            "password": PASSWORD
        })
        r_data = r.json()
    return r_data["access_token"] 

def get_items(client: httpx.Client) -> None:
        r = client.get("/items")
        for item in r.json():
            print(f"Item ID: {item['id']},\t Title: {item['title']},\t\t Done: {item['done']}")

def get_item(client: httpx.Client, item_id: int) -> None:
    r = client.get(f"/items/{item_id}")
    print(r.text)

def delete_item(client: httpx.Client, item_id: int) -> None:
    r = client.delete(f"/items/{item_id}")
    print(f"Item with ID {item_id} deleted. Status code: {r.status_code}")

def patch_item(client: httpx.Client, item_id: int, title: str, tags: list[dict], done: bool) -> None:
    r = client.patch(f"/items/{item_id}",
        json={
            "title": title,
            #"user_id": user_id,
            "tags": tags,
            "done": done
        })
    print(f"Item with ID {item_id} updated. Status code: {r.status_code}")

if __name__ == "__main__":
    main()