/**
 * Gerenciador de Pontuação Dupla com persistência em LocalStorage
 */
export class ScoreManager {
    constructor(scoreBlackEl, scoreWhiteEl) {
        this.scoreBlackEl = scoreBlackEl;
        this.scoreWhiteEl = scoreWhiteEl;
        this.storageKey = 'pense_minigame_scores';
        this.scores = this.load();
        this.render();
    }

    /**
     * Carrega a pontuação salva no LocalStorage
     */
    load() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            if (saved) {
                const parsed = JSON.parse(saved);
                return {
                    black: Math.max(0, parseInt(parsed.black, 10) || 0),
                    white: Math.max(0, parseInt(parsed.white, 10) || 0)
                };
            }
        } catch (error) {
            console.warn('Não foi possível ler as pontuações do LocalStorage:', error);
        }
        return { black: 0, white: 0 };
    }

    /**
     * Persiste as pontuações atuais no LocalStorage
     */
    save() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.scores));
        } catch (error) {
            console.warn('Não foi possível salvar as pontuações no LocalStorage:', error);
        }
    }

    /**
     * Adiciona 1 ponto ao piloto atual e atualiza tela e armazenamento
     */
    addPoint(pilotColor) {
        if (!pilotColor || this.scores[pilotColor] === undefined) return;

        this.scores[pilotColor] += 1;
        this.save();
        this.render(pilotColor);
    }

    /**
     * Atualiza os elementos visuais na barra de seleção
     */
    render(highlightPilot = null) {
        if (this.scoreBlackEl) {
            this.scoreBlackEl.textContent = this.scores.black;
            if (highlightPilot === 'black') {
                this.animateScore(this.scoreBlackEl);
            }
        }

        if (this.scoreWhiteEl) {
            this.scoreWhiteEl.textContent = this.scores.white;
            if (highlightPilot === 'white') {
                this.animateScore(this.scoreWhiteEl);
            }
        }
    }

    /**
     * Efeito de pulso rápido ao ganhar ponto
     */
    animateScore(element) {
        element.classList.remove('scale-125', 'text-amber-400');
        void element.offsetWidth; // força reflow
        element.classList.add('scale-125', 'text-amber-400', 'transition-transform');
        setTimeout(() => {
            element.classList.remove('scale-125', 'text-amber-400');
        }, 300);
    }
}

