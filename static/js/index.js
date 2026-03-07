import { splitText, stagger, waapi } from '/static/js/anime.js';

const { words, chars } = splitText("h2");

waapi.animate(words, {
	color: ['red', 'orange', 'yellow', 'blue', 'magenta', 'purple'],
	duration: 2000,
	delay: stagger(500),
	loop: true,
});

window.mister = function (evt) {
	let dx = (evt.x / document.documentElement.scrollWidth) * 100;
	let dy = (evt.y / document.documentElement.scrollHeight) * 100;
	dx = Math.round(dx);
	dy = Math.round(dy);
	return [dx, dy]
}
