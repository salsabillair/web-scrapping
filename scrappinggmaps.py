from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import json
import pandas as pd

params = {
    "api_key": "70712791a53194601aadbe233b2291235fb2634497939125ebeaa8c4d78cad22",
    "engine": "google_maps_reviews",
    "hl": "id",
    "data_id": "0x2dd7fb7a12000981:0x29bec54b13972b2"
}

search = GoogleSearch(params)

reviews = []
page_num = 0

while True:
    page_num += 1
    results = search.get_dict()

    # Log respon dari API
    print(f"Respon dari API (Halaman {page_num}):")
    print(json.dumps(results, indent=2, ensure_ascii=False))

    if "error" not in results:
        for result in results.get("reviews", []):
            reviews.append({
                "page": page_num,
                "name": result.get("user").get("name"),
                "link": result.get("user").get("link"),
                "thumbnail": result.get("user").get("thumbnail"),
                "rating": result.get("rating"),
                "date": result.get("date"),
                "snippet": result.get("snippet"),
                "images": result.get("images"),
                "local_guide": result.get("user").get("local_guide"),
            })
    else:
        print("Terjadi kesalahan:", results["error"])
        break

    if results.get("serpapi_pagination") and results["serpapi_pagination"].get("next"):
        search.params_dict.update(dict(parse_qsl(urlsplit(results["serpapi_pagination"]["next"]).query)))
    else:
        break

print(json.dumps(reviews, indent=2, ensure_ascii=False))

# Simpan ke CSV jika ada ulasan
if reviews:
    df = pd.DataFrame(reviews)
    df.to_csv("data.csv", index=False)
    print("Data disimpan ke data.csv")
else:
    print("Tidak ada ulasan untuk disimpan.")
