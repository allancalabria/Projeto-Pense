import { Entity } from './Entity.js';
import { SPRITE_CONFIGS, GAME_CONFIGS } from './config.js';

/**
 * Entidade Alvo (Personagem no solo que vira anjo e sobe aos céus ao morrer)
 */
export class Target extends Entity {
    constructor(boxEl, imgEl, spriteBasePath) {
        super(boxEl, imgEl, SPRITE_CONFIGS.targetAlive);
        this.spriteBasePath = spriteBasePath;
        this.isDead = false;
        this.baseX = 0;
        this.wobbleTimer = 0;
        this.deadTimer = 0;
        this.ascendSpeed = 3.6;
    }

    spawn(pilotColor) {
        this.isDead = false;
        this.wobbleTimer = 0;
        this.deadTimer = 0;
        this.setRotation(0);
        this.box.style.opacity = '1';

        // O alvo é a cor contrária ao piloto escolhido
        const spriteName = pilotColor === 'black' ? 'front-w.png' : 'front-b.png';
        this.animator.setSrc(`${this.spriteBasePath}${spriteName}`, SPRITE_CONFIGS.targetAlive);

        // Posição horizontal aleatória no chão
        const minTargetX = window.innerWidth * 0.35;
        const maxTargetX = window.innerWidth * 0.75;
        const targetX = Math.floor(minTargetX + Math.random() * (maxTargetX - minTargetX));

        this.baseX = targetX;
        this.setPosition(targetX, 0);
        this.show();
    }

    die() {
        this.isDead = true;
        this.wobbleTimer = 0;
        this.deadTimer = 0;
        this.baseX = this.x;
        this.box.style.opacity = '1';
        // Troca para o sprite de anjo com auréola animada
        this.animator.setSrc(`${this.spriteBasePath}dead.png`, SPRITE_CONFIGS.targetDead);
    }

    update(deltaMs, dt) {
        super.update(deltaMs, dt);

        if (this.isDead) {
            this.deadTimer += deltaMs;

            // O anjo voa subindo aos céus com uma suave oscilação lateral
            this.y += this.ascendSpeed * dt;
            this.wobbleTimer += deltaMs * 0.005;
            this.x = this.baseX + Math.sin(this.wobbleTimer) * 14;

            // Reduz a opacidade gradualmente até desaparecer ao final da animação
            const duration = GAME_CONFIGS.angelAscendDurationMs || 2200;
            const progress = Math.min(this.deadTimer / duration, 1);
            const opacity = Math.max(0, 1 - progress);
            this.box.style.opacity = opacity.toFixed(3);

            this.setPosition(this.x, this.y);
            this.setRotation(Math.sin(this.wobbleTimer) * 8);
        }
    }

    reset() {
        super.reset();
        this.isDead = false;
        this.wobbleTimer = 0;
        this.deadTimer = 0;
        this.box.style.opacity = '1';
        this.setRotation(0);
    }
}
