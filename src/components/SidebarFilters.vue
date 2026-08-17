<template>
  <aside class="sidebar">
    <h2 class="sidebar-title">Фильтры</h2>
    <div class="filter-box">
      <!-- Возраст -->
      <div class="filter-group age-filter-group">
        <label>Возраст</label>
        
        <div class="custom-dropdown" ref="dropdownRef">
          <div class="select-wrapper" @click="toggleDropdown">
            <span class="select-value">{{ selectedAge }}</span>
            <img :src="getImageUrl('/image/chevrondown1.svg')" class="select-icon" alt="arrow" />
          </div>
          
          <div class="dropdown-list" :class="{ show: isDropdownOpen }">
            <div 
              v-for="age in ageOptions" 
              :key="age" 
              class="dropdown-item" 
              :class="{ active: selectedAge === age }"
              @click="selectAge(age)"
            >
              {{ age }}
            </div>
          </div>
        </div>
      </div>

      <!-- Пол -->
      <div class="filter-group">
        <label>Пол</label>
        <div class="checkbox-group">
          <label class="custom-checkbox">
            <input 
              type="checkbox" 
              class="hidden-cb" 
              v-model="genderMale"
              @change="emitGenderChange"
            />
            <span class="check-box">
              <img v-if="genderMale" :src="getImageUrl('/image/check.svg')" alt="check" />
            </span>
            Мужской
          </label>
          
          <label class="custom-checkbox">
            <input 
              type="checkbox" 
              class="hidden-cb" 
              v-model="genderFemale"
              @change="emitGenderChange"
            />
            <span class="check-box">
              <img v-if="genderFemale" :src="getImageUrl('/image/check.svg')" alt="check" />
            </span>
            Женский
          </label>
        </div>
      </div>

      <!-- Каталог -->
      <div class="filter-group menu-list">
        <label>Каталог</label>
        <ul>
          <li 
            v-for="cat in displayCategories" 
            :key="cat.name"
            :class="{ 'active-category': cat.expanded }"
          >
            <div class="menu-item" @click="toggleCategory(cat)">
              <span class="menu-text">{{ cat.name }}</span>
              <span v-if="cat.count > 0" class="menu-count">{{ cat.count }}</span>
              <img :src="getImageUrl('/image/chevrondown1.svg')" class="chevron" alt="chevron" />
            </div>
            
            <ul v-if="cat.subItems && cat.subItems.length" class="sub-menu">
              <li 
                v-for="sub in cat.subItems" 
                :key="sub.name"
                @click.stop="selectSubCategory(cat, sub)"
              >
                <span class="menu-text">• {{ sub.name }}</span>
                <span v-if="sub.count > 0" class="menu-count">{{ sub.count }}</span>
              </li>
            </ul>
          </li>
        </ul>
      </div>

    </div>
  </aside>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  selectedAge: {
    type: String,
    default: 'Любой'
  },
  selectedCategory: {
    type: String,
    default: null
  },
  selectedSubCategory: {
    type: String,
    default: null
  },
  activities: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:selectedAge', 'update:gender', 'selectCategory'])

const dropdownRef = ref(null)
const isDropdownOpen = ref(false)

const genderMale = ref(true)
const genderFemale = ref(true)

const ageOptions = [
  'Любой',
  '1 год', '2 года', '3 года', '4 года', '5 лет',
  '6 лет', '7 лет', '8 лет', '9 лет', '10 лет',
  '11 лет', '12 лет', '13 лет', '14 лет', '15 лет',
  '16 лет', '17 лет', '18 лет'
]

const categories = ref([
  { name: 'Силовой спорт', expanded: false },
  { name: 'Единоборства', expanded: false },
  { name: 'ДПИ и ремесла', expanded: false },
  { name: 'Техническое конструирование', expanded: false },
  { name: 'Словесность', expanded: false },
  { name: 'Иностранные языки', expanded: false },
  { name: 'Развитие интеллекта', expanded: false },
  { name: 'Информационные технологии', expanded: false },
  { name: 'История и Традиции', expanded: false },
  { name: 'Педагогика', expanded: false },
  { name: 'Музыка и звук', expanded: false },
  { name: 'Пение', expanded: false },
  { name: 'Хореография(танцы)', expanded: false },
  { name: 'Зрелищные искусства', expanded: false },
  { name: 'Мода и стиль', expanded: false },
  { name: 'Познавательные развлечения', expanded: false },
  { name: 'Туризм', expanded: false },
  { name: 'Естественные науки', expanded: false },
  { name: 'Люди и животные', expanded: false },
  { name: 'Эстетические виды спорта', expanded: false },
  { name: 'Технические виды спорта', expanded: false },
  { name: 'Командно-игровой спорт', expanded: false },
  { name: 'Индивидуально игровой спорт', expanded: false },
  { name: 'Водные виды спорта', expanded: false },
  { name: 'Лёгкая атлетика и гимнастика', expanded: false },
  { name: 'Физкультура', expanded: false }
])

function normalizeKey(str) {
  if (!str) return ''
  return str.toLowerCase()
            .replace(/^#/, '')
            .replace(/[-–—\s]+/g, '')
            .trim()
}

function getClubName(item) {
  if (!item) return ''
  let title = (item.title || '').trim()
  title = title.replace(/\s*\([^)]*\)/g, '').trim()
  return title || item.title
}

const expandedCategories = ref({})

watch(() => props.selectedCategory, (newCat) => {
  if (newCat) {
    expandedCategories.value[normalizeKey(newCat)] = true
  }
}, { immediate: true })

const displayCategories = computed(() => {
  const allActivities = props.activities || []

  // Группируем все кружки по нормализованным ключам категорий
  const activitiesByCatKey = {}

  allActivities.forEach(item => {
    const rawCat = (item.category || '').trim()
    if (!rawCat) return

    const normKey = normalizeKey(rawCat)
    if (!activitiesByCatKey[normKey]) {
      activitiesByCatKey[normKey] = {
        catName: rawCat.replace(/^#/, '').trim(),
        clubs: {},
        totalCount: 0
      }
    }

    const clubName = getClubName(item) || item.title || 'Кружок'
    activitiesByCatKey[normKey].totalCount += 1
    activitiesByCatKey[normKey].clubs[clubName] = (activitiesByCatKey[normKey].clubs[clubName] || 0) + 1
  })

  const knownNormKeys = new Set()

  const list = categories.value.map(cat => {
    const normKey = normalizeKey(cat.name)
    knownNormKeys.add(normKey)

    const catData = activitiesByCatKey[normKey]
    
    let subItems = []
    let totalCount = 0

    if (catData) {
      totalCount = catData.totalCount
      subItems = Object.keys(catData.clubs).map(clubName => ({
        name: clubName,
        count: catData.clubs[clubName]
      }))
    }

    return {
      ...cat,
      expanded: !!expandedCategories.value[normKey],
      count: totalCount,
      subItems: subItems
    }
  })

  // Добавляем категории из базы данных, которых нет в предустановленном списке
  Object.keys(activitiesByCatKey).forEach(normKey => {
    if (!knownNormKeys.has(normKey)) {
      const catData = activitiesByCatKey[normKey]
      const subItems = Object.keys(catData.clubs).map(clubName => ({
        name: clubName,
        count: catData.clubs[clubName]
      }))

      list.push({
        name: catData.catName,
        expanded: !!expandedCategories.value[normKey],
        count: catData.totalCount,
        subItems: subItems
      })
    }
  })

  return list
})

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value
}

function selectAge(age) {
  emit('update:selectedAge', age)
  isDropdownOpen.value = false
}

function emitGenderChange() {
  emit('update:gender', { male: genderMale.value, female: genderFemale.value })
}

function toggleCategory(cat) {
  const normKey = normalizeKey(cat.name)
  const isCurrentlyExpanded = !!expandedCategories.value[normKey]
  expandedCategories.value[normKey] = !isCurrentlyExpanded

  if (!isCurrentlyExpanded) {
    emit('selectCategory', { category: cat.name, subCategory: null })
  } else {
    if (props.selectedCategory === cat.name) {
      emit('selectCategory', { category: null, subCategory: null })
    }
  }
}

function selectSubCategory(category, subCategory) {
  if (props.selectedSubCategory === subCategory.name) {
    emit('selectCategory', { category: category.name, subCategory: null })
  } else {
    emit('selectCategory', { category: category.name, subCategory: subCategory.name })
  }
}

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isDropdownOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
})
</script>
