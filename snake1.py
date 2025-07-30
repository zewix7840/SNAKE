import pygame
import random
import os

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_blue = (0, 0, 128)
light_blue = (0, 100, 200)

dis_width = 900
dis_height = 500

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by ZёWix')

clock = pygame.time.Clock()

snake_block = 20
initial_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

save_dir = os.path.expanduser("~/.snake_game_scores")
os.makedirs(save_dir, exist_ok=True)

language_choice = "English"  

def get_translation(text):
    translations = {
        "Pause menu": {
            "English": "Pause menu",
            "Русский": "Меню паузы",
            "Turkmen": "Toxtamak menyusy"
        },
        "Continue": {
            "English": "Continue",
            "Русский": "Продолжить",
            "Turkmen": "Dowam etmek"
        },
        "Save Score": {
            "English": "Save Score",
            "Русский": "Сохранить счет",
            "Turkmen": "Bahasy saklamak"
        },
        "Main Menu": {
            "English": "Main Menu",
            "Русский": "Главное меню",
            "Turkmen": "Esasy menyu"
        },
        "Quit": {
            "English": "Quit",
            "Русский": "Выйти",
            "Turkmen": "Çykmak"
        },
        "Your Score:": {
            "English": "Your Score:",
            "Русский": "Ваш счет:",
            "Turkmen": "Siziň Bahasyňyz:"
        },
        "Lives left:": {
            "English": "Lives left:",
            "Русский": "Осталось жизней:",
            "Turkmen": "Galýan durmuşlar:"
        },
        "Press C to Continue": {
            "English": "Press C to Continue",
            "Русский": "Нажмите C, чтобы продолжить",
            "Turkmen": "Dowam etmek üçin C basyň"
        },
        "You Lost! Press C-Play Again or Q-Quit": {
            "English": "You Lost! Press C-Play Again or Q-Quit",
            "Русский": "Вы проиграли! Нажмите C - сыграть снова или Q - выйти",
            "Turkmen": "Jüpüntiňiz! Yzyna başlamak üçin C ýa-da çykmak üçin Q basyň"
        },
        "Previous score detected.": {
            "English": "Previous score detected.",
            "Русский": "Обнаружен предыдущий счет.",
            "Turkmen": "Öňki baha tapyldy."
        },
        "Do you want to continue or start new?": {
            "English": "Do you want to continue or start new?",
            "Русский": "Хотите продолжить или начать заново?",
            "Turkmen": "Dowam etmek isleýärsiňizmi ýa-da täzeden başlamak?"
        },
        "New Game": {
            "English": "New Game",
            "Русский": "Новая игра",
            "Turkmen": "Täze Oýun"
        },
        "Resume": {
            "English": "Resume",
            "Русский": "Продолжить",
            "Turkmen": "Dowam etmek"
        },
        "Infinite Mode": {
            "English": "Infinite Mode",
            "Русский": "Бесконечный режим",
            "Turkmen": "Çäksiz Rejim"
        },
        "Lives Mode": {
            "English": "Lives Mode",
            "Русский": "Режим жизней",
            "Turkmen": "Durmuş Rejimi"
        },
        "Settings": {
            "English": "Settings",
            "Русский": "Настройки",
            "Turkmen": "Sazlamalar"
        },
        "Apply Settings": {
            "English": "Apply Settings",
            "Русский": "Применить настройки",
            "Turkmen": "Sazlamalary Ulanyñ"
        },
        "Back": {
            "English": "Back",
            "Русский": "Назад",
            "Turkmen": "Yza"
        },
        "Speed: Slow": {
            "English": "Speed: Slow",
            "Русский": "Скорость: Медленно",
            "Turkmen": "Tizlik: Haýal"
        },
        "Speed: Medium": {
            "English": "Speed: Medium",
            "Русский": "Скорость: Средняя",
            "Turkmen": "Tizlik: Ortaça"
        },
        "Speed: Fast": {
            "English": "Speed: Fast",
            "Русский": "Скорость: Быстро",
            "Turkmen": "Tizlik: Çalt"
        }
    }

    if text in translations:
        return translations[text].get(language_choice, text)

    return text

snake_List = []
Length_of_snake = 1

foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

def get_save_file_path(mode):
    return os.path.join(save_dir, f"{mode}_score.txt")

def get_lives_file_path():
    return os.path.join(save_dir, "lives.txt")

def draw_heart(surface, x, y):
    heart_shape = [
        "  XX  XX  ",
        " XXXXXXXX ",
        "XXXXXXXXXX",
        " XXXXXXXX ",
        "  XXXXXX  ",
        "   XXXX   ",
        "    XX    "
    ]
    for row_index, row in enumerate(heart_shape):
        for col_index, pixel in enumerate(row):
            if pixel == 'X':
                pygame.draw.rect(surface, red, (x + col_index * 2, y + row_index * 2, 2, 2))

def draw_hearts(lives):
    for i in range(lives):
        draw_heart(dis, dis_width - (i + 1) * 22, 10)

def Your_score(score):
    value = score_font.render(get_translation("Your Score:") + str(score), True, yellow)
    dis.blit(value, [10, 10])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, position):
    translated_msg = get_translation(msg)
    mesg = font_style.render(translated_msg, True, color)
    mesg_rect = mesg.get_rect(center=position)
    dis.blit(mesg, mesg_rect)

def draw_button(text, color, rect, pressed=False):
    wrapped_text = wrap_text(get_translation(text), rect.width - 10)
    darker_color = tuple(max(0, c - 50) for c in color)
    draw_color = darker_color if pressed else color
    pygame.draw.rect(dis, draw_color, rect)
    pygame.draw.rect(dis, black, rect, 2)

    total_text_height = len(wrapped_text) * font_style.get_height()
    starting_y = rect.top + (rect.height - total_text_height) // 2

    for i, line in enumerate(wrapped_text):
        text_surface = font_style.render(line, True, white)
        text_rect = text_surface.get_rect(center=(rect.centerx, starting_y + i * font_style.get_height()))
        dis.blit(text_surface, text_rect)

def wrap_text(text, max_width):
    words = text.split()
    lines, current_line = [], []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font_style.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if not current_line:
                return [word[:max_width // font_style.size(word[0])[0]]]  
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def handle_button_click(event, buttons):
    """ Проверка нажатия кнопок с анимацией """
    if not buttons:
        return  

    for button, callback in buttons:
        if event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
            draw_button("Button", light_blue, button, pressed=True)
            pygame.display.update()  
            pygame.time.delay(150)  

        if event.type == pygame.MOUSEBUTTONUP and button.collidepoint(event.pos):
            draw_button("Button", light_blue, button, pressed=False)  
            pygame.display.update()  
            if callback:
                callback()


buttons = [
    (pygame.Rect(100, 100, 200, 50), lambda: print("Button 1 clicked")),
    (pygame.Rect(100, 200, 200, 50), lambda: print("Button 2 clicked"))
]


def main_game_loop():
    running = True
    speed_texts = ["Slow", "Medium", "Fast"]
    current_speed = 1  

    while running:
        dis.fill((30, 30, 30))  

        current_speed = max(1, min(current_speed, len(speed_texts)))
        speed_text = speed_texts[current_speed - 1]  

        print(f"Current speed: {current_speed} ({speed_text})")

        for button, _ in buttons:
            draw_button("Button", light_blue, button)

        pygame.display.update()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_button_click(event, buttons)  

    pygame.quit()

def save_score(score, mode):
    with open(get_save_file_path(mode), "w") as file:
        file.write(str(score))

def load_score(mode):
    try:
        with open(get_save_file_path(mode), "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_lives(lives):
    with open(get_lives_file_path(), "w") as file:
        file.write(str(lives))

def load_lives():
    try:
        with open(get_lives_file_path(), "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 3

def set_language(language):
    global language_choice
    language_choice = language

def set_speed(speed):
    global initial_speed
    if 1 <= speed <= 3:
        initial_speed = [10, 15, 20][speed - 1]
    else:
        print(f"Invalid speed value: {speed}. Expected 1, 2, or 3.")

if len(snake_List) > Length_of_snake:
    snake_List = snake_List[-Length_of_snake:]

foodx = max(0, min(dis_width - snake_block, foodx))
foody = max(0, min(dis_height - snake_block, foody))

def pause_menu(score, mode):
    paused = True
    while paused:
        dis.fill(dark_blue)

        center_x = dis_width / 2
        center_y = dis_height / 2

        message("Pause menu", yellow, (dis_width / 2, 30))

        resume_button = pygame.Rect(center_x - 100, center_y - 120, 200, 50)
        save_score_button = pygame.Rect(center_x - 100, center_y - 60, 200, 50)
        main_menu_button = pygame.Rect(center_x - 100, center_y, 200, 50)
        quit_button = pygame.Rect(center_x - 100, center_y + 60, 200, 50)

        draw_button("Resume", light_blue, resume_button)
        draw_button("Save Score", light_blue, save_score_button)
        draw_button("Main Menu", light_blue, main_menu_button)
        draw_button("Quit", light_blue, quit_button)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    paused = False
                elif save_score_button.collidepoint(event.pos):
                    save_score(score, mode)
                elif main_menu_button.collidepoint(event.pos):
                    main_menu()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

def gameLoop(mode):
    set_language(language_choice)
    set_speed(initial_speed)
    saved_score = load_score(mode)
    lives = load_lives() if mode == "lives" else None

    if saved_score > 0:
        choice_made = False
        while not choice_made:
            dis.fill(dark_blue)
            message("Previous score detected.", yellow, (dis_width / 2, dis_height / 3))
            message("Do you want to continue or start new?", white, (dis_width / 2, dis_height / 3 + 40))

            continue_button = pygame.Rect(dis_width / 2 - 150, dis_height / 2 - 30, 140, 50)
            new_game_button = pygame.Rect(dis_width / 2 + 10, dis_height / 2 - 30, 140, 50)

            draw_button("Continue", light_blue, continue_button)
            draw_button("New Game", light_blue, new_game_button)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        score = saved_score
                        choice_made = True
                    elif new_game_button.collidepoint(event.pos):
                        score = 0
                        lives = 3 if mode == "lives" else None
                        choice_made = True
    else:
        score = 0

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    snake_speed = initial_speed

    while not game_over:

        while game_close:
            dis.fill(blue)
            if mode == "lives" and lives > 0:
                message(f"Lives left: {lives}", yellow, (dis_width / 2, dis_height / 2))
                message("Press C to Continue", white, (dis_width / 2, dis_height / 2 + 50))
            else:
                message("You Lost! Press C-Play Again or Q-Quit", red, (dis_width / 2, dis_height / 3))
                Your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        main_menu()
                    if event.key == pygame.K_c:
                        if lives > 0:
                            game_close = False
                        else:
                            gameLoop(mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu(score, mode)
                elif event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if mode == "infinite":
            if x1 >= dis_width:
                x1 = 0
            elif x1 < 0:
                x1 = dis_width - snake_block
            if y1 >= dis_height:
                y1 = 0
            elif y1 < 0:
                y1 = dis_height - snake_block
        else:
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                if mode == "lives":
                    lives -= 1
                    save_lives(lives)
                    if lives == 0:
                        game_close = True
                    else:
                        x1 = dis_width / 2
                        y1 = dis_height / 2
                        x1_change = 0
                        y1_change = 0
                        snake_List = [[x1, y1]]
                        Length_of_snake = 1
                        continue
                else:
                    game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        snake_head_rect = pygame.Rect(x1, y1, snake_block, snake_block)
        food_rect = pygame.Rect(foodx, foody, snake_block, snake_block)

        pygame.draw.rect(dis, green, food_rect)

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            snake_List = snake_List[-Length_of_snake:]

        for x in snake_List[:-1]:
            if x == snake_Head:
                if mode == "lives":
                    lives -= 1
                    save_lives(lives)
                    if lives == 0:
                        game_close = True
                    else:
                        x1 = dis_width / 2
                        y1 = dis_height / 2
                        x1_change = 0
                        y1_change = 0
                        snake_List = [[x1, y1]]
                        Length_of_snake = 1
                        continue
                else:
                    game_close = True

        our_snake(snake_block, snake_List)
        Your_score(score)
        if mode == "lives":
            draw_hearts(lives)

        pygame.display.update()

        if snake_head_rect.colliderect(food_rect):
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            foodx = max(0, min(dis_width - snake_block, foodx))
            foody = max(0, min(dis_height - snake_block, foody))
            Length_of_snake += 1
            score += 1

            if Length_of_snake % 5 == 0:
                snake_speed += 5

        save_score(score, mode)
        if mode == "lives":
            save_lives(lives)
        clock.tick(snake_speed)

def settings_menu():
    settings = True
    current_language = language_choice
    current_speed = initial_speed // 5

    while settings:
        dis.fill(dark_blue)

        center_x = dis_width / 2
        center_y = dis_height / 2

        language_button = pygame.Rect(center_x - 100, center_y - 90, 200, 50)
        speed_button = pygame.Rect(center_x - 100, center_y - 30, 200, 50)
        apply_button = pygame.Rect(center_x - 100, center_y + 30, 200, 50)
        back_button = pygame.Rect(center_x - 100, center_y + 90, 200, 50)

        speed_texts = ['Slow', 'Medium', 'Fast']
        current_speed = max(1, min(current_speed, len(speed_texts)))  
        speed_text = speed_texts[current_speed - 1]

        draw_button(f"Language: {current_language}", light_blue, language_button)
        draw_button(f"Speed: {speed_text}", light_blue, speed_button)
        draw_button("Apply Settings", light_blue, apply_button)
        draw_button("Back", light_blue, back_button)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if language_button.collidepoint(event.pos):
                    if current_language == "English":
                        current_language = "Русский"
                    elif current_language == "Русский":
                        current_language = "Turkmen"
                    else:
                        current_language = "English"
                elif speed_button.collidepoint(event.pos):
                    current_speed = (current_speed % 3) + 1
                elif apply_button.collidepoint(event.pos):
                    set_language(current_language)
                    set_speed(current_speed)
                    print(f"Settings applied: Language={current_language}, Speed={current_speed}")
                elif back_button.collidepoint(event.pos):
                    settings = False

def main_menu():
    menu = True
    while menu:
        dis.fill(dark_blue)

        center_x = dis_width / 2
        center_y = dis_height / 2

        infinite_button = pygame.Rect(center_x - 100, center_y - 150, 200, 50)
        lives_button = pygame.Rect(center_x - 100, center_y - 90, 200, 50)
        settings_button = pygame.Rect(center_x - 100, center_y - 30, 200, 50)
        continue_button = pygame.Rect(center_x - 100, center_y + 30, 200, 50)
        quit_button = pygame.Rect(center_x - 100, center_y + 90, 200, 50)

        draw_button("Infinite Mode", light_blue, infinite_button)
        draw_button("Lives Mode", light_blue, lives_button)
        draw_button("Settings", light_blue, settings_button)
        draw_button("Continue Game", light_blue, continue_button)
        draw_button("Quit", light_blue, quit_button)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if infinite_button.collidepoint(event.pos):
                    gameLoop("infinite")
                elif lives_button.collidepoint(event.pos):
                    gameLoop("lives")
                elif settings_button.collidepoint(event.pos):
                    settings_menu()
                elif continue_button.collidepoint(event.pos):
                    infinite_score = load_score("infinite")
                    lives_score = load_score("lives")
                    lives = load_lives()

                    if infinite_score > 0 or lives_score > 0:
                        if infinite_score >= lives_score:
                            gameLoop("infinite")
                        else:
                            gameLoop("lives")
                    else:
                        print("No saved games found.")
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

main_menu()
