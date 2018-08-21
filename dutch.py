import os
import sys
import json
import random


class Card:
    def __init__(self, dutch, english):
        self.entry = {"dutch": dutch, "english": english}


class Dictionary:

    @classmethod
    def set_file_path(cls):
        directory = os.path.dirname(__file__)
        file_path = os.path.join(directory, "dictionary.json")
        return file_path

    @classmethod
    def load_dictionary(cls):
        file_path = cls.set_file_path()
        with open(file_path, mode="r") as file:
            dictionary = json.load(file)
        return dictionary

    @classmethod
    def save_dictionary(cls, dictionary):
        file_path = cls.set_file_path()
        with open(file_path, "w") as file:
            file.write(json.dumps(dictionary, indent=4))

    @classmethod
    def edit_card(cls, card):
        print("\nedit card: \ndutch: {}\nenglish: {}".format(
            card["dutch"], card["english"]))
        new_dutch = input("\nnew dutch: ")
        if new_dutch == "delete()":
            return "delete()"
        elif new_dutch != "":
            card["dutch"] = new_dutch
        new_english = input("new english: ")
        if new_english == "delete()":
            return "delete()"
        elif new_english != "":
            card["english"] = new_english
        return card

    @classmethod
    def search_card(cls):
        dictionary = cls.load_dictionary()
        console_input = input("\nplease enter what you are looking for: ")
        found_cards = [
            card for card in dictionary if card["dutch"] == console_input
            or card["english"] == console_input]
        if len(found_cards) > 0:
            print("these have been found:")
            for card in found_cards:
                print("dutch: {}\nenglish: {}\n".format(
                    card["dutch"], card["english"]))
                confirmation = input("do you want to edit it? (y/n) ")
                if confirmation == "y":
                    new_card = cls.edit_card(card)
                    dictionary.remove(card)
                    if new_card != "delete()":
                        dictionary.append(new_card)
                    cls.save_dictionary(dictionary)
        else:
            print("nothing has been found")

    @classmethod
    def run_input(cls):
        dictionary = cls.load_dictionary()
        while True:
            dutch = input("\ndutch: ")
            if dutch == "quit()":
                break
            elif dutch == "edit()":
                dictionary[-1] = cls.edit_card(dictionary[-1])
                if dictionary[-1] == "delete()":
                    dictionary.pop(-1)
                cls.save_dictionary(dictionary)
                continue
            elif dutch == "search()":
                cls.search_card()
                continue
            english = input("english: ")
            if english == "quit()":
                break
            elif english == "edit()":
                continue
            elif english == "search()":
                cls.search_card()
                continue
            new_card = Card(dutch, english)
            if new_card.entry not in dictionary:
                dictionary.append(new_card.entry)
                cls.save_dictionary(dictionary)

    @classmethod
    def run_test(cls):
        dictionary = cls.load_dictionary()
        completed_cards = []
        while True:
            pool_cards = [
                card for card in dictionary if
                card not in completed_cards]
            card = random.sample(pool_cards, 1)[0]
            coin = random.randint(0, 1)
            if coin == 0:
                input_language = "dutch"
                output_language = "english"
            else:
                input_language = "english"
                output_language = "dutch"
            answer = input("\n%s = " % card[input_language])
            if answer == "quit()":
                break
            elif answer == "edit()":
                new_card = cls.edit_card(card)
                dictionary.remove(card)
                if new_card != "delete()":
                    dictionary.append(new_card)
                cls.save_dictionary(dictionary)
                continue
            elif answer == "search()":
                cls.search_card()
            elif answer == card[output_language]:
                print("precies!")
            else:
                print(card[output_language])
            completed_cards.append(card)
            if len(completed_cards) == len(dictionary):
                break

    @classmethod
    def run_script(cls):
        try:
            script_type = sys.argv[1]
            print(
                "possible commands: \"quit()\", \"search()\", \"edit()\", "
                "\"delete()\"")
            if script_type == "input":
                cls.run_input()
            elif script_type == "test":
                cls.run_test()
        except IndexError:
            print("no argument provided, please enter \"input\" or \"test\"")


Dictionary.run_script()
