from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, RoundedRectangle, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
import random

Window.size = (1080, 2052)

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.food_size = Window.width/20
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.current_color = None
        self.last_direction = None
        self.eat_new = None
        self.all_snake = []
        self.snake_positions = []
        
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.background = Rectangle(pos = (0, 0), size = (1080, 2052))        
        with self.canvas:
            Color(1, 1, 1, 1)
            self.first_block = RoundedRectangle(
                pos = (Window.width/2, Window.height/2),
                size = (self.food_size, self.food_size), radius = [6])
            Color(0, 0, 0, 1)
            self.eye1 = Ellipse(pos = (self.first_block.pos[0] + self.food_size*1/5, self.first_block.pos[1] + self.food_size*4/5), size = (6, 6))
            self.eye2 = Ellipse(pos = (self.first_block.pos[0] + self.food_size*2/3, self.first_block.pos[1] + self.food_size*4/5), size = (6, 6))
            self.current_color = [random.random(), random.random(), random.random(), 1]
            Color(rgba = self.current_color, group = "food") # группа для отдельного изменения цвета
            x = self.food_size * (random.randint(0, int(Window.width))//self.food_size)
            y = self.food_size * (random.randint(0, int(Window.height))//self.food_size)
            self.food = Ellipse(pos = (x, y), size = (self.food_size, self.food_size))
        with self.canvas.after:
            self.score_label = Label(pos = (30, 1900), text = str(self.score), font_size = 100, color = (0.12, 0.7, 0.7, 1))
            self.pause_label = Label(pos = (500, 1500), text = "", font_size = 100, color = (0.12, 0.7, 0.7, 1))
            self.pause_image = Image(source = "pause.png", pos = (920, 1885), size = (130, 130))
        self.pause_button = Button(pos = (870, 1850), size = (200, 200), text = "||", font_size = 60, on_press = self.pause, color = (0, 0, 0, 0), background_color = (0, 0, 0, 0))
        self.add_widget(self.pause_button)        
               
        self.all_snake.append(self.first_block)
        self.snake_positions.append(self.first_block.pos)
        
    def on_touch_down(self, touch):
        self.start_x, self.start_y = touch.x, touch.y
        return super().on_touch_down(touch)
        
    def on_touch_up(self, touch):
        self.end_x, self.end_y = touch.x, touch.y
        self.control()
     # управление змейкой
    def control(self):
        if self.start_x < self.end_x and abs(self.start_y - self.end_y) < self.end_x - self.start_x:
            Clock.schedule_interval(self.right, 1/5)
        elif self.start_x > self.end_x and abs(self.start_y - self.end_y) < self.start_x - self.end_x:
            Clock.schedule_interval(self.left, 1/5)
        elif self.start_y < self.end_y and abs(self.start_x - self.end_x) < self.end_y - self.start_y:
            Clock.schedule_interval(self.up, 1/5)
        elif self.start_y > self.end_y and abs(self.start_x - self.end_x) < self.start_y - self.end_y:
            Clock.schedule_interval(self.down, 1/5)
                         
    # движение змейки        
    def update_field(self, dx, dy, e1_x, e1_y, e2_x, e2_y):
        x, y = self.first_block.pos
        x += dx
        y += dy
        if self.eat_new == True:
            self.first_block.pos = (x, y)
            self.eye1.pos = self.first_block.pos[0] + self.food_size*e1_x, self.first_block.pos[1] + self.food_size*e1_y
            self.eye2.pos = self.first_block.pos[0] + self.food_size*e2_x, self.first_block.pos[1] + self.food_size*e2_y
            self.eat_new = False
        else:
            for element in reversed(self.all_snake[1:]):
                x1, y1 = self.all_snake[self.all_snake.index(element) - 1].pos
                element.pos = (x1, y1)
            
            self.first_block.pos = (x, y)
            self.snake_positions.pop()
            self.snake_positions.insert(0, self.first_block.pos)    
            self.eye1.pos = self.first_block.pos[0] + self.food_size*e1_x, self.first_block.pos[1] + self.food_size*e1_y
            self.eye2.pos = self.first_block.pos[0] + self.food_size*e2_x, self.first_block.pos[1] + self.food_size*e2_y
        self.eat_food()
        self.wall_hit()
        self.hit_yourself()
        
    # проверка, съел ли еду    
    def eat_food(self):
        if abs(self.first_block.pos[0] - self.food.pos[0]) < self.food_size and abs(self.first_block.pos[1] - self.food.pos[1]) < self.food_size:
            self.score += 1
            self.score_label.text = str(self.score)
            self.new_element()
            self.draw_food()
    
        # появление еды в случайном месте
    def draw_food(self):
        self.current_color = (random.random(), random.random(), random.random(), 1)
        self.canvas.get_group("food")[0].rgba = self.current_color
        x = self.food_size * (random.randint(0, int(Window.width))//self.food_size)
        y = self.food_size * (random.randint(0, int(Window.height))//self.food_size)
        while (x, y) in self.snake_positions:
            x = self.food_size * (random.randint(0, int(Window.width))//self.food_size)
            y = self.food_size * (random.randint(0, int(Window.height))//self.food_size)
        self.food.pos = (x, y)
    
        # добавление нового элемента к змейке        
    def new_element(self):
        with self.canvas.before:
            Color(rgba = self.current_color)
            new = RoundedRectangle(
                size = (self.food_size, self.food_size),
                radius = [6])
        if len(self.all_snake) == 1:
            if self.last_direction == "right":
                new.pos = (self.all_snake[-1].pos[0] - self.food_size, self.all_snake[-1].pos[1])
            elif self.last_direction == "left":
                new.pos = (self.all_snake[-1].pos[0] + self.food_size, self.all_snake[-1].pos[1])
            elif self.last_direction == "up":
                new.pos = (self.all_snake[-1].pos[0], self.all_snake[-1].pos[1] - self.food_size)
            elif self.last_direction == "down":
                new.pos = (self.all_snake[-1].pos[0], self.all_snake[-1].pos[1] + self.food_size)                       
        else:
            self.eat_new = True
            new.pos = self.first_block.pos

        self.all_snake.insert(1, new)      
        self.snake_positions.insert(1, new.pos)

     # удар об стену       
    def wall_hit(self):
        x, y = self.first_block.pos
        if x < 0 or x > (Window.width - self.food_size) or y < 0 or y > (Window.height - self.food_size):
            self.game_over()
            
      # удар об себя      
    def hit_yourself(self):
        x, y = self.first_block.pos
        if (x, y) in self.snake_positions[2:]:
            self.game_over()

    # поворот направо
    def right(self, dt):
        Clock.unschedule(self.left)
        if (self.dx == 0 and self.dy == 0) or (self.dx == 0 and self.dy == self.food_size):
            Clock.unschedule(self.up)
            self.dx, self.dy = self.food_size, 0
        elif self.dx == 0 and self.dy == -self.food_size:
            Clock.unschedule(self.down)
            self.dx, self.dy = self.food_size, 0
        self.last_direction = "right"
        e1_x, e1_y, e2_x, e2_y = 4/5, 2/3, 4/5, 1/5
        self.update_field(self.dx, self.dy, e1_x, e1_y, e2_x, e2_y)
    
    # поворот налево     
    def left(self, dt):
        Clock.unschedule(self.right)
        if (self.dx == 0 and self.dy == 0) or (self.dx == 0 and self.dy == self.food_size):
            Clock.unschedule(self.up)
            self.dx, self.dy = -self.food_size, 0
        elif self.dx == 0 and self.dy == -self.food_size:
            Clock.unschedule(self.down)
            self.dx, self.dy = -self.food_size, 0
        self.last_direction = "left"
        e1_x, e1_y, e2_x, e2_y = 1/15, 1/5, 1/15, 2/3
        self.update_field(self.dx, self.dy, e1_x, e1_y, e2_x, e2_y)
        
    # поворот вверх
    def up(self, dt):
        Clock.unschedule(self.down)
        if (self.dx == 0 and self.dy == 0) or (self.dx == self.food_size and self.dy == 0):
            Clock.unschedule(self.right)
            self.dx, self.dy = 0, self.food_size
        elif self.dx == -self.food_size and self.dy == 0:
            Clock.unschedule(self.left)
            self.dx, self.dy = 0, self.food_size
        self.last_direction = "up"
        e1_x, e1_y, e2_x, e2_y = 1/5, 4/5, 2/3, 4/5
        self.update_field(self.dx, self.dy, e1_x, e1_y, e2_x, e2_y)
        
    # поворот вниз
    def down(self, dt):
        Clock.unschedule(self.up)
        if (self.dx == 0 and self.dy == 0) or (self.dx == self.food_size and self.dy == 0):
            Clock.unschedule(self.right)
            self.dx, self.dy = 0, -self.food_size
        elif self.dx == -self.food_size and self.dy == 0:
            Clock.unschedule(self.left)
            self.dx, self.dy = 0, -self.food_size
        self.last_direction = "down"
        e1_x, e1_y, e2_x, e2_y = 1/5, 1/15, 2/3, 1/15
        self.update_field(self.dx, self.dy, e1_x, e1_y, e2_x, e2_y)
     
     # постановка и снятие с паузы
    def pause(self, instance):
        if self.pause_button.text == "||":
            Clock.unschedule(self.right)
            Clock.unschedule(self.left)
            Clock.unschedule(self.up)
            Clock.unschedule(self.down)
            self.pause_label.text = "PAUSE"
            self.pause_button.text = "->"
            self.pause_image.source = "play.png"
        elif self.pause_button.text == "->":
            self.pause_button.text = "||"        
            self.pause_label.text = ""
            self.pause_image.source = "pause.png"
        
    # конец игры   
    def game_over(self, *args):
        Clock.unschedule(self.right)
        Clock.unschedule(self.left)
        Clock.unschedule(self.up)
        Clock.unschedule(self.down)
        self.layout = GridLayout(cols = 1, spacing = 6)
        self.total = Label(text = f"YOUR SCORE - {self.score}", font_size = 40)
        self.restart_button = Button(text = "RESTART", on_press = self.restart)
        self.saveform_button = Button(text = "SAVE THE RESULT", on_press = self.saveform)
        self.leaders_button = Button(text = "BEST RESULTS", on_press = self.leaders)
        self.layout.add_widget(self.total)
        self.layout.add_widget(self.restart_button)
        self.layout.add_widget(self.saveform_button)
        self.layout.add_widget(self.leaders_button)
        self.popup = Popup(title = "GAME OVER!", title_color = (0.7, 0.28, 0.28, 1), title_align = "center", title_size = 60, separator_height = 0, content = self.layout, pos = (300, 1100), auto_dismiss = False, size_hint = (None, None), size = (500, 600))
        self.popup.open()
        
    def restart(self, *args):
        self.popup.dismiss()
        self.canvas.clear()
        self.canvas.before.clear()
        self.canvas.after.clear()
        self.__init__()
        
       # открытие формы сохранения результата
    def saveform(self, *args):
        self.total.text = "ENTER YOUR NAME"
        self.name_input = TextInput(font_size = 60, multiline = False)
        self.save_button = Button(text = "SAVE", on_press = self.save)
        self.layout.remove_widget(self.restart_button)
        self.layout.remove_widget(self.saveform_button)
        self.layout.remove_widget(self.leaders_button)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.save_button)
        self.popup.size = (500, 500)
     
       # сохранение результата в файл   
    def save(self, *args):
        if self.name_input.text == "":
            self.layout.remove_widget(self.name_input)
            self.layout.remove_widget(self.save_button)
            self.saveform()
        else:
            with open('leaders.txt', 'a') as leaders_file:
                leaders_file.write(f"{self.score} - {self.name_input.text}\n")
            with open('leaders.txt', 'r') as leaders_file:
                lines = [line.strip() for line in leaders_file]
            tops = sorted(lines, key = lambda s: int(s.split(" - ")[0]), reverse = True)
            with open('leaders.txt', 'w') as leaders_file:
                for  line in tops:
                    leaders_file.write(line + '\n')
            self.game_over()
      
        # вывод топ 10 лучших результатов  
    def leaders(self, *args):
        self.popup.title = "TOP - 10\n\n"
        self.popup.title_align = "left"
        self.popup.title_size = 45
        self.popup.size = (500, 900)
        self.layout.remove_widget(self.total)
        self.layout.remove_widget(self.restart_button)
        self.layout.remove_widget(self.saveform_button)
        self.layout.remove_widget(self.leaders_button)
        with open('leaders.txt', 'r') as leaders_file:
            lines = [line.strip() for line in leaders_file]
        for line in lines[0: 10]:
            self.popup.title += f"{line}\n"
        self.close_button = Button(text = "CLOSE", on_press = self.close_top)
        self.layout.add_widget(self.close_button)

    def close_top(self, *args):
        self.popup.dismiss()
        self.game_over()

class SnakeApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        return MyWidget()

if __name__ == "__main__":
    SnakeApp().run()