import { Game } from './game';

(() => {
  const canvas = document.querySelector('canvas');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const game = new Game(canvas);
  game.run();

  window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    // game.doSomething()
  });
})();
