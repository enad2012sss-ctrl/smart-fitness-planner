<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fitness Planner Pro+</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root { --primary: #00e676; --bg: #0b0f1a; --card: #1e293b; --text: #fff; }
    body { background: var(--bg); color: var(--text); font-family: sans-serif; display: flex; justify-content: center; }
    .app-container { width: 100%; max-width: 450px; background: #111827; min-height: 100vh; padding: 20px; }
    .screen { display: none; }
    .screen.active { display: block; }
    .input-field { width: 100%; padding: 15px; margin: 10px 0; border-radius: 15px; border: none; background: #0f172a; color: white; }
    .btn { width: 100%; padding: 15px; border-radius: 15px; border: none; background: var(--primary); font-weight: bold; cursor: pointer; }
    .card { background: var(--card); padding: 20px; border-radius: 20px; margin-top: 15px; }
  </style>
</head>
<body>

<div class="app-container">
  <!-- شاشة الدخول -->
  <div id="login-screen" class="screen active">
    <h1>🏋️ Fitness Pro+</h1>
    <input type="text" id="user" class="input-field" placeholder="اسم المستخدم (admin)">
    <input type="password" id="pass" class="input-field" placeholder="كلمة المرور (1234)">
    <button class="btn" onclick="login()">دخول</button>
  </div>

  <!-- الشاشة الرئيسية -->
  <div id="main-screen" class="screen">
    <h2>مرحباً بك!</h2>
    <button class="btn" onclick="show('measure-screen')">القياسات</button>
  </div>

  <!-- شاشة القياسات -->
  <div id="measure-screen" class="screen">
    <button onclick="show('main-screen')">رجوع</button>
    <div class="card">
      <input type="number" id="weight" class="input-field" placeholder="الوزن (كجم)">
      <button class="btn" onclick="saveData()">حفظ</button>
    </div>
    <div class="card"><canvas id="myChart"></canvas></div>
  </div>
</div>

<script>
  function show(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
  }

  function login() {
    if(document.getElementById('user').value === 'admin' && document.getElementById('pass').value === '1234') show('main-screen');
    else alert('خطأ في البيانات');
  }

  function saveData() {
    let weight = document.getElementById('weight').value;
    let data = JSON.parse(localStorage.getItem('fits') || '[]');
    data.push(weight);
    localStorage.setItem('fits', JSON.stringify(data));
    updateChart();
  }

  function updateChart() {
    let ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: { labels: ['1', '2'], datasets: [{ label: 'الوزن', data: JSON.parse(localStorage.getItem('fits')), borderColor: '#00e676' }] }
    });
  }
</script>

</body>
</html>
