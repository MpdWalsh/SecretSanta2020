#!/usr/bin/env python3

import yaml
import random
import yagmail

with open(r'./config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

sender = config['sender']
participants = config['participants']

pickers = list(participants.keys())
random.shuffle(pickers)

unclaimed_names = pickers.copy()
matches = []



def add_match(picker, drawn):
    match = (picker, drawn)
    matches.append(match)

def random_trade(picker_pair):
    trader_pair = random.choice(matches)
    matches.remove(trader_pair)

    _picker, picked = picker_pair
    trader, trading = trader_pair
    
    add_match(trader, picked)

    return trading



for picker in pickers:
    if len(unclaimed_names) == 1:
        picked = unclaimed_names.pop()

        if picked == picker:
            match = (picker, picked)
            picked = random_trade(match)

    else:
        names = unclaimed_names.copy()
        if picker in names:
            names.remove(picker)

        picked = random.choice(names)
        unclaimed_names.remove(picked)

    add_match(picker, picked)



with yagmail.SMTP(sender) as yag:
    for match in matches:
        santa, giftee = match
        wishlist = participants[giftee]['wishlist']

        email = participants[santa]['email']
        subject = santa + "'s Secret Santa 2020 pick!"
        msg = """
Hello, {0}! Thank you for participating in Secret Santa 2020! :)
This year's event will be held on December 24th. There is a $50 spending limit.

You've drawn {1} as your giftee.
You can find {1}'s wishlist here: {2}

Your giftee may still be adding things to the list. Be sure to reopen the page periodically to remain up to date.
            """.format(santa, giftee, wishlist)

        print("Messaging " + santa)

        #DEBUG STRING
        #print(f"{email}\n{subject}\n{msg}\n===============")

        yag.send(
            to=email,
            subject=subject,
            contents=msg
        )

print("Finished.")
