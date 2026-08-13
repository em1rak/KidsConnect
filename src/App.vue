<template>
  <div class="scroll-container">
    <div class="app-container">
      <AppHeader />
      <router-view />
    </div>
  </div>
</template>

<script setup>
import AppHeader from './components/AppHeader.vue'
</script>
