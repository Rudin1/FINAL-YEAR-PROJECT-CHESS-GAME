import pygame as p
from AI.chess_board import board_game
from AI.chess_board import Move
import time

# OPTIONS
LEN_SQ = 80
DIM = 8
LEN_WIN = DIM*LEN_SQ
IMAGES = {}
COLOR_SQ_1 = 'white' # https://www.webucator.com/blog/2015/03/python-color-constants-module/ for colors
COLOR_SQ_2 = '#8B8989'
COLOR_HIGH_1 =["blue","#FFD700"] # (selected normal, ignored king check)
pm_color = 'red'
alpha = 100
flag_highlight_sq = False
promotion_flag = False
AI_PLAY = False

''' load images, we will use it when drawing an square image'''
def loadImages():
    pieces = ["wp","wr","wk","wb","wn","wq","bp","br","bn","bb","bk","bq"] # color,kind
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("img/" + piece + ".png"),(LEN_SQ,LEN_SQ))
        # CALL BY IMAGES['wp']


''' draw board'''
def draw_board(screen,selected_sq,possible_moves):
    global highlight,pm_color
    colors = [p.Color(COLOR_SQ_1), p.Color(COLOR_SQ_2)]
    potential_moves = []
    if len(possible_moves) != 0:

        #for i in possible_moves: potential_moves.append(i.to_sq) # get possible moves in (x,y) format
        potential_moves = [i.to_sq for i in possible_moves]
    # draw board squares
    for r in range(DIM):
        for c in range(DIM):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*LEN_SQ,r*LEN_SQ,LEN_SQ,LEN_SQ))

            # paint the possible move sq's (if given one)
            if (r, c) in potential_moves:
                color = p.Color(pm_color)
                s = p.Surface((LEN_SQ, LEN_SQ))  # per-pixel alpha
                s.set_alpha(alpha)  # alpha level
                s.fill(color)
                screen.blit(s, (c*LEN_SQ, r*LEN_SQ))
                #p.draw.circle(screen, color,(c*SQ_SIZE+ 32,r*SQ_SIZE +32),10)

    # paint the selected sq (if given one)
    if len(selected_sq) != 0:
        x,y = selected_sq[0],selected_sq[1]
        trans = 100
        if flag_highlight_sq: color = p.Color(COLOR_HIGH_1[1]); trans = 150 # color for king in check if not selected
        else: color = p.Color(COLOR_HIGH_1[0]); # selected sq normal
        s = p.Surface((LEN_SQ, LEN_SQ))  # per-pixel alpha
        s.set_alpha(trans)  # alpha level
        s.fill(color)
        screen.blit(s, (y*LEN_SQ, x*LEN_SQ))


''' draw pieces on board'''
def draw_pieces(screen,board):
    for r in range(DIM):
        for c in range(DIM):
            if board[r][c] != '--':
                name = board[r][c]
                screen.blit(IMAGES[name],p.Rect(c*LEN_SQ,r*LEN_SQ,LEN_SQ,LEN_SQ))



''' draw game, first board, second pieces on it '''
def draw_game_state(screen,board,selected_sq = (),possible_moves = []):
    draw_board(screen,selected_sq,possible_moves)
    draw_pieces(screen,board)
    clock = p.time.Clock().tick(30)
    p.display.flip()


''' select piece by mouse click, or exit game (x)'''
def mouse_action(screen,game):
    while 1:
        for e in p.event.get():
            if e.type == p.QUIT:
                return -1,-1 # or exit()

            elif e.type == p.MOUSEBUTTONDOWN and not promotion_flag:
                location = p.mouse.get_pos()
                x, y = location[1] // LEN_SQ, location[0] // LEN_SQ
                return x,y

            elif e.type == p.KEYDOWN:
                    if e.key == p.K_p:      # undo move
                        game.undo_move()
                        game.undo_move()
                        global AI_PLAY
                        AI_PLAY = False
                        draw_game_state(screen, game.board) # draw
                        return -2,-2
                    elif e.key == p.K_r:
                        print("restart")
                        return -3,-3
                    else:
                        return -2, -2 # if no use just pass (other keys)



''' highlight square '''
def highlight_check(screen, board,king):
    draw_board(screen,king,[])
    draw_pieces(screen, board)
    clock = p.time.Clock().tick(30)
    p.display.flip()



''' main '''
def main(win,lvl):
    #p.init()
    #screen = p.display.set_mode((LEN_WIN, LEN_WIN))  # width,height
    #screen.fill(p.Color("white"))

    p.display.set_caption('game')
    screen = win
    quited = False
    loadImages()  # once before while loop

    while not quited:
        running = True
        game_state = board_game()
        game_state.depth_tree = lvl
        print("-----")
        print(game_state.depth_tree)
        print("----")
        draw_game_state(screen, game_state.board)  # screen,board,sq_from,possible_moves = []): ----------

        flag_pass_mouse_1 = False
        global flag_highlight_sq,AI_PLAY
        flag = False  # variable helper to flag_highlight_sq

        AI_PLAY = False
#----------------------------------------------------------------------------------------------------------------------------------
        while running:

            if AI_PLAY:
                #print(f"mainnn ==== > {game_state.get_turn_board()}")
                move = game_state.negamax(game_state.depth_tree)



                game_state.make_move(move)
                draw_game_state(screen, game_state.board)
                game_state.turn *= -1
                AI_PLAY = False
            else:


                    #print(f"TURN GAME =  - {game_state.get_turn_board()} - ")
                if game_state.is_stalemate(): print("DRAW - GAME OVER")
                if game_state.is_checkmate():
                    print(" - CHECKMATED - GAME OVER"); running = False


                if game_state.is_in_check(): # if current king in check
                    print("*******check")
                    print(game_state.get_turn_board())
                    flag = True




                # mouse 1
                ####---------------------------------------------------------------------------------------------------------------------------
                if not flag_pass_mouse_1:

                    a, b = mouse_action(screen,game_state)
                    if a == -3:  running = False  # break loop and restart game

                    if a == -1: quited = True; running = False                             # quit by pressing (x)
                    elif a == -2 or game_state.board[a][b] == '--': continue               # if undo_move or selected empty sq --> jump
                    if game_state.board[a][b][0] != game_state.get_turn_board(): continue  # if selected color not in turns time --> continue


                    possible_moves = game_state.get_moves(a,b) # get move of spesific sq
                    draw_game_state(screen, game_state.board,(a,b),possible_moves)  # screen,board,sq_from,possible_moves

                flag_pass_mouse_1 = False # for the next turn




                # mouse 2
                ####---------------------------------------------------------------------------------------------------------------------------
                x, y = mouse_action(screen,game_state)
                if x == -3: running = False  # break loop and restart game
                if x == -1: quited = True; running = False



                from_sq, to_sq = (a, b), (x, y)                                  # piece move from --> to (x,y)
                if game_state.board[x][y][0] == game_state.get_turn_board():     # if selected piece with same color
                    possible_moves = game_state.get_moves(x, y)                  # get move of spesific sq
                    draw_game_state(screen, game_state.board, (x, y),possible_moves)  # draw possible_moves
                    flag_pass_mouse_1 = True;                                    # pass mouse 1 (and assign to a,b = x,y) ===> (from_sq of next move) = (to_sq of previous move)
                    a,b = x,y
                    continue
                if from_sq == to_sq: flag_pass_mouse_1 = True; continue          # if selected same sqaure --> jump to mouse 2
                flag_changed_turn = False


                # 3 move
                ####---------------------------------------------------------------------------------------------------------------------------
                move = Move(from_sq,to_sq,game_state.board) # create move
                move = game_state.check_type_move(move) # determine if its normal, enpassant or castling

                #print(f"move.to_sq = {move.to_sq}\n")
                validation = game_state.is_move_valid(move) # check move validation(from,to,board)
                if validation:
                    flag_highlight_sq = False

                    game_state.make_move(move,True) # (from,to,board)
                    game_state.is_pawn_promotion() # -----  promote only to queen, correct it latter -----

                    AI_PLAY = True # AI turn to play
                    game_state.turn *= -1               # change turns
                    flag_changed_turn = True



                draw_game_state(screen, game_state.board)  # screen,board,sq_from,possible_moves
                game_state.nullify_recursion_possible_moves = False # sea





                # king in check and not selected, highlight checked king
                if flag and not flag_changed_turn:
                    flag_highlight_sq = True
                    # get position of current turn king
                    king = game_state.get_turn_board() + 'k'
                    if king == 'wk':king = game_state.king_white
                    else: king = game_state.king_black

                    temp = king

                    for i in range(3):
                        highlight_check(screen, game_state.board,temp)
                        time.sleep(0.1)
                        if flag_highlight_sq: flag_highlight_sq = False; temp = ()
                        else: flag_highlight_sq = True; temp = king

                        draw_game_state(screen, game_state.board) # draw for last normal board

                flag = False


def start_ai(win,arr_options):
    global COLOR_SQ_1,COLOR_SQ_2,pm_color,COLOR_HIGH_1,alpha

    COLOR_SQ_1 = arr_options[0]
    COLOR_SQ_2 = arr_options[1]
    pm_color = arr_options[2]
    COLOR_HIGH_1 = arr_options[3]
    alpha = arr_options[4]

    print("-------",arr_options)

    main(win,arr_options[6])





'''else:  # (color,location)
    print("sjot")
    loc, turn_piece = promotion[1], promotion[0]
    if e.key == p.K_q:  # queen
        game.board[loc[0]][loc[1]] = turn_piece + 'q'
        break

    elif e.key == p.K_r:  # rook
        game.board[loc[0]][loc[1]] = turn_piece + 'r'
        break
    elif e.key == p.K_b:  # bishop
        game.board[loc[0]][loc[1]] = turn_piece + 'b'
        break
    elif e.key == p.K_n:  # knight
        game.board[loc[0]][loc[1]] = turn_piece + 'n'
        break

    else:
        print("wrong input")

        print("CHOOSE PROMOTION : 'q' = Queen ||  'r' = Rook || 'n' = Knight || 'b' = Bishop")'''