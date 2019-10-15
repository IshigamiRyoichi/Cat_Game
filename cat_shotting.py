from random import randint
import pyxel

#ウィンドウと自機のサイズ設定
WINDOW_H = 120
WINDOW_W = 160
SHIP_H = 16
SHIP_W = 16


#変数の定義とリストの管理
class APP:

    def __init__(self):
        self.IMG_ID0 = 0
        self.IMG_ID1 = 1
        self.IMG_ID2 = 2
        self.IMG_ID0_X = 60
        self.IMG_ID0_Y = 65
        self.game_over = False
        self.game_end = False
        self.boss_flug = False
        self.boss_count = 1
        self.score = 0
        self.shots = []
        self.enemys = []
        self.boss_hp = 500
        self.bombs = []
        self.p_ship = Ship()
        self.state = 0
    

        #メインウィンドウの作成
        pyxel.init(WINDOW_W, WINDOW_H, caption="Cat Shotting Game!")
        # ドット絵を読み込む
        pyxel.image(self.IMG_ID0).load(0, 0, "assets/cat_16x16.png")
        pyxel.image(self.IMG_ID1).load(0, 0, "assets/pyxel_logo_38x16.png")
        pyxel.image(self.IMG_ID2).load(0, 0, "assets/pyxel_logo_152x64.png")

        pyxel.mouse(False)
      
        pyxel.run(self.update, self.draw)#位置情報の更新と描画
    def input_key(self):
        if pyxel.btnp(pyxel.KEY_S):
            self.state = 1

    def update(self):
        self.input_key()
        
        if self.state == 0:
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()

        else: 
            #Ｑを押せばゲーム終了 
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()

            #自機の更新
            if self.game_over == False:
                self.p_ship.update(pyxel.mouse_x, pyxel.mouse_y)

                #弾の処理
            shot_count = len(self.shots)
            for j in range (shot_count):
                if self.shots[j].pos_y > 20:
                    self.shots[j].pos_y = self.shots[j].pos_y - 3
                else:
                    del self.shots[j]
                    break

                #弾の処理
                shot_hit = len(self.shots)
                for h in range (shot_hit):
                    enemy_hit = len(self.enemys)
                    for e in range (enemy_hit):
                        if ((self.enemys[e].ene_x <= self.shots[h].pos_x 
                            <= self.enemys[e].ene_x + 20)and(self.enemys[e].ene_y 
                            <= self.shots[h].pos_y <= self.enemys[e].ene_y + 20)):
                            #敵に当たったらその座標に爆発を乗せる
                            new_bomb = Bomb(self.enemys[e].ene_x, 
                                            self.enemys[e].ene_y)
                            self.bombs.append(new_bomb)
                            del self.enemys[e]
                            if self.boss_flug == False:
                                self.score = self.score + 100
                            break#敵に当たったらbreak
                    else:
                        continue
                    break#敵に当たったらbreak

            enemy_atk = len(self.enemys)
            for e in range (enemy_atk):
                if (((self.enemys[e].ene_x >= self.p_ship.ship_x) and
                    (self.enemys[e].ene_x <= self.p_ship.ship_x + 15) and
                    (self.enemys[e].ene_y >= self.p_ship.ship_y) and
                    (self.enemys[e].ene_y <= self.p_ship.ship_y + 15))or
                    ((self.enemys[e].ene_x + 15 >= self.p_ship.ship_x) and
                    (self.enemys[e].ene_x + 15 <= self.p_ship.ship_x + 15) and
                    (self.enemys[e].ene_y + 15 >= self.p_ship.ship_y) and
                    (self.enemys[e].ene_y + 15 <= self.p_ship.ship_y + 15))):
                    self.game_over = True
                    new_bomb = Bomb(self.p_ship.ship_x, self.p_ship.ship_y)  
                    self.bombs.append(new_bomb)

                #敵の更新
                #敵として出現
            if self.game_end == False:
                if self.boss_flug == False:
                    if pyxel.frame_count % 20 == 0:
                        new_enemy = Enemy()
                        self.enemys.append(new_enemy)
            #ボスの弾として出現
                else:
                    if pyxel.frame_count % 8 == 0:
                        new_enemy = Enemy()
                        self.enemys.append(new_enemy)
            
            enemy_count = len(self.enemys)
            for e in range (enemy_count):
                enemy_vec1 = randint(0, 7)
                enemy_vec2 = enemy_vec1 % 2
                if self.enemys[e].ene_y < 115:
                    if enemy_vec2 > 0:
                        self.enemys[e].ene_x = self.enemys[e].ene_x + 4
                        self.enemys[e].ene_y = self.enemys[e].ene_y + 1.5
                    else:
                        self.enemys[e].ene_x = self.enemys[e].ene_x - 4
                        self.enemys[e].ene_y = self.enemys[e].ene_y + 1.5
                    
                else:
                    del self.enemys[e]
                    break

            #画面の爆発が3以上になったら古いものから消していく
            if len(self.bombs) > 3:
                del self.bombs[0] 

                #ボスを出現させる
            if self.boss_flug == False: #ボス未出現の状態で
                if self.score != 0:     #ゲーム開始直後ではなく
                    if self.score % 2000 == 0: #スコアxxxx点に達したら
                        if self.game_end == False: #ゲームクリアフラグがない場合にボス発生
                            self.boss_flug = True
                            self.boss_hp = 300 * self.boss_count#ボスのHP設定

            if self.boss_flug == True:        
                shot_hit = len(self.shots)        
                for h in range (shot_hit):
                    if ((40 <= self.shots[h].pos_x <= 110)and
                        (10 <= self.shots[h].pos_y <= 20)):
                        self.boss_hp = self.boss_hp - 2
                        new_bomb = Bomb(self.shots[h].pos_x, self.shots[h].pos_y)
                        self.bombs.append(new_bomb) 
                    
                #ボスが倒れた場合
                if self.boss_hp <= 0:
                    if self.boss_flug == True:
                        self.score = self.score + 5000#スコアが＋5000
                        pyxel.cls(0)
                        self.boss_flug = False
                        #ボスのtア押した回数を数える
                        self.boss_count = self.boss_count + 1
                        if self.boss_count == 6:
                            self.game_end = True
            
    #resetの設定
    def reset(self):
        self.game_start = False
        self.game_over = False
        self.game_end = False
        self.boss_flug = False
        self.boss_count = 1
        self.score = 0
        self.shots = []
        self.enemys = []
        self.boss_hp = 500
        self.bombs = []
        self.p_ship = Ship()

        pyxel.playm(0, loop=True)

    #描画
    def draw(self):
        pyxel.cls(0)
        self.input_key()
        if self.state == 0:
            pyxel.text(55, 30, "Cat Shotting!", pyxel.frame_count % 16)
            pyxel.text(45, 45, "Press 'S' to start", 8)
            pyxel.blt(self.IMG_ID0_X,self.IMG_ID0_Y,self.IMG_ID1,0,0,38,16)
            self.cat()

        else:
            #得点描写
            pyxel.text(1, 2, "score:" + str(self.score), 9)
            pyxel.text(120, 2, "boss:" + str(self.boss_hp), 9)
            
            #自機の描画
            pyxel.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 0, 0, 
                    -SHIP_W, SHIP_H, 5)

            #弾の発射
            if self.game_over == False:
                if pyxel.btn(pyxel.KEY_SPACE):
                    if len(self.shots) < 11:
                #make shot instance
                        new_shot = Shot()
                        new_shot.update(self.p_ship.ship_x, self.p_ship.ship_y, 8)
                        self.shots.append(new_shot)
            
            #弾の描画
            for i in self.shots:
                pyxel.rect(i.pos_x+7, i.pos_y-3, 7, 7, 12)

            #敵の描画
            for i in self.enemys:
                if self.boss_flug == False:
                    enemy_flug = randint(0, 7)
                    if enemy_flug % 2 == 0:
                        pyxel.blt(i.ene_x, i.ene_y, 1, 0, 0, -SHIP_W, SHIP_H, 5)
                    else:
                        pyxel.blt(i.ene_x, i.ene_y, 1, 16, 0, -SHIP_W, SHIP_H, 5)
                else:
                    enemy_flug = randint(0, 7)
                    if enemy_flug % 2 == 0:
                        pyxel.blt(i.ene_x, i.ene_y, 1, 0, 4, -SHIP_W, SHIP_H, 5)
                    else:
                        pyxel.blt(i.ene_x, i.ene_y, 1, 16, 4, -SHIP_W, SHIP_H, 5)
            #ボスの描画
            if self.boss_flug == True:
                pyxel.blt(50, 2, 2, 0, 0, 65, 60, 0)
                
            #爆発の描写
            for i in self.bombs:
                pyxel.circ(i.bomb_x, i.bomb_y, 7, 9)
                pyxel.circ(i.bomb_x, i.bomb_y, 5, 8)
                pyxel.circ(i.bomb_x, i.bomb_y, 2, 10)

            #ゲームオーバー
            if self.game_over:
                pyxel.text(60, 30, "Game Over!", pyxel.frame_count % 16)
                pyxel.text(45, 45, "'R' is rest's botm", 12)
                pyxel.text(45, 60, "'Q' is finish's botm", 12)
            
            #ゲームクリア
            if self.game_end:
                pyxel.text(60, 30, "Completed!", pyxel.frame_count % 16)
                pyxel.text(45, 45, "'R' is rest's botm", 12)
                pyxel.text(45, 60, "'Q' is finish's botm", 12)

#オブジェクトのクラス
    def cat(self):
            x = pyxel.mouse_x
            y = pyxel.mouse_y

            if pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
                pyxel.blt(x,y,self.IMG_ID0,0,0,-SHIP_W,SHIP_H,5)
            else:
                pyxel.blt(x,y,self.IMG_ID0,0,0,SHIP_W,SHIP_H,5)

class Ship:   
    def __init__(self):
        self.ship_x = 0
        self.ship_y = 0
  
    def update(self, x, y):
        self.ship_x = x
        self.ship_y = y
class Shot:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.color = 8 # 0~15
    def update(self, x, y, color):
        self.pos_x = x
        self.pos_y = y
        self.color = color
      
class Enemy:
    def __init__(self):
        self.ene_x = randint(30, 125)
        self.ene_y = 5
  
    def update(self, x, y):
        self.ene_x = x
        self.ene_y = y
class Bomb:
    def __init__(self, x, y):
        self.bomb_x = x
        self.bomb_y = y       
                  
APP()