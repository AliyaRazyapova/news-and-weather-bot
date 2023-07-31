<script>
export default {
  name: 'ResponseList',
  props: ['templates'],
  methods: {
    goToTemplateDetail() {
      //
    }
  }
}
</script>

<template>
  <div>
    <h1>Список настроек ответов бота</h1>
    <ul>
      <li v-for="template in templates" :key="template.id">
        <a @click="goToTemplateDetail(template.id)">{{ template.command }}</a>
      </li>
    </ul>
  </div>
</template>

<style scoped>

</style>