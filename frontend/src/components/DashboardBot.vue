<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "DashboardBot",
  props: ['totalDialogs', 'totalUserMessages', 'totalBotResponse', 'popularCommands']
})
</script>

<template>
  <div>
    <h1>Дашборд</h1>
    <p>Всего диалогов: {{ totalDialogs }}</p>
    <p>Сообщений от пользователя: {{ totalUserMessages }}</p>
    <p>Ответов бота: {{ totalBotResponse }}</p>
    <h2>Популярные команды:</h2>
    <ul>
      <li v-for="command in popularCommands" :key="command.message">
        {{ command.message }} - {{ command.count }}
      </li>
    </ul>
  </div>
</template>

<style scoped>

</style>