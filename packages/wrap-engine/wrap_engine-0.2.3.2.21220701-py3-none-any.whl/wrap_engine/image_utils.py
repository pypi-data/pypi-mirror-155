import pygame

def surface_has_color(surf, color):
    m = pygame.mask.from_threshold(surf, color, [1, 1, 1])

    return m.count()>0

def get_not_used_color(surf):
    for r in range(0, 256):
        for g in range(0, 256):
            for b in range(0, 256):
                if not surface_has_color(surf, [r, g, b]):
                    return [r, g, b]

    return False