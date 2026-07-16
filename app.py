<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fitness Planner Pro+ المطور</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    /* تم الحفاظ على التصميم الأساسي مع إضافات جمالية */
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
    body { background: #0b0f1a; min-height: 100vh; display: flex; justify-content: center; align-items: center; }
    .app-container { width: 100%; max-width: 450px; min-height: 100vh; background: #111827; position: relative; padding: 20px; overflow-y: auto; }
    
    /* تحسينات الواجهة */
    .btn-delete { color: #ef4444; cursor: pointer; font-size: 12px; margin-right: 10px; }
    .bmi-card { background: #1e293b; padding: 15px; border-radius: 20px; text-align: center; margin-bottom: 15px; border: 1px solid #00e676; }
    .bmi-value { font-size: 24px; color: #00e676; font-weight: bold; }
    
    /* بقية التنسيقات كما هي في الكود الأصلي لضمان الاستقرار */
    .screen { display: none; flex-direction: column; }
    .screen.active { display: flex; }
    /* ... (تم اختصار التنسيقات هنا لتوفير المساحة، استخدم التنسيقات الأصلية) ... */
  </style>
</head>
<body>
  <div class="app-container">
    <div id="measurements-screen" class="screen">
      <div class="sub-header">
        <button class="back-btn" onclick="navigateTo('home')">←</button>
        <h3>📏 القياسات والـ BMI</h3>
      </div>
      <div class="bmi-card" id="bmiDisplay">مؤشر كتلة الجسم (BMI): --</div>
      <div class="measure-inputs">
        <input type="number" id="weight" placeholder="⚖️ الوزن (كجم)" />
        <input type="number" id="height" placeholder="📏 الطول (سم) - للحساب الدقيق" />
        <button class="save-btn" onclick="saveMeasurement()">💾 حفظ القياس</button>
      </div>
      <div class="chart-container"><canvas id="weightChart"></canvas></div>
      <div class="history-list" id="historyList"></div>
    </div>
    </div>

  <script>
    // تطوير دالة الحفظ مع حساب BMI
    function saveMeasurement() {
      const weight = parseFloat(document.getElementById('weight').value);
      const height = parseFloat(document.getElementById('height').value) / 100;
      
      if (!weight || !height) return alert('⚠️ يرجى إدخال الوزن والطول');
      
      const bmi = (weight / (height * height)).toFixed(1);
      const data = JSON.parse(localStorage.getItem('fitness_measurements')) || [];
      
      data.push({ date: new Date().toLocaleDateString('ar-EG'), weight, bmi });
      localStorage.setItem('fitness_measurements', JSON.stringify(data));
      
      updateBMI(bmi);
      renderMeasurements();
      initChart();
    }

    function updateBMI(val) {
      document.getElementById('bmiDisplay').innerHTML = `مؤشر كتلة الجسم (BMI): <span class="bmi-value">${val}</span>`;
    }

    function deleteMeasurement(index) {
      let data = JSON.parse(localStorage.getItem('fitness_measurements'));
      data.splice(index, 1);
      localStorage.setItem('fitness_measurements', JSON.stringify(data));
      renderMeasurements();
      initChart();
    }

    // تعديل دالة العرض لتشمل زر الحذف
    function renderMeasurements() {
      const data = JSON.parse(localStorage.getItem('fitness_measurements')) || [];
      const container = document.getElementById('historyList');
      container.innerHTML = '<h4>📊 التاريخ</h4>';
      data.forEach((d, i) => {
        container.innerHTML += `
          <div class="history-item">
            <span>${d.date} | BMI: ${d.bmi}</span>
            <span>⚖️ ${d.weight}كجم <span class="btn-delete" onclick="deleteMeasurement(${i})">🗑️</span></span>
          </div>`;
      });
    }
    
    // ... (بقية المنطق البرمجي)
  </script>
</body>
</html>
