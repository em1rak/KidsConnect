<template>
  <div class="top-bar">
    <div class="search-box">
      <img :src="getImageUrl('/image/search1.svg')" alt="Search" class="icon-sm" />
      <input 
        type="text" 
        placeholder="Поиск" 
        :value="searchQuery" 
        @input="$emit('update:searchQuery', $event.target.value)"
      />
    </div>

    <div class="tabs">
      <button 
        class="tab" 
        :class="{ active: activeTab === 'all' }" 
        @click="$emit('update:activeTab', 'all')"
      >
        Все
      </button>
      <button 
        class="tab" 
        :class="{ active: activeTab === 'paid' }" 
        @click="$emit('update:activeTab', 'paid')"
      >
        Платные
      </button>
      <button 
        class="tab" 
        :class="{ active: activeTab === 'free' }" 
        @click="$emit('update:activeTab', 'free')"
      >
        Бесплатные
      </button>
    </div>

    <button class="map-btn" @click="$emit('toggleMap')">
      На карте
      <img :src="getImageUrl('/image/Group.svg')" alt="Map" class="icon-sm" />
    </button>
  </div>
</template>

<script setup>
defineProps({
  searchQuery: {
    type: String,
    default: ''
  },
  activeTab: {
    type: String,
    default: 'all'
  }
})

defineEmits(['update:searchQuery', 'update:activeTab', 'toggleMap'])

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}
</script>
