<template>
  <div class="content-wrapper">
    <!-- Верхняя навигация -->
    <div class="top-nav">
      <router-link to="/profile" class="btn-back">
        <img :src="getImageUrl('/image/Group3302.svg')" alt="Back" class="icon-sm" /> Назад в профиль
      </router-link>
    </div>

    <!-- Заголовок страницы -->
    <div class="page-header">

      <h1 class="page-title">{{ isEdit ? 'Редактирование карточки кружка' : 'Создание новой карточки кружка' }}</h1>
      <p class="page-subtitle">{{ isEdit ? 'Внесите изменения в информацию о вашем кружке' : 'Заполните информацию о вашей секции для публикации в каталоге KidsConnect' }}</p>
    </div>

    <!-- Загрузка данных -->
    <div v-if="isLoadingData" class="loading-state">
      <div class="spinner"></div>
      <span>Загрузка данных кружка...</span>
    </div>

    <!-- Основная форма -->
    <form v-else @submit.prevent="submitForm" class="create-card-form">
      
      <!-- Секция 1: Основные данные -->
      <div class="form-card-section">

        <h2 class="section-heading"><img :src="getImageUrl('/image/Инфо.svg')" alt="icon" class="icon" />
          Основная информация
        </h2>

        <div class="form-grid">
          <div class="form-group full-width">
            <label class="form-label">Название кружка / секции *</label>
            <input 
              v-model="form.title" 
              type="text" 
              class="form-input" 
              placeholder="например, Лёгкая атлетика (в Юбилейном мкр.)" 
              required 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Категория *</label>
            <div class="custom-dropdown category-dropdown" ref="categoryDropdownRef">
              <div class="select-wrapper category-select-wrapper" @click.stop="isCategoryDropdownOpen = !isCategoryDropdownOpen">
                <span class="select-value">{{ form.category || 'Выберите категорию' }}</span>
                <img :src="getImageUrl('/image/chevrondown1.svg')" class="select-icon" alt="arrow" />
              </div>
              
              <div class="dropdown-list category-dropdown-list" :class="{ show: isCategoryDropdownOpen }">
                <div 
                  v-for="cat in categoryOptions" 
                  :key="cat" 
                  class="dropdown-item" 
                  :class="{ active: form.category === cat }"
                  @click.stop="selectCategoryOption(cat)"
                >
                  {{ cat }}
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Пол (Целевая аудитория) *</label>
            <div class="checkbox-row gap-4 mt-1">
              <label class="custom-checkbox">
                <input 
                  type="checkbox" 
                  class="hidden-cb" 
                  v-model="form.gender_male" 
                />
                <span class="check-box">
                  <img v-if="form.gender_male" :src="getImageUrl('/image/check.svg')" alt="check" />
                </span>
                <span>Мужской</span>
              </label>

              <label class="custom-checkbox">
                <input 
                  type="checkbox" 
                  class="hidden-cb" 
                  v-model="form.gender_female" 
                />
                <span class="check-box">
                  <img v-if="form.gender_female" :src="getImageUrl('/image/check.svg')" alt="check" />
                </span>
                <span>Женский</span>
              </label>
            </div>
          </div>

          <div class="form-group">
            
            <label class="form-label">Возрастная группа *</label>
            <input 
              v-model="form.age_group" 
              type="text" 
              class="form-input" 
              placeholder="например, 10-18 лет" 
              required 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Адрес проведения *</label>
            <input 
              v-model="form.address" 
              type="text" 
              class="form-input" 
              placeholder="например, г. Иркутск, Юбилейный мкр., стр. 49/1" 
              required 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Место / Площадка</label>
            <input 
              v-model="form.place" 
              type="text" 
              class="form-input" 
              placeholder="например, ФОК 'Юбилейный'" 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Стоимость занятий *</label>
            <div class="checkbox-row gap-4">
              <label class="custom-checkbox">
                <input 
                  type="checkbox" 
                  class="hidden-cb" 
                  v-model="form.is_free" 
                  @change="onFreeChange" 
                />
                <span class="check-box">
                  <img v-if="form.is_free" :src="getImageUrl('/image/check.svg')" alt="check" />
                </span>
                <span>Занятия бесплатные</span>
              </label>

              <label class="custom-checkbox">
                <input 
                  type="checkbox" 
                  class="hidden-cb" 
                  v-model="form.is_first_free" 
                />
                <span class="check-box">
                  <img v-if="form.is_first_free" :src="getImageUrl('/image/check.svg')" alt="check" />
                </span>
                <span>Первое бесплатно</span>
              </label>
            </div>
            <div v-if="!form.is_free" class="price-input-row mt-2">
              <input 
                v-model.number="priceAmount" 
                type="number" 
                min="0"
                step="1"
                class="form-input price-number-input" 
                placeholder="Вставьте сумму (например, 500)" 
              />
              <div class="custom-dropdown price-unit-dropdown" ref="unitDropdownRef">
                <div class="select-wrapper price-select-wrapper" @click.stop="isUnitDropdownOpen = !isUnitDropdownOpen">
                  <span class="select-value">{{ priceUnit }}</span>
                  <img :src="getImageUrl('/image/chevrondown1.svg')" class="select-icon" alt="arrow" />
                </div>
                
                <div class="dropdown-list price-dropdown-list" :class="{ show: isUnitDropdownOpen }">
                  <div 
                    v-for="unit in unitOptions" 
                    :key="unit" 
                    class="dropdown-item" 
                    :class="{ active: priceUnit === unit }"
                    @click.stop="selectUnit(unit)"
                  >
                    {{ unit }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Обложка кружка (Изображение)</label>
            <div class="file-upload-box">
              <input type="file" @change="handleFileUpload" accept="image/*" class="file-input" id="cover-file" />
              
              <label for="cover-file" class="file-label-btn">
                <img :src="getImageUrl('/image/Загрузить.svg')" alt="icon" class="icon" />
                Загрузить файл
              </label>
              <span v-if="isUploading" class="uploading-text">Загрузка...</span>
              <span v-else-if="form.image_url" class="uploaded-success-text">
                Файл прикреплен
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Секция 2: Группы и преподаватель -->
      <div class="form-card-section mt-4">
        <h2 class="section-heading">
          Группы и расписание
        </h2>

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Подзаголовок группы / Этап</label>
            <input 
              v-model="form.group_subtitle" 
              type="text" 
              class="form-input" 
              placeholder="например, Этап начальной подготовки" 
            />
          </div>

          <div class="form-group">
            <label class="form-label">ФИО Преподавателя</label>
            <input 
              v-model="form.teacher_name" 
              type="text" 
              class="form-input" 
              placeholder="например, Петрова Елена Александровна" 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Количество мест в группе</label>
            <input 
              v-model="form.spots_info" 
              type="text" 
              class="form-input" 
              placeholder="например, 15 из 20" 
            />
          </div>

          <div class="form-group">
            <label class="form-label">Длительность программы</label>
            <input 
              v-model="form.duration" 
              type="text" 
              class="form-input" 
              placeholder="например, 12 месяцев" 
            />
          </div>

          <div class="form-group full-width">
            <label class="form-label">Расписание занятий *</label>
            
            <!-- Дни недели (7 кнопок) -->
            <div class="days-selector-wrapper">
              <span class="sub-label">Выберите дни недели:</span>
              <div class="days-buttons-grid">
                <button
                  v-for="day in weekDaysOptions"
                  :key="day"
                  type="button"
                  class="day-btn"
                  :class="{ active: selectedDays.includes(day) }"
                  @click="toggleDay(day)"
                >
                  {{ day }}
                </button>
              </div>
            </div>

            <!-- Временные ячейки -->
            <div class="time-slots-wrapper mt-3">
              <span class="sub-label">Время занятий:</span>
              <div class="time-slots-list">
                <div 
                  v-for="(slot, index) in timeSlots" 
                  :key="index" 
                  class="time-slot-item"
                >
                  <input 
                    type="text" 
                    v-model="slot.value" 
                    class="form-input time-input" 
                    placeholder="например, 08:00 - 10:00" 
                  />
                  <button 
                    v-if="timeSlots.length > 1" 
                    type="button" 
                    class="btn-remove-time" 
                    @click="removeTimeSlot(index)"
                    title="Удалить ячейку времени"
                  >
                    ×
                  </button>
                </div>
              </div>

              <button type="button" class="btn-add-slot mt-2" @click="addTimeSlot">
                Добавить дополнительное время
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Секция 3: Описание и программы -->
      <div class="form-card-section mt-4">
        <h2 class="section-heading">
          Описание и Содержание программы
        </h2>

        <div class="form-group full-width">
          <label class="form-label">Описание кружка</label>
          <textarea 
            v-model="form.description" 
            rows="4" 
            class="form-input form-textarea" 
            placeholder="Подробное описание вида спорта, секции или кружка..." 
          ></textarea>
        </div>

        <div class="form-group full-width mt-3">
          <label class="form-label">Базовый уровень (текстовое описание)</label>
          <textarea 
            v-model="form.base_level_info" 
            rows="5" 
            class="form-input form-textarea" 
            placeholder="Введите информацию о Базовом уровне (часы, теории, практики, предметные области...)" 
          ></textarea>
        </div>

        <div class="form-group full-width mt-3">
          <label class="form-label">Углубленный уровень (текстовое описание)</label>
          <textarea 
            v-model="form.advanced_level_info" 
            rows="5" 
            class="form-input form-textarea" 
            placeholder="Введите информацию об Углубленном уровне (соревнования, усложненная подготовка...)" 
          ></textarea>
        </div>
      </div>

      <!-- Ошибка при публикации -->
      <div v-if="errorMsg" class="error-banner mt-3">
        {{ errorMsg }}
      </div>

      <!-- Кнопки действий -->
      <div class="form-actions mt-4">
        <router-link to="/profile" class="btn-cancel">
          Отмена
        </router-link>
        <button type="submit" class="btn-submit" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="spinner-sm"></span>
          <span>{{ isSubmitting ? 'Сохранение...' : (isEdit ? 'Сохранить изменения' : 'Опубликовать кружок') }}</span>
        </button>
      </div>

    </form>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api'

const router = useRouter()
const route = useRoute()

const editId = computed(() => route.query.id ? Number(route.query.id) : null)
const isEdit = computed(() => !!editId.value)

const isSubmitting = ref(false)
const isUploading = ref(false)
const isLoadingData = ref(false)
const errorMsg = ref('')

const isCategoryDropdownOpen = ref(false)
const categoryDropdownRef = ref(null)

const priceAmount = ref(null)
const priceUnit = ref('руб.')
const isUnitDropdownOpen = ref(false)
const unitDropdownRef = ref(null)

const weekDaysOptions = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
const selectedDays = ref(['Пн', 'Вт', 'Чт', 'Сб'])
const timeSlots = ref([{ value: '08:00 - 10:00' }, { value: '18:00 - 19:30' }])

function toggleDay(day) {
  const idx = selectedDays.value.indexOf(day)
  if (idx > -1) {
    selectedDays.value.splice(idx, 1)
  } else {
    selectedDays.value.push(day)
  }
}

function addTimeSlot() {
  timeSlots.value.push({ value: '' })
}

function removeTimeSlot(index) {
  if (timeSlots.value.length > 1) {
    timeSlots.value.splice(index, 1)
  }
}

const categoryOptions = [
  'Силовой спорт',
  'Единоборства',
  'ДПИ и ремесла',
  'Техническое конструирование',
  'Словесность',
  'Иностранные языки',
  'Развитие интеллекта',
  'Информационные технологии',
  'История и Традиции',
  'Педагогика',
  'Музыка и звук',
  'Пение',
  'Хореография(танцы)',
  'Зрелищные искусства',
  'Мода и стиль',
  'Познавательные развлечения',
  'Туризм',
  'Естественные науки',
  'Люди и животные',
  'Эстетические виды спорта',
  'Технические виды спорта',
  'Командно-игровой спорт',
  'Индивидуально игровой спорт',
  'Водные виды спорта',
  'Лёгкая атлетика и гимнастика',
  'Физкультура'
]

function selectCategoryOption(cat) {
  form.category = cat
  isCategoryDropdownOpen.value = false
}

function handleCategoryClickOutside(event) {
  if (categoryDropdownRef.value && !categoryDropdownRef.value.contains(event.target)) {
    isCategoryDropdownOpen.value = false
  }
}

const unitOptions = [
  'руб.',
  'руб./мес.',
  'руб. / занятие',
  'руб. / 8 занятий',
  'руб. / 12 занятий'
]

function selectUnit(unit) {
  priceUnit.value = unit
  isUnitDropdownOpen.value = false
}

function handleUnitClickOutside(event) {
  if (unitDropdownRef.value && !unitDropdownRef.value.contains(event.target)) {
    isUnitDropdownOpen.value = false
  }
}

const form = reactive({
  title: '',
  category: 'Силовой спорт',
  gender_male: true,
  gender_female: true,
  age_group: '',
  address: '',
  place: '',
  image_url: '',
  is_free: false,
  is_first_free: false,
  price: '',
  group_subtitle: '',
  teacher_name: '',
  spots_info: '',
  duration: '',
  schedule: '',
  description: '',
  base_level_info: '',
  advanced_level_info: ''
})

onMounted(async () => {
  window.addEventListener('click', handleUnitClickOutside)
  window.addEventListener('click', handleCategoryClickOutside)
  if (isEdit.value) {
    isLoadingData.value = true
    try {
      const data = await api.getActivityById(editId.value)
      form.title = data.title || ''
      form.category = data.category || 'Силовой спорт'
      form.gender_male = data.gender_male !== undefined && data.gender_male !== null ? !!data.gender_male : true
      form.gender_female = data.gender_female !== undefined && data.gender_female !== null ? !!data.gender_female : true
      form.age_group = data.age_group || ''
      form.address = data.address || ''
      form.place = data.place || ''
      form.image_url = data.image_url || ''
      form.is_free = !!data.is_free
      form.is_first_free = !!data.is_first_free
      form.price = data.price || ''

      if (data.price && data.price !== 'Бесплатно' && data.price !== 'Не указана') {
        const match = data.price.match(/\d+/)
        if (match) {
          priceAmount.value = Number(match[0])
          const remaining = data.price.replace(match[0], '').trim()
          if (remaining) priceUnit.value = remaining
        }
      }

      if (data.schedule) {
        form.schedule = data.schedule
        const firstDigitMatch = data.schedule.match(/\d/)
        if (firstDigitMatch) {
          const dayPart = data.schedule.slice(0, firstDigitMatch.index)
          const timePart = data.schedule.slice(firstDigitMatch.index)

          const parsedDays = weekDaysOptions.filter(d => dayPart.includes(d))
          if (parsedDays.length > 0) {
            selectedDays.value = parsedDays
          }

          const parsedSlots = timePart.split(',').map(s => s.trim()).filter(Boolean)
          if (parsedSlots.length > 0) {
            timeSlots.value = parsedSlots.map(s => ({ value: s }))
          }
        } else {
          const parsedDays = weekDaysOptions.filter(d => data.schedule.includes(d))
          if (parsedDays.length > 0) {
            selectedDays.value = parsedDays
          }
        }
      }

      form.group_subtitle = data.group_subtitle || ''
      form.teacher_name = data.teacher_name || ''
      form.spots_info = data.spots_info || ''
      form.duration = data.duration || ''
      form.description = data.description || ''
      form.base_level_info = data.base_level_info || ''
      form.advanced_level_info = data.advanced_level_info || ''
    } catch (err) {
      errorMsg.value = err.message || 'Не удалось загрузить данные кружка'
    } finally {
      isLoadingData.value = false
    }
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleUnitClickOutside)
  window.removeEventListener('click', handleCategoryClickOutside)
})

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}

function onFreeChange() {
  if (form.is_free) {
    form.price = 'Бесплатно'
    priceAmount.value = null
  }
}

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  isUploading.value = true
  try {
    const uploadedUrl = await api.uploadImage(file)
    form.image_url = uploadedUrl
  } catch (err) {
    errorMsg.value = err.message || 'Ошибка загрузки файла'
  } finally {
    isUploading.value = false
  }
}

async function submitForm() {
  isSubmitting.value = true
  errorMsg.value = ''
  try {
    let computedPrice = 'Бесплатно'
    if (!form.is_free) {
      if (priceAmount.value !== null && priceAmount.value !== '') {
        computedPrice = `${priceAmount.value} ${priceUnit.value}`
      } else {
        computedPrice = 'Не указана'
      }
    }

    const daysStr = selectedDays.value.join(', ')
    const validSlots = timeSlots.value.map(s => s.value.trim()).filter(Boolean)
    const slotsStr = validSlots.join(', ')
    const finalSchedule = [daysStr, slotsStr].filter(Boolean).join(' ')

    const payload = {
      title: form.title,
      category: form.category,
      gender_male: form.gender_male,
      gender_female: form.gender_female,
      age_group: form.age_group,
      address: form.address,
      place: form.place,
      image_url: form.image_url || '/image/Group330.svg',
      is_free: form.is_free,
      is_first_free: form.is_first_free,
      price: computedPrice,
      group_subtitle: form.group_subtitle,
      teacher_name: form.teacher_name,
      spots_info: form.spots_info,
      duration: form.duration,
      schedule: finalSchedule,
      description: form.description,
      base_level_info: form.base_level_info,
      advanced_level_info: form.advanced_level_info
    }
    
    if (isEdit.value) {
      await api.updateActivity(editId.value, payload)
      router.push(`/detail?id=${editId.value}`)
    } else {
      const created = await api.createActivity(payload)
      router.push(`/detail?id=${created.id}`)
    }
  } catch (err) {
    errorMsg.value = err.message || 'Не удалось сохранить кружок'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.content-wrapper {
  width: 100%;
}

.top-nav {
  margin-bottom: 20px;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-color, #ffffff);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 500;
  color: var(--text-main, #333333);
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-back:hover {
  background: #e0e0e0;
}

.icon-sm {
  width: 16px;
  height: 16px;
}


.page-header {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #2F050F;
  margin: 0 0 6px 0;
}

.page-subtitle {
  font-size: 15px;
  color: var(--text-light, #666666);
  margin: 0;
}

.create-card-form {
  display: flex;
  flex-direction: column;
}

.form-card-section {
  background: var(--bg-color, #ffffff);
  border-radius: 5px;
  border-top: 2px solid var(--primary-dark, #70232f);
  padding: 20px;
  display: flex;
  flex-direction: column;
  box-shadow: none;
}

.section-heading {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-dark, #70232f);
  text-transform: uppercase;
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #e5e7eb;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.full-width {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-main, #333333);
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  font-size: 14px;
  color: var(--text-main, #333333);
  background-color: #ffffff;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

select.form-input {
  cursor: pointer;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-dark, #70232f);
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
  line-height: 1.5;
}

.checkbox-row {
  display: flex;
  align-items: center;
  margin-top: 6px;
}

.file-upload-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-input {
  display: none;
}

.file-label-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-wrapper, #efefef);
  border: 1px solid #d1d5db;
  padding: 10px 16px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-main, #333333);
  cursor: pointer;
  transition: all 0.2s ease;
}

.file-label-btn:hover {
  background: #e5e7eb;
}

.uploading-text {
  font-size: 13px;
  color: var(--primary-dark, #70232f);
  font-weight: 600;
}

.uploaded-success-text {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #059669;
  font-weight: 600;
}

.error-banner {
  background: #fee2e2;
  color: #991b1b;
  padding: 12px 16px;
  border-radius: 5px;
  font-weight: 600;
  font-size: 14px;
  border: 1px solid #fca5a5;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
  background: var(--bg-color, #ffffff);
  border-radius: 5px;
  border-top: 2px solid var(--primary-dark, #70232f);
  padding: 20px;
  box-shadow: none;
}

.btn-cancel {
  background: var(--bg-color, #ffffff);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-main, #333333);
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-submit {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--primary-dark, #70232f);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: none;
}

.btn-submit:hover:not(:disabled) {
  background: #581b25;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-sm {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s infinite linear;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.mt-2 { margin-top: 8px; }
.mt-3 { margin-top: 12px; }
.mt-4 { margin-top: 20px; }
.gap-4 { gap: 16px; flex-wrap: wrap; }

.category-dropdown {
  position: relative;
  width: 100%;
}

.category-select-wrapper {
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  padding: 10px 14px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  box-sizing: border-box;
  transition: border-color 0.2s ease;
}

.category-select-wrapper:hover {
  border-color: var(--primary-dark, #70232f);
}

.category-dropdown-list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  width: 100%;
  max-height: 240px;
  background: #ffffff;
  border-radius: 5px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 100;
  padding: 4px 0;
}

.price-input-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.price-number-input {
  flex: 1;
}

.price-unit-dropdown {
  width: 190px;
  flex-shrink: 0;
  position: relative;
}

.price-select-wrapper {
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  padding: 10px 14px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  box-sizing: border-box;
  transition: border-color 0.2s ease;
}

.price-select-wrapper:hover {
  border-color: var(--primary-dark, #70232f);
}

.price-dropdown-list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  width: 100%;
  max-height: 220px;
  background: #ffffff;
  border-radius: 5px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 100;
  padding: 4px 0;
}

.sub-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-main, #333333);
  margin-bottom: 8px;
}

.days-buttons-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.day-btn {
  width: 40px;
  height: 40px;
  border-radius: 5px;
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: var(--text-main, #333333);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.day-btn:hover {
  border-color: var(--primary-dark, #70232f);
  color: var(--primary-dark, #70232f);
  background: #fce8eb;
}

.day-btn.active {
  background: var(--primary-dark, #70232f);
  color: #ffffff;
  border-color: var(--primary-dark, #70232f);
  box-shadow: none;
}

.time-slots-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.time-slot-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.time-input {
  max-width: 320px;
}

.btn-remove-time {
  background: #fef2f2;
  border: 1px solid #fee2e2;
  color: #dc2626;
  width: 40px;
  height: 40px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-remove-time:hover {
  background: #dc2626;
  color: #ffffff;
  border-color: #dc2626;
}

.btn-add-slot {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fce8eb;
  color: var(--primary-dark, #70232f);
  border: 1px solid #f8c8d0;
  padding: 8px 14px;
  border-radius: 5px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-add-slot:hover {
  background: var(--primary-dark, #70232f);
  color: #ffffff;
  border-color: var(--primary-dark, #70232f);
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  .price-input-row {
    flex-direction: column;
  }
  .price-unit-dropdown {
    width: 100%;
  }
  .time-input {
    max-width: 100%;
  }
}
</style>
