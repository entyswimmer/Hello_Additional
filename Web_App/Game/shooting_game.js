// ======== シューティングゲーム 基本構成 ========

// プレイヤーの位置
let playerX, playerY;
// 弾のリスト
let bullets = [];
// 敵のリスト
let enemies = [];
// スコア
let score = 0;
// ゲームオーバーフラグ
let gameOver = false;

function setup() {
  createCanvas(400, 600);
  playerX = width / 2;
  playerY = height - 50;
  textSize(20);
}

function draw() {
  background(0);

  if (gameOver) {
    fill(255, 0, 0);
    textAlign(CENTER);
    text("GAME OVER", width / 2, height / 2);
    text("Score: " + score, width / 2, height / 2 + 30);
    text("Press R to restart", width / 2, height / 2 + 60);
    return;
  }

  // プレイヤー描画
  fill(0, 255, 0);
  triangle(playerX - 10, playerY + 10, playerX + 10, playerY + 10, playerX, playerY - 10);

  // プレイヤー操作
  if (keyIsDown(LEFT_ARROW)) playerX -= 5;
  if (keyIsDown(RIGHT_ARROW)) playerX += 5;
  playerX = constrain(playerX, 10, width - 10);

  // 弾の更新と描画
  for (let i = bullets.length - 1; i >= 0; i--) {
    let b = bullets[i];
    b.y -= 8;
    fill(255, 255, 0);
    ellipse(b.x, b.y, 5);
    if (b.y < 0) bullets.splice(i, 1);
  }

  // 敵の生成（ランダムに）
  if (frameCount % 60 === 0) {
    enemies.push({ x: random(20, width - 20), y: 0 });
  }

  // 敵の更新と描画
  for (let i = enemies.length - 1; i >= 0; i--) {
    let e = enemies[i];
    e.y += 3;
    fill(255, 0, 0);
    rect(e.x - 10, e.y - 10, 20, 20);

    // 弾との当たり判定
    for (let j = bullets.length - 1; j >= 0; j--) {
      let b = bullets[j];
      if (dist(b.x, b.y, e.x, e.y) < 15) {
        enemies.splice(i, 1);
        bullets.splice(j, 1);
        score += 10;
        break;
      }
    }

    // プレイヤーとの当たり判定
    if (dist(playerX, playerY, e.x, e.y) < 20) {
      gameOver = true;
    }

    // 画面外に出た敵を削除
    if (e.y > height) enemies.splice(i, 1);
  }

  // スコア表示
  fill(255);
  textAlign(LEFT);
  text("SCORE: " + score, 10, 30);
}

// スペースキーで弾を発射
function keyPressed() {
  if (key === " " && !gameOver) {
    bullets.push({ x: playerX, y: playerY - 15 });
  }
  // Rでリスタート
  if (key === "r" || key === "R") {
    resetGame();
  }
}

// ゲームリセット
function resetGame() {
  bullets = [];
  enemies = [];
  score = 0;
  gameOver = false;
  playerX = width / 2;
}
