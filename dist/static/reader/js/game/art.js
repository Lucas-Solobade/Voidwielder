const TAU = Math.PI * 2;
const circle = (ctx, x, y, r, color) => {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(x, y, r, 0, TAU);
  ctx.fill();
};
const ellipse = (ctx, x, y, rx, ry, color) => {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.ellipse(x, y, rx, ry, 0, 0, TAU);
  ctx.fill();
};
const rounded = (ctx, x, y, w, h, r, color) => {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.roundRect(x, y, w, h, r);
  ctx.fill();
};

function star(ctx, x, y, radius, color, rotation = 0) {
  ctx.fillStyle = color;
  ctx.beginPath();
  for (let i = 0; i < 10; i += 1) {
    const angle = rotation - Math.PI / 2 + i * Math.PI / 5;
    const r = i % 2 ? radius * .48 : radius;
    const px = x + Math.cos(angle) * r;
    const py = y + Math.sin(angle) * r;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.closePath();
  ctx.fill();
}

function cloud(ctx, x, y, scale, color) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale, scale);
  ellipse(ctx, 0, 5, 55, 19, color);
  circle(ctx, -31, -4, 19, color);
  circle(ctx, 0, -13, 27, color);
  circle(ctx, 34, -1, 20, color);
  ctx.restore();
}

function backdrop(ctx, level, camera, time) {
  const gradient = ctx.createLinearGradient(0, 0, 0, 540);
  gradient.addColorStop(0, level.sky[0]);
  gradient.addColorStop(1, level.sky[1]);
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 960, 540);
  circle(ctx, 770 - camera * .035, 95, level.theme === 'night' ? 58 : 45, level.theme === 'cloud' ? '#ffe9a0' : '#fff4bd');
  for (let i = 0; i < 65; i += 1) {
    const x = ((i * 193.7 - camera * .12) % 1150 + 1150) % 1150 - 80;
    const y = 20 + ((i * 73) % 325);
    const glow = .45 + .45 * Math.sin(time * 2.2 + i * 3);
    circle(ctx, x, y, i % 9 === 0 ? 2.5 : 1.2, `rgba(255,248,218,${glow})`);
  }
  ctx.save();
  ctx.translate(-camera * .22, 0);
  for (let i = -1; i < 10; i += 1) {
    const x = i * 300 + (i % 2) * 90;
    if (level.theme === 'garden') {
      ellipse(ctx, x + 80, 505, 220, 140, '#5765a1');
      ellipse(ctx, x + 210, 510, 210, 110, '#465889');
    } else if (level.theme === 'cloud') {
      cloud(ctx, x + 80, 310 + (i % 3) * 24, 1.8, '#d9b4c7');
      cloud(ctx, x + 250, 390, 2.3, '#d5a9ae');
    } else {
      rounded(ctx, x, 340 - i % 3 * 33, 66, 200, 10, '#3b3a75');
      ellipse(ctx, x + 34, 345 - i % 3 * 33, 66, 32, '#51508d');
      circle(ctx, x + 34, 320 - i % 3 * 33, 9, '#ffd77d');
    }
  }
  ctx.restore();
  ctx.save();
  ctx.translate(-camera * .48, 0);
  for (let i = 0; i < 16; i += 1) {
    const x = i * 210 + 50;
    if (level.theme === 'garden') {
      rounded(ctx, x, 354, 14, 120, 7, '#3b597a');
      circle(ctx, x + 7, 354, 36, '#529a9d');
      circle(ctx, x - 17, 367, 21, '#70adb0');
      circle(ctx, x + 29, 368, 23, '#70adb0');
    } else if (level.theme === 'cloud') {
      cloud(ctx, x, 420 - i % 3 * 18, .9, '#f8d9d4');
    } else {
      ellipse(ctx, x, 450, 50, 75, '#34336b');
      circle(ctx, x, 377, 7, '#ffd77d');
    }
  }
  ctx.restore();
}

function drawPlatform(ctx, item, theme, ground = false) {
  const top = theme === 'garden' ? '#91d1ab' : theme === 'cloud' ? '#fff1cf' : '#b3a5df';
  const body = theme === 'garden' ? '#536f86' : theme === 'cloud' ? '#8d79a2' : '#4f4b84';
  rounded(ctx, item.x, item.y, item.w, item.h, ground ? 12 : 11, body);
  rounded(ctx, item.x, item.y, item.w, ground ? 16 : 12, 8, top);
  ctx.fillStyle = '#ffffff3c';
  for (let x = item.x + 20; x < item.x + item.w - 5; x += 54) {
    ctx.fillRect(x, item.y + (ground ? 28 : 15), 18, 3);
  }
  if (!ground) {
    ellipse(ctx, item.x + 18, item.y + item.h + 3, 11, 4, '#19204670');
    ellipse(ctx, item.x + item.w - 18, item.y + item.h + 3, 11, 4, '#19204670');
  }
}

function drawLetter(ctx, item, time) {
  const y = item.y + Math.sin(time * 3 + item.x) * 4;
  ctx.save();
  ctx.translate(item.x, y);
  ctx.rotate(Math.sin(time * 2 + item.x) * .12);
  ctx.shadowColor = '#ffe68b';
  ctx.shadowBlur = 16;
  rounded(ctx, -13, -9, 26, 18, 4, '#ffdf76');
  ctx.shadowBlur = 0;
  ctx.strokeStyle = '#b86672';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(-11, -7);
  ctx.lineTo(0, 2);
  ctx.lineTo(11, -7);
  ctx.stroke();
  star(ctx, 0, 1, 4, '#fffef4', time);
  ctx.restore();
}

function drawPlayer(ctx, player, time) {
  if (player.invulnerable > 0 && Math.floor(time * 14) % 2) return;
  const running = Math.abs(player.vx) > 25 && player.grounded;
  const hop = running ? Math.sin(time * 18) * 3 : Math.sin(time * 3) * 2;
  const tilt = player.hurtTime > 0 ? -.18 * player.facing : running ? player.vx / 1800 : 0;
  ctx.save();
  ctx.translate(player.x + player.w / 2, player.y + player.h / 2 + hop);
  ctx.rotate(tilt);
  const squash = player.landSquash > 0 ? .12 * player.landSquash : 0;
  ctx.scale(1 + squash, 1 - squash);
  ellipse(ctx, -9, 20, 9, 5, '#40356f');
  ellipse(ctx, 10, 20, 9, 5, '#40356f');
  const armWave = running ? Math.sin(time * 18) * 8 : Math.sin(time * 4) * 3;
  ellipse(ctx, -18, 4 + armWave, 6, 11, '#f3a6bc');
  ellipse(ctx, 18, 4 - armWave, 6, 11, '#f3a6bc');
  ellipse(ctx, 0, 0, 19, 21, '#ffbacb');
  ellipse(ctx, -5, -7, 8, 5, '#ffd5dc');
  ctx.fillStyle = '#ffd16c';
  ctx.beginPath();
  ctx.moveTo(-17, 8);
  ctx.quadraticCurveTo(-4, 17, 15, 7);
  ctx.lineTo(18, 13);
  ctx.quadraticCurveTo(0, 25, -18, 15);
  ctx.fill();
  const eyeY = player.vy < -70 ? -5 : player.vy > 80 ? 1 : -2;
  ellipse(ctx, -7, eyeY, 2.5, 4, '#372b55');
  ellipse(ctx, 7, eyeY, 2.5, 4, '#372b55');
  circle(ctx, -6, eyeY - 1.5, 1, '#fff');
  circle(ctx, 8, eyeY - 1.5, 1, '#fff');
  if (player.hurtTime > 0) {
    ctx.strokeStyle = '#372b55';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(0, 10, 3, Math.PI, TAU);
    ctx.stroke();
  } else if (player.vy < -70) {
    circle(ctx, 0, 9, 3, '#9b4766');
  } else {
    ctx.strokeStyle = '#9b4766';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(0, 6, 5, 0, Math.PI);
    ctx.stroke();
  }
  star(ctx, -10, -17, 7, '#ffe483', -.2);
  ctx.restore();
}

function drawEnemy(ctx, item, time) {
  if (!item.alive) return;
  ctx.save();
  ctx.translate(item.x, item.y + (item.type === 'floater' ? Math.sin(time * 5 + item.x) * 2 : 0));
  if (item.type === 'roller') {
    ellipse(ctx, 0, 0, 19, 15, item.stunned > 0 ? '#aab7c8' : '#ffc886');
    circle(ctx, -7, -13, 7, '#fbe5aa');
    circle(ctx, 8, -13, 7, '#fbe5aa');
    ellipse(ctx, -6, -3, 2, 3, '#5b426b');
    ellipse(ctx, 6, -3, 2, 3, '#5b426b');
    circle(ctx, 0, 5, 2, '#b96970');
  } else if (item.type === 'hopper') {
    ellipse(ctx, 0, 1, 19, 18, item.stunned > 0 ? '#aab7c8' : '#b4e6a8');
    ellipse(ctx, -12, -17, 6, 13, '#b4e6a8');
    ellipse(ctx, 12, -17, 6, 13, '#b4e6a8');
    circle(ctx, -7, -2, 2.4, '#395d62');
    circle(ctx, 7, -2, 2.4, '#395d62');
    ctx.strokeStyle = '#395d62';
    ctx.beginPath();
    ctx.arc(0, 3, 5, 0, Math.PI);
    ctx.stroke();
  } else {
    ellipse(ctx, 0, 0, 20, 12, item.stunned > 0 ? '#aab7c8' : '#a7d9ef');
    ellipse(ctx, -20, -3, 12, 7, '#e5f7ff');
    ellipse(ctx, 20, -3, 12, 7, '#e5f7ff');
    circle(ctx, -7, -1, 2.3, '#3a5575');
    circle(ctx, 7, -1, 2.3, '#3a5575');
  }
  if (item.stunned > 0) star(ctx, 0, -30, 6, '#fff0a7', time * 3);
  ctx.restore();
}

function drawBoss(ctx, boss, time) {
  if (boss.defeated) return;
  ctx.save();
  ctx.translate(boss.x, boss.y + Math.sin(time * 2) * 3);
  ctx.shadowColor = boss.mode === 'warning' ? '#ff6f98' : '#ffd67c';
  ctx.shadowBlur = boss.mode === 'warning' ? 30 : 12;
  ellipse(ctx, 0, 12, 57, 48, boss.hitFlash > 0 ? '#fff6d3' : boss.mode === 'exposed' ? '#cbbadf' : '#ebe0f5');
  ellipse(ctx, -35, 1, 27, 30, '#eee3f5');
  ellipse(ctx, 36, 3, 29, 28, '#eee3f5');
  ctx.shadowBlur = 0;
  ellipse(ctx, -19, 6, 5, boss.mode === 'exposed' ? 2 : 7, '#43335f');
  ellipse(ctx, 19, 6, 5, boss.mode === 'exposed' ? 2 : 7, '#43335f');
  ctx.strokeStyle = '#644d78';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(0, 19, boss.mode === 'exposed' ? 7 : 11, boss.mode === 'exposed' ? 0 : Math.PI, boss.mode === 'exposed' ? Math.PI : TAU);
  ctx.stroke();
  rounded(ctx, -28, -49, 56, 14, 6, '#665289');
  star(ctx, 0, -53, 12, '#ffdb72', time * .5);
  if (boss.mode === 'warning') {
    ctx.strokeStyle = '#ff819f';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(0, 0, 74 + Math.sin(time * 13) * 5, 0, TAU);
    ctx.stroke();
  }
  ctx.restore();
  for (const wave of boss.waves) {
    ctx.save();
    ctx.translate(wave.x, wave.y);
    ctx.rotate(time * 6);
    star(ctx, 0, 0, 20, '#ff8ea3', time);
    circle(ctx, 0, 0, 7, '#ffe2af');
    ctx.restore();
  }
}

function mailbox(ctx, goal, ready, time) {
  ctx.save();
  ctx.translate(goal.x, goal.y);
  rounded(ctx, -6, 0, 12, 75, 4, '#624e8c');
  rounded(ctx, -32, -20, 64, 50, 15, ready ? '#ffdf78' : '#aa9cac');
  rounded(ctx, -20, 0, 40, 7, 3, '#746082');
  rounded(ctx, -5, -13, 10, 17, 2, ready ? '#e69673' : '#746082');
  if (ready) {
    star(ctx, 0, -44, 12 + Math.sin(time * 4) * 2, '#fff3ad', time);
    circle(ctx, -42, -38, 3, '#fff2b2');
    circle(ctx, 42, -48, 2, '#fff2b2');
  }
  ctx.restore();
}

export function renderGame(ctx, game) {
  const { level, player, particles, camera, time } = game;
  ctx.clearRect(0, 0, 960, 540);
  backdrop(ctx, level, camera, time);
  ctx.save();
  ctx.translate(-Math.round(camera), 0);
  for (const item of level.ground) drawPlatform(ctx, item, level.theme, true);
  for (const item of level.platforms) drawPlatform(ctx, item, level.theme);
  for (const hazard of level.hazards) {
    for (let x = hazard.x + 5; x < hazard.x + hazard.w; x += 14) {
      ctx.fillStyle = '#e58d9f';
      ctx.beginPath();
      ctx.moveTo(x - 6, hazard.y + 15);
      ctx.lineTo(x, hazard.y);
      ctx.lineTo(x + 6, hazard.y + 15);
      ctx.fill();
    }
  }
  for (const item of level.letters) if (!item.taken) drawLetter(ctx, item, time);
  for (const item of level.enemies) drawEnemy(ctx, item, time);
  mailbox(ctx, level.goal, !level.boss || level.boss.defeated, time);
  if (level.boss) drawBoss(ctx, level.boss, time);
  for (const particle of particles) {
    ctx.globalAlpha = Math.max(0, particle.life / particle.maxLife);
    circle(ctx, particle.x, particle.y, particle.size, particle.color);
  }
  ctx.globalAlpha = 1;
  if (game.burstTime > 0) {
    ctx.strokeStyle = `rgba(176,248,250,${game.burstTime / .35})`;
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.arc(player.x + player.w / 2, player.y + player.h / 2, 130 * (1 - game.burstTime / .35), 0, TAU);
    ctx.stroke();
  }
  drawPlayer(ctx, player, time);
  ctx.restore();
  if (level.boss && !level.boss.defeated && player.x > 2100) {
    rounded(ctx, 660, 18, 250, 28, 12, '#24213ec9');
    ctx.fillStyle = '#fff';
    ctx.font = '700 15px system-ui';
    ctx.fillText('Rabugão das Nuvens', 674, 37);
    for (let i = 0; i < level.boss.hp; i += 1) star(ctx, 866 + i * 14, 32, 6, '#ffcf70');
    if (level.boss.mode === 'exposed') {
      rounded(ctx, 322, 62, 315, 36, 18, '#fff2ca');
      ctx.fillStyle = '#4a356d';
      ctx.font = '800 18px system-ui';
      ctx.fillText('Ele cansou! Aproxime-se e sopre (X)!', 340, 86);
    }
  }
}
