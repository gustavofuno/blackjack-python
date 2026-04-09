import random

class Card:
    SUITS = (" hearts", " diamonds", " clubs", " spades")
    RANKS = ("2","3","4","5","6","7","8","9","10","J","Q","K","A")
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    @property
    def value(self):
        if self.rank in ("J", "Q", "K"):
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:

    def __init__(self):
        self.cards = [Card(suit,rank) for suit in Card.SUITS for rank in Card.RANKS]
        random.shuffle(self.cards)
    
    def deal(self):
        if not self.cards:
            raise ValueError("the deck is empty")
        return self.cards.pop()
    
class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)

    @property
    def value(self):
        total = sum(c.value for c in self.cards)
        aces = sum(1 for c in self.cards if c.rank == "A")
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total
    
    @property
    def is_bust(self):
        return self.value > 21
    
    @property
    def is_blackjack(self):
        return len(self.cards) == 2 and self.value == 21
    
    @property
    def can_double(self):
        return len(self.cards) == 2 and (self.value == 10 or self.value == 11)

    def __str__(self):
        return '  '.join(str(c) for c in self.cards) + f"  (total: {self.value})"
    
class Player:

    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = Hand()

    def place_bet(self, amount):
        if amount <= 0:
            raise ValueError("the amount needs to be positive")
        if amount > self.chips:
            raise ValueError("bet bigger then money chips")
        else:
            self.chips -= amount
        return amount


def main():
    
    deck = Deck()
    player = Player("gustavo", 200)

    while True:
        if len(deck.cards) < 10:
            deck = Deck()
        
        player.hand = Hand()
        dealer = Hand()

        print("//   BLACKJACK   //")

        bet = int(input(f"You have {player.chips} chips, How much do you want to bet?  "))
        player.place_bet(bet)

        player.hand.add_card(deck.deal())
        dealer.add_card(deck.deal())
        player.hand.add_card(deck.deal())
        dealer.add_card(deck.deal())

        print(player.hand)
        print(str(dealer.cards[0]))
        
        player_bust = False

        if player.hand.is_blackjack:
            print("congrats!! You have a blackjack!")
            player.chips += bet * 2.5

        else:
            while True:
                
                choice = input("Do you want to (1 - stand) or (2 - hit) or (3 - double): ")

                if choice == "1":
                    break
                elif choice == "2":
                    player.hand.add_card(deck.deal())
                    if player.hand.is_bust:
                        print(f"you lost with {player.hand.value}!")
                        player_bust = True
                        break
                    else:
                        print(f"You have {player.hand.value}")
                elif choice == "3":
                    if player.hand.can_double:
                        player.place_bet(bet)
                        player.hand.add_card(deck.deal())
                        print(f"you have {player.hand.value}!")
                        if player.hand.is_bust:
                            print(f"you had {player.hand.value}, you lost!")
                            player_bust = True
                        break  # exits loop whether bust or not
                    else:
                        print("you can't double!")
                        # no break, loops back to question
                elif choice == "stop" or choice == "break":
                    print("Blackjack ended!")
                    return
                else:
                    print("Type 1 or 2")

            if not player_bust:
                while dealer.value < 17:
                    dealer.add_card(deck.deal())
                    
                if dealer.is_bust:
                    print(f"dealer had {dealer.value}, You won!")
                    player.chips += bet * 2
                elif dealer.value > player.hand.value:
                    print(f"you had {player.hand.value} and dealer had {dealer.value}, you lost!")
                elif dealer.value == player.hand.value:
                    print("you draw!")
                    player.chips += bet
                else:
                    player.chips += bet * 2
                    print(f"you had {player.hand.value} and dealer had {dealer.value}, you won!")


if __name__ == "__main__":
    main()