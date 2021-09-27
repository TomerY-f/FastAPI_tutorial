import json


def json_editor():
    books = {"More books": {"book_1": "Two_Bears", "book_2": "Back_to_Mahatama"}}

    with open("package.json", 'r+') as json_file:
        loaded_json = json.load(json_file)
        loaded_json.update(books)
        json_file.seek(0)
        json.dump(loaded_json, json_file)

        print(type(loaded_json))
        print(loaded_json)