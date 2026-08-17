<template>
  <article class="card">
    <div class="card-image">
      <img 
        :src="getImageUrl(item.image || '/image/Group330.svg')" 
        @error="$event.target.src = getImageUrl('/image/Group330.svg')" 
        alt="Preview" 
      />
    </div>
    <div class="card-content">
      <div class="card-header">
        <h3>
          {{ item.title }}
          <span v-if="item.locationText" class="location-text">{{ item.locationText }}</span>
        </h3>
        
        <!-- Бейджи стоимости и особенностей -->
        <div v-if="item.priceGroup" class="price-group">
          <span v-if="item.priceGroup.outlineBadge" class="badge badge-outline">
            {{ item.priceGroup.outlineBadge }}
          </span>
          <span 
            class="badge badge-free" 
            :class="{ 'price-badge': item.priceGroup.subText }"
          >
            <span>{{ item.priceGroup.mainText }}</span>
            <span v-if="item.priceGroup.subText">{{ item.priceGroup.subText }}</span>
          </span>
        </div>
        <span v-else-if="item.isFree" class="badge badge-free">Бесплатно</span>
        <span v-else class="badge badge-free">{{ item.price }}</span>
      </div>

      <div class="card-details">
        <p v-if="item.hashtag" class="hashtag">{{ item.hashtag }}</p>

        <p v-if="item.age" class="info-row">
          <img :src="getImageUrl('/image/Frame397.svg')" class="icon" alt="age" /> {{ item.age }}
        </p>

        <p v-if="item.address" class="info-row">
          <img :src="getImageUrl('/image/layer1.svg')" class="icon" alt="address" /> {{ item.address }}
        </p>

        <p v-if="item.place" class="info-row">
          <img :src="getImageUrl('/image/Group.svg')" class="icon" alt="place" /> {{ item.place }}
        </p>

        <div v-if="item.schedule" class="schedule-row">
          <div class="schedule-days">
            <img :src="getImageUrl('/image/clock_time_icon_1429031.svg')" class="icon" alt="clock" />
            <span>{{ item.schedule.days }}</span>
          </div>
          <span 
            v-for="(slot, idx) in item.schedule.slots" 
            :key="idx" 
            class="time-slot"
          >
            {{ slot }}
          </span>
        </div>
      </div>

      <router-link :to="item.detailUrl || (item.id ? `/detail?id=${item.id}` : '/detail')" class="btn-more">
        Подробнее
      </router-link>
    </div>
  </article>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})


function getImageUrl(path) {
  if (!path) return import.meta.env.BASE_URL + 'image/Group330.svg'
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  if (path.startsWith('/uploads/') || path.startsWith('uploads/') || path.startsWith('/media/') || path.startsWith('media/')) {
    return 'http://127.0.0.1:8000/' + path.replace(/^\//, '')
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}
</script>