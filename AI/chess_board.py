import copy
import numpy as np

options = ['q','r','n','k']

class board_game():
    def __init__(self):

        self.king_white, self.king_black = (7, 4), (0, 4)   # position of kings
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]


        self.castling_rook = [[True]*2,[True]*2]    # castling rooks (white=l,r  ||  black= l,r)
        self.castling_king = [True] * 2             # castling kings (white,black) first moves

        self.array_flags = [0]*6                    # if false, cant switch castling flags
        self.current_turn_number = 1
        self.move_timeline = []                     # save all moves in case the user undo the moves
        self.turn = 1                               # white = (1), black = (-1)

        # get function moves of every piece pieces
        self.move_pieces_functions = {"p" : self.get_pawn_moves,"r" : self.get_rook_moves,"n" : self.get_knight_moves,
                               "b" : self.get_bishop_moves, "k" : self.get_king_moves , "q" : self.get_queen_moves}

        #### can replace with kings positions circle
        self.nullify_recursion_possible_moves = False # dont recurse in function get_all_possible_moves
        self.recursed_count = 0
        ####

        self.depth_tree = 2
        self.DEPTH_MAX = 3  # DEPTH_MAX
        self.flag_map_king = 0
        self.best_move = 0



    # 1 ) add to score the value choosing this place from map pieces (= from_sq)
    # 2 ) add to score the value of capturing/moving to the place (to_sq, PLUS  ==
    # in case of en passant, + enemy pawn)
    # in case of castling, + map values of rooks)
    def get_score(self,move,turn):
        score = 0

        if turn == 'b':
            row = 0 # black
            temp_king_map = self.king_map[self.flag_map_king]
            temp_piece_map = self.get_map[move.kind_from_sq[1]]

        else:
            # white
            # we need to flip the map pieces (white prespective)
            row = 7
            temp_king_map = np.flipud(self.king_map[self.flag_map_king])
            temp_piece_map = np.flipud(self.get_map[move.kind_from_sq[1]])

        # score === value piece on map (choose score) +++ move to place (move or capture enemy piece)
        if move.kind_from_sq[1] == 'k': score += temp_king_map[move.from_sq[0]][move.from_sq[1]]     # value king on map piece
        else: score += temp_piece_map[move.from_sq[0]][move.from_sq[1]]                              # value of any piece that != king
        score += self.get_value_piece[move.kind_to_sq[1]]                                            # value of capture piece (or empty space = 0)


        return score


    # evaluation function is based on Claude Shannon's formula:
    # ====> f(p) = 200(K-K') + 9(Q-Q')+ 5(R-R') + 3(B-B' + N-N') + 1(P-P')- 0.5(D-D' + S-S' + I-I')+ 0.1(M-M') + ...
    ## KQRBNP = number of kings, queens, rooks, bishops, knights and pawns
    ## D,S,I = double, blocked and isolated pawns
    ## M = mobility ( number of legal moves)

    def evaluate(self):
        # [0,0] = (black, white)
        k,q,r,b,p,n = [0,0],[0,0],[0,0],[0,0],[0,0],[0,0]   # count pieces
        double,blocked,isolated  =[0,0],[0,0],[0,0]                           # doubled, blocked and isolated pawns
        flag_isolated = [[True]*8]*2
        m = [0,0]                                           # mobility (the number of legal moves)

        for i in range(8):
            count_pawns = [0,0] # initialize
            for j in range(8):
                # count doubles for each color, for each col
                if self.board[j][i] == 'bp': count_pawns[0] += 1;
                if self.board[j][i] == 'wp': count_pawns[1] += 1

                # count blocked pawns
                if 0 < j < 7:
                    if self.board[j][i] == 'bp' and self.board[j+1][i][0] == 'w': blocked[0] += 1
                    if self.board[j][i] == 'wp' and self.board[j - 1][i][0] == 'b': blocked[1] += 1

                # isolated
                if count_pawns[0] != 0: flag_isolated[0][i]= False
                if count_pawns[1] != 0: flag_isolated[1][i] = False

                # see if there is a double for each col
                if count_pawns[0] > 0: double[0] += 1      # col with double black
                if count_pawns[1] > 0: double[1] += 1      # col with double white

                # add the count of pawns to p:
                p[0]+=count_pawns[0]
                p[1] += count_pawns[1]

                # count of pieces
                # ---------------black----------------#
                if self.board[j][i] == 'bb': b[0] += 1
                if self.board[j][i] == 'br': r[0] += 1
                if self.board[j][i] == 'bq': q[0] += 1
                if self.board[j][i] == 'bk': n[0] += 1
                if self.board[j][i] == 'bk': k[0] += 1

                #---------------white-----------------#
                if self.board[j][i] == 'wb': b[1] += 1
                if self.board[j][i] == 'wr': r[1] += 1
                if self.board[j][i] == 'wq': q[1] += 1
                if self.board[j][i] == 'wk': n[1] += 1
                if self.board[j][i] == 'wk': k[1] += 1


        # count how many isolations for each color
        for i in range(8):
            if i == 0:
                if flag_isolated[0][0] == True and flag_isolated[0][1] == False: isolated[0] += 1    # black
                if flag_isolated[1][0] == True and flag_isolated[1][1] == False: isolated[0] += 1    # white

            if 1<i<7:
                if flag_isolated[0][i-1]== False and flag_isolated[0][i] == True and flag_isolated[0][i+1] == False:isolated[0] += 1        # black
                if flag_isolated[1][i - 1] == False and flag_isolated[1][i] == True and flag_isolated[1][i + 1] == False: isolated[1] += 1  # white

            if i == 7:
                if flag_isolated[0][7] == True and flag_isolated[0][6] == False: isolated[0] += 1    # black
                if flag_isolated[1][7] == True and flag_isolated[1][6] == False: isolated[0] += 1    # white

        # count mobility

        m[0] = len(self.get_all_possible_moves('b'))
        m[1] = len(self.get_all_possible_moves('w'))

        if self.get_turn_board()=='b': cr , nt = 0,1 # cr = current_turn ,nt = opponent_turn
        else: cr ,nt= 1,0

        # f(p) = 200(K-K') + 9(Q-Q')+ 5(R-R') + 3(B-B' + N-N') + 1(P-P')- 0.5(D-D' + S-S' + I-I')+ 0.1(M-M')
        formula_1 = 200*(k[cr]-k[nt]) + 9*(q[cr]-q[nt])+ 5*(r[cr]-r[nt]) + 3*(b[cr]-b[nt] +n[cr]-n[nt]) + 1*(p[cr]-p[nt])
        formula_2 =  -0.5*(double[cr]-double[nt] + blocked[cr]-blocked[nt]+ isolated[cr]-isolated[nt])+ 0.1*(m[cr]-m[nt])

        Shannon_f = formula_1+formula_2
        return Shannon_f



    def negamax(self, depth=2,a= -np.inf,b= np.inf):  # True == black turn
        #if depth == 2: print(f"turns ==== > {self.get_turn_board()}")
        if depth == 0:
            return self.evaluate()

        score = -np.inf
        best_score = -np.inf
        for move in self.get_all_possible_moves(self.get_turn_board()):
            self.make_move(move)

            self.turn = self.turn * (-1)  # next turn
            score = max(score,-self.negamax(depth -1,-b,-a)) #-1 *
            self.turn = self.turn * (-1)  # prev turn again

            a = max(a,score)

            if depth == self.depth_tree:
                if score > best_score:
                    best_score = score
                    self.best_move = copy.deepcopy(move)

            self.undo_move()

            if a >= b: print(f"a = {a}, b = {b}");break ####################
        if depth == self.depth_tree : return self.best_move
        else: return score







    # CHECK if current king in check
    def is_in_check(self):
        all_enemy_possible_moves = self.get_all_possible_moves(self.get_turn_enemy(),True) # True for pawn attack, not including normal moves (of pawn)
        all_enemy_possible_moves = [i.to_sq for i in all_enemy_possible_moves]  # convert to (x,y) to_sq

        # get position of current turn king
        king = self.get_turn_board() + 'k'
        if king == 'wk':king = self.king_white
        else: king = self.king_black

        return king in all_enemy_possible_moves


    # 3 condition for checkmate:
    # 1) king cant move
    # AND
    # 2) if there are 2 or more checking king --> one directly and the other indirectly (blocked) and these 2 must move --> checkmate
    # 3) else if only 1 checking king --> if cant capture or block --> chackmated
    def is_checkmate(self):

        # CHECK if king in check for every move ((2) + (3) + (1))
        # make every move (current turn), if still in check --> cant solve (includes kings moves (1),double check)
        all_turn_moves = self.get_all_possible_moves(self.get_turn_board())
        result = self.remove_move_checks(all_turn_moves)
        return len(result) == 0



    # check if game state is in stalemate
    def is_stalemate(self):
        turn = self.get_turn_board() # in letter
        result = self.get_all_possible_moves(turn)
        if len(result) == 0:
            return True
        return False

    # get all possible moves of the current color/turn
    def get_all_possible_moves(self,turn,exclude_pawn = False): #exclude pawn = for king, find forbbiden places of possible attack by pawns
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j][0] == turn:
                    piece = self.board[i][j][1] # take piece kind
                    piece_moves_function = self.move_pieces_functions[piece]  # get the right move function of specific piece
                    if piece == 'p' and exclude_pawn: possible_moves = piece_moves_function(i, j,exclude_pawn)
                    else: possible_moves = piece_moves_function(i, j)  # get valid moves list
                    if len(possible_moves) != 0:
                        moves.extend(possible_moves)


        return moves  # get ultimate moves = without moves that causes cheking

    # return as letter
    def get_turn_enemy(self):
        if self.turn == 1: return 'b'
        else: return 'w'

    # return as letter
    def get_turn_board(self):
        if self.turn == 1: return 'w'
        else: return 'b'

    # return as number
    def get_turn_num(self,turn):
        if turn == 'w': return 1
        else: return -1

    def remove_move_checks(self,all_moves): # remove all moves that causes check
        flag_check = False

        if self.get_turn_board() == 'w': addition = 1
        else: addition = -1


        for i in range(len(all_moves)-1,-1,-1):
            if  all_moves[i].type_move == 'normal': # moves that are not enpassant or castling
                #print("normal")
                self.make_move(all_moves[i])
                if self.is_in_check(): flag_check = True
                self.undo_move()
                if flag_check: all_moves.remove(all_moves[i])
                flag_check = False

            elif all_moves[i].type_move == 'enpassant': # enpassant
                #print("enpassant")
                self.make_move(all_moves[i])
                if self.is_in_check(): flag_check = True
                self.undo_move()
                if flag_check: all_moves.remove(all_moves[i]) # if causes check --> remove
                flag_check = False

            else: # castling
                #print("castling")
                self.make_move(all_moves[i])

                if self.is_in_check(): flag_check = True
                self.undo_move()
                if flag_check: all_moves.remove(all_moves[i]) # if causes check --> remove
                flag_check = False


        return all_moves



    def is_castling(self,x,y):
        arr = []
        # first move king must be True and atleat 1 rook == true
        # white
        if self.get_turn_board() == 'w':
            if self.castling_king[0] == False: return arr
            elif self.castling_rook[0][0] == False and self.castling_rook[0][1] == False: return arr
            else:
                x = 7


        # black
        else:
            if self.castling_king[1] == False: return arr
            elif self.castling_rook[1][0] == False and self.castling_rook[1][1] == False: return arr
            else: x = 0

        y = 4 # (x,y of king)



        # conditions:
        # 1 cant castle in check
        if self.is_in_check(): return arr

        # 2 cant castle through a check or into a check = (2 place from left) or (right) not in (enemy possible moves)
        # 3 need empty spaces all the way
        cols = [(2,3),(5,6)] # way
        place_jump = [2,6] # king jump
        from_y = [0,7] # rook from
        to_y = [3, 5] # rook to



        enemy_moves = self.get_all_possible_moves(self.get_turn_enemy(),True)
        enemy_moves = [i.to_sq for i in enemy_moves]  # convert to (x,y) to_sq
        piece = self.get_turn_board() + 'r'
        if self.get_turn_board()=='w': turn_castling = 0
        else: turn_castling = 1
        # check both sides
        for i in range(2):
                if not (x,cols[i][0]) in enemy_moves and not (x,cols[i][1]) in enemy_moves and \
                        self.board[x][cols[i][0]] == '--' and self.board[x][cols[i][1]] == '--' and self.castling_rook[turn_castling][i]:
                    arr.append(Move((x,y),(x,place_jump[i]),self.board,'castling',[piece,(x,from_y[i]),(x,to_y[i])])) #[piece_rook,from_position,to_position]))

        return arr


    ''' return if piece got en passant move''' #------------------------- #------------------------- #------------------------- #------------------------- #-------------------------
    def is_enpassant_move(self,x,y):

        arr = []
        row = 3 # white
        if self.get_turn_board() == 'b': row = 4

        if x != row: return [] # not an enpassant
        step = 1

        if len(self.move_timeline) == 0: return []
        # function find enpassant position if there is (pawn jumped 2 steps ahead)
        res = self.find_enpassant_location(self.board,self.move_timeline[-1])

        if len(res) == 0: return []
        enemy_piece_pawn = res[1]
        en_passant_loc = res[0]

        if self.get_turn_board() == 'w':  addition = -1 # addition 1 to white goes up (x-1)
        else:  addition = 1 #  1 to black goes down (x+1)

        for i in range(2):
            if self.inside_move(x,y+step) and self.board[x][y+step] == enemy_piece_pawn and (x,y+step) == en_passant_loc: # found an enpassant pawn
                arr.append(Move((x,y),(x+addition,y+step),self.board,'enpassant',[enemy_piece_pawn,en_passant_loc]))

            step = -1

        return arr


    ''' get moves of specific piece by location'''
    def get_moves(self, x, y):
        piece = self.board[x][y][1]  # kind


        piece_moves_function = self.move_pieces_functions[piece] # get right function
        moves = piece_moves_function(x,y)      # get 'moves'


        if piece == 'p': # check if there are enpassant moves pawn on side
            en_passnat = self.is_enpassant_move(x,y)
            moves.extend(en_passnat)


        if piece == 'k':  # if king, check if can do castling
            castling = self.is_castling(x, y)
            moves.extend(castling)


        moves = self.remove_move_checks(moves)  # get ultimate moves =

        return moves

    ''' determine the type of selected final move '''
    def check_type_move(self,move):

        # an enpassant move
        arr = self.is_enpassant_move(move.from_sq[0], move.from_sq[1])
        if move in arr:
            for i in arr:
                if i == move: return i # enpassant
        else:
            arr = self.is_castling(move.from_sq[0], move.from_sq[1])
            if move in arr:
                for i in arr:
                    if i == move: return i # castling

        return move # normal



    ''' check if move is valid'''
    def is_move_valid(self,move):
        turn,piece,board = move.kind_from_sq[0],move.kind_from_sq[1],move.board # (turn_letter,piece,board)
        x,y = move.from_sq[0],move.from_sq[1] # (row,col)

        piece_moves_function = self.move_pieces_functions[piece]   # get the right move function of specific piece
        possible_moves = piece_moves_function(x,y) # get valid moves list

        if piece == 'p': # check if there are enpassant moves pawn on side
            en_passnat = self.is_enpassant_move(x,y)
            possible_moves.extend(en_passnat)

        if piece == 'k':  # if king, check if can do castling
            castling = self.is_castling(x,y)
            possible_moves.extend(castling)

        possible_moves = self.remove_move_checks(possible_moves)

        return move in possible_moves


    def inside_move(self,a,b):
        return 0 <= a <= 7 and 0 <= b <= 7


    def get_pawn_moves(self, x, y, flag_attack_only = False):

        piece,turn = self.board[x][y][1], self.board[x][y][0]
        legal_moves = []
        step,legal_places,first_row = 1,[],1  # black
        if turn != 'b': step,first_row = -1,6  # white


        if not flag_attack_only:

            # 1 move ahead
            if self.inside_move(x + step, y) and self.board[x + step][y] == '--' : legal_moves.append(Move((x,y),(x + step, y),self.board))

            # 2 move ahead , (first move,empty sqs step 1 ,and 2P) # and save move position maybe its a en passant
            if first_row == x and self.board[x + step][y] == '--' and self.board[x + step*2][y] == '--'  :
                legal_moves.append(Move((x,y),(x + step*2, y),self.board))


                    # right black / white left (not empty,enemy color)
            if self.inside_move(y + step, x + step) and self.board[x + step][y + step][0] !='-' and  self.board[x + step][y + step][0] != self.board[x][y][0]:
                legal_moves.append(Move((x,y),(x + step, y + step),self.board))

            # left black / white right
            if self.inside_move(x + step, y - step) and self.board[x + step][y - step][0] !='-' and  self.board[x + step][y - step][0] != self.board[x][y][0]:
                legal_moves.append(Move((x,y),(x + step, y - step),self.board))

        else: # flag_attack_only  for king needs only attack positions

            # right black / white left (not empty,enemy color)
            if self.inside_move(y + step, x + step):
                legal_moves.append(Move((x, y), (x + step, y + step), self.board))

            # left black / white right
            if self.inside_move(x + step, y - step):
                legal_moves.append(Move((x, y), (x + step, y - step), self.board))


        return legal_moves


    def get_rook_moves(self,x,y):
        # --- y axis
        legal_moves = []
        step = addition = 1
        for i in range(2):  # left
            while self.inside_move(x, y - step):
                if self.board[x][y - step][0] == '-' or self.board[x][y - step][0] != self.board[x][y][0]: # (empty or enemy piece)
                    legal_moves.append(Move((x, y), (x, y - step), self.board))

                if self.board[x][y - step][0] != '-': break # (if not empty --> break)

                step += addition

            # (right)- step
            step = addition = -1

        # --- x axis
        step = addition = 1

        for i in range(2):  # up
            while self.inside_move(x - step, y):
                if self.board[x - step][y][0] == '-' or self.board[x - step][y][0] != self.board[x][y][0]:
                    legal_moves.append(Move((x, y), (x - step, y), self.board))

                if self.board[x - step][y][0] != '-': break # (if not empty --> break)

                step += addition
            # (down)
            step = addition = -1

        return legal_moves

    def get_knight_moves(self,a,b):
        legal_moves = []
        arr = [(a - 2, b + 1), (a - 2, b - 1), (a + 1, b + 2), (a - 1, b + 2), (a + 2, b + 1), (a + 2, b - 1),
               (a + 1, b - 2), (a - 1, b - 2)]

        for x, y in arr:
            if self.inside_move(x, y):
                if self.board[x][y][0] == '-' or (
                        self.board[a][b][0] != self.board[x][y][0] and self.board[x][y][0] != '-'):
                    legal_moves.append(Move((a, b), (x, y), self.board))

        return legal_moves

    def get_bishop_moves(self,x,y):
        arr = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        legal_moves = []
        for i in range(4):
            c1, c2 = arr[i][0], arr[i][1]
            addition_x, addition_y = c1, c2
            while self.inside_move(x + addition_x, y + addition_y):  # right down

                if self.board[x + addition_x][y + addition_y][0] == '-':
                    legal_moves.append(Move((x, y), (x + addition_x, y + addition_y), self.board))

                elif self.board[x + addition_x][y + addition_y][0] != self.board[x][y][0]:  # opponent color
                    legal_moves.append(Move((x, y), (x + addition_x, y + addition_y), self.board))
                    break
                else:
                    break  # same color

                addition_x += c1
                addition_y += c2

        return legal_moves




    def get_king_moves(self,x,y):

        legal_moves = []
        arr = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]  # up,right...
        for i in range(8):
            c1, c2 = arr[i][0], arr[i][1]
            if self.inside_move(x + c1, y + c2):  # right down
                if self.board[x + c1][y + c2][0] == '-' : legal_moves.append(Move((x, y), (x + c1, y + c2), self.board))
                if self.board[x + c1][y + c2][0] != '-' and self.board[x + c1][y + c2][0] != self.board[x][y][0]:  # no color or op color
                    legal_moves.append(Move((x, y), (x + c1, y + c2), self.board))

        if self.nullify_recursion_possible_moves == False:
            self.recursed_count+=1

            self.nullify_recursion_possible_moves = True

            all_enemy_possible_moves = self.get_all_possible_moves(self.get_turn_enemy(),True) # get all enemy & exculde moves pawns. we treat them up in 'no_pawns_attacks_diagnol'
            all_enemy_possible_moves = [i.to_sq for i in all_enemy_possible_moves] # convert to (x,y) to_sq

            for i in range(len(legal_moves)-1,-1,-1): # remove same squares
                if legal_moves[i].to_sq in all_enemy_possible_moves:
                    legal_moves.remove(legal_moves[i])


        # init nullify_recursion_possible_moves every 1 recursion to defualt = False
        if self.recursed_count == 1:
            self.nullify_recursion_possible_moves = False
            self.recursed_count = 0




        return legal_moves

    def get_queen_moves(self,x,y):

        # queen moves = rook + bishop moves
        legal_moves_1 = self.get_bishop_moves(x,y)
        legal_moves_2 = self.get_rook_moves(x,y)
        legal_moves_1.extend(legal_moves_2)

        return legal_moves_1


    ''' make selected move '''
    def make_move(self,move,final = False):

        self.board[move.to_sq[0]][move.to_sq[1]]  = self.board[move.from_sq[0]][move.from_sq[1]]  # move first piece
        self.board[move.from_sq[0]][move.from_sq[1]]  = '--' # after move --> empty

        self.move_timeline.append(move)   # save move
        if move.kind_from_sq == 'wk': self.king_white = (move.to_sq[0],move.to_sq[1])   # update white/black king positions if necessary
        if move.kind_from_sq == 'bk': self.king_black = (move.to_sq[0], move.to_sq[1])


        #  enpassant move, update
        if move.type_move == 'enpassant':
            self.board[move.location_pawn[0]][move.location_pawn[1]] = '--'

        # castling info -------
        if move.type_move == 'castling':
            self.board[move.rook_from[0]][move.rook_from[1]] = '--'
            self.board[move.rook_to[0]][move.rook_to[1]] = move.castling_piece


        # if first move made (one from the 6 options piece castlings) save turn number
        if self.get_turn_board() == 'w':
            castling_color, piece_king, piece_rook,row,step = 0, 'wk', 'wr',7,0
        else:
            castling_color, piece_king, piece_rook,row,step = 1, 'bk', 'br',0,3


        if self.board[row][4] != piece_king and self.castling_king[castling_color] == True: # if moved --> first move false
            self.castling_king[castling_color] = False
            self.array_flags[0+step] = self.current_turn_number   # remember turn number


        if self.board[row][0] != piece_rook and self.castling_rook[castling_color][0] == True:
            self.castling_rook[castling_color][0] = False
            self.array_flags[1+step] = self.current_turn_number

        if self.board[row][7] != piece_rook and self.castling_rook[castling_color][1] == True:
            self.castling_rook[castling_color][1] = False
            self.array_flags[2+step] = self.current_turn_number


        # update turn number increase
        self.current_turn_number += 1

    ''' promote pawns if they reached last row '''
    def is_pawn_promotion(self):
        for j in range(8):
            if self.get_turn_board() == 'w': row = 0
            else: row = 7
            if self.board[row][j][1] == 'p': self.board[row][j] = self.board[row][j][0] + 'q'



    ''' print current board '''
    def print_board(self,m):
        for i in range(8):
            for j in range(8):
                print(m[i][j],end=" || ")
            print()

    ''' finds enpassant move, meaning only works in 1 turn ahead, else it wont work'''
    def find_enpassant_location(self,current_board,move):
        if self.get_turn_enemy() == 'b': row,piece,step = 3,'bp',-2
        else: row,piece,step = 4,'wp',2

        for i in range(8): # run over the selected row
            if current_board[row][i] == piece:
                if move.board[row+step][i] == piece:
                    return [(row,i),piece]   # found enpassant move, return location of jumped pawn

        return []



    def undo_move(self):

        if len(self.move_timeline) != 0:
            self.current_turn_number -= 1  # update turn number decrease

            last_move = self.move_timeline.pop()

            # update king position if its a king change
            if last_move.kind_from_sq == 'wk': self.king_white = (last_move.from_sq[0], last_move.from_sq[1])  # update white/black king positions if necessary
            if last_move.kind_from_sq == 'bk': self.king_black = (last_move.from_sq[0], last_move.from_sq[1])

            # restore piece before move excuted
            self.board[last_move.to_sq[0]][last_move.to_sq[1]] = last_move.kind_to_sq
            self.board[last_move.from_sq[0]][last_move.from_sq[1]] = last_move.kind_from_sq



            if last_move.type_move == 'enpassant': # restore current enpassant possible move location
                self.board[last_move.location_pawn[0]][last_move.location_pawn[1]] = last_move.captured_pawn

            if last_move.type_move == 'castling':
                self.board[last_move.rook_from[0]][last_move.rook_from[1]] = last_move.castling_piece
                self.board[last_move.rook_to[0]][last_move.rook_to[1]] = '--'


            # piece moved = turn move = keep that way
            self.turn = self.get_turn_num(last_move.kind_from_sq[0])

            # find when first move made (6 options)
            if self.get_turn_board() == 'w':
                castling_color, piece_king, piece_rook, row, step = 0, 'wk', 'wr', 7, 0
            else:
                castling_color, piece_king, piece_rook, row, step = 1, 'bk', 'br', 0, 3



            if self.board[row][4] == piece_king and self.castling_king[castling_color] == False and self.array_flags[0 + step] == self.current_turn_number:
                self.castling_king[castling_color] = True
                self.array_flags[0 + step] = 0

            if self.board[row][0] == piece_rook and self.castling_rook[castling_color][0] == False and self.array_flags[1 + step] == self.current_turn_number:
                self.castling_rook[castling_color][0] = True
                self.array_flags[1 + step] = 0

            if self.board[row][7] == piece_rook and self.castling_rook[castling_color][1] == False and self.array_flags[2 + step] == self.current_turn_number:
                self.castling_rook[castling_color][1] = True
                self.array_flags[2 + step] = 0



        # ------------------------------------------------------MOVE CLASS--------------------------------------------------------------------------------------------#

class Move():
    def __init__(self, from_sq, to_sq,board,type_move = 'normal',enpassant_pawn_or_castling_rook = []):
        self.type_move = type_move   # castling,en passant, normal
        self.board = board #copy.deepcopy(board)      # use it in function move
        self.from_sq = from_sq  # position x,y
        self.to_sq = to_sq      # position x,y
        self.kind_to_sq = board[to_sq[0]][to_sq[1]]         # kind sq
        self.kind_from_sq =  board[from_sq[0]][from_sq[1]]  # kind sq
        self.id_move = from_sq[0]*1000 + from_sq[1]*100 +to_sq[0]*10 + to_sq[1]  # hash function, unique id for every move in current board

        if self.type_move == 'enpassant':
            self.captured_pawn = enpassant_pawn_or_castling_rook[0]  # (wp or bp)
            self.location_pawn = enpassant_pawn_or_castling_rook[1]  # (x,y)

        # arr.append(Move((x,y),(x,place_jump[i]),self.board,'castling',[piece,(x,from_y[i]),(x,to_y[i])])) #[piece_rook,from_position,to_position]))
        if self.type_move == 'castling':
            self.castling_piece = enpassant_pawn_or_castling_rook[0]     # rook
            self.rook_from = enpassant_pawn_or_castling_rook[1]          # (x,y)
            self.rook_to = enpassant_pawn_or_castling_rook[2]            # (x,y)



    def __eq__(self, other):
        return self.id_move == other.id_move



        '''self.board = [
            ["br", "--", "--", "bq", "bk", "--", "--", "br"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wr", "--", "--", "--", "wk", "--", "--", "wr"],
        ]
        self.king_white, self.king_black = (7, 4), (0, 4)'''

        '''self.king_white, self.king_black = (7, 0), (0, 0)
        self.board = [
            ["bk","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","bp","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","wp","--","--","--"],
            ["--","--","--","--","--","--","wp","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wk","--","--","--","--","--","--","--"],
        ]'''
