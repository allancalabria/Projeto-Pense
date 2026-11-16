import { Entity } from './Entity.js';
import { SPRITE_CONFIGS, GAME_CONFIGS } from './config.js';

/**
 * Entidade Bomba
 */
export class Bomb extends Entity {
    constructor(boxEl, imgEl, spriteBasePath) {
        super(boxEl, imgEl, SPRITE_CONFIGS.bomb);
        this.spriteBasePath = spriteBasePath;
        this.isDropped = false;
        this.isActive = false;
    }

    drop(fromX, fromY, initialVx) {
        this.isDropped = true;
        this.isActive = true;
        this.animator.applyConfig(SPRITE_CONFIGS.bomb);

        this.setPosition(fromX, fromY);
        this.vx = initialVx * GAME_CONFIGS.bombMomentumMultiplier;
        this.vy = 0;
        this.setRotation(0);
        this.show();
    }

    update(deltaMs, dt) {
        if (!this.isActive) return;

        super.update(deltaMs, dt);

        // Física da queda com gravidade e inércia horizontal
        this.vy += GAME_CONFIGS.gravity * dt;
        this.x += this.vx * dt;
        this.y -= this.vy * dt;

        // Rotação dinâmica inclinando o nariz da bomba para baixo
        const angle = Math.atan2(this.vy, this.vx) * (180 / Math.PI);
        this.setRotation(angle);
        this.setPosition(this.x, this.y);
    }

    collidesWith(otherEntity, padding = 4) {
        const bombRect = this.getBounds();
        const otherRect = otherEntity.getBounds();

        return !(
            bombRect.right < otherRect.left + padding ||
            bombRect.left > otherRect.right - padding ||
            bombRect.bottom < otherRect.top + padding ||
            bombRect.top > otherRect.bottom
        );
    }

    hasHitGround() {
        return this.y <= 0;
    }

    deactivate() {
        this.isActive = false;
        this.hide();
    }

    reset() {
        super.reset();
        this.isDropped = false;
        this.isActive = false;
    }
}

