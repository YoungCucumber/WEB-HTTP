import os
import sys

import pygame
import requests

ll = input('Введите координаты через запятую (по умолчанию: 135,-30): ')
ll = '135,-30' if ll == '' else ll
spn = input('Введите масштаб через запятую (по умолчанию: 35,35): ')
spn = '35,35' if spn == '' else spn


def set_spn(spn, val):
    return list(map(lambda x: x + val, spn))


def get_link(ll, spn):
    return f'https://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=sat'


def save_image(ll, spn):
    url = get_link(ll, spn)
    response = requests.get(url)

    if not response:
        print("Ошибка выполнения запроса:")
        print(url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


save_image(ll, spn)
map_file = 'map.png'

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            spn = list(map(float, spn.split(',')))
            if event.key == pygame.K_PAGEUP:
                spn = set_spn(spn, -1)
                spn = ','.join(list((map(str, spn))))
                save_image(ll, spn)
            elif event.key == pygame.K_PAGEDOWN:
                spn = set_spn(spn, 1)
                spn = ','.join(list((map(str, spn))))
                save_image(ll, spn)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    clock.tick(120)

pygame.quit()

os.remove(map_file)
