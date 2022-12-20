import re

class KeepAwayGame:
    
    def __init__(self) -> None:
        self.players = []
        
    def add_player(self, player):
        self.players.append(player)
        
    def play_round(self):
        for player in self.players:
            player.take_turn()
            
    def count_monkey_business(self) -> int:
        activity = {i: p.inspected_items for i, p in enumerate(self.players)}
        sorted_activity = {k: v for k, v in sorted(activity.items(), key=lambda item: item[1], reverse=True)}
        monkey_business = 1
        i = 0
        for k in sorted_activity:
            if i > 1:
                break
            monkey_business *= sorted_activity[k]
            i += 1
            
        return monkey_business

class Monkey:
    operation_pattern = re.compile(r'^new = old (?P<operator>\*|\+) (?P<factor>\d+|old)$')
    
    def play(self, game: KeepAwayGame, starting_items: list, operation: str, test: tuple) -> None:
        self.game = game
        self.items = starting_items
        self.resolve_operation(operation)
        self.resolve_test(test)
        self.inspected_items = 0
        self.game.add_player(self)
        
    def resolve_operation(self, operation: str):
        '''Input format: new = old * 19'''
        m = re.match(self.operation_pattern, operation)
        [self.operator, self.factor] = m.group('operator', 'factor')
    
    def resolve_test(self, test: tuple):
        '''
        Input format:
        (divisor, monkey_if_divisible, monkey_if_not_divisible)
        Example: (23, 2, 3)        
        '''
        self.divisor = test[0]
        self.recipients = test[1:]
        
    def inspect_current_item(self):
        item = self.items[0]
        second = item if self.factor == 'old' else int(self.factor)
        
        '''Worry level increases during inspection'''
        item = item + second if self.operator == '+' else item * second
            
        '''Worry level decreases after inspection'''
        item //= 3
        
        self.items[0] = item
        self.inspected_items += 1
        
    def test_current_item(self) -> int:
        divisible = self.items[0] % self.divisor == 0
        i = 0 if divisible else 1
        return self.recipients[i]
        
    def throw_current_item(self, recipient: int):
        item = self.items.pop(0)
        self.game.players[recipient].receive_item(item)
    
    def take_turn(self):
        while self.items:
            self.inspect_current_item()
            self.throw_current_item(self.test_current_item())
    
    def receive_item(self, item):
        self.items.append(item)
      
game = KeepAwayGame()
items_pattern = re.compile(r'^Starting items: (.*)$')
operation_pattern = re.compile(r'new = old (\*|\+) (\d+|old)$')
divisor_pattern = re.compile(r'^Test: divisible by (\d+)$')
decision_pattern = re.compile(r'^If (true|false): throw to monkey (\d+)$')

# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

with open('input11.txt') as f:
    lines = [line.strip() for line in f.readlines()]
    chunks = list(divide_chunks(lines, 7))
    for chunk in chunks:
        starting_items = re.match(items_pattern, chunk[1]).group(1).split(', ')
        starting_items = [int(x) for x in starting_items]
        operation = re.search(operation_pattern, chunk[2]).group(0)
        divisor = int(re.match(divisor_pattern, chunk[3]).group(1))
        first_recipient = int(re.match(decision_pattern, chunk[4]).group(2))
        second_recipient = int(re.match(decision_pattern, chunk[5]).group(2))
        test = (divisor, first_recipient, second_recipient)
        m = Monkey()
        m.play(game, starting_items, operation, test)
    
for i in range(20):
    game.play_round()
    
business = game.count_monkey_business()
print(business)
        
        