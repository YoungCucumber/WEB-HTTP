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


def get_link(ll, spn, l='map'):
    return f'https://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l={l}'


def set_coordinates(ll, dy, dx):
    y, x = [int(i) for i in ll.split(',')]
    if -84 < x < 84:
        x += dx
    if -179 < y < 179:
        y += dy
    return f'{y},{x}'


def save_image(ll, spn, l='map'):
    url = get_link(ll, spn, l)
    response = requests.get(url)

    if not response:
        print("Ошибка выполнения запроса:")
        print(url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
        file.close()


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
            if event.key == pygame.K_PAGEUP:
                spn = list(map(float, spn.split(',')))
                spn = set_spn(spn, -1)
                spn = ','.join(list((map(str, spn))))
            elif event.key == pygame.K_PAGEDOWN:
                spn = list(map(float, spn.split(',')))
                spn = set_spn(spn, 1)
                spn = ','.join(list((map(str, spn))))
            elif event.key == pygame.K_UP:
                ll = set_coordinates(ll, 0, 1)
            elif event.key == pygame.K_DOWN:
                ll = set_coordinates(ll, 0, -1)
            elif event.key == pygame.K_RIGHT:
                ll = set_coordinates(ll, 1, 0)
            elif event.key == pygame.K_LEFT:
                ll = set_coordinates(ll, -1, 0)
            elif event.key == pygame.K_1:
                l = 'map'
            elif event.key == pygame.K_2:
                l = 'sat'
            elif event.key == pygame.K_3:
                l = 'sat,skl'
            save_image(ll, spn, l)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    clock.tick(120)

pygame.quit()

os.remove(map_file)
