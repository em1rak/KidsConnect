<template>
  <header class="header">
    <router-link to="/" class="logo">
      <img :src="getImageUrl('/image/LeavesPlay1.svg')" alt="Logo" class="logo-icon" />
      <span>KidsConnect</span>
    </router-link>

    <div v-if="authStore.isAuthenticated.value" class="user-menu">
      <router-link to="/profile" class="user-info" title="Перейти в личный кабинет">
        <img :src="getImageUrl('/image/Логин1.svg')" alt="icon" class="icon" />
        <span class="user-name">{{ authStore.user.value?.name }}</span>
        <span class="role-badge" :class="authStore.user.value?.role">
          {{ authStore.isLeader.value ? 'Руководитель' : 'Родитель' }}
        </span>
      </router-link>
      
      <router-link to="/profile" class="btn-profile">Профиль</router-link>
      <button class="btn-logout" @click="handleLogout">Выйти</button>
    </div>
      
    <router-link v-else to="/auth" class="auth-btn">
      <img :src="getImageUrl('/image/Логин.svg')" alt="icon" class="icon" />
      <span>Войти / Регистрация</span>
    </router-link>
  </header>
</template>

<script setup>
import { onMounted } from 'vue'
import { authStore } from '../authStore'

function getImageUrl(path) {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}

onMounted(() => {
  authStore.checkAuth()
})

function handleLogout() {
  authStore.logout()
}
</script>

<style scoped>
.logo {
  text-decoration: none;
  color: #ffffff !important;
}

.logo span {
  color: #ffffff !important;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
}

.user-info {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: background-color 0.2s ease;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.25);
}

.user-name {
  color: #ffffff;
  font-weight: 600;
}

.role-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
  background-color: rgba(255, 255, 255, 0.25);
  color: #ffffff;
  margin-left: 4px;
}

.role-badge.leader {
  background-color: #ffd54f;
  color: #3e2723;
}

.btn-profile {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-profile:hover {
  background: rgba(255, 255, 255, 0.35);
  border-color: #ffffff;
}

.btn-logout {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: #ffffff;
}

.auth-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: var(--bg-color, #ffffff);
  color: var(--primary-dark, #70232f);
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-left: auto;
}

.auth-btn:hover {
  background-color: #f8f8f8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.auth-icon {
  flex-shrink: 0;
}
</style>

