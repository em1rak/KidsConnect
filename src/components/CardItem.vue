<template>
  <article class="card">
    <div class="card-image">
      <img :src="getImageUrl(item.image || '/image/Group330.svg')" alt="Preview" />
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
          <img src="/image/Frame397.svg" class="icon" alt="age" /> {{ item.age }}
        </p>

        <p v-if="item.address" class="info-row">
          <img src="/image/layer1.svg" class="icon" alt="address" /> {{ item.address }}
        </p>

        <a 
          v-if="item.place" 
          :href="item.placeUrl || 'https://posleurokov.ru/irkutsk/61894'" 
          target="_blank" 
          class="place-link info-row"
        >
          <img src="/image/Group.svg" class="icon" alt="place" /> {{ item.place }}
        </a>

        <div v-if="item.schedule" class="schedule-row">
          <div class="schedule-days">
            <img src="/image/clock_time_icon_1429031.svg" class="icon" alt="clock" />
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

      <router-link :to="item.detailUrl || '/detail'" class="btn-more">
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
  if (!path) return ''
  return import.meta.env.BASE_URL + path.replace(/^\//, '')
}
</script>