<template>
  <div class="content-wrapper">
    <!-- Верхняя навигация -->
    <div class="top-nav">
      <router-link to="/" class="nav-btn">
        <img :src="getImageUrl('/image/Group3302.svg')" alt="Back" class="icon-sm" /> Назад
      </router-link>
      <button class="nav-btn">
        На карте <img :src="getImageUrl('/image/Group.svg')" alt="Map" class="icon-sm" />
      </button>
    </div>

    <!-- Заголовок страницы -->
    <h1 class="page-title">{{ activity?.title || 'Лёгкая атлетика (в Юбилейном мкр.)' }}</h1>

    <!-- Главная карточка с деталями -->
    <section class="detail-section">
      <div class="detail-main">
        <!-- Картинка -->
        <div 
          class="detail-image" 
          :style="{ backgroundImage: `url('${getImageUrl(activity?.image_url || '/image/Group330.svg')}')` }"
        ></div>

        <div class="detail-info">
          <div class="detail-badges">
            <span class="badge badge-outline" v-if="activity?.is_first_free">Первое бесплатно</span>
            <span class="badge badge-outline" v-else>Набор открыт</span>
            <span class="badge badge-free font-semibold">{{ activity?.is_free ? 'Бесплатно' : (activity?.price || 'Бесплатно') }}</span>
          </div>

          <div class="detail-info-rows">
            <div class="info-row">
              <img :src="getImageUrl('/image/Frame397.svg')" class="icon" alt="age" />
              <span>{{ activity?.age_group || '10-18 лет' }}</span>
            </div>
            <div class="info-row">
              <img :src="getImageUrl('/image/layer1.svg')" class="icon" alt="address" />
              <span>{{ activity?.address || 'г. Иркутск, Юбилейный мкр., стр. 49/1' }}</span>
            </div>
            <div class="info-row" v-if="activity?.place">
              <img :src="getImageUrl('/image/Group.svg')" class="icon" alt="location" />
              <span class="font-medium">{{ activity.place }}</span>
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
          <h3 class="group-subtitle">{{ activity?.group_subtitle || 'Этап начальной подготовки' }}</h3>
          <div class="group-stats">
            <div class="stat-item" v-if="activity?.teacher_name">
              <img :src="getImageUrl('/image/educationcapsvgrepocom1.svg')" class="icon" alt="teacher" />
              <span>{{ activity.teacher_name }}</span>
            </div>
            <div class="stat-item" v-if="activity?.spots_info">
              <img :src="getImageUrl('/image/GroupMan.svg')" class="icon" alt="spots" />
              <span>{{ activity.spots_info }}</span>
            </div>
            <div class="stat-item" v-if="activity?.duration">
              <img :src="getImageUrl('/image/Group331.svg')" class="icon" alt="duration" />
              <span>{{ activity.duration }}</span>
            </div>
          </div>
        </div>

        <!-- Правая колонка Расписание -->
        <div class="schedule-column">
          <h2 class="section-title">РАСПИСАНИЕ ЗАНЯТИЙ</h2>
          <div class="schedule-grid">
            <div class="schedule-row">
              <img :src="getImageUrl('/image/clock_time_icon_1429031.svg')" class="icon" alt="clock" />
              <span class="schedule-days">{{ parsedSchedule.days }}</span>
              <span 
                v-for="(slot, idx) in parsedSchedule.slots" 
                :key="idx" 
                class="time-slot"
              >
                {{ slot }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Секция Описание -->
    <section class="detail-section">
      <h2 class="section-title">ОПИСАНИЕ</h2>
      <p class="description-text">
        {{ activity?.description || 'Легкая атлетика - олимпийский вид спорта, объединяющий беговые виды, спортивную ходьбу, технические виды (прыжки и метания), многоборья, пробеги (бег по шоссе), кроссы (бег по пересеченной местности).' }}
      </p>
    </section>

    <!-- Секция Содержание программы (Аккордеон) -->
    <section class="detail-section accordion-section">
      <h2 class="section-title">СОДЕРЖАНИЕ ПРОГРАММЫ</h2>

      <div class="accordion-container">
        <!-- Уровень 1: Базовый уровень -->
        <div 
          class="accordion-item" 
          :class="{ active: openAccordions.includes(1) }"
          @click="toggleAccordion(1)"
        >
          <div class="accordion-header">
            <h3 class="accordion-title">Базовый уровень</h3>
            <img :src="getImageUrl('/image/Group3300.svg')" class="chevron" alt="chevron" />
          </div>
          <div class="accordion-content">
            <div v-if="activity?.base_level_info" class="formatted-text">
              {{ activity.base_level_info }}
            </div>
            <template v-else>
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
              <ul>
                <li>Обязательные предметы области (количество часов − 25);</li>
                <li>Вариативные предметные области (количество часов − 15);</li>
                <li>Теория (количество часов − 7);</li>
                <li>Практика (количество часов − 4);</li>
                <li>Самостоятельная работа (количество часов − 4);</li>
                <li>Аттестация (количество часов − 4).</li>
              </ul>
            </template>
          </div>
        </div>

        <!-- Уровень 2: Углубленный уровень -->
        <div 
          class="accordion-item" 
          :class="{ active: openAccordions.includes(2) }"
          @click="toggleAccordion(2)"
        >
          <div class="accordion-header">
            <h3 class="accordion-title">Углубленный уровень</h3>
            <img :src="getImageUrl('/image/Group3300.svg')" class="chevron" alt="chevron" />
          </div>
          <div class="accordion-content">
            <div v-if="activity?.advanced_level_info" class="formatted-text">
              {{ activity.advanced_level_info }}
            </div>
            <template v-else>
              <p>Углубленный уровень сложности первый-второй год обучения, 504 часа.</p>
              <ul>
                <li>Обязательные предметы области (количество часов − 30);</li>
                <li>Вариативные предметные области (количество часов − 20);</li>
                <li>Теория (количество часов − 9);</li>
                <li>Практика (количество часов − 433);</li>
                <li>Самостоятельная работа (количество часов − 8);</li>
                <li>Аттестация (количество часов − 4).</li>
              </ul>
            </template>
          </div>
        </div>
      </div>
    </section>

    <!-- Модальное окно записи -->
    <transition name="fade">
      <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
        <div class="modal-card">
          <div class="modal-header">
            <h3 class="modal-title">Запись в кружок</h3>
            <button class="btn-close" @click="showModal = false" aria-label="Закрыть">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <div v-if="successMsg" class="success-banner">
            <p>{{ successMsg }}</p>
            <router-link to="/profile" class="btn-view-profile">Перейти в профиль</router-link>
          </div>

          <form v-else @submit.prevent="submitBooking" class="modal-form">
            <p class="modal-subtitle">Заполните данные для отправки заявки</p>

            <div class="form-group">
              <label class="form-label">ФИО Родителя</label>
              <input 
                v-model="form.parent_name" 
                type="text" 
                class="form-input" 
                placeholder="например, Иванов Иван Иванович" 
                required 
              />
            </div>

            <div class="form-group">
              <label class="form-label">Имя ребенка</label>
              <input 
                v-model="form.child_name" 
                type="text" 
                class="form-input" 
                placeholder="например, Алексей" 
                required 
              />
            </div>

            <div class="form-group">
              <label class="form-label">Возраст ребенка</label>
              <input 
                v-model.number="form.child_age" 
                type="number" 
                min="1" 
                max="18" 
                class="form-input" 
                placeholder="например, 10" 
                required 
              />
            </div>

            <div class="form-group">
              <label class="form-label">Контактный телефон</label>
              <input 
                v-model="form.phone" 
                type="tel" 
                class="form-input" 
                placeholder="+7 (900) 000-00-00" 
                required 
              />
            </div>

            <div v-if="errorMsg" class="error-banner">
              {{ errorMsg }}
            </div>

            <div class="modal-actions">
              <button type="button" class="btn-cancel" @click="showModal = false">Отмена</button>
              <button type="submit" class="btn-submit" :disabled="isSubmitting">
                {{ isSubmitting ? 'Отправка...' : 'Отправить заявку' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { authStore } from '../authStore'
import api from '../api'

const route = useRoute()
const activityId = computedId()

function computedId() {
  const q = route.query.id
  return q ? Number(q) : 1
}

const activity = ref(null)
const loadingActivity = ref(true)

const parsedSchedule = computed(() => {
  const scheduleStr = activity.value?.schedule
  if (!scheduleStr) {
    return {
      days: 'Пн, Вт, Чт, Сб',
      slots: ['08:00 - 10:00', '18:00 - 19:30']
    }
  }

  const firstDigitMatch = scheduleStr.match(/\d/)
  if (firstDigitMatch && firstDigitMatch.index > 0) {
    const daysPart = scheduleStr.slice(0, firstDigitMatch.index).trim().replace(/,\s*$/, '')
    const timePart = scheduleStr.slice(firstDigitMatch.index).trim()

    const slots = timePart.split(',').map(s => s.trim()).filter(Boolean)
    return {
      days: daysPart || 'Расписание по запросу',
      slots: slots
    }
  }

  return {
    days: scheduleStr.trim(),
    slots: []
  }
})

onMounted(async () => {
  try {
    activity.value = await api.getActivityById(activityId)
  } catch (e) {
    console.warn('Используются стандартные данные кружка:', e)
  } finally {
    loadingActivity.value = false
  }
})

function getImageUrl(path) {
  if (!path) return import.meta.env.BASE_URL + 'image/Group330.svg'
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  if (path.startsWith('/uploads/') || path.startsWith('/media/') || path.startsWith('uploads/')) {
    return 'http://127.0.0.1:8000/' + path.replace(/^\//, '')
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}

// Список открытых секций аккордеона программы
const openAccordions = ref([1])

function toggleAccordion(id) {
  const index = openAccordions.value.indexOf(id)
  if (index > -1) {
    openAccordions.value.splice(index, 1)
  } else {
    openAccordions.value.push(id)
  }
}

// Переменные модального окна
const showModal = ref(false)
const isSubmitting = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const form = reactive({
  parent_name: '',
  child_name: '',
  child_age: null,
  phone: ''
})

function handleEnroll() {
  form.parent_name = authStore.user.value?.name || ''
  form.phone = authStore.user.value?.phone || ''
  form.child_name = ''
  form.child_age = null
  errorMsg.value = ''
  successMsg.value = ''
  showModal.value = true
}

async function submitBooking() {
  isSubmitting.value = true
  errorMsg.value = ''
  try {
    const bookingData = {
      parent_name: form.parent_name,
      child_name: form.child_name,
      child_age: form.child_age,
      phone: form.phone,
      activity_id: activity.value?.id || activityId
    }
    await api.createBooking(bookingData)
    successMsg.value = 'Заявка успешно отправлена! Вы можете отслеживать ее статус в личном кабинете.'
  } catch (err) {
    errorMsg.value = err.message || 'Ошибка при отправке заявки'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
/* Дополнительные стили для модального окна */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  box-sizing: border-box;
}

.modal-card {
  background: #ffffff;
  width: 100%;
  max-width: 440px;
  border-radius: 5px;
  border-top: 2px solid var(--primary-dark, #70232f);
  padding: 24px;
  box-shadow: none;
  box-sizing: border-box;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f3f4f6;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-dark, #70232f);
  text-transform: uppercase;
  margin: 0;
}

.btn-close {
  background: #f3f4f6;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: #fee2e2;
  color: #70232f;
}

.modal-subtitle {
  font-size: 14px;
  color: var(--text-light, #666666);
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-main, #333333);
}

.form-input {
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 14px;
  color: var(--text-main, #333333);
  background-color: #ffffff;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-dark, #70232f);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-cancel {
  background: var(--bg-color, #ffffff);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-main, #333333);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-submit {
  background: var(--primary-dark, #70232f);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
  cursor: pointer;
  transition: background-color 0.2s ease;
  box-shadow: none;
}

.btn-submit:hover:not(:disabled) {
  background: #581b25;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-banner {
  text-align: center;
  padding: 20px 10px;
}

.success-banner p {
  color: #065f46;
  font-weight: 600;
  margin-bottom: 20px;
}

.btn-view-profile {
  display: inline-block;
  background: var(--primary-dark, #70232f);
  color: #ffffff;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: 500;
}

.error-banner {
  background: #fee2e2;
  color: #991b1b;
  padding: 10px 14px;
  border-radius: 5px;
  font-size: 13px;
  margin-top: 12px;
}
</style>