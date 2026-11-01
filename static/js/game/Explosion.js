import { Entity } from './Entity.js';
import { SPRITE_CONFIGS } from './config.js';

/**
 * Entidade Explosão
 */
export class Explosion extends Entity {
    constructor(boxEl, imgEl) {
        super(boxEl, imgEl, SPRITE_CONFIGS.explosion);
    }

    explode(x, y) {
        this.animator.applyConfig(SPRITE_CONFIGS.explosion);
        this.setPosition(x, Math.max(0, y));
        this.show();
    }
}

