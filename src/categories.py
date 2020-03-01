top_dict = ["camiseta", "t-shirt"]
trouser_dict = ["trouser", "pantalón", "pantalon", "vaquero", "shorts", "jeans"]
pullover_dict = ["pullover", "sudadera", "jersey", "cazadora", "blazer", "blazers"]
dress_dict = ["dress", "vestido", "falda"]
coat_dict = ["coat", "abrigo", "plumifero", "plumífero"]
sandal_dict = ["sandalia","tacones"]
shirt_dict = ["shirt", "camisa"]
sneaker_dict = ["sneaker", "tenis", "playeros", "playeras"]
bag_dict = ["bag", "mochila", "bolso", "bolsa", "bolsos"]
ancle_bot_dict = ["ancle boot", "zapato", "zapatos"]

def find_category(description):
    if not description:
        return None
    if any(word in description.lower() for word in top_dict):
        return "t-shirt"
    if any(word in description.lower() for word in trouser_dict):
        return "trouser"
    if any(word in description.lower() for word in pullover_dict):
        return "pullover"
    if any(word in description.lower() for word in dress_dict):
        return "dress"
    if any(word in description.lower() for word in coat_dict):
        return "coat"
    if any(word in description.lower() for word in sandal_dict):
        return "sandal"
    if any(word in description.lower() for word in shirt_dict):
        return "shirt"
    if any(word in description.lower() for word in sneaker_dict):
        return "sneaker"
    if any(word in description.lower() for word in bag_dict):
        return "bag"
    if any(word in description.lower() for word in ancle_bot_dict):
        return "ancle_bot"
    return None