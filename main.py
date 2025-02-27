'''
coding:utf-8
author: 瓜子（王嘉诚）
create: 2025-02-01
人工智能主题游戏
'''

import pygame
import classes_and_funcs
import snake
import sys
import random
from time import *


# 初始化 Pygame
pygame.init()

# 设置窗口大小
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
stage = "PRESTART"
# 创建窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 设置窗口标题
pygame.display.set_caption("未来之心")
player = classes_and_funcs.Player(r"assets\images\玩家站立.png")
# 加载背景图片
background_image = pygame.image.load(r"assets\images\标题背景图.png")
# 调整图片大小以适应窗口
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
# 图片加载
start_future = pygame.image.load(r"assets\images\开始未来.jpg")
start_future = pygame.transform.scale(start_future, (WINDOW_WIDTH, WINDOW_HEIGHT))
# 加载标题图片，设置标题图片位置（水平居中，距离顶部75像素），经调整后，字体大小为36，字体位置为(WINDOW_WIDTH // 2 - 80, 75)
title = classes_and_funcs.Font("未来之心", (WINDOW_WIDTH // 2 - 80, 75), 36, r"assets\fonts\STXINWEI.ttf", (13, 102, 171))

# 加载飞机图片
plane_image = pygame.image.load(r"assets\images\标题背景飞机.png")
# 缩放飞机图片到原来的一半大小
plane_image = pygame.transform.scale(plane_image, (plane_image.get_width() // 2, plane_image.get_height() // 2))
plane_rect = plane_image.get_rect()
plane_rect.x, plane_rect.y = WINDOW_WIDTH, 50  # 初始x位置在窗口最右侧，距离顶部100px
plane_speed, plane_speed_y = -0.75, -0.5  # 向左移动的速度，垂直移动的速度
plane_active = False  # 控制飞机是否在移动
last_plane_time = pygame.time.get_ticks()  # 上次飞机出现的时间
plane_delay = 3000  # 初始延迟时间（3秒）

# 创建渐暗效果幕布（以后会有用的）
fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
fade_surface.fill((0, 0, 0))

# 加载并播放背景音乐
pygame.mixer.init()  # 初始化音频混音器
pygame.mixer.music.load(r"assets\sounds\启动背景音乐.mp3")
pygame.mixer.music.play(-1)  # -1表示循环播放

click_sound = pygame.mixer.Sound(r"assets\sounds\按钮点击音效.mp3")
alert_sound = pygame.mixer.Sound(r"assets\sounds\Alert.wav")

# 按钮控件
start_button = classes_and_funcs.Button("开始游戏", (WINDOW_WIDTH // 2 - 200, 300), size = (160, 36), border_color=(13, 163, 171))
printer = classes_and_funcs.Font('', (0, 0), color=(255, 255, 255))  # 游戏打字员，填两个参数应付一下
# 游戏主循环
running = True
text_stage = 'start_1'
fade_alpha = 255  # 初始完全不透明
while running:
    # 处理事件
    for event in pygame.event.get():
        # 如果点击关闭按钮，退出游戏
        if event.type == pygame.QUIT:
            running = False
    
    if stage == "PRESTART":
        # 绘制背景图片
        screen.blit(background_image, (0, 0))
        # 绘制标题图片
        title.draw(screen) # 绘制标题，效果等于screen.blit(title.text, title.position)
        start_button.draw(screen) 
        # 处理飞机逻辑
        current_time = pygame.time.get_ticks()
        
        # 如果飞机不在活动状态，检查是否应该启动新的飞机
        if not plane_active:
            if current_time - last_plane_time > plane_delay:
                plane_active = True
                plane_rect.x = WINDOW_WIDTH
                # 设置新的随机延迟时间（3-7秒）
                plane_delay = random.randint(3000, 7000)
        
        # 如果飞机处于活动状态，更新位置
        else:
            plane_rect.x += plane_speed
            plane_rect.y += plane_speed_y
            # 当飞机完全离开屏幕时
            if plane_rect.right < 0:
                plane_active = False
                last_plane_time = current_time
            screen.blit(plane_image, plane_rect)

        # 处理按钮逻辑
        if start_button.is_clicked:
            # 创建渐暗效果
            pygame.mixer.music.stop()
            click_sound.play()
            for alpha in range(1, 255+1, 2):  # 128步完成渐变
                fade_surface.set_alpha(alpha)
                screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                pygame.time.delay(20)  # 每步延迟20毫秒，总共约2.56秒
            
            stage = "START"  # 确保在渐暗效果后改变游戏状态

    if stage == "START":
        if text_stage == 'start_1':
            if printer.type(screen, "哎呀……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):  # 添加右括号
                text_stage = 'start_2'
        elif text_stage == 'start_2':
            if printer.type(screen, "作业真多……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):
                text_stage = 'start_3'
        elif text_stage == 'start_3':
            if printer.type(screen, "大不了拼了！作业尽管放马过来！", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):
                text_stage = 'start_4'
        elif text_stage == 'start_4':
            if printer.type(screen, "可恶，又是作文。不讲武德……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):
                text_stage = 'start_5'
        elif text_stage == 'start_5':
            if printer.type(screen, "题目叫，额……未来的……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):
                text_stage = 'start_6'
        elif text_stage == 'start_6':
            if printer.type(screen, "ZZZ……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):
                text_stage = 'start_7'
        elif text_stage == 'start_7':
            if printer.type(screen, "……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):
                sleep(2) # 2秒后继续
                text_stage = 'start_8'
        elif text_stage == 'start_8':
            if printer.type(screen, "哦……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):
                text_stage = 'start_9'
        elif text_stage == 'start_9':
            if printer.type(screen, "这是哪里……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)):
                text_stage = 'no_typing_start'
        
        elif text_stage == 'no_typing_start' or text_stage == 'start_10' or text_stage == 'start_11' or text_stage == 'start_12' or text_stage == 'start_13' or text_stage == 'start_14' or text_stage == 'start_15' or text_stage == 'start_16' or text_stage == 'start_17' or text_stage == 'no_typing_start_1':
            screen.blit(start_future, (0, 0))
            if fade_alpha > 0:
                fade_alpha -= 0.1  # 每次循环减少透明度
                fade_surface.set_alpha(fade_alpha)
                screen.blit(fade_surface, (0, 0))
            else:  # 渐明效果完成
                player.rect.x = WINDOW_WIDTH // 4
                player.rect.y = 500  
                if text_stage == 'no_typing_start':
                    text_stage = 'start_10'
                if text_stage == 'start_10':
                    if printer.type(screen, "“Hi你好啊！”", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)):
                        text_stage = 'start_11'       
                elif text_stage =='start_11':
                    if printer.type(screen, "你谁啊啊啊？我不是在写作文的时候睡着了吗！", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)):
                        text_stage = 'start_12'
                elif text_stage == 'start_12':
                    if printer.type(screen, "“我是未来啊！稀客稀客……”", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)):
                        text_stage = 'start_13'
                elif text_stage == 'start_13':
                    if printer.type(screen, "“你问我能干什么吗？虽然我是未来，其实也不能干什么……", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)):
                        text_stage = 'start_14'
                elif text_stage == 'start_14':
                    if printer.type(screen, "主要是作者没更完，这毕竟是alpha版本……四处逛逛吧！”", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)):
                        text_stage = 'start_15'
                elif text_stage == 'start_15':
                    if printer.type(screen, "“现在你在未来的人工智能科技管理中心的入口，我们都在管理现有的人工智能社会协助系统。这里有各种AI模型……”", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)):
                        text_stage = 'start_16'
                elif text_stage == 'start_16':
                    for _ in range(10):
                        pygame.mixer.Sound.play(alert_sound)
                    if printer.type(screen, "“不好，出事了！真是的，我都不能向你介绍了……总之问题严重，模型密钥被盗了！”", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)):
                        text_stage = 'start_17'
                elif text_stage == 'start_17':
                    if printer.type(screen, "“还是作者的问题，你不能和我一起出任务了，你能做的只有帮我们拆除警卫机器人的防火墙！干起来吧！”", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)):
                        text_stage = 'no_typing_start_1'
                elif text_stage == 'no_typing_start_1':
                    snake.snake_game()
                
                
                screen.blit(player.image, player.rect)  
            
            
    # 更新显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()
