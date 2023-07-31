<script>
export default{
  props: ['template'],
  data() {
    return {
      editedTemplate: {
        command: this.template.command,
        response: this.template.response,
      },
    };
  },
  methods: {
    editTemplate() {
      //
    }
  }
}
</script>

<template>
  <div>
    <h1>Редактирование настроек ответа для команды "{{ editedTemplate.command }}"</h1>
    <form @submit="editTemplate">
      <label for="command">Команда:</label>
      <input type="text" v-model="editedTemplate.command" />
      <br>
      <label for="response">Текст ответа:</label>
      <textarea v-model="editedTemplate.response" />
      <br>
      <button type="submit">Сохранить</button>
    </form>
  </div>
</template>

<style scoped>

</style>