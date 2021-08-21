<template>
  <div>
    <vue-word-cloud
      style="height:480px;width:640px;"
      :words="sourceData"
      :color="([, weight]) => weight > 30 ? 'MediumSpringGreen' : weight > 20 ? 'DeepSkyBlue' : weight > 10 ? 'DeepPink' : weight > 5 ? 'DarkOrchid' : 'Indigo'"
      font-family="Indie Flower"
    />
  </div>
</template>


<script>
import VueWordCloud from 'vuewordcloud';
 
export default {
  components: { [VueWordCloud.name]: VueWordCloud },
  props: ['sourceData']
};
</script>

<style scoped>
  @import url("https://fonts.googleapis.com/css?family=Indie+Flower");
</style>
