<template>
  <div class="content-wrapper">
    <!-- Верхняя панель (Поиск, Вкладки, Карта) -->
    <TopBar 
      v-model:searchQuery="searchQuery"
      v-model:activeTab="activeTab"
    />

    <!-- Контейнер для Контента и Сайдбара -->
    <div class="main-layout">
      <!-- Левая колонка со списком секций и карточек -->
      <main class="cards-column">
        <section 
          v-for="group in filteredGroups" 
          :key="group.title" 
          class="category-section"
        >
          <h2 class="category-title">{{ group.title }}</h2>
          <div class="cards-list">
            <CardItem 
              v-for="item in group.items" 
              :key="item.id" 
              :item="item" 
            />
          </div>
        </section>

        <div v-if="isLoading" class="loading-state" style="padding: 40px; text-align: center; color: #70232f; font-weight: 600;">
          Загрузка кружков...
        </div>

        <div v-else-if="filteredGroups.length === 0" class="no-results" style="padding: 40px; text-align: center; color: #666;">
          Ничего не найдено по вашему запросу
        </div>
      </main>

      <!-- Правая колонка: Фильтры (Сайдбар) -->
      <SidebarFilters 
        v-model:selectedAge="selectedAge"
        :selectedCategory="selectedCategory"
        :selectedSubCategory="selectedSubCategory"
        :activities="allRawActivities"
        @update:gender="handleGenderChange"
        @selectCategory="handleSelectCategory"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import TopBar from '../components/TopBar.vue'
import CardItem from '../components/CardItem.vue'
import SidebarFilters from '../components/SidebarFilters.vue'
import api from '../api'

const searchQuery = ref('')
const activeTab = ref('all') // Режимы: 'all' (все), 'paid' (платные), 'free' (бесплатные)
const selectedAge = ref('Любой')
const selectedCategory = ref(null)
const selectedSubCategory = ref(null)
const genderFilter = ref({ male: true, female: true })
const isLoading = ref(true)

const rawSections = ref([])

const allRawActivities = computed(() => {
  const result = []
  rawSections.value.forEach(section => {
    result.push(...section.items)
  })
  return result
})

function parseSchedule(scheduleStr) {
  if (!scheduleStr) return { days: 'Расписание по запросу', slots: [] }

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
}

async function fetchActivities() {
  isLoading.value = true
  try {
    const list = await api.getActivities()
    if (!list || list.length === 0) {
      rawSections.value = []
      return
    }

    const groupedData = {}
    list.forEach(item => {
      const categoryName = item.category || 'Другое'
      if (!groupedData[categoryName]) {
        groupedData[categoryName] = []
      }

      let priceGroup = null
      if (!item.is_free && item.price) {
        priceGroup = {
          mainText: item.price,
          outlineBadge: item.is_first_free ? 'Первое бесплатно' : null
        }
      }

      const parsedSched = parseSchedule(item.schedule)
      const imageUrl = item.image_url ? item.image_url : '/image/Group330.svg'

      groupedData[categoryName].push({
        id: item.id,
        title: item.title,
        category: item.category || categoryName,
        locationText: item.place ? `(${item.place})` : '',
        isFree: !!item.is_free,
        priceGroup: priceGroup,
        hashtag: item.category ? `#${item.category}` : '',
        gender_male: item.gender_male !== undefined && item.gender_male !== null ? item.gender_male : true,
        gender_female: item.gender_female !== undefined && item.gender_female !== null ? item.gender_female : true,
        age: item.age_group,
        address: item.address,
        place: item.place || '',
        image: imageUrl,
        schedule: {
          days: parsedSched.days,
          slots: parsedSched.slots
        }
      })
    })

    rawSections.value = Object.keys(groupedData).map(key => ({
      title: key,
      items: groupedData[key]
    }))
  } catch (err) {
    console.warn('Не удалось загрузить кружки с бэкенда:', err)
    rawSections.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchActivities()
})

function handleGenderChange(val) {
  genderFilter.value = val
}

function handleSelectCategory(catData) {
  if (!catData || (!catData.category && !catData.subCategory)) {
    selectedCategory.value = null
    selectedSubCategory.value = null
    return
  }

  if (catData.subCategory) {
    if (selectedSubCategory.value === catData.subCategory) {
      selectedSubCategory.value = null
      selectedCategory.value = null
    } else {
      selectedSubCategory.value = catData.subCategory
      selectedCategory.value = catData.category
    }
  } else if (catData.category) {
    if (selectedCategory.value === catData.category && !selectedSubCategory.value) {
      selectedCategory.value = null
    } else {
      selectedCategory.value = catData.category
      selectedSubCategory.value = null
    }
  }
}

function parseAgeRange(ageStr) {
  if (!ageStr) return null
  const nums = ageStr.match(/\d+/g)
  if (!nums) return null
  if (nums.length === 1) {
    const num = parseInt(nums[0], 10)
    return { min: num, max: num }
  } else if (nums.length >= 2) {
    const num1 = parseInt(nums[0], 10)
    const num2 = parseInt(nums[1], 10)
    return { min: Math.min(num1, num2), max: Math.max(num1, num2) }
  }
  return null
}

const filteredGroups = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  const tab = activeTab.value
  const ageStr = selectedAge.value
  const targetAgeNum = ageStr !== 'Любой' ? parseInt(ageStr.match(/\d+/)?.[0] || '0', 10) : null
  const selCat = selectedCategory.value ? selectedCategory.value.toLowerCase() : null
  const selSubCat = selectedSubCategory.value ? selectedSubCategory.value.toLowerCase() : null

  return rawSections.value
    .map(section => {
      const sectionTitleLower = section.title.toLowerCase()

      const filteredItems = section.items.filter(item => {
        // 1. Вкладки Все / Бесплатные / Платные
        if (tab === 'free' && !item.isFree) return false
        if (tab === 'paid' && item.isFree) return false

        // 2. Фильтр по возрасту
        if (targetAgeNum !== null && targetAgeNum > 0) {
          const itemRange = parseAgeRange(item.age)
          if (itemRange) {
            if (targetAgeNum < itemRange.min || targetAgeNum > itemRange.max) {
              return false
            }
          }
        }

        // 3. Фильтр по полу (Мужской / Женский)
        const wantMale = genderFilter.value.male
        const wantFemale = genderFilter.value.female
        if (!wantMale && !wantFemale) return false
        if (wantMale && !wantFemale && !item.gender_male) return false
        if (wantFemale && !wantMale && !item.gender_female) return false

        // 4. Фильтр по категориям из Сайдбара
        if (selSubCat) {
          const itemTitleLower = (item.title || '').toLowerCase()
          const itemHashtagLower = (item.hashtag || '').toLowerCase()
          const itemLocationLower = (item.locationText || '').toLowerCase()
          const itemPlaceLower = (item.place || '').toLowerCase()

          const matchSub = itemTitleLower.includes(selSubCat) ||
                           itemHashtagLower.includes(selSubCat) ||
                           itemLocationLower.includes(selSubCat) ||
                           itemPlaceLower.includes(selSubCat) ||
                           sectionTitleLower.includes(selSubCat)
          if (!matchSub) return false
        } else if (selCat) {
          const itemTitleLower = (item.title || '').toLowerCase()
          const itemHashtagLower = (item.hashtag || '').toLowerCase()
          const itemLocationLower = (item.locationText || '').toLowerCase()
          const itemPlaceLower = (item.place || '').toLowerCase()

          const matchCat = sectionTitleLower.includes(selCat) ||
                           itemTitleLower.includes(selCat) ||
                           itemHashtagLower.includes(selCat) ||
                           itemLocationLower.includes(selCat) ||
                           itemPlaceLower.includes(selCat)
          if (!matchCat) return false
        }

        // 5. Поиск в поисковой строке
        if (query) {
          const matchTitle = item.title.toLowerCase().includes(query)
          const matchHashtag = item.hashtag && item.hashtag.toLowerCase().includes(query)
          const matchLocation = item.locationText && item.locationText.toLowerCase().includes(query)
          const matchPlace = item.place && item.place.toLowerCase().includes(query)
          const matchCat = sectionTitleLower.includes(query)
          if (!matchTitle && !matchHashtag && !matchLocation && !matchPlace && !matchCat) {
            return false
          }
        }

        return true
      })

      return {
        ...section,
        items: filteredItems
      }
    })
    .filter(section => section.items.length > 0)
})
</script>
