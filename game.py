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
            f"{name}, тебе помогут 3 насекомых-друга:",
            "Пчёлка Бип • Божья коровка Лаки • Жук Рокки",
        ]
    )
    print()


def challenge_honey() -> int:
    slow_print(f"{BLUE}Пчёлка Бип:{RESET} Нужно собрать правильный ритм крыльев!")
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
        slow_print(f"{GREEN}Идеально! Бип даёт тебе каплю золотого мёда.{RESET}")
        return 1
    slow_print(f"{YELLOW}Почти! Бип всё равно верит в тебя.{RESET}")
    return 0


def challenge_spots() -> int:
    slow_print(f"{RED}Лаки:{RESET} Помоги посчитать пятнышки на моих друзьях!")
    nums = [random.randint(1, 5) for _ in range(3)]
    total = sum(nums)
    draw_frame([
        f"Коровка 1: {nums[0]} пятн.",
        f"Коровка 2: {nums[1]} пятн.",
        f"Коровка 3: {nums[2]} пятн.",
        "Сколько всего пятнышек?",
    ])
    raw = input("Твой ответ: ").strip()
    if raw.isdigit() and int(raw) == total:
        slow_print(f"{GREEN}Верно! Лаки даёт тебе алую искорку.{RESET}")
        return 1
    slow_print(f"{YELLOW}Ничего, математика тренируется каждый день!{RESET}")
    return 0


def challenge_tunnel() -> int:
    slow_print(f"{MAGENTA}Жук Рокки:{RESET} Я знаю короткий путь по тоннелям.")
    draw_frame([
        "Выбери безопасный тоннель:",
        "1) Тоннель с листиком",
        "2) Тоннель с камушком",
        "3) Тоннель с каплей",
        "Подсказка: правильный номер = 2 + 1",
    ])
    answer = input("Номер тоннеля: ").strip()
    if answer == "3":
        slow_print(f"{GREEN}Отличный выбор! Рокки даёт тебе кристалл росы.{RESET}")
        return 1
    slow_print(f"{YELLOW}Рокки улыбается: иногда лучше проверить ещё раз!{RESET}")
    return 0


def finale(points: int, name: str) -> None:
    print()
    slow_print("Ты возвращаешься к Сердцу Сада...", 0.03)
    if points == 3:
        draw_frame([
            f"{GREEN}{BOLD}СУПЕР-ФИНАЛ!{RESET}",
            f"{name}, ты собрал(а) все 3 артефакта!",
            "Радужный Нектар восстановлен.",
            "Ночное небо озарили тысячи светлячков ✨",
        ])
    elif points == 2:
        draw_frame([
            f"{GREEN}{BOLD}ОТЛИЧНЫЙ ФИНАЛ!{RESET}",
            f"{name}, ты собрал(а) 2 артефакта из 3.",
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


def main() -> None:
    random.seed()
    name = intro()
    mission_briefing(name)

    ready = ask_choice("Готов(а) начать миссию?", {"y": "Да!", "n": "Сначала выйти"})
    if ready == "n":
        slow_print("До скорой встречи в Саду Светлячков!")
        return

    points = 0
    points += challenge_honey()
    points += challenge_spots()
    points += challenge_tunnel()
    finale(points, name)

    again = ask_choice("Сыграем ещё раз?", {"y": "Да, ещё один заход", "n": "Пока хватит"})
    if again == "y":
        clear_screen()
        main()
    else:
        slow_print("Спасибо за игру! Передай Мие привет от команды жуков 🐞")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nИгра остановлена. До встречи!")
        sys.exit(0)
