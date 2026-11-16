import { Entity } from './Entity.js';
import { SPRITE_CONFIGS, GAME_CONFIGS } from './config.js';

/**
 * Entidade Avião (Player)
 */
export class Plane extends Entity {
    constructor(boxEl, imgEl, spriteBasePath) {
        super(boxEl, imgEl, SPRITE_CONFIGS.plane);
        this.spriteBasePath = spriteBasePath;
    }

    setup(pilotColor) {
        const spriteName = pilotColor === 'black' ? 'plane-b.png' : 'plane-w.png';
        this.animator.setSrc(`${this.spriteBasePath}${spriteName}`, SPRITE_CONFIGS.plane);

        // Posição inicial: surge à esquerda e sobrevoa subindo em diagonal
        const startX = -this.width - 20;
        const startY = Math.max(70, window.innerHeight * 0.18);
        this.setPosition(startX, startY);

        this.vx = GAME_CONFIGS.planeSpeedX;
        this.vy = GAME_CONFIGS.planeSpeedY;
        this.setRotation(GAME_CONFIGS.planeAngleDeg);
        this.show();
    }

    update(deltaMs, dt) {
        super.update(deltaMs, dt);
        this.x += this.vx * dt;
        this.y += this.vy * dt;
        this.setPosition(this.x, this.y);
    }

    isOffscreen() {
        return this.x > window.innerWidth + 100;
    }
}

