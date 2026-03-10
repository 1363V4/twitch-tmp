import { splitText, stagger, waapi } from '/static/js/anime.js';

// console.log(words, chars);
// don't forget to say chars:true!
// need to delay this

window.fun = function () {
	const { words, chars } = splitText("h1", {chars: true});

	waapi.animate(chars, {
		color: ['red', 'orange', 'yellow', 'blue', 'magenta', 'purple'],
		duration: 2000,
		delay: stagger(500),
		loop: true,
	});
};


window.fe_work = function (evt) {
	let dx = (evt.x / document.documentElement.scrollWidth) * 100;
	let dy = (evt.y / document.documentElement.scrollHeight) * 100;
	dx = Math.round(dx);
	dy = Math.round(dy);
	return [dx, dy]
}
