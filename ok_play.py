# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:03:41 2020

@author: Chris
"""
NUM_TILES = 10

class Board:
    def __init__(self):
        self.squares_taken = {}
        
    def check_pos_taken(self, pos):
        print('Checking_pos_taken:', pos)
        return (pos in self.squares_taken.keys())
    
    def add_to_line(self, tile, new_pos):
        if self.check_pos_taken(new_pos):
                tile_there = self.squares_taken[new_pos]
                if tile_there.player == tile.player:
                    return 1
        return 0
    
    def check_vertical(self, tile):
        line = 1
        for up in range(1, 5):
            if self.add_to_line(tile.x, tile.y + up):
                line += 1
            else:   
                break
        for down in range(1, 5):
            if self.add_to_line(tile.x, tile.y - down):
                line += 1
            else:
                break
        return line >= 4
    
    
    def check_pos_allowed(self, pos):
        print(f'checking {pos} allowed')
        if self.check_pos_taken(pos):
            print('No deal - square already taken')
            return False
        for x, y in [(-1,0), (1,0), (0,-1), (0,1)]:
            if self.check_pos_taken(((pos[0] + x), (pos[1] + y))):
                print(f'legit move as tile at {[(pos[0] + x), (pos[1] + y)]}')
                return True
        print('Not connected to any existing tiles - try again')
        return False
            
    def place_tile(self, tile, pos):
        self.squares_taken[pos] = tile
        tile.pos = pos
        tile.x, tile.y = pos
        print('tile placed at', pos)
    
    def check_winning_move(self, tile):
        print('checking winning move')
        if tile.pos == 'rack':
            return False
        for right, up, left, down in [(1, 0, -1, 0),
                                      (0, 1, 0, -1),
                                      (1, 1, -1, -1),
                                      (1, -1, -1, 1)]:
            line = 1
            stopped1, stopped2 = False, False
            for i in range(1, 5):
                if self.add_to_line(tile, (tile.x + right * i, tile.y + up * i)) and not stopped1:
                    line += 1
                else:   
                    stopped1 = True
                if self.add_to_line(tile, (tile.x + left * i, tile.y + down * i)) and not stopped2:
                    line += 1
                else:
                    stopped2 = True
            if line >= 4:
                print(f'Line! length {line}')
                return True
        return False

    def __str__(self):
        xmax = max(i[0] for i in self.squares_taken.keys())
        xmin = min(i[0] for i in self.squares_taken.keys())
        ymax = max(i[1] for i in self.squares_taken.keys())
        ymin = min(i[1] for i in self.squares_taken.keys())
        out = ''
        for y in range( ymax+1, ymin-2, -1):
            for x in range(xmin-1, xmax+2):
                if (x, y) == (0, 0):
                    out += '0'
                    continue
                if (x, y) in self.squares_taken.keys():
                    tile = self.squares_taken[(x,y)]
                    out += tile.player.name[0]
                else:
                    out+='-'
            out+= '\n'
        print(out, len(out))
        print()
        return out
        
class Tile:
    def __init__(self, pos, player):
        self.pos = pos
        self.player = player
        print('tile created:', pos, player)
    
    def __str__(self):
        return self.pos

    def played(self):
        return (self.pos != 'rack')

class Player:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.tiles = [Tile('rack', self) for i in range(10)]
    
    def all_tiles_down(self):
        return all([tile.played() for tile in self.tiles])
    
    def tile_from_rack(self):
        '''Assumes not all tiles played'''
        for tile in self.tiles:
            if tile.played():
                continue
            return tile
    
    def __str__(self):
        return self.name
    
player_names = [('chris', 'blue'), ('liam', 'green'), ('dave', 'yellow')]
    
def process_loc(pos):
    try:
        sep = pos.split(',')
        sep = [num.strip() for num in sep] 
        print('sep input', sep)
        if len(sep) != 2:
            print(len(sep), '- length is not 2')
            return False
        return int(sep[0]), int(sep[1])
    except Exception as e:
        print(e)
        return False

def start(player_names):
    board = Board()
    players = [Player(pair[0], pair[1]) for pair in player_names]
    return board, players


def play(players):
    board = Board()
    players = [Player(pair[0], pair[1]) for pair in player_names]
    game_over = False
    for i in range(1000):
        active_player = players[i% (len(players))]
        print(f'Active player: {active_player}')
        if active_player.all_tiles_down():
            pass
            # Select tile from played ones
        else:
            active_tile = active_player.tile_from_rack()
        
        move_done = False
        
        if i == 0:
            board.place_tile(active_tile, (0,0))
            move_done = True
            
        while not move_done:
            inp = input('Pick new pos: ')
            if inp == 'exit':
                game_over = True
                break
            new_pos = process_loc(inp)
            if not new_pos:
                continue
            if not board.check_pos_allowed(new_pos):
                continue
            board.place_tile(active_tile, new_pos)
            move_done = True
        print(f'at end of turn, tiles at {board.squares_taken.keys()}')
        if board.check_winning_move(active_tile):
            print(f'{active_player} wins!')
            game_over = True
        
        if game_over:
            break
    return board

board = play(player_names)
    
