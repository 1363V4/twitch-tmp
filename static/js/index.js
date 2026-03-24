import { splitText, stagger, waapi } from '/static/js/anime.js';

// console.log(words, chars);
// don't forget to say chars:true!
// need to delay this

function fun() {
	const { words, chars } = splitText("h1", {chars: true});

	waapi.animate(chars, {
		color: ['red', 'orange', 'yellow', 'blue', 'magenta', 'purple'],
		duration: 2000,
		delay: stagger(500),
		loop: true,
	});
};
fun()

// pour éviter les problèmes de sous-pixel et de latence, on arrondit les valeurs en fonction du device pixel ratio
function roundByDPR(value) {
	const dpr = window.devicePixelRatio || 1;
	return Math.round(value * dpr) / dpr;
}

/**
 * 
 * @param {MouseEvent} evt 
 */
window.fe_work = function (evt) {
	let dx = (evt.x / document.documentElement.scrollWidth) * 100;
	let dy = (evt.y / document.documentElement.scrollHeight) * 100;
	dx = roundByDPR(dx);
	dy = roundByDPR(dy);
	const body = document.getElementById("body");
	// pour envoyer les données au backend
	body.setAttribute("data-signals", JSON.stringify({ x:dx, y:dy }));
	// on synchro la position localement pour éviter la latence
	const cursor = document.querySelector("[data-main-cursor]");
	if (cursor) {
		cursor.style.translate = `${dx}dvw ${dy}dvh`;
	}
};




