<template>
  <div class="content-wrapper">
    <!-- Навигация назад -->
    <div class="top-nav">
      <router-link to="/" class="nav-btn">
        <img src="/image/Group3302.svg" alt="Back" class="icon-sm" /> На главную
      </router-link>
    </div>

    <div class="auth-container">
      <div class="auth-card">
        <!-- Шапка формы / Табы -->
        <div class="auth-header">
          <h1 class="auth-title">{{ activeTab === 'login' ? 'Вход в аккаунт' : 'Регистрация' }}</h1>
          <p class="auth-subtitle">
            {{ activeTab === 'login' ? 'Добро пожаловать в KidsConnect! Войдите для доступа к записи' : 'Создайте аккаунт, чтобы легко записывать детей в кружки' }}
          </p>
          
          <div class="auth-tabs">
            <button 
              class="auth-tab" 
              :class="{ active: activeTab === 'login' }"
              @click="activeTab = 'login'"
            >
              Авторизация
            </button>
            <button 
              class="auth-tab" 
              :class="{ active: activeTab === 'register' }"
              @click="activeTab = 'register'"
            >
              Регистрация
            </button>
          </div>
        </div>

        <!-- Уведомление об ошибке -->
        <div v-if="errorMessage" class="alert-error">
          <span>{{ errorMessage }}</span>
        </div>

        <!-- Уведомление об успешной форме -->
        <div v-if="successMessage" class="alert-success">
          <span>{{ successMessage }}</span>
        </div>

        <!-- ФОРМА ВХОДА (LOGIN) -->
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label for="login-email">Email или номер телефона</label>
            <div class="input-wrapper">
              <input 
                id="login-email"
                v-model="loginForm.login" 
                type="text" 
                placeholder="name@example.com или +7 (900) 000-00-00" 
                required 
              />
            </div>
          </div>

          <div class="form-group">
            <div class="label-row">
              <label for="login-password">Пароль</label>
              <a href="#" @click.prevent="handleForgotPassword" class="forgot-link">Забыли пароль?</a>
            </div>
            <div class="input-wrapper">
              <input 
                id="login-password"
                v-model="loginForm.password" 
                :type="showPassword ? 'text' : 'password'" 
                placeholder="Введите ваш пароль" 
                required 
              />
              <button type="button" class="eye-btn" @click="showPassword = !showPassword">
                {{ showPassword ? 'Скрыть' : 'Показать' }}
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="loginForm.rememberMe" />
              <span>Запомнить меня</span>
            </label>
          </div>

          <button type="submit" class="btn-submit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Вход...' : 'Войти' }}
          </button>
        </form>

        <!-- ФОРМА РЕГИСТРАЦИИ (REGISTER) -->
        <form v-else @submit.prevent="handleRegister" class="auth-form">
          <div class="form-group">
            <label for="reg-name">Ваше имя</label>
            <div class="input-wrapper">
              <input 
                id="reg-name"
                v-model="registerForm.name" 
                type="text" 
                placeholder="Иван Иванов" 
                required 
              />
            </div>
          </div>

          <div class="form-group">
            <label for="reg-role">Роль в системе</label>
            <div class="input-wrapper">
              <select id="reg-role" v-model="registerForm.role" class="select-role" required>
                <option value="parent">Родитель</option>
                <option value="leader">Руководитель кружка</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="reg-email">Электронная почта</label>
            <div class="input-wrapper">
              <input 
                id="reg-email"
                v-model="registerForm.email" 
                type="email" 
                placeholder="name@example.com" 
                required 
              />
            </div>
          </div>

          <div class="form-group">
            <label for="reg-phone">Номер телефона</label>
            <div class="input-wrapper">
              <input 
                id="reg-phone"
                v-model="registerForm.phone" 
                type="tel" 
                placeholder="+7 (964) 460 67-67" 
                required 
                maxlength="18"
                @input="handlePhoneInput"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="reg-password">Пароль</label>
            <div class="input-wrapper">
              <input 
                id="reg-password"
                v-model="registerForm.password" 
                :type="showRegPassword ? 'text' : 'password'" 
                placeholder="Не менее 6 символов" 
                required 
                minlength="6"
              />
              <button type="button" class="eye-btn" @click="showRegPassword = !showRegPassword">
                {{ showRegPassword ? 'Скрыть' : 'Показать' }}
              </button>
            </div>
          </div>

          <div class="form-group">
            <label for="reg-confirm">Подтверждение пароля</label>
            <div class="input-wrapper">
              <input 
                id="reg-confirm"
                v-model="registerForm.confirmPassword" 
                :type="showRegPassword ? 'text' : 'password'" 
                placeholder="Повторите пароль" 
                required 
              />
            </div>
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="registerForm.agree" required />
              <span>Я согласен с <a href="#" class="terms-link">условиями обработки персональных данных</a></span>
            </label>
          </div>

          <button type="submit" class="btn-submit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Регистрация...' : 'Зарегистрироваться' }}
          </button>
        </form>

        <div class="auth-footer">
          <p v-if="activeTab === 'login'">
            Ещё нет аккаунта? 
            <button class="switch-link" @click="activeTab = 'register'">Зарегистрироваться</button>
          </p>
          <p v-else>
            Уже есть аккаунт? 
            <button class="switch-link" @click="activeTab = 'login'">Войти</button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../authStore'

const router = useRouter()
const activeTab = ref('login')

const showPassword = ref(false)
const showRegPassword = ref(false)
const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const loginForm = ref({
  login: '',
  password: '',
  rememberMe: false
})

const registerForm = ref({
  name: '',
  email: '',
  phone: '',
  role: 'parent',
  password: '',
  confirmPassword: '',
  agree: false
})

let lastPhoneDigits = ''

function handlePhoneInput(e) {
  let rawValue = e.target.value
  let digits = rawValue.replace(/\D/g, '')

  if (digits.length === 1 && (digits === '7' || digits === '8')) {
    digits = ''
  } else if (digits.startsWith('7') || digits.startsWith('8')) {
    digits = digits.slice(1)
  }
  digits = digits.slice(0, 10)

  if (e.inputType === 'deleteContentBackward' && digits === lastPhoneDigits && digits.length > 0) {
    digits = digits.slice(0, -1)
  }

  lastPhoneDigits = digits

  let formatted = ''
  if (rawValue.length > 0) {
    if (digits.length === 0 && (rawValue.includes('7') || rawValue.includes('8'))) {
      formatted = '+7 ('
    } else if (digits.length > 0) {
      formatted = '+7 (' + digits.slice(0, 3)
      if (digits.length >= 3) {
        formatted += ') ' + digits.slice(3, 6)
      }
      if (digits.length >= 6) {
        formatted += ' ' + digits.slice(6, 8)
      }
      if (digits.length >= 8) {
        formatted += '-' + digits.slice(8, 10)
      }
    }
  }

  registerForm.value.phone = formatted
  e.target.value = formatted
}

watch(activeTab, () => {
  errorMessage.value = ''
  successMessage.value = ''
})

async function handleLogin() {
  errorMessage.value = ''
  successMessage.value = ''
  isSubmitting.value = true
  try {
    await authStore.login({
      login: loginForm.value.login,
      password: loginForm.value.password
    })
    successMessage.value = 'Вы успешно вошли в аккаунт!'
    setTimeout(() => {
      router.push('/')
    }, 1000)
  } catch (err) {
    errorMessage.value = err.message || 'Ошибка авторизации'
  } finally {
    isSubmitting.value = false
  }
}

async function handleRegister() {
  errorMessage.value = ''
  successMessage.value = ''

  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    errorMessage.value = 'Пароли не совпадают!'
    return
  }

  isSubmitting.value = true
  try {
    await authStore.register({
      name: registerForm.value.name,
      email: registerForm.value.email,
      phone: registerForm.value.phone,
      role: registerForm.value.role,
      password: registerForm.value.password
    })
    successMessage.value = 'Регистрация прошла успешно! Выполняется вход...'
    setTimeout(() => {
      router.push('/')
    }, 1000)
  } catch (err) {
    errorMessage.value = err.message || 'Ошибка регистрации'
  } finally {
    isSubmitting.value = false
  }
}

function handleForgotPassword() {
  alert('Ссылка для восстановления пароля отправлена на ваш e-mail.')
}
</script>

<style scoped>
.top-nav {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: var(--bg-color, #ffffff);
  padding: 10px 20px;
  border-radius: 5px;
  color: var(--text-main, #333333);
  font-size: 16px;
  font-weight: 500;
  border: none;
  text-decoration: none;
  transition: background 0.2s ease;
}

.nav-btn:hover {
  background: #e0e0e0;
}

.icon-sm {
  width: 16px;
  height: 16px;
}

.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
}

.auth-card {
  background: var(--bg-color, #ffffff);
  border-radius: 5px;
  border-top: 2px solid var(--primary-dark, #70232f);
  padding: 30px;
  width: 100%;
  max-width: 440px;
  box-shadow: none;
}

.auth-header {
  text-align: center;
  margin-bottom: 24px;
}

.auth-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--primary-dark, #70232f);
  margin-bottom: 8px;
}

.auth-subtitle {
  font-size: 14px;
  color: var(--text-light, #666666);
  line-height: 1.4;
  margin-bottom: 20px;
}

/* Табы авторизации/регистрации */
.auth-tabs {
  display: flex;
  background: var(--bg-wrapper, #efefef);
  border-radius: 5px;
  padding: 4px;
  gap: 4px;
}

.auth-tab {
  flex: 1;
  border: none;
  background: transparent;
  padding: 8px 14px;
  font-size: 15px;
  font-weight: 600;
  color: var(--text-main, #333333);
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.auth-tab.active {
  background: var(--bg-color, #ffffff);
  color: var(--primary-dark, #70232f);
  box-shadow: none;
}

.alert-success {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #e8f5e9;
  color: #2e7d32;
  border-radius: 5px;
  padding: 12px 16px;
  font-size: 14px;
  margin-bottom: 20px;
  border: 1px solid #a5d6a7;
}

.alert-error {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 5px;
  padding: 12px 16px;
  font-size: 14px;
  margin-bottom: 20px;
  border: 1px solid #ffcdd2;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-main, #333333);
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.forgot-link, .terms-link {
  font-size: 12px;
  color: var(--primary-color, #d86b79);
  text-decoration: underline;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  padding: 10px 14px;
  font-size: 14px;
  color: var(--text-main, #333333);
  outline: none;
  transition: border-color 0.2s ease;
}

.input-wrapper input:focus {
  border-color: var(--primary-dark, #70232f);
}

.select-role {
  width: 100%;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 5px;
  padding: 10px 14px;
  font-size: 14px;
  color: var(--text-main, #333333);
  outline: none;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.select-role:focus {
  border-color: var(--primary-dark, #70232f);
}

.eye-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2px;
  font-size: 12px;
  color: var(--text-light, #666666);
}

.form-options {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-main, #333333);
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  accent-color: var(--primary-dark, #70232f);
  width: 16px;
  height: 16px;
}

.btn-submit {
  width: 100%;
  background-color: var(--primary-dark, #70232f);
  color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 12px 20px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 6px;
  box-shadow: none;
}

.btn-submit:hover:not(:disabled) {
  background-color: #581b25;
}

.btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.auth-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: var(--text-light, #666666);
}

.switch-link {
  background: none;
  border: none;
  color: var(--primary-color, #d86b79);
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  padding: 0 4px;
  font-size: 14px;
}
</style>
