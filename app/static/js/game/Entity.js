import { SpriteAnimator } from './SpriteAnimator.js';

/**
 * Classe Base que encapsula comportamento comum de todos os elementos visuais do jogo
 */
export class Entity {
    constructor(boxEl, imgEl, spriteConfig) {
        this.box = boxEl;
        this.img = imgEl;
        this.animator = new SpriteAnimator(boxEl, imgEl, spriteConfig);
        this.x = 0;
        this.y = 0;
        this.vx = 0;
        this.vy = 0;
        this.visible = false;
    }

    get width() {
        return this.animator.boxWidth;
    }

    get height() {
        return this.animator.boxHeight;
    }

    show() {
        this.visible = true;
        this.box.style.display = 'block';
    }

    hide() {
        this.visible = false;
        this.box.style.display = 'none';
    }

    setPosition(x, y) {
        this.x = x;
        this.y = y;
        this.box.style.left = `${x}px`;
        this.box.style.bottom = `${y}px`;
    }

    setRotation(deg) {
        this.box.style.transform = `rotate(${deg}deg)`;
    }

    getBounds() {
        return this.box.getBoundingClientRect();
    }

    update(deltaMs, dt) {
        this.animator.update(deltaMs);
    }

    reset() {
        this.hide();
        this.x = 0;
        this.y = 0;
        this.vx = 0;
        this.vy = 0;
        this.setRotation(0);
    }
}

