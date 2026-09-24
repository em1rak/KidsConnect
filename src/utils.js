/**
 * Вспомогательные утилиты проекта KidsConnect
 */

/**
 * Формирование корректного URL для статических и загруженных изображений
 * @param {string} path - Путь к изображению
 * @param {string} fallback - Запасной путь по умолчанию
 * @returns {string}
 */
export function getImageUrl(path, fallback = '/image/Group330.svg') {
  if (!path) {
    const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
    return base + fallback.replace(/^\//, '')
  }
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:')) {
    return path
  }
  if (path.startsWith('/uploads/') || path.startsWith('uploads/') || path.startsWith('/media/') || path.startsWith('media/')) {
    return 'http://127.0.0.1:8000/' + path.replace(/^\//, '')
  }
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/'
  return base + path.replace(/^\//, '')
}

/**
 * Парсинг строки расписания на дни и временные слоты
 * @param {string} scheduleStr - Строка вида "Пн, Ср 08:00 - 10:00, 18:00 - 19:30"
 * @returns {{ days: string, slots: string[] }}
 */
export function parseSchedule(scheduleStr) {
  if (!scheduleStr) {
    return {
      days: 'Расписание по запросу',
      slots: []
    }
  }

  const firstDigitMatch = scheduleStr.match(/\d/)
  if (firstDigitMatch && firstDigitMatch.index > 0) {
    const daysPart = scheduleStr.slice(0, firstDigitMatch.index).trim().replace(/,\s*$/, '')
    const timePart = scheduleStr.slice(firstDigitMatch.index).trim()
    const slots = timePart.split(',').map(s => s.trim()).filter(Boolean)
    return {
      days: daysPart || 'Расписание по запросу',
      slots
    }
  }

  return {
    days: scheduleStr.trim(),
    slots: []
  }
}
