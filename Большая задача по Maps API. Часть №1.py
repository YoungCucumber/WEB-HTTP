import os
import sys

import pygame
import requests

ll = input('Введите координаты через запятую (по умолчанию: 135,-30): ')
ll = '135,-30' if ll == '' else ll
spn = input('Введите масштаб через запятую (по умолчанию: 35,35): ')
spn = '35,35' if spn == '' else spn

url = f'https://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=sat'
response = requests.get(url)

if not response:
    print("Ошибка выполнения запроса:")
    print(url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

os.remove(map_file)
