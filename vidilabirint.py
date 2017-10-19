from microbit import *
map_blocks = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'\
'w   wggk   m     m    w    d              kw'\
'w g d         m     mkw    w              mw'\
'w s wwwwwdwwwwwwwwwwwww ww wwwwwwwwwdwwwwwww'\
'w m w              wkm     w      kw      mw'\
'w k wk             wkm     d      mw      kw'\
'wwwwwwwwwwwwwwwwdwwwwwwwwwwwwwwdwwwwdwwwwwww'\
'w   w    d  dmkw   k w          gwk        w'\
'w e w  g w  wmkw     d          gwm        w'\
'w   w    w  wwwwwwwwww kwwwwwwwwwwwwwwwwdwww'\
'w   wwwwdw  w   w  mkwwwwkm          gg   mw'\
'wwwdw    wg w g w   m   wwwwmmwwdwwwwwwwwwww'\
'w mmm    w  w   w         gwwww          mkw'\
'w mmm    w  m   d          dmmd          mkw'\
'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
map_width = 44
map_height = 15
map_blocks_cleared = []
num_keys = 0
num_garlic = 0
SENSITIVITY = 200
BLANK = Image('00000:00000:00000:00000:00000:')
KEY = Image('00000:00099:99999:99099:99000:')
DOOR1 = Image('99099:99099:99099:99099:99099:')
DOOR2 = Image('90009:90009:90009:90009:90009:')
ALL_DOORS = [DOOR1, DOOR2, BLANK]
MON = Image('09090:90909:09990:09090:90090:')
MON0 = Image('09990:95949:09990:09090:09090:')
MONSTER = [MON, MON0, BLANK]
MON1 = Image('05050:50505:05550:05050:50050:')
MON2 = Image('03330:31313:03330:03030:03030:')
MONSTEREND = [MON1, MON2, BLANK]
GARLIC = Image('00077:09990:93339:09990:77000:')
def get_map_block(x, y):
    map_x = min(max(x, 0), map_width - 1)
    map_y = min(max(y, 0), map_height - 1)
    block_number = map_x + map_y * map_width
    if not block_number in map_blocks_cleared:
        return map_blocks[block_number]
    else:
        return ' '
def find_start():
    for y in range(map_height):
        for x in range(map_width):
            if get_map_block(x, y) == 's':
                return x, y
    return 0, 0
def show_world(player_x, player_y):
    screen = BLANK.copy()
    for y in range(5):
        map_y = player_y + y - 2
        for x in range(5):
            map_x = player_x + x - 2
            block = get_map_block(map_x, map_y)
            if block == 'w':
                screen.set_pixel(x, y, 4)
            elif block == 'd':
                screen.set_pixel(x, y, 4 if (running_time() % 1000 < 500) else 0)
            elif block == 'm':
                screen.set_pixel(x, y, 6 if (running_time() % 1000 < 100) else 0)
            elif block == 'g':
                screen.set_pixel(x, y, 8 if (running_time() % 1000 < 900) else 0)
            elif block == 'k':
                screen.set_pixel(x, y, 8 if (running_time() % 200 < 100) else 0)
            elif block == 'e':
                screen.set_pixel(x, y, int(running_time() / 50) % 10)
    screen.set_pixel(2, 2, 9)
    display.show(screen)
def show_keys():
    for i in range(3):
        display.show([KEY, str(num_keys)])
def show_garlic():
    for i in range(3):
        display.show([GARLIC, str(num_garlic)])
def show_monster_end():
    display.show(MONSTER)
def show_monter_kill():
    display.show(MONSTEREND)
def show_door_opening():
    display.show(ALL_DOORS)
def monster_at(new_x, new_y):
    global num_garlic
    global map_blocks_cleared
    if num_garlic > 0:
        num_garlic = num_garlic - 1
        map_blocks_cleared.append(new_x + new_y * map_width)
        show_monter_kill()
    else:
        show_monster_end()
        sleep(1000)
        display.scroll("Izgubili ste zivot !!! ", loop=True)
def collect_key_at(x, y):
    global num_keys
    global map_blocks_cleared
    num_keys = num_keys + 1
    map_blocks_cleared.append(x + y * map_width)
    show_keys()
def collect_garlic_at(x, y):
    global num_garlic
    global map_blocks_cleared
    num_garlic = num_garlic + 1
    map_blocks_cleared.append(x + y * map_width)
    show_garlic()
def try_to_open_door_at(x, y):
    global num_keys
    global map_blocks_cleared
    if num_keys > 0:
        num_keys = num_keys - 1
        map_blocks_cleared.append(x + y * map_width)
        show_door_opening()
    else:
        show_keys()
player_x, player_y = find_start()
while button_a.was_pressed() == False:
    display.scroll("VIDILABirint!")
while True:
    if button_a.was_pressed():
        acc_x = accelerometer.get_x()
        acc_y = accelerometer.get_y()
        new_x = player_x
        new_y = player_y
        if abs(acc_x) > abs(acc_y):
            if acc_x < -SENSITIVITY:
                new_x = player_x - 1
            elif acc_x > SENSITIVITY:
                new_x = player_x + 1
        else:
            if acc_y < -SENSITIVITY:
                new_y = player_y - 1
            elif acc_y > SENSITIVITY:
                new_y = player_y + 1
        if new_x != player_x or new_y != player_y:
            block = get_map_block(new_x, new_y)
            if block == 'w':
                pass
            elif block == 'd':
                try_to_open_door_at(new_x, new_y)
                button_a.was_pressed()
            elif block == 'm':
                monster_at(new_x, new_y)
                button_a.was_pressed()                
            elif block == 'k':
                collect_key_at(new_x, new_y)
                button_a.was_pressed() 
            elif block == 'g':
                collect_garlic_at(new_x, new_y)
                button_a.was_pressed()
            elif block == 'e':
                break
            else:
                player_x = new_x
                player_y = new_y
    show_world(player_x, player_y)
show_door_opening()
sleep(1000)
display.scroll("Sjajno! Pobjegli ste iz VIDILABirinta!", loop=True)