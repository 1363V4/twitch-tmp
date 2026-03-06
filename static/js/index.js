import { splitText, stagger, waapi } from '/static/js/anime.js';

const { words, chars } = splitText("h2");

// hey chat what color am i missing

waapi.animate(words, {
	color: ['red', 'orange', 'yellow', 'blue', 'magenta', 'purple'],
	duration: 2000,
	delay: stagger(500),
	loop: true,
});
