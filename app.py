<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fitness Planner Pro+</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js">
  </script>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }
    body {
      background: #0b0f1a;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .app-container {
      width: 100%;
      max-width: 450px;
      min-height: 100vh;
      background: #111827;
      box-shadow: 0 0 50px rgba(0, 230, 118, 0.06);
      position: relative;
      overflow-y: auto;
      padding: 20px 18px 30px;
    }
    .screen {
      display: none;
      flex-direction: column;
      animation: fadeIn 0.3s ease;
    }
    .screen.active {
      display: flex;
    }
    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(12px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    #login-screen {
      justify-content: center;
      align-items: center;
      height: 90vh;
      gap: 28px;
    }
    #login-screen h1 {
      color: #fff;
      font-size: 36px;
      font-weight: 900;
      letter-spacing: 1px;
    }
    #login-screen h1 span {
      color: #00e676;
    }
    .login-box {
      width: 100%;
      background: #1e293b;
      padding: 32px 20px;
      border-radius: 32px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .login-box input {
      padding: 16px 18px;
      border: none;
      border-radius: 18px;
      background: #0f172a;
      color: #fff;
      font-size: 16px;
      outline: 2px solid transparent;
      transition: 0.3s;
    }
    .login-box input:focus {
      outline-color: #00e676;
    }
    .login-box input::placeholder {
      color: #64748b;
    }
    .login-btn {
      padding: 16px;
      border: none;
      border-radius: 18px;
      background: linear-gradient(135deg, #00e676, #00c853);
      color: #0b0f1a;
      font-size: 20px;
      font-weight: 800;
      cursor: pointer;
      transition: 0.3s;
    }
    .login-btn:hover {
      transform: scale(1.02);
      box-shadow: 0 0 30px #00e67666;
    }
    .login-error {
      color: #f87171;
      font-size: 14px;
      text-align: center;
      display: none;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 14px;
      border-bottom: 1px solid #1e293b;
      margin-bottom: 20px;
    }
    .header h2 {
      color: #fff;
      font-size: 22px;
    }
    .header h2 span {
      color: #00e676;
    }
    .logout-btn {
      background: #1e293b;
      color: #cbd5e1;
      border: none;
      padding: 8px 18px;
      border-radius: 30px;
      font-size: 14px;
      cursor: pointer;
      transition: 0.3s;
    }
    .logout-btn:hover {
      background: #ef4444;
      color: #fff;
    }
    .grid-cards {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 8px;
    }
    .card-item {
      background: #1e293b;
      border-radius: 26px;
      padding: 20px 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 6px;
      cursor: pointer;
      transition: 0.3s;
      border: 1px solid transparent;
      min-height: 148px;
      justify-content: center;
    }
    .card-item:hover {
      transform: translateY(-6px);
      border-color: #00e676;
      background: #263544;
      box-shadow: 0 10px 30px rgba(0, 230, 118, 0.08);
    }
    .card-icon {
      font-size: 44px;
      line-height: 1;
    }
    .card-title {
      color: #fff;
      font-size: 17px;
      font-weight: 700;
    }
    .card-desc {
      color: #94a3b8;
      font-size: 12px;
    }
    .card-item:nth-child(1) .card-icon {
      color: #fbbf24;
    }
    .card-item:nth-child(2) .card-icon {
      color: #38bdf8;
    }
    .card-item:nth-child(3) .card-icon {
      color: #a78bfa;
    }
    .card-item:nth-child(4) .card-icon {
      color: #34d399;
    }
    .sub-header {
      display: flex;
      align-items: center;
      gap: 14px;
      padding-bottom: 14px;
      border-bottom: 1px solid #1e293b;
      margin-bottom: 20px;
    }
    .back-btn {
      background: #1e293b;
      color: #fff;
      border: none;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      font-size: 22px;
      cursor: pointer;
      transition: 0.3s;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .back-btn:hover {
      background: #00e676;
      color: #0b0f1a;
    }
    .sub-header h3 {
      color: #fff;
      font-size: 20px;
    }
    .exercise-list {
      display: flex;
      flex-direction: column;
      gap: 18px;
      padding-bottom: 10px;
    }
    .exercise-card {
      background: #1e293b;
      border-radius: 24px;
      padding: 16px;
      border: 1px solid #2d3a4f;
      transition: 0.3s;
    }
    .exercise-card:hover {
      border-color: #00e676;
    }
    .exercise-row {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .exercise-img {
      width: 64px;
      height: 64px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
      flex-shrink: 0;
      background: #0f172a;
      border: 2px solid #2d3a4f;
    }
    .exercise-card:nth-child(1) .exercise-img {
      border-color: #fbbf24;
      background: #fbbf2433;
    }
    .exercise-card:nth-child(2) .exercise-img {
      border-color: #38bdf8;
      background: #38bdf833;
    }
    .exercise-card:nth-child(3) .exercise-img {
      border-color: #a78bfa;
      background: #a78bfa33;
    }
    .exercise-card:nth-child(4) .exercise-img {
      border-color: #34d399;
      background: #34d39933;
    }
    .exercise-card:nth-child(5) .exercise-img {
      border-color: #fb7185;
      background: #fb718533;
    }
    .exercise-info h4 {
      color: #fff;
      font-size: 18px;
    }
    .muscle-tag {
      background: #0f172a;
      padding: 2px 14px;
      border-radius: 30px;
      color: #94a3b8;
      font-size: 12px;
      border: 1px solid #2d3a4f;
      display: inline-block;
      margin-top: 4px;
    }
    .benefits {
      background: #0f172a;
      border-radius: 16px;
      padding: 12px 16px;
      margin-top: 12px;
      border-right: 4px solid #00e676;
    }
    .benefits p {
      color: #cbd5e1;
      font-weight: 600;
      font-size: 14px;
      margin-bottom: 6px;
    }
    .benefits ul {
      list-style: none;
      padding: 0;
    }
    .benefits ul li {
      color: #94a3b8;
      font-size: 13px;
      padding: 3px 0 3px 20px;
      background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%2300e676" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>') right center no-repeat;
      background-size: 14px;
    }
    .add-exercise-btn {
      background: #1e293b;
      border: 2px dashed #2d3a4f;
      border-radius: 24px;
      padding: 16px;
      color: #94a3b8;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: 0.3s;
      text-align: center;
    }
    .add-exercise-btn:hover {
      border-color: #00e676;
      color: #00e676;
      background: #0f172a;
    }
    .measure-inputs {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 18px;
    }
    .measure-inputs input {
      padding: 14px 16px;
      border-radius: 18px;
      border: 1px solid #1e293b;
      background: #0f172a;
      color: #fff;
      font-size: 16px;
      outline: none;
      transition: 0.3s;
    }
    .measure-inputs input:focus {
      border-color: #00e676;
    }
    .measure-inputs .row {
      display: flex;
      gap: 12px;
    }
    .measure-inputs .row input {
      flex: 1;
    }
    .save-btn {
      background: #00e676;
      color: #0b0f1a;
      border: none;
      padding: 14px;
      border-radius: 18px;
      font-weight: 800;
      font-size: 18px;
      cursor: pointer;
      transition: 0.3s;
      margin-top: 4px;
    }
    .save-btn:hover {
      box-shadow: 0 0 25px #00e67677;
      transform: scale(1.01);
    }
    .chart-container {
      background: #1e293b;
      border-radius: 24px;
      padding: 15px;
      margin: 18px 0;
      height: 200px;
    }
    .history-list {
      background: #1e293b;
      border-radius: 24px;
      padding: 15px;
      max-height: 180px;
      overflow-y: auto;
    }
    .history-list h4 {
      color: #cbd5e1;
      font-size: 14px;
      margin-bottom: 10px;
    }
    .history-item {
      display: flex;
      justify-content: space-between;
      color: #94a3b8;
      font-size: 13px;
      padding: 6px 0;
      border-bottom: 1px solid #0f172a;
    }
    .ai-greeting {
      background: #1e293b;
      border-radius: 24px;
      padding: 18px;
      margin-bottom: 20px;
      border-right: 6px solid #a78bfa;
    }
    .ai-greeting p {
      color: #e2e8f0;
      font-size: 15px;
      line-height: 1.7;
    }
    .ai-grid {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .ai-card {
      background: #1e293b;
      border-radius: 20px;
      padding: 16px;
      display: flex;
      align-items: flex-start;
      gap: 14px;
      border: 1px solid #2d3a4f;
    }
    .ai-card .icon {
      font-size: 28px;
      background: #0f172a;
      padding: 8px;
      border-radius: 16px;
    }
    .ai-card .text h5 {
      color: #fff;
      font-size: 16px;
    }
    .ai-card .text p {
      color: #94a3b8;
      font-size: 14px;
      line-height: 1.6;
    }
    .tabs {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 12px;
      margin-bottom: 16px;
    }
    .tab-btn {
      background: #1e293b;
      border: none;
      padding: 10px 18px;
      border-radius: 30px;
      color: #94a3b8;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: 0.3s;
    }
    .tab-btn.active {
      background: #00e676;
      color: #0b0f1a;
    }
    .tips-content {
      display: none;
      flex-direction: column;
      gap: 12px;
    }
    .tips-content.active-tip {
      display: flex;
    }
    .tip-item {
      background: #1e293b;
      border-radius: 20px;
      padding: 16px;
      border-right: 4px solid #38bdf8;
    }
    .tip-item h5 {
      color: #fff;
      font-size: 16px;
    }
    .tip-item p {
      color: #94a3b8;
      font-size: 14px;
      line-height: 1.6;
      margin-top: 4px;
    }
    .footer-note {
      margin-top: 30px;
      color: #475569;
      text-align: center;
      font-size: 12px;
    }
    @media (max-width: 420px) {
      .exercise-img {
        width: 54px;
        height: 54px;
        font-size: 26px;
      }
      .card-item {
        min-height: 130px;
        padding: 16px 8px;
      }
      .card-icon {
        font-size: 36px;
      }
      .card-title {
        font-size: 15px;
      }
      .app-container {
        padding: 14px 12px;
      }
    }
  </style>
</head>
<body>
  <div class="app-container">

    <!-- LOGIN -->
    <div id="login-screen" class="screen active">
      <h1>🏋️ <span>Fitness</span> Pro+</h1>
      <div class="login-box">
        <input type="text" id="username" placeholder="👤 اسم المستخدم" value="admin" />
        <input type="password" id="password" placeholder="🔒 كلمة المرور" value="1234" />
        <button class="login-btn" onclick="handleLogin()">🚀 دخول</button>
        <div class="login-error" id="loginError">❌ اسم المستخدم أو كلمة المرور غير صحيحة</div>
      </div>
      <p style="color:#475569;font-size:13px;">admin / 1234</p>
    </div>

    <!-- MAIN -->
    <div id="main-screen" class="screen">
      <div class="header">
        <h2>مرحباً 👋 <span>متمرن</span></h2>
        <button class="logout-btn" onclick="handleLogout()">خروج</button>
      </div>
      <div class="grid-cards">
        <div class="card-item" onclick="navigateTo('exercises')">
          <div class="card-icon">📋</div>
          <div class="card-title">جدول تماريني</div>
          <div class="card-desc">صور + فوائد</div>
        </div>
        <div class="card-item" onclick="navigateTo('measurements')">
          <div class="card-icon">📏</div>
          <div class="card-title">القياسات</div>
          <div class="card-desc">رسم بياني + تاريخ</div>
        </div>
        <div class="card-item" onclick="navigateTo('ai')">
          <div class="card-icon">🤖</div>
          <div class="card-title">AI مدرب</div>
          <div class="card-desc">توصيات مخصصة</div>
        </div>
        <div class="card-item" onclick="navigateTo('tips')">
          <div class="card-icon">💡</div>
          <div class="card-title">إرشادات</div>
          <div class="card-desc">نصائح احترافية</div>
        </div>
      </div>
      <div class="footer-note">🔥 جميع الصفحات مطورة بالكامل</div>
    </div>

    <!-- EXERCISES -->
    <div id="exercises-screen" class="screen">
      <div class="sub-header">
        <button class="back-btn" onclick="navigateTo('home')">←</button>
        <h3>📋 تماريني</h3>
      </div>
      <div class="exercise-list" id="exerciseList"></div>
      <div class="add-exercise-btn" onclick="addExercise()">➕ إضافة تمرين جديد</div>
    </div>

    <!-- MEASUREMENTS -->
    <div id="measurements-screen" class="screen">
      <div class="sub-header">
        <button class="back-btn" onclick="navigateTo('home')">←</button>
        <h3>📏 القياسات</h3>
      </div>
      <div class="measure-inputs">
        <div class="row">
          <input type="number" id="weight" placeholder="⚖️ الوزن (كجم)" step="0.1" />
          <input type="number" id="fat" placeholder="🧴 الدهون (%)" step="0.1" />
        </div>
        <input type="number" id="waist" placeholder="📐 محيط الخصر (سم)" step="0.1" />
        <button class="save-btn" onclick="saveMeasurement()">💾 حفظ القياس</button>
      </div>
      <div class="chart-container">
        <canvas id="weightChart"></canvas>
      </div>
      <div class="history-list" id="historyList">
        <h4>📊 آخر القياسات</h4>
      </div>
    </div>

    <!-- AI -->
    <div id="ai-screen" class="screen">
      <div class="sub-header">
        <button class="back-btn" onclick="navigateTo('home')">←</button>
        <h3>🤖 AI مدرب</h3>
      </div>
      <div class="ai-greeting" id="aiGreeting">
        <p>🧠 مرحباً! قمت بتحليل بياناتك الأخيرة. إليك توصياتي الذكية:</p>
      </div>
      <div class="ai-grid" id="aiGrid"></div>
    </div>

    <!-- TIPS -->
    <div id="tips-screen" class="screen">
      <div class="sub-header">
        <button class="back-btn" onclick="navigateTo('home')">←</button>
        <h3>💡 إرشادات</h3>
      </div>
      <div class="tabs" id="tipTabs">
        <button class="tab-btn active" onclick="switchTipTab(0)">🏃 قبل التمرين</button>
        <button class="tab-btn" onclick="switchTipTab(1)">🧘 بعد التمرين</button>
        <button class="tab-btn" onclick="switchTipTab(2)">🥗 تغذية</button>
        <button class="tab-btn" onclick="switchTipTab(3)">🤸 إطالة</button>
      </div>
      <div id="tipsContainer"></div>
    </div>

  </div>

  <script>
    // ================================================================
    // 1. DATA
    // ================================================================
    let exercisesData = [
      { name: "Bench Press", muscle: "Chest", emoji: "🏋️", benefits: ["تقوية عضلات الصدر والكتفين", "زيادة القوة الدفعية",
          "تحسين تمارين الضغط"
        ] },
      { name: "Squat", muscle: "Legs", emoji: "🦵", benefits: ["بناء الفخذين والأرداف", "تعزيز القوة الأساسية",
          "حرق سعرات عالية"
        ] },
      { name: "Pull-up", muscle: "Back", emoji: "🤸", benefits: ["توسيع عرض الظهر", "تقوية البايسبس", "زيادة قوة القبضة"] },
      { name: "Plank", muscle: "Core", emoji: "🧘", benefits: ["تقوية الجذع والبطن", "تحسين التوازن", "حماية الظهر"] },
      { name: "Bicep Curl", muscle: "Arms", emoji: "💪", benefits: ["تضخيم العضلة ذات الرأسين", "تقوية الساعد",
          "تحسين مظهر الذراعين"
        ] }
    ];

    const tipsData = [
      { title: "إحماء ديناميكي", desc: "قم بـ 5 دقائق من القفز أو الركض الخفيف مع تمارين دوران الذراعين لتحضير المفاصل." },
      { title: "تبريد وتمدد", desc: "أنهِ التمرين بتمارين إطالة ثابتة لكل عضلة لمدة 30 ثانية لتقليل الألم." },
      { title: "وجبة ما بعد التمرين", desc: "تناول بروتين (دجاج / بيض) مع كاربوهيدرات (أرز / بطاطا) خلال ساعة من التمرين." },
      { title: "تمارين الإطالة اليومية", desc: "خصص 10 دقائق صباحاً لتمارين اليوجا أو الإطالة لتحسين المرونة ومنع التيبس." }
    ];

    // ================================================================
    // 2. SCREEN NAVIGATION
    // ================================================================
    const screens = {
      login: document.getElementById('login-screen'),
      main: document.getElementById('main-screen'),
      exercises: document.getElementById('exercises-screen'),
      measurements: document.getElementById('measurements-screen'),
      ai: document.getElementById('ai-screen'),
      tips: document.getElementById('tips-screen')
    };

    function showScreen(id) {
      Object.values(screens).forEach(s => s.classList.remove('active'));
      screens[id].classList.add('active');
    }

    function navigateTo(page) {
      if (page === 'home') { showScreen('main'); return; }
      if (page === 'exercises') { renderExercises();
        showScreen('exercises'); return; }
      if (page === 'measurements') { renderMeasurements();
        showScreen('measurements');
        setTimeout(initChart, 150); return; }
      if (page === 'ai') { generateAIAdvice();
        showScreen('ai'); return; }
      if (page === 'tips') { renderTips(0);
        showScreen('tips'); }
    }

    // ================================================================
    // 3. EXERCISES
    // ================================================================
    function renderExercises() {
      const container = document.getElementById('exerciseList');
      container.innerHTML = '';
      exercisesData.forEach((ex, idx) => {
        const card = document.createElement('div');
        card.className = 'exercise-card';
        card.innerHTML = `
            <div class="exercise-row">
              <div class="exercise-img">${ex.emoji}</div>
              <div class="exercise-info">
                <h4>${ex.name}</h4>
                <span class="muscle-tag">🎯 ${ex.muscle}</span>
              </div>
            </div>
            <div class="benefits">
              <p>✨ فوائد التمرين</p>
              <ul>${ex.benefits.map(b => `<li>${b}</li>`).join('')}</ul>
            </div>
          `;
        container.appendChild(card);
      });
    }

    function addExercise() {
      const name = prompt("أدخل اسم التمرين الجديد:");
      if (!name) return;
      const muscle = prompt("المجموعة العضلية (مثال: Chest, Legs, Back, Core, Arms):");
      if (!muscle) return;
      const emoji = prompt("أدخل إيموجي للتمرين (مثال: 🏋️):") || "🏋️";
      const benefits = [];
      for (let i = 1; i <= 3; i++) {
        const b = prompt(`أدخل فائدة رقم ${i} (أو اضغط إلغاء للتوقف):`);
        if (b) benefits.push(b);
        else break;
      }
      if (benefits.length === 0) benefits.push("فائدة افتراضية");
      exercisesData.push({ name, muscle, emoji, benefits });
      renderExercises();
    }

    // ================================================================
    // 4. MEASUREMENTS
    // ================================================================
    let chartInstance = null;

    function getMeasurements() {
      return JSON.parse(localStorage.getItem('fitness_measurements')) || [];
    }

    function saveMeasurement() {
      const weight = parseFloat(document.getElementById('weight').value);
      const fat = parseFloat(document.getElementById('fat').value);
      const waist = parseFloat(document.getElementById('waist').value);
      if (!weight) return alert('⚠️ الرجاء إدخال الوزن على الأقل');
      const data = getMeasurements();
      data.push({ date: new Date().toLocaleDateString('ar-EG'), weight, fat, waist });
      localStorage.setItem('fitness_measurements', JSON.stringify(data));
      document.getElementById('weight').value = '';
      document.getElementById('fat').value = '';
      document.getElementById('waist').value = '';
      renderMeasurements();
      initChart();
    }

    function renderMeasurements() {
      const data = getMeasurements();
      const container = document.getElementById('historyList');
      let html = `<h4>📊 آخر القياسات (${data.length})</h4>`;
      if (data.length === 0) {
        html += `<p style="color:#64748b;">لا توجد قياسات مسجلة</p>`;
      } else {
        const last = data.slice(-5).reverse();
        last.forEach(d => {
          html +=
            `<div class="history-item"><span>${d.date}</span><span>⚖️ ${d.weight}كجم | 🧴 ${d.fat || '--'}% | 📐 ${d.waist || '--'}سم</span></div>`;
        });
      }
      container.innerHTML = html;
    }

    function initChart() {
      const ctx = document.getElementById('weightChart').getContext('2d');
      const data = getMeasurements();
      if (chartInstance) chartInstance.destroy();

      const labels = data.map(d => d.date);
      const weights = data.map(d => d.weight);

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'الوزن (كجم)',
            data: weights,
            borderColor: '#00e676',
            backgroundColor: 'rgba(0, 230, 118, 0.12)',
            tension: 0.3,
            fill: true,
            pointBackgroundColor: '#00e676',
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { labels: { color: '#cbd5e1' } } },
          scales: {
            x: { ticks: { color: '#64748b', maxTicksLimit: 6 } },
            y: { ticks: { color: '#64748b' } }
          }
        }
      });
    }

    // ================================================================
    // 5. AI
    // ================================================================
    function generateAIAdvice() {
      const data = getMeasurements();
      const last = data.length > 0 ? data[data.length - 1] : null;
      const count = data.length;

      let weightAdvice = "ابدأ بتسجيل قياساتك للحصول على توصيات دقيقة.";
      let foodAdvice = "تناول وجبة متوازنة تحتوي على بروتين و خضار.";
      let recoveryAdvice = "احصل على 7-8 ساعات نوم يومياً.";

      if (last) {
        const w = last.weight;
        if (w > 80) weightAdvice = "⚡ بناءً على وزنك الحالي، ركز على تمارين الكارديو 3 مرات أسبوعياً مع الحفاظ على تدريب المقاومة.";
        else if (w > 60) weightAdvice = "💪 وزنك مثالي! ركز على زيادة الأوزان تدريجياً في تمارين الحديد لبناء العضلات.";
        else weightAdvice = "🥩 يبدو وزنك منخفضاً نسبياً. زد من السعرات الحرارية مع بروتين عالي الجودة لتحفيز النمو العضلي.";

        if (last.fat && last.fat > 20) foodAdvice =
          "🍗 نسبة الدهون مرتفعة قليلاً. قلل السكريات والنشويات المكررة، واستبدلها بالدهون الصحية (أفوكادو، مكسرات).";
        else if (last.fat && last.fat < 12) foodAdvice = "🥑 نسبة الدهون منخفضة جداً. أضف مصادر دهون صحية لدعم هرموناتك وطاقتك.";
        else foodAdvice = "🥗 تغذيتك متوازنة جيداً. استمر بتناول البروتين مع كل وجبة والخضار الملونة.";

        if (count > 3) recoveryAdvice = "🧘 لاحظت التزامك بالقياسات! خصص يوم راحة نشط (مشي أو يوغا) لتحسين الاستشفاء العضلي.";
        else recoveryAdvice = "🛌 لا تنسى تمارين التنفس العميق بعد التمرين لتهدئة الجهاز العصبي وتسريع الاستشفاء.";
      }

      document.getElementById('aiGreeting').innerHTML =
        `<p>🧠 مرحباً! بناءً على تحليل ${count} قياس مسجل ${last ? `(آخر وزن: ${last.weight}كجم)` : ''}، إليك توصياتي الذكية:</p>`;

      document.getElementById('aiGrid').innerHTML = `
          <div class="ai-card"><div class="icon">🏋️</div><div class="text"><h5>توصية التمارين</h5><p>${weightAdvice}</p></div></div>
          <div class="ai-card"><div class="icon">🥗</div><div class="text"><h5>توصية التغذية</h5><p>${foodAdvice}</p></div></div>
          <div class="ai-card"><div class="icon">🛌</div><div class="text"><h5>توصية الاستشفاء</h5><p>${recoveryAdvice}</p></div></div>
        `;
    }

    // ================================================================
    // 6. TIPS
    // ================================================================
    function renderTips(index) {
      const container = document.getElementById('tipsContainer');
      const tabs = document.querySelectorAll('.tab-btn');
      tabs.forEach((t, i) => t.classList.toggle('active', i === index));

      container.innerHTML = '';
      const tip = tipsData[index];
      const div = document.createElement('div');
      div.className = 'tips-content active-tip';
      div.innerHTML = `<div class="tip-item"><h5>${tip.title}</h5><p>${tip.desc}</p></div>`;
      container.appendChild(div);
    }

    function switchTipTab(index) {
      renderTips(index);
    }

    // ================================================================
    // 7. LOGIN / LOGOUT
    // ================================================================
    function handleLogin() {
      const u = document.getElementById('username').value.trim();
      const p = document.getElementById('password').value.trim();
      if (u === 'admin' && p === '1234') {
        document.getElementById('loginError').style.display = 'none';
        showScreen('main');
      } else {
        document.getElementById('loginError').style.display = 'block';
      }
    }

    function handleLogout() {
      showScreen('login');
      document.getElementById('password').value = '';
      document.getElementById('loginError').style.display = 'none';
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && screens.login.classList.contains('active')) handleLogin();
    });

    // ================================================================
    // 8. INIT
    // ================================================================
    window.onload = function() {
      showScreen('login');
      renderTips(0);
      if (getMeasurements().length === 0) {
        const demo = [
          { date: '01/07/2026', weight: 78, fat: 18, waist: 86 },
          { date: '05/07/2026', weight: 77.5, fat: 17.5, waist: 85 },
          { date: '10/07/2026', weight: 76.8, fat: 17, waist: 84 },
          { date: '15/07/2026', weight: 76.2, fat: 16.5, waist: 83 }
        ];
        localStorage.setItem('fitness_measurements', JSON.stringify(demo));
      }
    };
  </script>
</body>
</html>
