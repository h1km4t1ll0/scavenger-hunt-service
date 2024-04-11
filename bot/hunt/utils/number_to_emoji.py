emojis = {
    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
}
minus = "➖"

def number_to_emoji(number: int):
    neg = number < 0
    num = str(abs(number))
    for i in range(10):
        num = num.replace(str(i), emojis[str(i)])
    num = emojis["0"] * (3 - len(str(number))) + num
    if neg:
        num = minus + num
    else:
        num = emojis['0'] + num
    return num
