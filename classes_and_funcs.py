import pygame
pygame.mixer.init()  # 初始化音频系统

class Button:
    def __init__(self, text, position, size = (80, 18), font=r"assets\fonts\simfang.ttf", border_color = (0, 0, 0), background_color = (255, 255, 255)):
        self.text = text
        self.position = position #position 是按钮的坐标，position[0]是x坐标，position[1]是y坐标
        self.size = size
        self.font = font
        self.border_color = border_color
        self.background_color = background_color

    def draw(self, screen):
        # 先绘制背景色矩形
        pygame.draw.rect(screen, self.background_color, (self.position[0], self.position[1], self.size[0], self.size[1]))
        # 再绘制边框
        pygame.draw.rect(screen, self.border_color, (self.position[0], self.position[1], self.size[0], self.size[1]), self.size[1]//10)  # 最后的参数表示边框宽度与按钮宽度之比为1:10，并且取整
        # 绘制文字
        font = pygame.font.Font(self.font, self.size[1] - 4)
        text = font.render(self.text, True, (0, 0, 0))
        screen.blit(text, (self.position[0] + self.size[0] / 2 - text.get_width() / 2, self.position[1] + self.size[1] / 2 - text.get_height() / 2))

    @property
    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # 获取鼠标左键状态
        
        # 检查鼠标是否在按钮范围内
        button_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        if button_rect.collidepoint(mouse_pos):
            # 如果鼠标在按钮上并且刚刚松开（之前是按下状态）
            if not mouse_pressed and hasattr(self, '_is_pressing') and self._is_pressing:
                self._is_pressing = False
                return True
            # 如果鼠标按下，记录按下状态
            elif mouse_pressed:
                self._is_pressing = True
        else:
            # 如果鼠标移出按钮区域，重置按下状态
            self._is_pressing = False
            
        return False

class Font:
    def __init__(self, text, position, size=(80, 18), font=r"assets\fonts\simfang.ttf", color=(0, 0, 0)):
        self.text = text
        self.position = position
        self.size = size
        self.font = font
        self.color = color
        self.current_char = 0  # 当前显示到第几个字符

        self.last_update = pygame.time.get_ticks()  # 上次更新的时间
        # 加载打字声音
        self.type_sound = pygame.mixer.Sound(r"assets\sounds\敲击键盘打字声音.wav")

    def draw(self, screen):
        font = pygame.font.Font(self.font, self.size)
        text = font.render(self.text, True, self.color)
        screen.blit(text, self.position)

    def type(self, screen, text, position, color=(255, 255, 255)):
        font_obj = pygame.font.Font(self.font, 30)
        current_time = pygame.time.get_ticks()
        display_text = text[:self.current_char]
        text_surface = font_obj.render(display_text, True, color)
        text_rect = text_surface.get_rect(center=position)
        # 如果文字已经全部显示完毕
        if self.current_char == len(text):
            if not hasattr(self, 'finish_time'):
                self.finish_time = current_time  # 记录完成时间
            elif current_time - self.finish_time >= 2000:  # 2秒后清除文字
                self.current_char = 0  # 重置字符计数
                del self.finish_time  # 删除完成时间属性
                return True  # 返回True表示完成
        
        # 文字未显示完时，每100毫秒显示一个新字符
        if current_time - self.last_update >= 100:
            self.last_update = current_time
            if self.current_char < len(text):
                self.current_char += 1
                self.type_sound.play()
        
        # 清除之前的文字
        pygame.draw.rect(screen, (0, 0, 0), text_rect)  # 可以根据需要调整背景颜色
        # 直接渲染当前进度的文字
        font_obj = pygame.font.Font(self.font, 30)
        display_text = text[:self.current_char]
        text_surface = font_obj.render(display_text, True, color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)
        
        return False  # 返回False表示未完成

class Player(pygame.sprite.Sprite):
    def __init__(self, image, scale = (32, 65), position = (0, 0), speed = 2):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.speed = speed
    def step(self):
        keys = pygame.key.get_pressed()
        # 检测按键并更新位置
        if keys[pygame.K_w]:  # 按W键向上移动
            self.rect.y -= self.speed
        if keys[pygame.K_s]:  # 按S键向下移动
            self.rect.y += self.speed
        if keys[pygame.K_a]:  # 按A键向左移动
            self.rect.x -= self.speed
        if keys[pygame.K_d]:  # 按D键向右移动
            self.rect.x += self.speed
