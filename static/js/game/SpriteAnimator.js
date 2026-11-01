/**
 * Classe responsável pelo recorte e ciclo de animação de folhas de sprite (spritesheets)
 */
export class SpriteAnimator {
    constructor(boxEl, imgEl, config = null) {
        this.box = boxEl;
        this.img = imgEl;
        this.config = null;
        this.scale = 1;
        this.boxWidth = 0;
        this.boxHeight = 0;
        this.currentFrame = 0;
        this.timer = 0;

        if (config) {
            this.applyConfig(config);
        }
    }

    applyConfig(config) {
        this.config = config;
        this.scale = config.scale || 2.4;
        this.boxWidth = config.width * this.scale;
        this.boxHeight = config.height * this.scale;

        // Ajusta a caixa para recortar e exibir EXATAMENTE um frame por vez
        this.box.style.width = `${this.boxWidth}px`;
        this.box.style.height = `${this.boxHeight}px`;

        this.currentFrame = 0;
        this.timer = 0;
        this.updateFrame();
    }

    setSrc(src, config = null) {
        this.img.src = src;
        if (config) {
            this.applyConfig(config);
        }
    }

    update(deltaMs) {
        if (!this.config || !this.config.frames || this.config.frames.length <= 1 || !this.config.fps) {
            return;
        }

        this.timer += deltaMs;
        const interval = 1000 / this.config.fps;
        if (this.timer >= interval) {
            this.timer -= interval;
            this.currentFrame = (this.currentFrame + 1) % this.config.frames.length;
            this.updateFrame();
        }
    }

    updateFrame() {
        if (!this.config || !this.config.frames) return;
        const frameX = this.config.frames[this.currentFrame] || 0;
        const shiftX = frameX * this.scale;
        // Desloca a spritesheet horizontalmente para alinhar a coluna do frame atual
        this.img.style.transform = `translateX(-${shiftX}px)`;
    }
}

