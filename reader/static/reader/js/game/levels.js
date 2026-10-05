const platform = (x, y, w, h = 22) => ({ x, y, w, h });
const letter = (x, y) => ({ x, y, taken: false });
const enemy = (type, x, y, min, max) => ({ type, x, y, min, max, originY: y, direction: 1, timer: 0, stunned: 0, alive: true });

export const LEVELS = [
  {
    name: 'Jardim Lunar', width: 2520, theme: 'garden', sky: ['#22326a', '#8969ac'],
    story: 'As primeiras cartas caíram entre flores que dormem em pé.',
    spawn: { x: 70, y: 400 }, goal: { x: 2430, y: 385 },
    ground: [platform(0, 460, 680, 80), platform(765, 460, 590, 80), platform(1440, 460, 610, 80), platform(2135, 460, 385, 80)],
    platforms: [platform(350, 389, 160), platform(600, 397, 195), platform(1020, 376, 165), platform(1280, 393, 190), platform(1670, 382, 190), platform(1995, 390, 195)],
    letters: [letter(250, 415), letter(410, 342), letter(680, 353), letter(890, 415), letter(1080, 330), letter(1370, 350), letter(1600, 415), letter(1770, 340), letter(2070, 344), letter(2300, 415)],
    enemies: [enemy('roller', 555, 428, 490, 635), enemy('hopper', 990, 426, 900, 1110), enemy('floater', 1530, 336, 1470, 1650), enemy('roller', 1860, 428, 1800, 1970)],
    hazards: [{ x: 1160, y: 445, w: 46, h: 15 }, { x: 2260, y: 445, w: 45, h: 15 }],
  },
  {
    name: 'Arquipélago de Algodão', width: 2800, theme: 'cloud', sky: ['#1b4d78', '#e1a987'],
    story: 'Nuvens fofas, pontes tortas e carimbos voadores. Correio normal por aqui.',
    spawn: { x: 70, y: 400 }, goal: { x: 2710, y: 385 },
    ground: [platform(0, 460, 540, 80), platform(660, 460, 520, 80), platform(1320, 460, 500, 80), platform(1970, 460, 830, 80)],
    platforms: [platform(430, 392, 165), platform(550, 343, 150), platform(970, 379, 165), platform(1150, 330, 175), platform(1510, 380, 180), platform(1770, 344, 160), platform(2250, 382, 170), platform(2480, 340, 160)],
    letters: [letter(250, 415), letter(480, 348), letter(610, 300), letter(830, 415), letter(1035, 335), letter(1225, 285), letter(1450, 415), letter(1600, 335), letter(1830, 300), letter(2150, 415), letter(2340, 340), letter(2550, 300)],
    enemies: [enemy('hopper', 350, 426, 310, 480), enemy('floater', 780, 350, 700, 900), enemy('roller', 1040, 428, 960, 1150), enemy('floater', 1490, 300, 1400, 1650), enemy('hopper', 2100, 426, 2050, 2220), enemy('roller', 2560, 428, 2490, 2670)],
    hazards: [{ x: 900, y: 445, w: 45, h: 15 }, { x: 2200, y: 445, w: 43, h: 15 }],
  },
  {
    name: 'Observatório do Cochilo', width: 3000, theme: 'night', sky: ['#101638', '#5b4f91'],
    story: 'O Rabugão das Nuvens guardou a última caixa. Espere ele cansar e use o sopro!',
    spawn: { x: 70, y: 400 }, goal: { x: 2900, y: 385 },
    ground: [platform(0, 460, 610, 80), platform(710, 460, 540, 80), platform(1360, 460, 600, 80), platform(2050, 460, 950, 80)],
    platforms: [platform(490, 392, 170), platform(1120, 380, 170), platform(1260, 330, 160), platform(1740, 380, 190), platform(1920, 345, 160), platform(2340, 360, 145), platform(2720, 358, 145)],
    letters: [letter(230, 415), letter(550, 348), letter(820, 415), letter(1160, 335), letter(1315, 287), letter(1580, 415), letter(1820, 335), letter(1990, 300), letter(2210, 415), letter(2395, 316), letter(2750, 315)],
    enemies: [enemy('roller', 350, 428, 290, 540), enemy('floater', 860, 325, 760, 1030), enemy('hopper', 1510, 426, 1440, 1730), enemy('floater', 1840, 320, 1750, 1920)],
    hazards: [{ x: 1000, y: 445, w: 42, h: 15 }, { x: 1640, y: 445, w: 42, h: 15 }],
    boss: { x: 2640, y: 389 },
  },
];

export function createLevel(index) {
  const source = LEVELS[index];
  return {
    ...source,
    ground: source.ground.map((item) => ({ ...item })),
    platforms: source.platforms.map((item) => ({ ...item })),
    letters: source.letters.map((item) => ({ ...item })),
    enemies: source.enemies.map((item) => ({ ...item })),
    hazards: source.hazards.map((item) => ({ ...item })),
    boss: source.boss ? { ...source.boss, hp: 3, mode: 'warning', timer: 1.8, waves: [], hitFlash: 0, defeated: false, awake: false } : null,
  };
}
