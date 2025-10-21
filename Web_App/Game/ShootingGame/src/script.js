// キャンバス要素と描画コンテキストを取得
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// --- 定数と変数の設定 ---
const PLAYER_SIZE = 20;
const BULLET_SIZE = 5;
const ENEMY_SIZE = 15;
const PLAYER_SPEED = 5;
const BULLET_SPEED = 7;
const ENEMY_SPEED = 1;

let score = 0;
let isGameOver = false;

// プレイヤーオブジェクト
let player = {
    x: canvas.width / 2 - PLAYER_SIZE / 2,
    y: canvas.height - PLAYER_SIZE - 10,
    width: PLAYER_SIZE,
    height: PLAYER_SIZE
};

// 弾と敵の配列
let bullets = [];
let enemies = [];

// キー入力の状態を追跡
let keys = {};

// --- ゲームのリセット関数 ---
function resetGame() {
    score = 0;
    isGameOver = false;
    
    // プレイヤーの位置をリセット
    player.x = canvas.width / 2 - PLAYER_SIZE / 2;
    
    // 弾と敵の配列を空にする
    bullets = [];
    enemies = [];
    
    // ゲームループを再開
    requestAnimationFrame(gameLoop);
}


// --- イベントリスナー ---
window.addEventListener('keydown', (e) => {
    keys[e.code] = true;
});

window.addEventListener('keyup', (e) => {
    keys[e.code] = false;
});

// スペースキーとRキーの処理
window.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && !isGameOver) { // ゲームオーバー中は弾を発射しない
        fireBullet();
    }
    
    // ★ Rキーでゲームリセット ★
    if (e.code === 'KeyR' && isGameOver) {
        resetGame(); 
    }
});


// --- ゲームオブジェクトの描画関数 ---

// プレイヤーを描画
function drawPlayer() {
    ctx.fillStyle = 'blue';
    ctx.fillRect(player.x, player.y, player.width, player.height);
}

// 弾を描画
function drawBullets() {
    ctx.fillStyle = 'yellow';
    bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, BULLET_SIZE, BULLET_SIZE);
    });
}

// 敵を描画
function drawEnemies() {
    ctx.fillStyle = 'red';
    enemies.forEach(enemy => {
        ctx.fillRect(enemy.x, enemy.y, ENEMY_SIZE, ENEMY_SIZE);
    });
}

// スコアとゲームオーバーメッセージを描画
function drawText() {
    ctx.fillStyle = 'white';
    ctx.font = '20px Arial';
    ctx.fillText(`Score: ${score}`, 10, 30);
    
    if (isGameOver) {
        ctx.font = '40px Arial';
        ctx.fillStyle = 'red';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2);
        
        ctx.font = '20px Arial';
        ctx.fillStyle = 'white';
        ctx.fillText('Press R to Restart', canvas.width / 2, canvas.height / 2 + 50); // リスタートメッセージ
    }
}

// --- 更新ロジック ---

// プレイヤーの移動
function updatePlayer() {
    if (keys['ArrowLeft'] && player.x > 0) {
        player.x -= PLAYER_SPEED;
    }
    if (keys['ArrowRight'] && player.x < canvas.width - PLAYER_SIZE) {
        player.x += PLAYER_SPEED;
    }
}

// 弾の発射
function fireBullet() {
    // プレイヤーの中央から発射
    let newBullet = {
        x: player.x + PLAYER_SIZE / 2 - BULLET_SIZE / 2,
        y: player.y,
        width: BULLET_SIZE,
        height: BULLET_SIZE
    };
    bullets.push(newBullet);
}

// 弾の移動
function updateBullets() {
    // 弾を上に移動させ、画面外に出た弾を削除
    bullets = bullets.filter(bullet => {
        bullet.y -= BULLET_SPEED;
        return bullet.y > 0;
    });
}

// 敵の生成
let enemySpawnInterval = 2500; // 2.5秒ごとに敵を生成
let lastSpawnTime = 0;

function spawnEnemy(currentTime) {
    if (currentTime - lastSpawnTime > enemySpawnInterval) {
        let newEnemy = {
            x: Math.random() * (canvas.width - ENEMY_SIZE),
            y: -ENEMY_SIZE, // 画面外から出現
            width: ENEMY_SIZE,
            height: ENEMY_SIZE
        };
        enemies.push(newEnemy);
        lastSpawnTime = currentTime;
    }
}

// 敵の移動
function updateEnemies() {
    // 敵を下へ移動させ、画面外に出た（下端を超えた）敵はゲームオーバーの対象
    enemies = enemies.filter(enemy => {
        enemy.y += ENEMY_SPEED;
        
        // 敵が画面下部に到達したらゲームオーバー
        if (enemy.y + ENEMY_SIZE > canvas.height) {
            isGameOver = true;
            return false; // この敵は削除
        }
        return true; // 画面内に留まる敵
    });
}

// 衝突判定
function checkCollisions() {
    let newBullets = [];
    
    bullets.forEach(bullet => {
        let hit = false;
        
        // 敵と弾の衝突をチェック
        enemies = enemies.filter(enemy => {
            // 矩形同士の衝突判定
            if (bullet.x < enemy.x + enemy.width &&
                bullet.x + bullet.width > enemy.x &&
                bullet.y < enemy.y + enemy.height &&
                bullet.y + bullet.height > enemy.y) 
            {
                // 衝突！
                score += 10;
                hit = true; // 弾は消える
                return false; // 敵は消える
            }
            return true; // 衝突しなかった敵
        });

        if (!hit) {
            newBullets.push(bullet); // 衝突しなかった弾は残す
        }
    });
    
    bullets = newBullets; // 衝突で消えなかった弾に更新
}

// --- メインゲームループ ---
function gameLoop(timestamp) {
    if (isGameOver) {
        // ゲームオーバーならループを停止（メッセージはdrawTextで表示）
        draw();
        return;
    }
    
    // 1. 描画クリア
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 2. 更新
    updatePlayer();
    updateBullets();
    spawnEnemy(timestamp);
    updateEnemies();
    checkCollisions();
    
    // 3. 描画
    draw();
    
    // 次のフレームを要求
    requestAnimationFrame(gameLoop);
}

// 描画を集約する関数
function draw() {
    drawPlayer();
    drawBullets();
    drawEnemies();
    drawText();
}

// ゲーム開始
requestAnimationFrame(gameLoop);
