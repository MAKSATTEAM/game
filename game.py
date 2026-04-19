#!/usr/bin/env python3
"""
Mia's Bug Quest — terminal game in 90s 8-bit style.
"""

from __future__ import annotations

import random
import shutil
import sys
import time

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BLUE = "\033[94m"

HERO_BUTTERFLY = "Бабочка Луна"
HERO_ANT = "Муравей Тик"
HERO_DRAGONFLY = "Стрекоза Нова"


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def slow_print(text: str, delay: float = 0.015) -> None:
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def ask_choice(prompt: str, options: dict[str, str]) -> str:
    while True:
        print(prompt)
        for key, text in options.items():
            print(f"  {BOLD}[{key}]{RESET} {text}")
        answer = input(f"{YELLOW}> {RESET}").strip().lower()
        if answer in options:
            return answer
        print(f"{RED}Похоже, такой команды нет. Попробуй снова!{RESET}\n")


def draw_frame(lines: list[str]) -> None:
    width = min(max(len(line) for line in lines) + 4, shutil.get_terminal_size((90, 20)).columns)
    print(f"{MAGENTA}+{'-' * (width - 2)}+{RESET}")
    for line in lines:
        visible = line[: width - 4]
        print(f"{MAGENTA}| {RESET}{visible.ljust(width - 4)}{MAGENTA} |{RESET}")
    print(f"{MAGENTA}+{'-' * (width - 2)}+{RESET}")


def intro() -> str:
    clear_screen()
    title = [
        f"{CYAN}{BOLD}███╗   ███╗██╗ █████╗     ██████╗ ██╗   ██╗ ██████╗ {RESET}",
        f"{CYAN}{BOLD}████╗ ████║██║██╔══██╗    ██╔══██╗██║   ██║██╔════╝ {RESET}",
        f"{CYAN}{BOLD}██╔████╔██║██║███████║    ██████╔╝██║   ██║██║  ███╗{RESET}",
        f"{CYAN}{BOLD}██║╚██╔╝██║██║██╔══██║    ██╔══██╗██║   ██║██║   ██║{RESET}",
        f"{CYAN}{BOLD}██║ ╚═╝ ██║██║██║  ██║    ██████╔╝╚██████╔╝╚██████╔╝{RESET}",
        f"{CYAN}{BOLD}╚═╝     ╚═╝╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ {RESET}",
    ]
    for line in title:
        print(line)
    print()
    draw_frame(
        [
            f"{BOLD}MIA'S BUG QUEST: Тайна Радужного Нектара{RESET}",
            "8-bit terminal adventure в стиле 90-х",
            "Для игроков 6+ | Только клавиатура",
        ]
    )
    print()
    name = input(f"{GREEN}Как зовут юного исследователя? {RESET}").strip()
    if not name:
        name = "Друг"
    slow_print(f"Привет, {name}! Сегодня ты спасёшь Сад Светлячков.")
    return name


def mission_briefing(name: str) -> None:
    print()
    draw_frame(
        [
            f"{BOLD}Сюжет:{RESET} В волшебном саду пропал Радужный Нектар.",
            "Без него цветы грустят, а светлячки не светятся ночью.",
            f"{name}, тебе помогут 3 героя-команды:",
            f"{HERO_BUTTERFLY} • {HERO_ANT} • {HERO_DRAGONFLY}",
        ]
    )
    print()


def challenge_honey() -> int:
    slow_print(f"{MAGENTA}{HERO_BUTTERFLY}:{RESET} Нужно собрать правильный ритм крыльев!")
    rhythm = random.choice(["ab", "ba", "aab"])
    mapping = {"a": "ЖЖ", "b": "Ж-Ж"}
    hint = "  ".join(mapping[ch] for ch in rhythm)
    draw_frame([
        "Запомни ритм (3 секунды):",
        hint,
        "Введи код буквами a/b. Пример: ab",
    ])
    time.sleep(3)
    clear_screen()
    answer = input("Код ритма: ").strip().lower()
    if answer == rhythm:
        slow_print(f"{GREEN}Идеально! {HERO_BUTTERFLY} даёт тебе каплю золотого мёда.{RESET}")
        return 1
    slow_print(f"{YELLOW}Почти! {HERO_BUTTERFLY} всё равно верит в тебя.{RESET}")
    return 0


def challenge_spots() -> int:
    slow_print(f"{BLUE}{HERO_ANT}:{RESET} Помоги посчитать припасы команды!")
    nums = [random.randint(1, 5) for _ in range(3)]
    total = sum(nums)
    draw_frame([
        f"Лист 1: {nums[0]} зёрнышек.",
        f"Лист 2: {nums[1]} зёрнышек.",
        f"Лист 3: {nums[2]} зёрнышек.",
        "Сколько всего зёрнышек?",
    ])
    raw = input("Твой ответ: ").strip()
    if raw.isdigit() and int(raw) == total:
        slow_print(f"{GREEN}Верно! {HERO_ANT} даёт тебе алую искорку.{RESET}")
        return 1
    slow_print(f"{YELLOW}Ничего, математика тренируется каждый день!{RESET}")
    return 0


def challenge_tunnel() -> int:
    slow_print(f"{CYAN}{HERO_DRAGONFLY}:{RESET} Я знаю короткий путь по воздушным тоннелям.")
    draw_frame([
        "Выбери безопасный тоннель:",
        "1) Тоннель с листиком",
        "2) Тоннель с камушком",
        "3) Тоннель с каплей",
        "Подсказка: правильный номер = 2 + 1",
    ])
    answer = input("Номер тоннеля: ").strip()
    if answer == "3":
        slow_print(f"{GREEN}Отличный выбор! {HERO_DRAGONFLY} даёт тебе кристалл росы.{RESET}")
        return 1
    slow_print(f"{YELLOW}{HERO_DRAGONFLY} улыбается: иногда лучше проверить ещё раз!{RESET}")
    return 0


def challenge_colors() -> int:
    slow_print(f"{MAGENTA}{HERO_BUTTERFLY}:{RESET} Раскрась цветок по коду 90-х!")
    code = random.choice(["кзж", "зжк", "жкз"])
    legend = "к=красный, з=зелёный, ж=жёлтый"
    draw_frame([
        "Повтори цветовой код лепестков.",
        legend,
        f"Код: {code}",
        "Введи код точно так же.",
    ])
    answer = input("Код лепестков: ").strip().lower()
    if answer == code:
        slow_print(f"{GREEN}Точно! Цветок засиял пиксельными огоньками.{RESET}")
        return 1
    slow_print(f"{YELLOW}Неплохо! {HERO_BUTTERFLY} говорит: можно потренироваться ещё.{RESET}")
    return 0


def challenge_dew_math() -> int:
    slow_print(f"{BLUE}{HERO_ANT}:{RESET} Помоги посчитать капли росы для друзей.")
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    draw_frame([
        f"У {HERO_ANT} {a} капли росы.",
        f"{HERO_BUTTERFLY} принесла ещё {b} капли.",
        "Сколько стало всего?",
    ])
    answer = input("Ответ: ").strip()
    if answer.isdigit() and int(answer) == a + b:
        slow_print(f"{GREEN}Верно! {HERO_ANT} даёт тебе серебряную каплю.{RESET}")
        return 1
    slow_print(f"{YELLOW}Почти! {HERO_ANT} всё равно рад твоей помощи.{RESET}")
    return 0


def challenge_echo() -> int:
    slow_print(f"{CYAN}{HERO_DRAGONFLY}:{RESET} Повтори световой сигнал.")
    signal = random.choice(["*.*", "**.", ".**"])
    draw_frame([
        "Сигнал стрекозы:",
        signal,
        "Введи сигнал символами * и .",
    ])
    answer = input("Сигнал: ").strip()
    if answer == signal:
        slow_print(f"{GREEN}Отлично! {HERO_DRAGONFLY} включает ночной маячок.{RESET}")
        return 1
    slow_print(f"{YELLOW}Сигнал почти совпал. {HERO_DRAGONFLY} подмигивает и ждёт реванш!{RESET}")
    return 0


def finale(points: int, name: str) -> None:
    print()
    slow_print("Ты возвращаешься к Сердцу Сада...", 0.03)
    if points >= 6:
        draw_frame([
            f"{GREEN}{BOLD}СУПЕР-ФИНАЛ!{RESET}",
            f"{name}, ты собрал(а) все 6 артефактов!",
            "Радужный Нектар восстановлен.",
            "Ночное небо озарили тысячи светлячков ✨",
        ])
    elif points >= 4:
        draw_frame([
            f"{GREEN}{BOLD}ОТЛИЧНЫЙ ФИНАЛ!{RESET}",
            f"{name}, ты собрал(а) {points} артефакта(ов) из 6.",
            "Сад почти восстановлен — команда гордится тобой!",
            "Завтра можно пройти игру ещё раз и улучшить результат.",
        ])
    else:
        draw_frame([
            f"{YELLOW}{BOLD}ДОБРЫЙ ФИНАЛ{RESET}",
            f"{name}, главное — ты не сдался(ась)!",
            "Друзья-насекомые приглашают потренироваться",
            "и снова отправиться в приключение.",
        ])


def level1_garden(name: str) -> int:
    """Level 1: firefly garden."""
    mission_briefing(name)
    points = 0
    points += challenge_honey()
    points += challenge_spots()
    points += challenge_tunnel()
    points += challenge_colors()
    points += challenge_dew_math()
    points += challenge_echo()
    return points


def challenge_reeds() -> int:
    slow_print(f"{CYAN}{HERO_DRAGONFLY}:{RESET} Нужно перелететь по кувшинкам до камыша!")
    pads = random.randint(4, 8)
    draw_frame([
        f"До камыша {pads} кувшинок.",
        f"{HERO_DRAGONFLY} прыгает через 2 кувшинки за раз.",
        "Сколько прыжков нужно, чтобы долететь?",
        "Подсказка: округляй вверх, если осталось 1.",
    ])
    answer = input("Твой ответ: ").strip()
    correct = (pads + 1) // 2
    if answer.isdigit() and int(answer) == correct:
        slow_print(f"{GREEN}Супер! Ты точно рассчитал(а) маршрут.{RESET}")
        return 1
    slow_print(f"{YELLOW}Неплохо! {HERO_DRAGONFLY} всё равно благодарит за помощь.{RESET}")
    return 0


def challenge_wind() -> int:
    slow_print(f"{CYAN}{HERO_DRAGONFLY}:{RESET} Ветер меняет направление!")
    sequence = random.choice(["лево право право", "право лево право", "лево лево право"])
    draw_frame([
        "Запомни путь полёта на 3 секунды:",
        sequence,
        "Потом введи первые буквы без пробела.",
        "Пример: лпп",
    ])
    time.sleep(3)
    clear_screen()
    answer = input("Код пути: ").strip().lower()
    correct = "".join(word[0] for word in sequence.split())
    if answer == correct:
        slow_print(f"{GREEN}Идеально! {HERO_DRAGONFLY} даёт тебе Синий Ветерок.{RESET}")
        return 1
    slow_print(f"{YELLOW}Почти! {HERO_DRAGONFLY} подбадривает тебя на новый полёт.{RESET}")
    return 0


def challenge_froggy() -> int:
    slow_print(f"{CYAN}{HERO_DRAGONFLY}:{RESET} Лягушонок охраняет короткую тропу.")
    safe = random.choice(["1", "2", "3"])
    clue = {
        "1": "Безопасный лист не справа от красного.",
        "2": "Безопасный лист находится ровно в центре.",
        "3": "Безопасный лист справа от синего.",
    }[safe]
    draw_frame([
        "Перед тобой 3 листа: [1] Синий, [2] Красный, [3] Золотой",
        f"Подсказка Нова: {clue}",
        "Выбери безопасный лист (1/2/3).",
    ])
    answer = input("Твой выбор: ").strip()
    if answer == safe:
        slow_print(f"{GREEN}Отлично! Лягушонок пропускает тебя дальше.{RESET}")
        return 1
    slow_print(f"{YELLOW}{HERO_DRAGONFLY} говорит: бывает, пробуем ещё в следующий раз!{RESET}")
    return 0


def challenge_boost() -> int:
    slow_print(f"{CYAN}{HERO_DRAGONFLY}:{RESET} Включи ускорение точно по таймеру!")
    target = random.choice(["3", "4", "5"])
    draw_frame([
        "Когда скажу 'СТАРТ', мысленно считай секунды.",
        f"Нажми Enter, когда пройдёт примерно {target} сек.",
        "Для малышей можно считать вслух: 'раз, два...'",
    ])
    input("Нажми Enter для старта...")
    print("СТАРТ!")
    start = time.time()
    input()
    elapsed = time.time() - start
    if abs(elapsed - int(target)) <= 1.1:
        slow_print(f"{GREEN}Класс! Тайминг почти идеальный ({elapsed:.1f} сек).{RESET}")
        return 1
    slow_print(f"{YELLOW}Неплохо! Было {elapsed:.1f} сек — это уже тренировка пилота.{RESET}")
    return 0


def challenge_bubbles() -> int:
    slow_print(f"{MAGENTA}{HERO_BUTTERFLY}:{RESET} Лопаем пузырьки в правильном порядке.")
    order = random.choice(["123", "231", "312"])
    draw_frame([
        "Порядок пузырьков:",
        order,
        "Введи три цифры подряд.",
    ])
    answer = input("Порядок: ").strip()
    if answer == order:
        slow_print(f"{GREEN}Точно! {HERO_BUTTERFLY} дарит тебе Лазурный Ключ.{RESET}")
        return 1
    slow_print(f"{YELLOW}Почти! {HERO_BUTTERFLY} хвалит за внимательность.{RESET}")
    return 0


def challenge_stars() -> int:
    slow_print(f"{BLUE}{HERO_ANT}:{RESET} Сколько звёзд отражается в пруду?")
    stars = [random.randint(1, 3) for _ in range(4)]
    total = sum(stars)
    draw_frame([
        f"У кувшинки A: {stars[0]} зв.",
        f"У кувшинки B: {stars[1]} зв.",
        f"У кувшинки C: {stars[2]} зв.",
        f"У кувшинки D: {stars[3]} зв.",
        "Сколько звёзд всего?",
    ])
    answer = input("Твой ответ: ").strip()
    if answer.isdigit() and int(answer) == total:
        slow_print(f"{GREEN}Верно! {HERO_ANT} включает Большой Маяк.{RESET}")
        return 1
    slow_print(f"{YELLOW}{HERO_ANT}: хороший старт, в следующий раз точно получится!{RESET}")
    return 0


def level2_pond(name: str) -> int:
    print()
    draw_frame([
        f"{BOLD}Уровень 2: Пруд стрекоз{RESET}",
        "Вечереет, и над водой вспыхивают неоновые блики.",
        f"Команда {HERO_BUTTERFLY}, {HERO_ANT} и {HERO_DRAGONFLY}",
        "просит восстановить Маяк Лилии.",
        f"{name}, собери 6 небесных символов полёта!",
    ])
    points = 0
    points += challenge_reeds()
    points += challenge_wind()
    points += challenge_froggy()
    points += challenge_boost()
    points += challenge_bubbles()
    points += challenge_stars()
    return points


def finale_level2(points: int, name: str) -> None:
    print()
    slow_print("Маяк Лилии начинает светиться...", 0.03)
    if points >= 6:
        draw_frame([
            f"{GREEN}{BOLD}ФИНАЛ УРОВНЯ 2: ЛЕГЕНДА ПРУДА!{RESET}",
            f"{name}, ты мастер воздушных троп!",
            "Стрекозы запустили неоновый хоровод над водой.",
            "Теперь путь к Ночному Саду открыт.",
        ])
    elif points >= 4:
        draw_frame([
            f"{GREEN}{BOLD}ФИНАЛ УРОВНЯ 2: ПИЛОТ КОМАНДЫ{RESET}",
            f"{name}, ты собрал(а) {points} символа(ов) из 6.",
            "Маяк горит мягким светом, а стрекозы хлопают крыльями.",
            "Ещё одна тренировка — и будет идеальный полёт!",
        ])
    else:
        draw_frame([
            f"{YELLOW}{BOLD}ФИНАЛ УРОВНЯ 2: ПЕРВЫЙ ВЗЛЁТ{RESET}",
            f"{name}, каждый пилот начинал с первых шагов.",
            "Стрекозы зовут тебя на дружескую тренировку у пруда.",
            "Завтра полёт получится ещё лучше!",
        ])


def main() -> None:
    random.seed()
    name = intro()
    ready = ask_choice("Готов(а) начать приключение?", {"y": "Да!", "n": "Сначала выйти"})
    if ready == "n":
        slow_print("До скорой встречи в Саду Светлячков!")
        return

    level = ask_choice(
        "Выбери уровень:",
        {
            "1": "Уровень 1 — Сад Светлячков",
            "2": "Уровень 2 — Пруд стрекоз",
        },
    )
    if level == "1":
        points = level1_garden(name)
        finale(points, name)
    else:
        points = level2_pond(name)
        finale_level2(points, name)

    again = ask_choice("Сыграем ещё раз?", {"y": "Да, ещё один заход", "n": "Пока хватит"})
    if again == "y":
        clear_screen()
        main()
    else:
        slow_print("Спасибо за игру! Передай Мие привет от команды героев 🐞")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nИгра остановлена. До встречи!")
        sys.exit(0)
