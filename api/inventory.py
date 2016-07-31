from .pokemon import Egg, Pokemon


class Inventory(object):
    def __init__(self, data):
        data = data.get("inventory_delta", {})
        self.last_updated = data.get("new_timestamp_ms", 0)

        items = data.get("inventory_items", [])
        self.items = {}
        self.candy = {}
        self.pokedex_entries = {}

        self.pokemon = []
        self.eggs = []
        for item in items:
            item = item.get("inventory_item_data", {})

            if "candy" in item:
                num_candy = item["candy"].get("candy", 0)
                family_id = item["candy"].get("family_id", 0)
                if num_candy == 0 or family_id == 0:
                    continue
                if family_id not in self.candy:
                    self.candy[family_id] = num_candy
                else:
                    self.candy[family_id] += num_candy

            elif "item" in item:
                num_item = item["item"].get("count", 0)
                item_id = item["item"].get("item_id", 0)
                # unseen = item["item"].get("unseen", False)
                if num_item == 0 or item_id == 0:
                    continue

                if item_id not in self.items:
                    self.items[item_id] = num_item
                else:
                    self.items[item_id] += num_item

            elif "pokemon_data" in item:
                current_data = item["pokemon_data"]
                if current_data.get("is_egg", False):
                    self.eggs.append(Egg(current_data))
                else:
                    self.pokemon.append(Pokemon(current_data))

            elif "egg_incubators" in item:
                # currently unimplemented
                pass
