import { Plane } from './Plane.js';
import { Bomb } from './Bomb.js';
import { Target } from './Target.js';
import { Explosion } from './Explosion.js';
import { ScoreManager } from './ScoreManager.js';
import { GAME_CONFIGS } from './config.js';

/**
 * Orquestrador Principal do Jogo (Máquina de Estados e Loop de Execução)
 */
export class Game {
    constructor() {
        this.wrapper = document.getElementById('gameWrapper');
        if (!this.wrapper) return;

        this.charSelect = document.getElementById('charSelect');
        this.charBlack = document.getElementById('charBlack');
        this.charWhite = document.getElementById('charWhite');

        const spritePath = this.wrapper.dataset.spritePath || '/static/img/sprites/';

        // Gerenciador de pontuação em LocalStorage
        this.scoreManager = new ScoreManager(
            document.getElementById('scoreBlack'),
            document.getElementById('scoreWhite')
        );
        this.currentPilot = null;

        // Instanciação orientada a objetos das entidades
        this.plane = new Plane(
            document.getElementById('player'),
            document.getElementById('playerImg'),
            spritePath
        );

        this.target = new Target(
            document.getElementById('target'),
            document.getElementById('targetImg'),
            spritePath
        );

        this.bomb = new Bomb(
            document.getElementById('bomb'),
            document.getElementById('bombImg'),
            spritePath
        );

        this.explosion = new Explosion(
            document.getElementById('explosion'),
            document.getElementById('explosionImg')
        );

        this.state = 'MENU'; // 'MENU' | 'PLAYING' | 'EXPLODING'
        this.animationFrameId = null;
        this.lastTime = performance.now();

        this.bindEvents();
    }

    bindEvents() {
        // Seleção de pilotos
        this.charBlack.addEventListener('click', (e) => {
            e.stopPropagation();
            this.start('black');
        });

        this.charWhite.addEventListener('click', (e) => {
            e.stopPropagation();
            this.start('white');
        });

        // Clique em qualquer lugar ou tecla espaço para soltar bomba
        window.addEventListener('click', () => {
            if (this.state === 'PLAYING') {
                this.dropBomb();
            }
        });

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && this.state === 'PLAYING') {
                e.preventDefault();
                this.dropBomb();
            }
        });
    }

    start(pilotColor) {
        this.state = 'PLAYING';
        this.currentPilot = pilotColor;
        this.wrapper.classList.add('playing');
        this.charSelect.classList.add('hidden');

        this.plane.setup(pilotColor);
        this.target.spawn(pilotColor);
        this.bomb.reset();
        this.explosion.reset();

        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }

        this.lastTime = performance.now();
        this.loop = this.loop.bind(this);
        this.animationFrameId = requestAnimationFrame(this.loop);
    }

    dropBomb() {
        if (this.state !== 'PLAYING' || this.bomb.isDropped) return;

        // A bomba surge no centro inferior do avião
        const bombX = this.plane.x + (this.plane.width / 2) - (this.bomb.width / 2);
        const bombY = this.plane.y - 10;
        this.bomb.drop(bombX, bombY, this.plane.vx);
    }

    loop(currentTime) {
        const deltaMs = Math.min(currentTime - this.lastTime, 100);
        const dt = deltaMs / 16.666;
        this.lastTime = currentTime;

        this.update(deltaMs, dt);

        if (this.state === 'PLAYING' || this.state === 'EXPLODING') {
            this.animationFrameId = requestAnimationFrame(this.loop);
        }
    }

    update(deltaMs, dt) {
        if (this.state === 'PLAYING') {
            this.plane.update(deltaMs, dt);
            this.target.update(deltaMs, dt);

            if (this.bomb.isActive) {
                this.bomb.update(deltaMs, dt);

                // Colisão com o alvo
                if (this.bomb.collidesWith(this.target)) {
                    this.triggerExplosion(this.bomb.x, this.bomb.y, true);
                    return;
                }

                // Colisão com o solo
                if (this.bomb.hasHitGround()) {
                    this.triggerExplosion(this.bomb.x, 0, false);
                    return;
                }
            }

            // Avião saiu da tela sem bomba ativa
            if (this.plane.isOffscreen() && !this.bomb.isActive) {
                this.resetToMenu();
            }
        } else if (this.state === 'EXPLODING') {
            this.plane.update(deltaMs, dt);
            this.explosion.update(deltaMs, dt);
            this.target.update(deltaMs, dt);
        }
    }

    triggerExplosion(x, y, hitTarget) {
        this.state = 'EXPLODING';
        this.bomb.deactivate();
        this.explosion.explode(x, y);

        if (hitTarget) {
            this.target.die();
            this.scoreManager.addPoint(this.currentPilot);
        }

        const duration = hitTarget 
            ? GAME_CONFIGS.angelAscendDurationMs 
            : GAME_CONFIGS.explosionDurationMs;

        setTimeout(() => {
            this.resetToMenu();
        }, duration);
    }

    resetToMenu() {
        this.state = 'MENU';
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }

        this.wrapper.classList.remove('playing');
        this.charSelect.classList.remove('hidden');

        this.plane.reset();
        this.target.reset();
        this.bomb.reset();
        this.explosion.reset();
    }
}

