import pygame as p
import copy
import AI.main_ai as ai
import ONLINE.server as server,ONLINE.client as client
import MULTIPLAYER.main as MP

clock = p.time.Clock()

p.init()
p.display.set_caption('Chess')
window = p.display.set_mode((640,640),0,32)

font = p.font.SysFont('kristenitc', 30,bold=True)
bg = p.transform.scale(p.image.load("bg.png"),(640,640))
sound_on = True

# OPTION SETTINGS
arr_options = [
    ['snow2', 'seagreen4',  "yellow2" , ["yellow3","red"],100,sound_on],
    ['snow2', 'saddlebrown',  "yellow2" , ["yellow3","red"],100,sound_on],
    ['white', '#8B8989', "royalblue4", ["blue", "#FFD700"],100,sound_on],
    ['snow2', 'deepskyblue3', "yellow1", ["firebrick4","darkgoldenrod1"] ,100,sound_on],
    ['snow2', 'firebrick1', "grey0", ["blue3","aquamarine"],100,sound_on],
    ['snow2', 'darkorchid3', "black", ["cadetblue1","aquamarine"],150,sound_on],
    ['white', 'grey23', "lightseagreen", ["cadetblue1","red"],150,sound_on],
    ['white', 'burlywood4', "black", ["cadetblue1","red"],150,sound_on]
]
current_types = 0 # CURRENT CHOICE


buttom_names = ['AI PLAYER','ONLINE','MULTIPLAYER','OPTIONS','EXIT']
def main_menu():

    window.blit(bg, (0, 0))
    # create btms to click
    button_1 = p.Rect(50, 100, 220, 50)  # ai
    button_2 = p.Rect(50, 200, 180, 50)  # online
    button_3 = p.Rect(50, 300, 300, 50)  # mp
    button_4 = p.Rect(50, 400, 200, 50)  # options
    button_5 = p.Rect(50, 500, 100, 50)  # exit

    # draw btms (bg same as main bg)
    p.draw.rect(window, p.Color('skyblue3'), button_1)
    p.draw.rect(window, p.Color('skyblue3'), button_2)
    p.draw.rect(window, p.Color('skyblue3'), button_3)
    p.draw.rect(window, p.Color('skyblue3'), button_4)
    p.draw.rect(window, p.Color('skyblue3'), button_5)
    click = False
    while 1:
        window.blit(bg, (0, 0))

        x,y = p.mouse.get_pos()

        # btm names
        window.blit(font.render(buttom_names[0], True, p.Color('aquamarine4')), (50, 100, 200, 50))
        window.blit(font.render(buttom_names[1], True, p.Color('aquamarine4')), (50, 200, 200, 50))
        window.blit(font.render(buttom_names[2], True, p.Color('aquamarine4')), (50, 300, 200, 50))
        window.blit(font.render(buttom_names[3], True, p.Color('aquamarine4')), (50, 400, 200, 50))
        window.blit(font.render(buttom_names[4], True, p.Color('aquamarine4')), (50, 500, 200, 50))

        ### if mouse hovers over a buttom, light it, and if clicked, open new fitted window
        if button_1.collidepoint((x,y)):
            explaition(window,"Play against AI player")
            window.blit(font.render(buttom_names[0], True, p.Color('lawngreen')), (50,100,200,50))
            if click:  AI_menu(window) # go to manu ai

        if button_2.collidepoint((x, y)):
            explaition(window, "Play online with another person")
            window.blit(font.render(buttom_names[1], True, p.Color('lawngreen')), (50, 200, 200, 50))
            if click:  ONLINE_menu(window)

        if button_3.collidepoint((x, y)):
            explaition(window, "Offline multiplayer")
            window.blit(font.render(buttom_names[2], True, p.Color('lawngreen')), (50, 300, 200, 50))
            if click:  MP.main(window,arr_options[current_types])

        if button_4.collidepoint((x,y)):
            explaition(window, "Set sound and colors")
            window.blit(font.render(buttom_names[3], True, p.Color('lawngreen')), (50,400,200,50))
            if click:  OPTIONS_menu(window)

        if button_5.collidepoint((x,y)):
            explaition(window, "<_<")
            window.blit(font.render(buttom_names[4], True, p.Color('lawngreen')), (50,500,200,50))
            if click: exit()


        click = False
        res = mouse_action()
        click = res


        p.display.update()
        clock.tick(60)

def explaition(window,text):
    font2 = p.font.SysFont('arial', 20, bold=True)
    window.blit(font2.render(text, True, p.Color('paleturquoise1')), (50, 615, 200, 50))

''' WINDOW MENU FOR AI BUTTOM '''
def AI_menu(window):
    buttom_names = ["Noobie","Normal","Serious","Back"]
    window.blit(bg, (0, 0))
    button_1 = p.Rect(50, 100, 220, 50)  # noob
    button_2 = p.Rect(50, 200, 180, 50)  # medium
    button_3 = p.Rect(50, 300, 300, 50)  # serious
    button_4 = p.Rect(50, 500, 300, 50)  # serious

    # draw btms (bg same as main bg)
    p.draw.rect(window, p.Color('skyblue3'), button_1)
    p.draw.rect(window, p.Color('skyblue3'), button_2)
    p.draw.rect(window, p.Color('skyblue3'), button_3)


    temp_option = copy.deepcopy(arr_options[current_types])

    temp_option.append(2)

    click = False
    while 1:
        window.blit(bg, (0, 0))
        x, y = p.mouse.get_pos()

        # btm names
        window.blit(font.render(buttom_names[0], True, p.Color('aquamarine4')), (50, 100, 200, 50))
        window.blit(font.render(buttom_names[1], True, p.Color('aquamarine4')), (50, 200, 200, 50))
        window.blit(font.render(buttom_names[2], True, p.Color('aquamarine4')), (50, 300, 200, 50))
        window.blit(font.render(buttom_names[3], True, p.Color('aquamarine4')), (50, 500, 200, 50))

        if button_1.collidepoint((x,y)):
            explaition(window, "Easy stuff")
            window.blit(font.render(buttom_names[0], True, p.Color('lawngreen')), (50,100,200,50))
            if click:  temp_option[-1] = 1 ; ai.start_ai(window,temp_option)

        if button_2.collidepoint((x, y)):
            explaition(window, "For normal poeple")
            window.blit(font.render(buttom_names[1], True, p.Color('lawngreen')), (50, 200, 200, 50))
            if click:  temp_option[-1] = 2 ; ai.start_ai(window,temp_option)

        if button_3.collidepoint((x, y)):
            explaition(window, "Serious game, for serious poeple")
            window.blit(font.render(buttom_names[2], True, p.Color('lawngreen')), (50, 300, 200, 50))
            if click:  temp_option[-1] = 3 ; ai.start_ai(window,temp_option)

        if button_4.collidepoint((x, y)):
            explaition(window, "Go back to main menu")
            window.blit(font.render(buttom_names[3], True, p.Color('lawngreen')), (50, 500, 200, 50))
            if click: return

        click = False
        res = mouse_action()
        click = res

        p.display.update()
        clock.tick(60)


''' WINDOW MENU FOR ONLINE BUTTOM '''
def ONLINE_menu(window):
    buttom_names = ["Host game","Join server","Back"]
    window.blit(bg, (0, 0))
    button_1 = p.Rect(50, 100, 200, 50)  # HOST
    button_2 = p.Rect(50, 200, 200, 50)  # JOIN
    button_3 = p.Rect(50, 500, 100, 50)  # Back


    # draw btms (bg same as main bg)
    p.draw.rect(window, p.Color('skyblue3'), button_1)
    p.draw.rect(window, p.Color('skyblue3'), button_2)
    p.draw.rect(window, p.Color('skyblue3'), button_3)

    temp_font = p.font.Font(None,32)

    click = False

    input_rect_host = p.Rect(260, 105, 250, 32)
    input_rect_join = p.Rect(260,205,250,32)

    active_color = p.Color("slategray1")
    passive_color = p.Color("darkslategrey")

    active_host = False
    active_join = False

    color_host = passive_color
    color_join = passive_color

    user_input_join = ''
    user_input_host = ''
    global arr_options,current_types

    temp_option = copy.deepcopy(arr_options[current_types])
    while 1:
        window.blit(bg, (0, 0))
        x, y = p.mouse.get_pos()

        # btm names
        window.blit(font.render(buttom_names[0], True, p.Color('aquamarine4')), (50, 100, 200, 50))
        window.blit(font.render(buttom_names[1], True, p.Color('aquamarine4')), (50, 200, 200, 50))
        window.blit(font.render(buttom_names[2], True, p.Color('aquamarine4')), (50, 500, 200, 50))

        if button_1.collidepoint((x,y)):
            explaition(window, "Enter your ip to create a server")
            window.blit(font.render(buttom_names[0], True, p.Color('lawngreen')), (50,100,200,50))
            if click:  server.start_online(window,user_input_host,temp_option)

        if button_2.collidepoint((x, y)):
            explaition(window, "Enter ip server you want to connect")
            window.blit(font.render(buttom_names[1], True, p.Color('lawngreen')), (50, 200, 200, 50))
            if click:  client.start_online(window,user_input_join,temp_option)


        if button_3.collidepoint((x, y)):
            explaition(window, "Go back to main menu")
            window.blit(font.render(buttom_names[2], True, p.Color('lawngreen')), (50, 500, 200, 50))
            if click: return # return back to manu

        click = False
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                exit()
            if e.type == p.KEYDOWN: # input text
                if active_join:
                    if e.key == p.K_BACKSPACE:
                        user_input_join = user_input_join[:-1]
                    else:
                        if len(user_input_join) < 20:
                            user_input_join += e.unicode
                elif active_host:
                    if e.key == p.K_BACKSPACE: user_input_host = user_input_host[:-1]
                    else:
                        if len(user_input_host) < 20:
                            user_input_host += e.unicode


            if e.type == p.MOUSEBUTTONDOWN:
                if e.button == 1:
                    click =  True
                if input_rect_host.collidepoint(e.pos): active_host = True
                else: active_host = False

                if input_rect_join.collidepoint(e.pos): active_join = True
                else: active_join = False




        if active_join:color_join = active_color
        else: color_join = passive_color

        if active_host:color_host = active_color
        else: color_host = passive_color



        # host
        p.draw.rect(window,color_host,input_rect_host,3)
        text_box = temp_font.render(user_input_host, True, p.Color("magenta4"))
        window.blit(text_box, (input_rect_host.x+5,input_rect_host.y+5))


        # join
        p.draw.rect(window,color_join,input_rect_join,3)
        text_box = temp_font.render(user_input_join, True, p.Color("magenta4"))
        window.blit(text_box, (input_rect_join.x+5,input_rect_join.y+5))


        p.display.update()
        clock.tick(60)






''' WINDOW MENU FOR OPTIONS BUTTOM '''
def OPTIONS_menu(window):
    font3 = p.font.SysFont('arial', 25, bold=True)
    buttom_direction = ["<<<",">>>"]
    window.blit(bg, (0, 0))

    # SOUND
    button_left = p.Rect(120, 10, 40, 30)  # noob
    button_right = p.Rect(230, 10, 40, 30)  # medium
    p.draw.rect(window, p.Color('skyblue3'), button_left)
    p.draw.rect(window, p.Color('skyblue3'), button_right)
    sound_text = 'ON'


    # BOARD COLOR
    button_type_left = p.Rect(380, 50, 40, 30)  # noob
    button_type_right = p.Rect(510, 50, 40, 30)  # medium
    p.draw.rect(window, p.Color('skyblue3'), button_type_left)
    p.draw.rect(window, p.Color('skyblue3'), button_type_right)

    #type_text = 'type 1'
    arr_types = ['1','2','3','4','5','6','7','8']

    board_imgs = []
    for img in range(len(arr_types)):
        board_imgs.append(  p.transform.scale(p.image.load("board_colors/" + arr_types[img] + ".png"),(200,200))  )


    click = False

    button_3 = p.Rect(50, 500, 100, 50)  # Back





    global current_types,sound_on
    while 1:
        window.blit(bg, (0, 0))

        # ALL NAMES HERE
        window.blit(font3.render('SOUND', True, p.Color('darkgreen')), (10, 10, 200, 50))  # SOUND
        window.blit(font3.render('BOARD COLOR', True, p.Color('darkgreen')), (380, 10, 200, 50))  # BOARD COLOR
        p.draw.rect(window, p.Color('skyblue3'), button_3)
        window.blit(font.render('Back', True, p.Color('aquamarine4')), (50, 500, 200, 50))

        x, y = p.mouse.get_pos()

        # btM SOUND
        window.blit(font3.render(buttom_direction[0], True, p.Color('aquamarine4')), (120, 10, 200, 50)) # left button
        window.blit(font3.render(sound_text, True, p.Color('gray')), (175, 10, 200, 50)) # middle text
        window.blit(font3.render(buttom_direction[1], True, p.Color('aquamarine4')), (230, 10, 200, 50)) # right button

        # BOARD COLOR
        window.blit(font3.render(buttom_direction[0], True, p.Color('aquamarine4')), (380, 50, 200, 50))  # left button
        window.blit(font3.render(arr_types[current_types], True, p.Color('gray')), (455, 50, 200, 50))  # middle text
        window.blit(font3.render(buttom_direction[1], True, p.Color('aquamarine4')), (510, 50, 200, 50))  # right button

        # CURRENT BOARD
        window.blit(board_imgs[current_types], p.Rect(370, 100, 200, 200))


        #----------------------------------------------------

        # SOUND
        if button_left.collidepoint((x,y)):
            explaition(window, "off , on")
            window.blit(font3.render(buttom_direction[0], True, p.Color('lawngreen')), (120,10,200,50))
            if click:
                if sound_text != 'OFF':  sound_text='OFF'; sound_on = False



        if button_right.collidepoint((x, y)):
            explaition(window,"off , on")
            window.blit(font3.render(buttom_direction[1], True, p.Color('lawngreen')), (230, 10, 200, 50))
            if click:
                if sound_text == 'OFF': sound_text='ON'; sound_on = True

        if button_3.collidepoint((x, y)):
            explaition(window, "Go back to main menu")
            window.blit(font.render('Back', True, p.Color('lawngreen')), (50, 500, 200, 50))
            if click: return  # return back to manu
        #----------------------------------------------------------------------------------------

        # BOARD COLOR
        if button_type_left.collidepoint((x,y)):
            explaition(window, "8 types of boards")
            window.blit(font3.render(buttom_direction[0], True, p.Color('lawngreen')), (380, 50, 200, 50))
            if click and current_types != 0: current_types-=1


        if button_type_right.collidepoint((x, y)):
            explaition(window, "8 types of boards")
            window.blit(font3.render(buttom_direction[1], True, p.Color('lawngreen')), (510, 50, 200, 50))
            if click and current_types != 7: current_types+=1



        click = False
        res = mouse_action()
        click = res

        p.display.update()
        clock.tick(60)






def mouse_action():
    for e in p.event.get():
        if e.type == p.QUIT:
            p.quit()
            exit()
        if e.type == p.KEYDOWN:
            pass
        if e.type == p.MOUSEBUTTONDOWN:
            if e.button == 1:
                return True
    return False




main_menu()

# board color
# # #COLOR_SQ_1 ,COLOR_SQ_2  'potential_moves:', COLOR_HIGH_1 ,alpha]
# +
# sound


# type 3
# #COLOR_SQ_1 = 'white',COLOR_SQ_2 = '#8B8989',  'potential_moves:' color = p.Color("red") , COLOR_HIGH_1 =["blue","#FFD700"] # type 3

# type 1
# COLOR_SQ_1 = 'snow2' # https://www.webucator.com/blog/2015/03/python-color-constants-module/ for colors
# COLOR_SQ_2 = 'seagreen4'
# COLOR_HIGH_1 =["yellow3","red"] # (selected normal, ignored king check)
# pm = yellow2

# type 2
# COLOR_SQ_1 = 'snow2' # https://www.webucator.com/blog/2015/03/python-color-constants-module/ for colors
# COLOR_SQ_2 = 'saddlebrown'
# COLOR_HIGH_1 =["yellow3","red"] # (selected normal, ignored king check)
#  pm = color = p.Color("royalblue4")

# type 4
# COLOR_SQ_1 = 'snow2' # https://www.webucator.com/blog/2015/03/python-color-constants-module/ for colors
# COLOR_SQ_2 = 'deepskyblue3'
# COLOR_HIGH_1 =["firebrick4","darkgoldenrod1"] # (selected normal, ignored king check)
# pm = color = p.Color("yellow1")

# type 5
# COLOR_SQ_1 = 'snow2' # https://www.webucator.com/blog/2015/03/python-color-constants-module/ for colors
# COLOR_SQ_2 = 'firebrick1'
# COLOR_HIGH_1 =["blue3","aquamarine"] # (selected normal, ignored king check)
# pm = color = p.Color("grey0")


# type 6
#COLOR_SQ_1 = 'snow2' # https://www.webucator.com/blog/2015/03/python-color-constants-module/ for colors
# COLOR_SQ_2 = 'darkorchid3'
# COLOR_HIGH_1 =["cadetblue1","aquamarine"] # (selected normal, ignored king check)
# pm = color = p.Color("black")


# type 7
# COLOR_SQ_1 = 'snow2' # https://www.webucator.com/blog/2015/03/python-color-constants-module/ for colors
# COLOR_SQ_2 = 'grey23'
# COLOR_HIGH_1 =["cadetblue1","red"] # (selected normal, ignored king check)
# pm = lightseagreen

# type 8
# COLOR_SQ_1 = 'white' # https://www.webucator.com/blog/2015/03/python-color-constants-module/ for colors
# COLOR_SQ_2 = 'burlywood4'
# COLOR_HIGH_1 =["cadetblue1","red"] # (selected normal, ignored king check)
# color = p.Color("black")