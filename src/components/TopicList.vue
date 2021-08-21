<template>
  <div>

    <div v-for="topic in sourceData" :key="topic.name">

        <b-button variant="primary" class="my-2" @click="selectTopic(topic)">{{topic.name}}</b-button>

    </div>

  </div>
</template>

<script>

/*
NOTES: 
- 
*/

export default {
  name: "TopicList",
  props: ['sourceData'],
  mounted() {
    // Select the first item in the topic list to emit to parent ??
    
  },
  methods: {
    selectTopic(topic) {
      // Emit the selected button value back to parent
      this.$emit('topicselected', topic)
    }
  }
}
</script>