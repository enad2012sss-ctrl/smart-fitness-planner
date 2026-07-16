<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fitness Planner Pro+ المطور</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
    body { background: #0b0f1a; min-height: 100vh; display: flex; justify-content: center; align-items: center; }
    .app-container { width: 100%; max-width: 450px; min-height: 100vh; background: #111827; box-shadow: 0 0 50px rgba(0, 230, 118, 0.06); position: relative; overflow-y: auto; padding: 20px 18px 30px; }
    
    /* الشاشات */
    .screen { display: none; flex-direction: column; animation: fadeIn 0.3s ease; }
    .screen.active { display: flex; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }

    /* التنسيقات المشتركة */
    .login-box { width: 100%; background: #1e293b; padding: 32px 20px; border-radius: 32px; display: flex; flex-direction: column; gap: 18px; }
    input { padding: 16px 18px; border: none; border-radius: 18px; background: #0f172a; color: #fff; font-size: 16px; outline: 2px solid transparent; }
    input:focus { outline-color: #00e676; }
    .login-btn, .save-btn { padding: 16px; border: none; border-radius: 18px; background: linear-gradient(135deg, #00e676, #00c853); color: #0b0f1a; font-weight: 800; cursor: pointer; }
    
    /* تحسينات الواجهة المضافة */
    .bmi-card { background: #1e293b; padding: 15px; border-radius: 20px; text-align: center; margin-bottom: 15px; border: 1px solid #00e676; color: #fff; }
    .bmi-value { font-size: 24px; color: #00e676; font-weight: bold; display: block; }
    .btn-delete { color: #ef4444; cursor: pointer; font-size: 14px; background: #0f172a; padding: 2px 8px; border-radius: 8px; }
    
    .header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 14px; border-bottom: 1px solid #1e293b; margin-bottom: 20px; color: #fff; }
    .grid-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .card-item { background: #1e293b; border-radius: 26px; padding: 20px 10px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 6px; cursor: pointer; transition: 0.3s; }
    .card-item:hover { transform: translateY(-6px); border: 1px solid #00e676; }
    
    .sub-header { display: flex; align-items: center; gap: 14px; padding-bottom: 14px; border-bottom: 1px solid #1e293b; margin-bottom: 20px; }
    .back-btn { background: #1e293b; color: #fff; border: none; width: 44px; height: 44px; border-radius: 50%; cursor: pointer; }
    
    .history-list { background: #1e293b; border-radius: 24px; padding: 15px; margin-top: 15px; color: #94a3b8; }
    .history-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #0f172a; align-items: center; }
    .chart-container { background: #1e293b; border-radius: 24px; padding: 15px; height: 200px; margin-top: 15px; }
  </style>
</head>
<body>
  <div class="app-container">
    <!-- شاشة الدخول -->
    <div id="login-screen" class="screen active">
      <h1>🏋️ Fitness Pro+</h1>
      <div class="login-box">
        <input type="text" id="username" placeholder="👤 اسم المستخدم (admin)" />
        <input type="password" id="password" placeholder="🔒 كلمة المرور (1234)" />
        <button class="login-btn" onclick="handleLogin()">🚀 دخول</button>
      </div>
    </div>

    <!-- الشاشة الرئيسية -->
    <div id="main-screen" class="screen">
      <div class="header"><h2>مرحباً بك مجدداً</h2></div>
      <div class="grid-cards">
        <div class="card-item" onclick="navigateTo('measurements')">📏 <div>القياسات</div></div>
        <div class="card-item" onclick="navigateTo('exercises')">📋 <div>التمارين</div></div>
      </div>
    </div>

    <!-- شاشة القياسات المحدثة -->
    <div id="measurements-screen" class="screen">
      <div class="sub-header">
        <button class="back-btn" onclick="navigateTo('home')">←</button>
        <h3>📏 متابعة الوزن والـ BMI</h3>
      </div>
      <div class="bmi-card" id="bmiDisplay">مؤشر كتلة الجسم (BMI): --</div>
      <div class="login-box" style="gap: 10px;">
        <input type="number" id="weight" placeholder="⚖️ الوزن (كجم)" />
        <input type="number" id="height" placeholder="📏 الطول (سم)" />
        <button class="save-btn" onclick="saveMeasurement()">💾 حفظ القياس</button>
      </div>
      <div class="chart-container"><canvas id="weightChart"></canvas></div>
      <div class="history-list" id="historyList"></div>
    </div>
  </div>

  <script>
    let chartInstance = null;

    function navigateTo(page) {
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
      if (page === 'home') document.getElementById('main-screen').classList.add('active');
      else if (page === 'measurements') {
        document.getElementById('measurements-screen').classList.add('active');
        renderMeasurements();
        initChart();
      }
    }

    function handleLogin() {
      const u = document.getElementById('username').value;
      const p = document.getElementById('password').value;
      if (u === 'admin' && p === '1234') navigateTo('home');
      else alert('بيانات خاطئة');
    }

    function saveMeasurement() {
      const weight = parseFloat(document.getElementById('weight').value);
      const height = parseFloat(document.getElementById('height').value) / 100;
      if (!weight || !height) return alert('يرجى إدخال البيانات كاملة');
      
      const bmi = (weight / (height * height)).toFixed(1);
      const data = JSON.parse(localStorage.getItem('fitness_data')) || [];
      data.push({ date: new Date().toLocaleDateString('ar-EG'), weight, bmi });
      localStorage.setItem('fitness_data', JSON.stringify(data));
      
      document.getElementById('bmiDisplay').innerHTML = `مؤشر BMI: <span class="bmi-value">${bmi}</span>`;
      renderMeasurements();
      initChart();
    }

    function deleteMeasurement(index) {
      let data = JSON.parse(localStorage.getItem('fitness_data'));
      data.splice(index, 1);
      localStorage.setItem('fitness_data', JSON.stringify(data));
      renderMeasurements();
      initChart();
    }

    function renderMeasurements() {
      const data = JSON.parse(localStorage.getItem('fitness_data')) || [];
      const list = document.getElementById('historyList');
      list.innerHTML = '<h4>📊 السجل التاريخي</h4>';
      data.forEach((d, i) => {
        list.innerHTML += `
          <div class="history-item">
            <span>${d.date} | BMI: ${d.bmi}</span>
            <span>${d.weight} كجم <span class="btn-delete" onclick="deleteMeasurement(${i})">حذف</span></span>
          </div>`;
      });
    }

    function initChart() {
      const ctx = document.getElementById('weightChart').getContext('2d');
      const data = JSON.parse(localStorage.getItem('fitness_data')) || [];
      if (chartInstance) chartInstance.destroy();
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map(d => d.date),
          datasets: [{ label: 'الوزن', data: data.map(d => d.weight), borderColor: '#00e676', tension: 0.3 }]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });
    }
  </script>
</body>
</html>
