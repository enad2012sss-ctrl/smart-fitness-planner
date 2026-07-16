ممتاز! راح أعطيك تطبيق عالمي متكامل فيه كل الميزات المطلوبة:

· ✅ تمارين جري بكل أنواعه
· ✅ تمارين حديد
· ✅ تمارين وزن جسم
· ✅ تمارين فتنس
· ✅ صور متحركة (GIF)
· ✅ شرح مفصل لكل تمرين
· ✅ عدد الجولات والتكرارات
· ✅ نظام ذكاء اصطناعي (AI)
· ✅ لوحة تحكم متطورة
· ✅ إنجازات وتحديات
· ✅ واجهة احترافية

---

👇 هذا هو التطبيق الكامل (نسخ - لصق - تشغيل):

```python
import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import hashlib
import json
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import base64
import time
import re

# ============ إعدادات الصفحة ============
st.set_page_config(
    page_title="🏋️ Smart Fitness Planner Pro",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ قاعدة البيانات ============
def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  email TEXT,
                  height REAL,
                  weight REAL,
                  age INTEGER,
                  gender TEXT,
                  fitness_level TEXT,
                  goal TEXT,
                  daily_calories_goal INTEGER DEFAULT 2000,
                  weekly_workouts_goal INTEGER DEFAULT 4,
                  experience_level TEXT DEFAULT 'مبتدئ',
                  injuries TEXT,
                  created_at TIMESTAMP)''')
    
    # جدول التمارين
    c.execute('''CREATE TABLE IF NOT EXISTS exercises
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  category TEXT,
                  muscle_group TEXT,
                  equipment TEXT,
                  difficulty TEXT,
                  description TEXT,
                  image_url TEXT,
                  gif_url TEXT,
                  video_url TEXT,
                  default_sets INTEGER,
                  default_reps INTEGER,
                  rest_time INTEGER,
                  calories_per_hour INTEGER,
                  popularity INTEGER DEFAULT 0,
                  instructions TEXT)''')
    
    # جدول خطط التمارين
    c.execute('''CREATE TABLE IF NOT EXISTS workout_plans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  plan_name TEXT,
                  goal TEXT,
                  difficulty TEXT,
                  days_per_week INTEGER,
                  created_at TIMESTAMP,
                  is_active BOOLEAN DEFAULT 1,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # جدول تفاصيل الخطط
    c.execute('''CREATE TABLE IF NOT EXISTS plan_exercises
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  plan_id INTEGER,
                  exercise_id INTEGER,
                  day_of_week INTEGER,
                  sets INTEGER,
                  reps INTEGER,
                  weight REAL,
                  duration INTEGER,
                  rest_time INTEGER,
                  order_index INTEGER,
                  FOREIGN KEY (plan_id) REFERENCES workout_plans (id),
                  FOREIGN KEY (exercise_id) REFERENCES exercises (id))''')
    
    # جدول تتبع التمارين
    c.execute('''CREATE TABLE IF NOT EXISTS workout_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  exercise_id INTEGER,
                  plan_id INTEGER,
                  date TIMESTAMP,
                  sets_completed INTEGER,
                  reps_completed INTEGER,
                  weight_used REAL,
                  duration_minutes INTEGER,
                  calories_burned REAL,
                  perceived_difficulty INTEGER,
                  notes TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (exercise_id) REFERENCES exercises (id),
                  FOREIGN KEY (plan_id) REFERENCES workout_plans (id))''')
    
    # جدول الوجبات
    c.execute('''CREATE TABLE IF NOT EXISTS meals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  category TEXT,
                  calories REAL,
                  protein REAL,
                  carbs REAL,
                  fats REAL,
                  fiber REAL,
                  sugar REAL,
                  recipe TEXT,
                  image_url TEXT,
                  prep_time INTEGER,
                  difficulty TEXT)''')
    
    # جدول تتبع الطعام
    c.execute('''CREATE TABLE IF NOT EXISTS food_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  meal_id INTEGER,
                  date TIMESTAMP,
                  serving_size REAL,
                  calories_consumed REAL,
                  protein_consumed REAL,
                  carbs_consumed REAL,
                  fats_consumed REAL,
                  meal_type TEXT,
                  notes TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (meal_id) REFERENCES meals (id))''')
    
    # جدول الإنجازات
    c.execute('''CREATE TABLE IF NOT EXISTS achievements
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  achievement_type TEXT,
                  achievement_name TEXT,
                  description TEXT,
                  icon TEXT,
                  achieved_date TIMESTAMP,
                  points INTEGER,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # جدول التحديات اليومية
    c.execute('''CREATE TABLE IF NOT EXISTS daily_challenges
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  challenge_date DATE,
                  challenge_type TEXT,
                  challenge_name TEXT,
                  target_value INTEGER,
                  current_value INTEGER DEFAULT 0,
                  is_completed BOOLEAN DEFAULT 0,
                  reward_points INTEGER,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # جدول تقدم المستخدم
    c.execute('''CREATE TABLE IF NOT EXISTS user_progress
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  date DATE,
                  weight REAL,
                  body_fat REAL,
                  muscle_mass REAL,
                  bmi REAL,
                  notes TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # جدول توصيات AI
    c.execute('''CREATE TABLE IF NOT EXISTS ai_recommendations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  recommendation_type TEXT,
                  recommendation_text TEXT,
                  confidence_score REAL,
                  created_at TIMESTAMP,
                  is_applied BOOLEAN DEFAULT 0,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # ========== إضافة التمارين ==========
    c.execute("SELECT COUNT(*) FROM exercises")
    if c.fetchone()[0] == 0:
        exercises_data = [
            # تمارين الجري
            ('جري سريع (Sprint)', 'جري', 'أرجل', 'وزن جسم', 'متقدم',
             'جري بأقصى سرعة لمسافة قصيرة لتطوير السرعة والقوة الانفجارية.',
             '🏃', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 5, 4, 90, 800, 0,
             '1. قف في وضع البداية\n2. ابدأ الجري بأقصى سرعة لمسافة 50-100 متر\n3. توقف واسترح 60-90 ثانية\n4. كرر 5-8 مرات'),
            
            ('جري تحمل (المسافات الطويلة)', 'جري', 'أرجل', 'وزن جسم', 'مبتدئ',
             'جري بسرعة ثابتة لمسافات طويلة لتحسين اللياقة القلبية والتنفسية.',
             '🏃', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 1, 1, 60, 600, 0,
             '1. ابدأ بجري خفيف\n2. حافظ على سرعة ثابتة\n3. اركض لمسافة 3-5 كم\n4. أنهِ بجري بطيء للتهدئة'),
            
            ('جري فترات (Interval)', 'جري', 'أرجل', 'وزن جسم', 'متقدم',
             'تبديل بين الجري السريع والبطيء لتحسين اللياقة والتحمل.',
             '🏃', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 8, 1, 60, 700, 0,
             '1. اركض بسرعة لمدة دقيقة\n2. امشِ أو اركض ببطء لمدة دقيقتين\n3. كرر 6-8 مرات\n4. أنهِ بتهدئة'),
            
            ('جري مرتفعات (Hills)', 'جري', 'أرجل', 'وزن جسم', 'متقدم',
             'جري على منحدرات لتقوية عضلات الأرجل وزيادة التحمل.',
             '⛰️', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 6, 1, 90, 750, 0,
             '1. ابحث عن منحدر مناسب\n2. اركض لأعلى المنحدر\n3. انزل مشياً للراحة\n4. كرر 6-8 مرات'),
            
            ('جري خفيف (ركض)', 'جري', 'أرجل', 'وزن جسم', 'مبتدئ',
             'ركض بسرعة خفيفة للإحماء أو التهدئة.',
             '🏃', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 1, 1, 30, 400, 0,
             '1. ابدأ بجري خفيف\n2. حافظ على تنفس منتظم\n3. استمر 10-15 دقيقة'),
            
            ('جري متعرج (Shuttle Run)', 'جري', 'أرجل', 'وزن جسم', 'متوسط',
             'جري بين نقطتين مع تغيير الاتجاه بسرعة لتحسين الرشاقة.',
             '🏃', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 6, 1, 60, 650, 0,
             '1. ضع نقطتين على مسافة 20 متر\n2. اركض بينهما بسرعة\n3. المس الأرض عند كل نقطة\n4. كرر 6-8 مرات'),
            
            # تمارين الحديد
            ('ضغط الصدر بالبار (Bench Press)', 'حديد', 'صدر', 'بار', 'متوسط',
             'تمرين أساسي لتقوية عضلات الصدر والكتفين والذراعين.',
             '🏋️', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 4, 10, 90, 500, 0,
             '1. استلقِ على مقعد الضغط\n2. امسك البار بعرض الكتفين\n3. أنزل البار بصدرك\n4. ادفع البار لأعلى\n5. كرر 3-4 مجموعات'),
            
            ('ضغط الصدر بالدمبل', 'حديد', 'صدر', 'دمبل', 'مبتدئ',
             'تمرين ممتاز للصدر مع نطاق حركة أوسع.',
             '🏋️', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 4, 12, 90, 450, 0,
             '1. استلقِ على المقعد مع دمبل في كل يد\n2. ارفع الدمبل لأعلى مع تمديد الذراعين\n3. أنزل الدمبل ببطء\n4. كرر 3-4 مجموعات'),
            
            ('سحب أمامي (Lat Pulldown)', 'حديد', 'ظهر', 'جهاز', 'مبتدئ',
             'تمرين لتقوية عضلات الظهر العريضة.',
             '🏋️', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 4, 12, 90, 450, 0,
             '1. اجلس على جهاز السحب\n2. امسك البار بعرض الكتفين\n3. اسحب البار لأسفل حتى صدرك\n4. ارجع ببطء للأعلى\n5. كرر 3-4 مجموعات'),
            
            ('قرفصاء بالبار (Barbell Squat)', 'حديد', 'أرجل', 'بار', 'متقدم',
             'تمرين شامل لكامل الجسم يركز على الأرجل والأرداف.',
             '🏋️', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 4, 10, 120, 600, 0,
             '1. ضع البار على كتفيك\n2. انزل للأسفل كأنك تجلس\n3. حافظ على استقامة الظهر\n4. ارفع لأعلى\n5. كرر 3-4 مجموعات'),
            
            ('تجديل البايسبس', 'حديد', 'ذراع', 'بار', 'مبتدئ',
             'تمرين لتقوية عضلات البايسبس (العضلة الأمامية للذراع).',
             '💪', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 4, 12, 60, 300, 0,
             '1. امسك البار بقبضة سفلية\n2. اثنِ ذراعيك لأعلى\n3. أنزل ببطء\n4. كرر 3-4 مجموعات'),
            
            ('تجديل الترايسيبس', 'حديد', 'ذراع', 'جهاز', 'مبتدئ',
             'تمرين لتقوية العضلة الخلفية للذراع.',
             '💪', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 4, 12, 60, 300, 0,
             '1. اسحب الحبل لأسفل مع تمديد الذراعين\n2. اثبت للحظة\n3. ارجع ببطء\n4. كرر 3-4 مجموعات'),
            
            # تمارين وزن الجسم
            ('ضغط (Push-up)', 'وزن جسم', 'صدر', 'وزن جسم', 'مبتدئ',
             'تمرين كلاسيكي لتقوية الصدر والذراعين.',
             '🤸', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 15, 60, 400, 0,
             '1. استلقِ على بطنك\n2. ارفع جسمك بيديك\n3. أنزل بصدرك للأرض\n4. ادفع للأعلى\n5. كرر 3 مجموعات'),
            
            ('ضغط واسع', 'وزن جسم', 'صدر', 'وزن جسم', 'متوسط',
             'نفس الضغط مع تباعد اليدين لتركيز أكثر على الصدر الخارجي.',
             '🤸', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 12, 60, 400, 0,
             '1. افتح يديك بعرض أوسع\n2. أنزل للأسفل\n3. ادفع للأعلى\n4. كرر 3 مجموعات'),
            
            ('سحب (Pull-up)', 'وزن جسم', 'ظهر', 'وزن جسم', 'متوسط',
             'تمرين ممتاز لتقوية الظهر والذراعين.',
             '🤸', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 8, 90, 450, 0,
             '1. علق على البار\n2. اسحب جسمك لأعلى\n3. أنزل ببطء\n4. كرر 3 مجموعات'),
            
            ('قرفصاء (Squat)', 'وزن جسم', 'أرجل', 'وزن جسم', 'مبتدئ',
             'تمرين أساسي لتقوية الأرجل والأرداف.',
             '🦵', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 20, 60, 350, 0,
             '1. قف مع فتح القدمين بعرض الكتفين\n2. انزل للأسفل كأنك تجلس\n3. حافظ على استقامة الظهر\n4. ارفع لأعلى\n5. كرر 3 مجموعات'),
            
            ('تمرين البطن (Crunch)', 'وزن جسم', 'بطن', 'وزن جسم', 'مبتدئ',
             'تمرين لتقوية عضلات البطن العلوية.',
             '💪', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 20, 30, 200, 0,
             '1. استلقِ على ظهرك\n2. اثنِ ركبتيك\n3. ارفع كتفيك عن الأرض\n4. انزل ببطء\n5. كرر 3 مجموعات'),
            
            ('تمرين البلانك (Plank)', 'وزن جسم', 'بطن', 'وزن جسم', 'مبتدئ',
             'تمرين لتقوية الجذع والاستقرار.',
             '💪', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 30, 45, 250, 0,
             '1. استلقِ على بطنك\n2. ارفع جسمك على المرفقين وأصابع القدمين\n3. حافظ على استقامة الجسم\n4. اثبت 30-60 ثانية\n5. كرر 3 مرات'),
            
            # تمارين الفتنس
            ('بيربي (Burpee)', 'فتنس', 'كامل الجسم', 'وزن جسم', 'متوسط',
             'تمرين شامل لكامل الجسم يجمع بين القوة والكارديو.',
             '🔥', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 10, 90, 600, 0,
             '1. قف بشكل مستقيم\n2. انزل للقرفصاء وضع يديك على الأرض\n3. اقفز للخلف لوضعية الضغط\n4. اقفز للأمام\n5. اقفز لأعلى مع التصفيق\n6. كرر 3 مجموعات'),
            
            ('متسلق الجبال (Mountain Climber)', 'فتنس', 'كامل الجسم', 'وزن جسم', 'متوسط',
             'تمرين كارديو ممتاز لتقوية القلب والجذع.',
             '⛰️', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 20, 30, 500, 0,
             '1. في وضعية الضغط\n2. اسحب ركبة واحدة تجاه صدرك\n3. بدلها بالركبة الأخرى بسرعة\n4. استمر 30-60 ثانية\n5. كرر 3 مجموعات'),
            
            ('قفزة القرفصاء', 'فتنس', 'أرجل', 'وزن جسم', 'متوسط',
             'تمرين انفجاري لتقوية الأرجل وزيادة القوة.',
             '🦵', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 15, 60, 500, 0,
             '1. قف بشكل مستقيم\n2. انزل للقرفصاء\n3. اقفز لأعلى بأقصى قوة\n4. اهبط برفق\n5. كرر 3 مجموعات'),
            
            ('تمارين الحبل (Jump Rope)', 'فتنس', 'كامل الجسم', 'حبل', 'مبتدئ',
             'تمرين كارديو ممتاز لحرق السعرات وتحسين التنسيق.',
             '🪢', 'https://media.giphy.com/media/3o7abKhOpu0N9H8l3K/giphy.gif', '', 3, 60, 30, 700, 0,
             '1. امسك الحبل من طرفيه\n2. ابدأ بالقفز فوق الحبل\n3. حافظ على إيقاع منتظم\n4. استمر 60 ثانية\n5. كرر 3 مجموعات'),
        ]
        
        c.executemany("""INSERT INTO exercises 
                        (name, category, muscle_group, equipment, difficulty, description, 
                         image_url, gif_url, video_url, default_sets, default_reps, 
                         rest_time, calories_per_hour, popularity, instructions) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", exercises_data)
        conn.commit()
    
    # ========== إضافة وجبات صحية ==========
    c.execute("SELECT COUNT(*) FROM meals")
    if c.fetchone()[0] == 0:
        meals_data = [
            ('شوفان مع فواكه', 'إفطار', 350, 12, 50, 8, 6, 15,
             'اطبخ الشوفان مع الحليب وأضف الفواكه المقطعة.', '🥣', 10, 'مبتدئ'),
            
            ('سلطة الدجاج المشوي', 'غداء', 450, 35, 20, 15, 8, 5,
             'قطع الدجاج المشوي فوق السلطة الخضراء.', '🥗', 20, 'مبتدئ'),
            
            ('سمك السلمون مع الخضار', 'غداء', 500, 40, 15, 25, 10, 3,
             'اشوي السلمون مع الخضار المشكلة.', '🐟', 25, 'متوسط'),
            
            ('زبادي يوناني مع عسل', 'وجبة خفيفة', 200, 20, 15, 8, 0, 20,
             'اخلط الزبادي مع العسل والمكسرات.', '🥛', 5, 'مبتدئ'),
            
            ('عصير البروتين الأخضر', 'وجبة خفيفة', 250, 25, 20, 5, 8, 10,
             'اخلط السبانخ والموز ومسحوق البروتين.', '🥤', 5, 'مبتدئ'),
            
            ('أرز بني مع دجاج', 'عشاء', 550, 35, 55, 15, 8, 5,
             'اطبخ الأرز البني مع الدجاج والخضار.', '🍚', 30, 'متوسط'),
        ]
        
        c.executemany("""INSERT INTO meals 
                        (name, category, calories, protein, carbs, fats, fiber, sugar, 
                         recipe, image_url, prep_time, difficulty) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", meals_data)
        conn.commit()
    
    conn.close()

# ============ وظائف المستخدم ============
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, email, height, weight, age, gender, fitness_level, goal):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO users 
                     (username, password, email, height, weight, age, gender, fitness_level, goal, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (username, hash_password(password), email, height, weight, age, gender, fitness_level, goal, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_user_profile(user_id, height, weight, age, gender, fitness_level, goal, daily_calories_goal, weekly_workouts_goal):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""UPDATE users 
                 SET height = ?, weight = ?, age = ?, gender = ?, fitness_level = ?, goal = ?,
                     daily_calories_goal = ?, weekly_workouts_goal = ?
                 WHERE id = ?""",
              (height, weight, age, gender, fitness_level, goal, daily_calories_goal, weekly_workouts_goal, user_id))
    conn.commit()
    conn.close()

# ============ وظائف التمارين ============
def get_all_exercises():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises")
    exercises = c.fetchall()
    conn.close()
    return exercises

def get_exercise_by_id(exercise_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,))
    exercise = c.fetchone()
    conn.close()
    return exercise

def search_exercises(search_term):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM exercises 
                 WHERE name LIKE ? OR muscle_group LIKE ? OR category LIKE ? 
                 OR description LIKE ?""",
              (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    exercises = c.fetchall()
    conn.close()
    return exercises

def filter_exercises(category=None, muscle_group=None, difficulty=None, equipment=None):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    query = "SELECT * FROM exercises WHERE 1=1"
    params = []
    
    if category and category != "الكل":
        query += " AND category = ?"
        params.append(category)
    if muscle_group and muscle_group != "الكل":
        query += " AND muscle_group = ?"
        params.append(muscle_group)
    if difficulty and difficulty != "الكل":
        query += " AND difficulty = ?"
        params.append(difficulty)
    if equipment and equipment != "الكل":
        query += " AND equipment = ?"
        params.append(equipment)
    
    query += " ORDER BY popularity DESC"
    
    c.execute(query, params)
    exercises = c.fetchall()
    conn.close()
    return exercises

# ============ وظائف خطط التمارين ============
def create_workout_plan(user_id, plan_name, goal, difficulty, days_per_week, exercises_data):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    c.execute("""INSERT INTO workout_plans 
                 (user_id, plan_name, goal, difficulty, days_per_week, created_at) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (user_id, plan_name, goal, difficulty, days_per_week, datetime.now()))
    plan_id = c.lastrowid
    
    for i, ex in enumerate(exercises_data):
        c.execute("""INSERT INTO plan_exercises 
                     (plan_id, exercise_id, day_of_week, sets, reps, weight, duration, rest_time, order_index) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (plan_id, ex['exercise_id'], ex.get('day_of_week', 1), 
                   ex.get('sets', 3), ex.get('reps', 10), ex.get('weight', 0),
                   ex.get('duration', 0), ex.get('rest_time', 60), i))
    
    conn.commit()
    conn.close()
    return plan_id

def get_user_workout_plans(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM workout_plans WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    plans = c.fetchall()
    conn.close()
    return plans

def get_plan_exercises(plan_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""SELECT pe.*, e.name, e.category, e.muscle_group, e.image_url, e.gif_url, e.instructions
                 FROM plan_exercises pe 
                 JOIN exercises e ON pe.exercise_id = e.id 
                 WHERE pe.plan_id = ?
                 ORDER BY pe.order_index""", (plan_id,))
    exercises = c.fetchall()
    conn.close()
    return exercises

# ============ وظائف تتبع التمارين ============
def log_workout(user_id, exercise_id, plan_id, sets_completed, reps_completed, weight_used, 
                duration_minutes, calories_burned, perceived_difficulty, notes):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""INSERT INTO workout_logs 
                 (user_id, exercise_id, plan_id, date, sets_completed, reps_completed, 
                  weight_used, duration_minutes, calories_burned, perceived_difficulty, notes) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (user_id, exercise_id, plan_id, datetime.now(), sets_completed, reps_completed,
               weight_used, duration_minutes, calories_burned, perceived_difficulty, notes))
    conn.commit()
    conn.close()

def get_workout_history(user_id, days=30):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""SELECT wl.*, e.name, e.category 
                 FROM workout_logs wl 
                 JOIN exercises e ON wl.exercise_id = e.id 
                 WHERE wl.user_id = ? AND wl.date >= ?
                 ORDER BY wl.date DESC""", (user_id, datetime.now() - timedelta(days=days)))
    logs = c.fetchall()
    conn.close()
    return logs

def get_workout_stats(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM workout_logs WHERE user_id = ?", (user_id,))
    total_workouts = c.fetchone()[0]
    
    c.execute("SELECT SUM(calories_burned) FROM workout_logs WHERE user_id = ?", (user_id,))
    total_calories = c.fetchone()[0] or 0
    
    c.execute("SELECT COUNT(DISTINCT DATE(date)) FROM workout_logs WHERE user_id = ?", (user_id,))
    total_days = c.fetchone()[0]
    
    c.execute("SELECT AVG(perceived_difficulty) FROM workout_logs WHERE user_id = ?", (user_id,))
    avg_difficulty = c.fetchone()[0] or 0
    
    conn.close()
    return {
        'total_workouts': total_workouts,
        'total_calories': total_calories,
        'total_days': total_days,
        'avg_difficulty': avg_difficulty
    }

# ============ وظائف الطعام ============
def get_all_meals():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM meals")
    meals = c.fetchall()
    conn.close()
    return meals

def log_meal(user_id, meal_id, serving_size, calories_consumed, protein_consumed, carbs_consumed, fats_consumed, meal_type, notes):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""INSERT INTO food_logs 
                 (user_id, meal_id, date, serving_size, calories_consumed, protein_consumed, 
                  carbs_consumed, fats_consumed, meal_type, notes) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (user_id, meal_id, datetime.now(), serving_size, calories_consumed, 
               protein_consumed, carbs_consumed, fats_consumed, meal_type, notes))
    conn.commit()
    conn.close()

def get_food_logs(user_id, days=7):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM food_logs 
                 WHERE user_id = ? AND date >= ?
                 ORDER BY date DESC""", (user_id, datetime.now() - timedelta(days=days)))
    logs = c.fetchall()
    conn.close()
    return logs

def get_nutrition_stats(user_id, days=7):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    c.execute("""SELECT SUM(calories_consumed) 
                 FROM food_logs 
                 WHERE user_id = ? AND date >= ?
                 GROUP BY DATE(date)""", (user_id, datetime.now() - timedelta(days=days)))
    daily_calories = [row[0] or 0 for row in c.fetchall()]
    
    c.execute("""SELECT AVG(calories_consumed) 
                 FROM food_logs 
                 WHERE user_id = ? AND date >= ?""", (user_id, datetime.now() - timedelta(days=days)))
    avg_calories = c.fetchone()[0] or 0
    
    conn.close()
    return {
        'daily_calories': daily_calories,
        'avg_calories': avg_calories
    }

# ============ وظائف الإنجازات ============
def add_achievement(user_id, achievement_type, achievement_name, description, icon, points):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    
    # تحقق من وجود الإنجاز مسبقاً
    c.execute("SELECT * FROM achievements WHERE user_id = ? AND achievement_name = ?", (user_id, achievement_name))
    if not c.fetchone():
        c.execute("""INSERT INTO achievements 
                     (user_id, achievement_type, achievement_name, description, icon, achieved_date, points) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (user_id, achievement_type, achievement_name, description, icon, datetime.now(), points))
        conn.commit()
    conn.close()

def get_user_achievements(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT * FROM achievements WHERE user_id = ? ORDER BY achieved_date DESC", (user_id,))
    achievements = c.fetchall()
    conn.close()
    return achievements

def get_total_points(user_id):
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute("SELECT SUM(p
```
