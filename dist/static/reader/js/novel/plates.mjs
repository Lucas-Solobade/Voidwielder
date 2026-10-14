// Four original, face-free engravings for the third act. All marks stay in the page frame.
const INK = '#242321';
const MID = '#77736b';
const PALE = '#c9c2b5';

function line(ctx, points, color = INK, width = 1.5) {
  ctx.beginPath();
  points.forEach(([x, y], index) => index ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.stroke();
}

function shape(ctx, points, fill = null, stroke = INK) {
  ctx.beginPath();
  points.forEach(([x, y], index) => index ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
  ctx.closePath();
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 1.5; ctx.stroke(); }
}

function arch(ctx, x, y, w, h) {
  ctx.beginPath();
  ctx.moveTo(x, y + h);
  ctx.lineTo(x, y + 25);
  ctx.quadraticCurveTo(x + w / 2, y - 24, x + w, y + 25);
  ctx.lineTo(x + w, y + h);
  ctx.strokeStyle = INK;
  ctx.lineWidth = 4;
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x + 8, y + h);
  ctx.lineTo(x + 8, y + 27);
  ctx.quadraticCurveTo(x + w / 2, y - 7, x + w - 8, y + 27);
  ctx.lineTo(x + w - 8, y + h);
  ctx.strokeStyle = MID;
  ctx.lineWidth = 1;
  ctx.stroke();
}

function water(ctx, start = 125, end = 190) {
  for (let row = start; row < end; row += 9) {
    for (let col = 24 + (row % 18); col < 580; col += 51) {
      const offset = Math.round(Math.sin((col + row) / 25) * 4);
      line(ctx, [[col, row + offset], [col + 23, row + offset - 1], [col + 33, row + offset]], row % 3 ? MID : INK, .75);
    }
  }
}

function hatch(ctx, x, y, w, h, step = 8) {
  ctx.save();
  ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
  for (let i = -h; i < w + h; i += step) line(ctx, [[x + i, y + h], [x + i + h, y]], MID, .55);
  ctx.restore();
}

function house(ctx, x, y, scale = 1) {
  ctx.save(); ctx.translate(x, y); ctx.scale(scale, scale);
  shape(ctx, [[0, 30], [60, 30], [60, 89], [0, 89]], '#eae5da');
  shape(ctx, [[-7, 31], [30, 3], [67, 31]], '#d8d1c3');
  line(ctx, [[8, 89], [8, 103], [14, 103]], INK, 2);
  line(ctx, [[52, 89], [52, 103], [58, 103]], INK, 2);
  shape(ctx, [[8, 43], [21, 43], [21, 58], [8, 58]], '#f7f2e8');
  shape(ctx, [[38, 43], [51, 43], [51, 58], [38, 58]], '#f7f2e8');
  line(ctx, [[30, 30], [30, 89]], MID, .7);
  for (let i = 35; i < 87; i += 10) line(ctx, [[2, i], [9, i]], MID, .5);
  ctx.restore();
}

function tree(ctx, x, y, size = 1) {
  ctx.save(); ctx.translate(x, y); ctx.scale(size, size);
  line(ctx, [[0, 75], [0, 26], [-7, 10]], INK, 3);
  line(ctx, [[0, 39], [11, 8]], INK, 2);
  for (const [a, b, r] of [[-15, 17, 17], [2, 8, 19], [20, 19, 15]]) {
    ctx.beginPath(); ctx.arc(a, b, r, .05, Math.PI * 1.9);
    ctx.strokeStyle = INK; ctx.lineWidth = 1.2; ctx.stroke();
    for (let k = -r / 2; k < r / 2; k += 6) line(ctx, [[a + k, b + 4], [a + k + 7, b - 3]], MID, .5);
  }
  ctx.restore();
}

function bell(ctx, x, y, size = 1) {
  ctx.save(); ctx.translate(x, y); ctx.scale(size, size);
  arch(ctx, -48, 0, 96, 100);
  line(ctx, [[0, 12], [0, 39]], INK, 2);
  ctx.beginPath(); ctx.moveTo(-13, 39); ctx.quadraticCurveTo(-16, 72, -24, 76);
  ctx.lineTo(24, 76); ctx.quadraticCurveTo(16, 72, 13, 39); ctx.closePath();
  ctx.fillStyle = '#d9d2c5'; ctx.fill(); ctx.strokeStyle = INK; ctx.lineWidth = 2; ctx.stroke();
  line(ctx, [[-26, 78], [26, 78]], INK, 2);
  ctx.beginPath(); ctx.arc(0, 83, 4, 0, Math.PI * 2); ctx.fillStyle = INK; ctx.fill();
  ctx.restore();
}

function wheel(ctx, x, y, radius) {
  ctx.beginPath(); ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.strokeStyle = INK; ctx.lineWidth = 2.5; ctx.stroke();
  ctx.beginPath(); ctx.arc(x, y, radius * .18, 0, Math.PI * 2); ctx.stroke();
  for (let i = 0; i < 8; i++) {
    const a = Math.PI * i / 4;
    line(ctx, [[x + Math.cos(a) * radius * .2, y + Math.sin(a) * radius * .2], [x + Math.cos(a) * radius * .94, y + Math.sin(a) * radius * .94]], INK, 1.3);
  }
}

function margin(ctx) {
  tree(ctx, 62, 41, .92); tree(ctx, 530, 54, .7);
  house(ctx, 128, 43, .9); house(ctx, 227, 26, 1.1); house(ctx, 365, 48, .83);
  shape(ctx, [[16, 136], [76, 124], [133, 133], [195, 120], [252, 130], [319, 117], [391, 127], [456, 119], [583, 128], [583, 190], [16, 190]], '#e9e3d8', null);
  water(ctx, 138, 187);
  line(ctx, [[34, 104], [102, 112], [171, 109], [235, 113], [315, 105], [382, 110], [481, 103], [563, 112]], INK, 1.1);
  for (let x = 43; x < 570; x += 61) line(ctx, [[x, 108], [x, 137]], MID, .7);
}

function gorge(ctx) {
  shape(ctx, [[16, 115], [71, 81], [139, 98], [183, 144], [214, 190], [16, 190]], '#ddd6c8');
  shape(ctx, [[584, 106], [517, 75], [458, 108], [426, 154], [401, 190], [584, 190]], '#ddd6c8');
  hatch(ctx, 20, 139, 155, 43); hatch(ctx, 456, 143, 120, 35);
  bell(ctx, 310, 17, 1.13); wheel(ctx, 390, 130, 25);
  line(ctx, [[323, 105], [377, 125]], INK, 2);
  for (let i = 0; i < 8; i++) line(ctx, [[179 + i * 8, 181], [278 + i * 5, 130]], MID, .65);
  water(ctx, 164, 189);
}

function threeBanks(ctx) {
  shape(ctx, [[15, 67], [120, 46], [205, 76], [315, 92], [396, 61], [584, 91], [584, 190], [15, 190]], '#e7e1d6', null);
  house(ctx, 58, 46, .57); house(ctx, 448, 53, .5);
  tree(ctx, 218, 42, .61); tree(ctx, 531, 44, .66);
  wheel(ctx, 305, 99, 34);
  ctx.beginPath(); ctx.moveTo(32, 165); ctx.bezierCurveTo(164, 128, 198, 182, 305, 158);
  ctx.bezierCurveTo(428, 128, 497, 161, 569, 134); ctx.strokeStyle = INK; ctx.lineWidth = 3; ctx.stroke();
  water(ctx, 145, 187);
  for (const [x, y] of [[133, 126], [336, 143], [480, 120]]) {
    ctx.beginPath(); ctx.arc(x, y, 3.4, 0, Math.PI * 2); ctx.fillStyle = INK; ctx.fill();
    line(ctx, [[x, y + 6], [x, y + 22]], MID, .8);
  }
}

function storm(ctx) {
  for (let i = 0; i < 8; i++) {
    const x = 32 + i * 77;
    line(ctx, [[x, 14], [x - 12, 49]], MID, .75);
    line(ctx, [[x + 27, 18], [x + 15, 57]], PALE, .75);
  }
  bell(ctx, 147, 26, .88); wheel(ctx, 217, 132, 28);
  house(ctx, 381, 41, .82); house(ctx, 488, 65, .64);
  line(ctx, [[18, 141], [118, 132], [198, 136], [271, 121], [339, 131], [417, 123], [580, 125]], INK, 2);
  shape(ctx, [[16, 151], [108, 143], [188, 148], [272, 137], [355, 145], [438, 136], [584, 139], [584, 190], [16, 190]], '#ddd6ca', null);
  water(ctx, 154, 189);
  for (let x = 28; x < 570; x += 19) line(ctx, [[x, 157], [x - 7, 177]], MID, .55);
}

export function drawActThreePlate(ctx, chapter) {
  ctx.save();
  ctx.fillStyle = '#f5f1e8'; ctx.fillRect(0, 0, 600, 200);
  ctx.beginPath(); ctx.rect(13, 13, 574, 174); ctx.clip();
  ({ 21: margin, 22: gorge, 23: threeBanks, 24: storm })[chapter]?.(ctx);
  ctx.restore();
  ctx.strokeStyle = INK; ctx.lineWidth = 1.5; ctx.strokeRect(8, 8, 584, 184);
  ctx.strokeStyle = PALE; ctx.lineWidth = .7; ctx.strokeRect(13, 13, 574, 174);
}
