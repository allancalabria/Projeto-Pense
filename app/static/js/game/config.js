/**
 * Configurações de Spritesheets e Física do Jogo
 */

export const SPRITE_CONFIGS = {
    plane: {
        width: 49,        // largura de 1 frame do avião
        height: 29,       // altura
        frames: [0, 49],  // colunas onde começam os frames
        fps: 12,          // taxa de animação
        scale: 2.4        // escala pixel art
    },
    bomb: {
        width: 9,         // largura de 1 bomba
        height: 9,        // altura
        frames: [0, 9],   // faísca frame 0 e frame 1
        fps: 10,
        scale: 2.8
    },
    targetAlive: {
        width: 14,
        height: 24,
        frames: [0],      // parado no chão
        fps: 0,
        scale: 2.4
    },
    targetDead: {
        width: 15,
        height: 23,
        frames: [0, 15],  // auréola animada do personagem derrotado
        fps: 5,
        scale: 2.4
    },
    explosion: {
        width: 14,
        height: 14,
        frames: [0, 14],  // expansão da explosão
        fps: 6,
        scale: 3.5
    }
};

export const GAME_CONFIGS = {
    gravity: 0.35,
    planeSpeedX: 4.2,
    planeSpeedY: 1.35,
    planeAngleDeg: -12,
    bombMomentumMultiplier: 0.75,
    explosionDurationMs: 1300,
    angelAscendDurationMs: 2200 // tempo para o anjo subir aos céus
};

