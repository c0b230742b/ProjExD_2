import os
import sys
import time
import random
import pygame as pg


WIDTH, HEIGHT = 1200, 750
move_dict = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
    }

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数；こうかとんRectまたは爆弾Rect
    戻り値：真理値タプル (横方向、縦方向)
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            screen.blit(bg_img, [0, 0]) #画面の初期化

            back_rect = pg.Surface((WIDTH, HEIGHT))
            pg.draw.rect(back_rect, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
            back_rect.set_alpha(50) #透明度の変更
            screen.blit(back_rect, [0, 0])
            pg.display.update()
           
            fonto = pg.font.Font(None, 80)
            txt_go = fonto.render("GameOver", True, (255, 0, 0))
            rct =txt_go.get_rect()
            rct.center = WIDTH/2,HEIGHT/2
            
            screen.blit(txt_go, rct)
            pg.display.update()

            crykk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0) 
            screen.blit(crykk_img, [300, HEIGHT/2-40])
            screen.blit(crykk_img, [900, HEIGHT/2-40])
            pg.display.update()

            
            
            time.sleep(5)
            return 
            
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in move_dict.items():
            if key_lst[k]: #pg.k_left, pg.k_rightなどのぶぶん
                sum_mv[0] +=v[0]
                sum_mv[1] += v[1] 
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
