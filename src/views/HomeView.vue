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

        <div v-if="filteredGroups.length === 0" class="no-results" style="padding: 40px; text-align: center; color: #666;">
          Ничего не найдено по вашему запросу
        </div>
      </main>

      <!-- Правая колонка: Фильтры (Сайдбар) -->
      <SidebarFilters 
        v-model:selectedAge="selectedAge"
        @update:gender="handleGenderChange"
        @selectCategory="handleSelectCategory"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import TopBar from '../components/TopBar.vue'
import CardItem from '../components/CardItem.vue'
import SidebarFilters from '../components/SidebarFilters.vue'

const searchQuery = ref('')
const activeTab = ref('all') // Режимы: 'all' (все), 'paid' (платные), 'free' (бесплатные)
const selectedAge = ref('Любой')
const genderFilter = ref({ male: true, female: true })

const rawSections = ref([
  {
    title: 'Силовой спорт',
    items: [
      {
        id: 1,
        title: 'Тяжелая атлетика',
        locationText: '(в Юбилейном мкр.)',
        isFree: true,
        hashtag: '#Тяжелая атлетика',
        age: '10-18 лет',
        address: 'г. Иркутск, Юбилейный мкр., стр. 49/1',
        place: 'ФОК “Юбилейный”',
        placeUrl: 'https://posleurokov.ru/irkutsk/61894',
        schedule: {
          days: 'Пн, Ср, Пт',
          slots: ['09:00 - 10:30', '12:00 - 13:30', '18:00 - 19:30']
        }
      },
      {
        id: 2,
        title: 'Тяжелая атлетика',
        locationText: '(на ул. Боткина)',
        isFree: false,
        priceGroup: {
          outlineBadge: 'Первое бесплатно',
          mainText: '500 руб.'
        },
        hashtag: '#Тяжелая атлетика',
        age: '10-18 лет',
        address: 'г. Иркутск, Юбилейный мкр., стр. 49/1',
        place: 'ФОК “Юбилейный”',
        placeUrl: 'https://posleurokov.ru/irkutsk/61894',
        schedule: {
          days: 'Пн, Ср, Пт',
          slots: ['09:00 - 10:30', '12:00 - 13:30']
        }
      },
      {
        id: 3,
        title: 'Тяжелая атлетика',
        locationText: '(на ул. Норильской)',
        isFree: false,
        priceGroup: {
          outlineBadge: 'Первое бесплатно',
          mainText: '3200 руб.',
          subText: '8 занятий'
        },
        hashtag: '#Тяжелая атлетика',
        age: '10-18 лет',
        address: 'г. Иркутск, Юбилейный мкр., стр. 49/1',
        place: 'ФОК “Юбилейный”',
        placeUrl: 'https://posleurokov.ru/irkutsk/61894',
        schedule: {
          days: 'Пн, Ср, Пт',
          slots: ['09:00 - 10:30', '12:00 - 13:30', '18:00 - 19:30']
        }
      },
      {
        id: 4,
        title: 'Пауэрлифтинг',
        locationText: '',
        isFree: true,
        hashtag: '#Пауэрлифтинг',
        age: '10-18 лет',
        address: 'г. Иркутск, Юбилейный мкр., стр. 49/1',
        place: 'ФОК “Юбилейный”',
        placeUrl: 'https://posleurokov.ru/irkutsk/61894',
        schedule: {
          days: 'Пн, Ср, Пт',
          slots: ['09:00 - 10:30', '12:00 - 13:30', '18:00 - 19:30']
        }
      }
    ]
  },
  {
    title: 'Единоборства',
    items: [
      {
        id: 5,
        title: 'Дзюдо',
        locationText: '',
        isFree: true,
        hashtag: '#Дзюдо',
        age: '6–18 лет',
        address: 'г Иркутск, ул Трудовая, д 115А',
        place: 'СК "Вымпел"',
        placeUrl: 'https://posleurokov.ru/irkutsk/61894',
        schedule: {
          days: 'Пн, Ср, Пт',
          slots: ['09:00 - 10:30', '12:00 - 13:30', '18:00 - 19:30']
        }
      },
      {
        id: 6,
        title: 'Вольная борьба',
        locationText: '(на ул. Норильская)',
        isFree: false,
        priceGroup: {
          outlineBadge: 'Первое бесплатно',
          mainText: '3200 руб.',
          subText: 'месяц'
        },
        hashtag: '#Дзюдо',
        age: '6–18 лет',
        address: 'г Иркутск, ул Трудовая, д 115А',
        place: 'СК "Вымпел"',
        placeUrl: 'https://posleurokov.ru/irkutsk/61894',
        schedule: {
          days: 'Пн, Ср, Пт',
          slots: ['09:00 - 10:30', '12:00 - 13:30', '18:00 - 19:30']
        }
      },
      {
        id: 7,
        title: 'Дзюдо',
        locationText: '',
        isFree: true,
        hashtag: '#Дзюдо',
        age: '6–18 лет',
        address: 'г Иркутск, ул Трудовая, д 115А',
        place: 'СК "Вымпел"',
        placeUrl: 'https://posleurokov.ru/irkutsk/61894',
        schedule: {
          days: 'Пн, Ср, Пт',
          slots: ['09:00 - 10:30', '12:00 - 13:30', '18:00 - 19:30']
        }
      },
      {
        id: 8,
        title: 'Вольная борьба',
        locationText: '(на ул. Норильская)',
        isFree: false,
        priceGroup: {
          mainText: '3200 руб.',
          subText: 'месяц'
        },
        hashtag: '#Дзюдо',
        age: '6–18 лет',
        address: 'г Иркутск, ул Трудовая, д 115А',
        place: 'СК "Вымпел"',
        placeUrl: 'https://posleurokov.ru/irkutsk/61894',
        schedule: {
          days: 'Пн, Ср, Пт',
          slots: ['09:00 - 10:30', '12:00 - 13:30', '18:00 - 19:30']
        }
      }
    ]
  }
])

function handleGenderChange(val) {
  genderFilter.value = val
}

function handleSelectCategory(catData) {
  if (catData.subCategory) {
    searchQuery.value = catData.subCategory
  } else if (catData.category) {
    searchQuery.value = catData.category
  }
}

const filteredGroups = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()
  const tab = activeTab.value

  return rawSections.value
    .map(section => {
      const filteredItems = section.items.filter(item => {
        // Фильтрация по вкладке (все / платные / бесплатные)
        if (tab === 'free' && !item.isFree) return false
        if (tab === 'paid' && item.isFree) return false

        // Фильтрация по поисковому запросу
        if (query) {
          const matchTitle = item.title.toLowerCase().includes(query)
          const matchHashtag = item.hashtag && item.hashtag.toLowerCase().includes(query)
          const matchLocation = item.locationText && item.locationText.toLowerCase().includes(query)
          const matchPlace = item.place && item.place.toLowerCase().includes(query)
          if (!matchTitle && !matchHashtag && !matchLocation && !matchPlace) {
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
