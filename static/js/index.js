import { splitText, stagger, waapi } from "/static/js/anime.js";

// why window it when you can just call it?

function fun() {
    const { words, chars } = splitText("h1", { chars: true });

    waapi.animate(chars, {
        color: ["red", "orange", "yellow", "blue", "magenta", "purple"],
        duration: 2000,
        delay: stagger(500),
        loop: true,
    });
};

// fun() ... meh il voit pas mon h1
window.addEventListener('DOMContentLoaded', fun())

// smoother

function roundByDPR(value) {
	const dpr = window.devicePixelRatio || 1;
	return Math.round(value * dpr) / dpr;
}

window.fe_work = function (evt) {
    let dx = (evt.x / document.documentElement.scrollWidth) * 100;
    let dy = (evt.y / document.documentElement.scrollHeight) * 100;
    // dx = Math.round(dx);
   	// dy = Math.round(dy);
    dx = roundByDPR(dx);
   	dy = roundByDPR(dy);
   	// const cursor = document.querySelector("[data-main-cursor]");
  	// if (cursor) {
 		// cursor.style.translate = `${dx}dvw ${dy}dvh`;
  	// }
    return [dx, dy];
};

// WC time yay

class FpsMeter extends HTMLElement {
    static MAX_SAMPLES = 5;
    static RENDER_INTERVAL_MS = 1000;

    #times = [];
    #lastRenderAt = 0;

    constructor() {
        super();
    }

    connectedCallback() {
        this.#render();
        document.addEventListener("datastar-fetch", this.#onFetch);
    }

    disconnectedCallback() {
        document.removeEventListener("datastar-fetch", this.#onFetch);
    }

    #onFetch = (evt) => {
        if (evt.detail?.type !== "finished") return;

        this.#times.push(performance.now());
        if (this.#times.length > FpsMeter.MAX_SAMPLES) {
            this.#times.shift();
        }
        const now = performance.now();
        if (now - this.#lastRenderAt < FpsMeter.RENDER_INTERVAL_MS) return;
        this.#lastRenderAt = now;

        this.#render();
    };

    #computeFps() {
        if (this.#times.length < 2) return null;

        const deltas = [];
        for (let i = 1; i < this.#times.length; i++) {
            deltas.push(this.#times[i] - this.#times[i - 1]);
        }

        const avgDelta = deltas.reduce((sum, d) => sum + d, 0) / deltas.length;
        if (avgDelta <= 0) return null;

        return Math.round(1000 / avgDelta);
    }

    #render() {
        const fps = this.#computeFps();
        const display = fps === null ? "--" : String(fps);

        this.innerHTML = `
      <span class="value">${display}</span>
      <span class="unit">fps</span>
    `;
    }
}

customElements.define("fps-meter", FpsMeter);

export { FpsMeter };
