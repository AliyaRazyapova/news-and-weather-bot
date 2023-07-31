<script>
import {defineComponent, onMounted, reactive} from 'vue'
import axios from "axios";

export default defineComponent({
  name: "MessageHistory",
  // props: ['messages'],
  setup() {
    const state = reactive({
      messages: [],
    });

    onMounted(() => {
      axios.get('http://localhost:8000/bot/history/')
          .then(response => {
            state.messages = response.data;
          })
          .catch(error => {
            console.error(error)
          });
    });

    return {
      messages: state.messages,
    };
  },
});
</script>

<template>
  <div>
    <h1>История сообщений</h1>
    <ul>
      <li v-for="message in messages" :key="message.id">
        <span>{{ message.timestamp }} - </span>
        <span v-if="message.is_bot">Бот:</span>
        <span v-else>Пользователь:</span>
        {{ message.message }}
      </li>
    </ul>
  </div>
</template>

<style scoped>

</style>