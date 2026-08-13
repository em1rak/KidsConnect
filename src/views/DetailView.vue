<template>
  <div class="content-wrapper">
    <!-- Верхняя навигация -->
    <div class="top-nav">
      <router-link to="/" class="nav-btn">
        <img src="/image/Group3302.svg" alt="Back" class="icon-sm" /> Назад
      </router-link>
      <button class="nav-btn">
        На карте <img src="/image/Group.svg" alt="Map" class="icon-sm" />
      </button>
    </div>

    <!-- Заголовок страницы -->
    <h1 class="page-title">Лёгкая атлетика (в Юбилейном мкр.)</h1>

    <!-- Главная карточка с деталями -->
    <section class="detail-section">
      <div class="detail-main">
        <!-- Картинка (Исправлено: динамический биндинг стиля + функция getImageUrl) -->
        <div 
          class="detail-image" 
          :style="{ backgroundImage: `url(${getImageUrl('/image/image.png')})` }"
        ></div>

        <div class="detail-info">
          <div class="detail-badges">
            <span class="badge badge-outline">Набор открыт</span>
            <span class="badge badge-free font-semibold">Бесплатно</span>
          </div>

          <div class="detail-info-rows">
            <div class="info-row">
              <img src="/image/Frame397.svg" class="icon" alt="age" />
              <span>10-18 лет</span>
            </div>
            <div class="info-row">
              <img src="/image/layer1.svg" class="icon" alt="address" />
              <span>г. Иркутск, Юбилейный мкр., стр. 49/1</span>
            </div>
            <div class="info-row">
              <img src="/image/Group.svg" class="icon" alt="location" />
              <span class="font-medium">ФОК “Юбилейный”</span>
            </div>
          </div>

          <button class="btn-main" @click="handleEnroll">Записаться</button>
        </div>
      </div>
    </section>

    <!-- Секция: Группы и Расписание  -->
    <section class="detail-section">
      <div class="groups-schedule-wrapper">
        <!-- Левая колонка: Группы -->
        <div class="groups-column">
          <h2 class="section-title">ГРУППЫ</h2>
          <h3 class="group-subtitle">Этап начальной подготовки</h3>
          <div class="group-stats">
            <div class="stat-item">
              <img src="/image/educationcapsvgrepocom1.svg" class="icon" alt="teacher" />
              <span>Петрова Елена Александровна</span>
            </div>
            <div class="stat-item">
              <img src="/image/GroupMan.svg" class="icon" alt="spots" />
              <span>15 из 20</span>
            </div>
            <div class="stat-item">
              <img src="/image/Group331.svg" class="icon" alt="duration" />
              <span>12 месяцев</span>
            </div>
          </div>
        </div>

        <!-- Правая колонка Расписание -->
        <div class="schedule-column">
          <h2 class="section-title">РАСПИСАНИЕ ЗАНЯТИЙ</h2>
          <div class="schedule-grid">
            <div class="schedule-row">
              <img src="/image/clock_time_icon_1429031.svg" class="icon" alt="clock" />
              <span class="schedule-days">Пн, Вт, Чт, Сб</span>
            </div>
            <div class="schedule-row">
              <img src="/image/clock_time_icon_1429031.svg" class="icon" alt="clock" />
              <span class="schedule-days">Пн, Вт, Чт, Сб</span>
              <div class="time-slots-group">
                <span class="time-slot">08:00 - 10:00</span>
                <span class="time-slot">18:00 - 19:30</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Секция Описание -->
    <section class="detail-section">
      <h2 class="section-title">ОПИСАНИЕ</h2>
      <p class="description-text">
        Легкая атлетика - олимпийский вид спорта, объединяющий беговые виды, спортивную ходьбу , технические виды (прыжки и метания), многоборья, пробеги (бег по шоссе), кроссы (бег по пересеченной местности).
      </p>
    </section>

    <!-- Секция Содержание программы (Аккордеон) -->
    <section class="detail-section accordion-section">
      <h2 class="section-title">СОДЕРЖАНИЕ ПРОГРАММЫ</h2>

      <div class="accordion-container">
        <!-- Уровень 1 -->
        <div 
          class="accordion-item" 
          :class="{ active: openAccordions.includes(1) }"
          @click="toggleAccordion(1)"
        >
          <div class="accordion-header">
            <h3 class="accordion-title">Базовый уровень</h3>
            <img src="/image/Group3300.svg" class="chevron" alt="chevron" />
          </div>
          <div class="accordion-content">
            <p>Базовый уровень сложности первый-второй год обучения, 252 часа.</p>
            <ul>
              <li>Обязательные предметы области (количество часов – 15);</li>
              <li>Вариативные предметные области (количество часов −10);</li>
              <li>Теория (количество часов −5);</li>
              <li>Практика (количество часов − 216);</li>
              <li>Самостоятельная работа (количество часов −2);</li>
              <li>Аттестация (количество часов − 4).</li>
            </ul>
            <p>Базовый уровень сложности третий-четвертый год обучения, 416 часов.</p>
            <p>Обязательные предметы области (количество часов − 25);</p>
            <ul>
              <li>Вариативные предметные области (количество часов − 15);</li>
              <li>Теория (количество часов − 7);</li>
              <li>Практика (количество часов − 361);</li>
              <li>Самостоятельная работа (количество часов − 4);</li>
              <li>Аттестация (количество часов − 4).</li>
            </ul>
            <p>Базовый уровень сложности пятый-шестой год обучения, 420 часов.</p>
            <ul>
              <li>Обязательные предметы области (количество часов − 27);</li>
              <li>Вариативные предметные области (количество часов − 15);</li>
              <li>Теория (количество часов − 8);</li>
              <li>Практика (количество часов − 360);</li>
              <li>Самостоятельная работа (количество часов − 6);</li>
              <li>Аттестация (количество часов − 4).</li>
            </ul>
          </div>
        </div>

        <!-- Уровень 2 -->
        <div 
          class="accordion-item" 
          :class="{ active: openAccordions.includes(2) }"
          @click="toggleAccordion(2)"
        >
          <div class="accordion-header">
            <h3 class="accordion-title">Углубленный уровень</h3>
            <img src="/image/Group3300.svg" class="chevron" alt="chevron" />
          </div>
          <div class="accordion-content">
            <p>Углубленный уровень сложности первый-второй год обучения, 504.</p>
            <ul>
              <li>Обязательные предметы области (количество часов − 30);</li>
              <li>Вариативные предметные области (количество часов − 20);</li>
              <li>Теория (количество часов − 9);</li>
              <li>Практика (количество часов − 433);</li>
              <li>Самостоятельная работа (количество часов − 8);</li>
              <li>Аттестация (количество часов − 4).</li>
            </ul>
            <p>Углубленный уровень сложности третий-четвертый год обучения, 588 часов.</p>
            <ul>
              <li>Обязательные предметы области (количество часов − 35);</li>
              <li>Вариативные предметные области (количество часов − 23);</li>
              <li>Теория (количество часов − 10);</li>
              <li>Практика (количество часов − 506);</li>
              <li>Самостоятельная работа (количество часов − 10);</li>
              <li>Аттестация (количество часов − 4).</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref } from 'vue'

function getImageUrl(path) {
  if (!path) return ''
  return import.meta.env.BASE_URL + path.replace(/^\//, '')
}

// Список открытых секций аккордеона программы
const openAccordions = ref([])

// Переключение раскрытия блока аккордеона по ID
function toggleAccordion(id) {
  const index = openAccordions.value.indexOf(id)
  if (index > -1) {
    openAccordions.value.splice(index, 1)
  } else {
    openAccordions.value.push(id)
  }
}

// Обработчик нажатия на кнопку "Записаться"
function handleEnroll() {
  alert('Заявка на запись отправлена!')
}
</script>