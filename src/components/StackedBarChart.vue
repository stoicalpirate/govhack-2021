<template>
  <div>
    <div ref="plot1" style="overflow: auto"></div>
  </div>
</template>

<script>
import  Plotly  from 'plotly.js-dist/plotly';

/*
NOTES: 
- Example here: https://forum.vuejs.org/t/using-plotly-from-within-a-vue-component/91846
*/

export default {
  name: "StackedBarChart",
  props: ['sourceData'],
  computed: {
    editedSourceData() {
      // Trying to dynamically add the "type": "bar" aspect rather than needing it in API data
      const updated = this.sourceData
      updated.forEach(element => element.push({"foo": "bar"}))
      console.log(updated)
      return {
        updated
      }
    },
    layout() {
      return {
        barmode: 'relative',
        width: this.sourceData[0].x.length * 50  // allow 50 px per column
        }
    }
  },
  mounted() {
    // Plot the chart  
    Plotly.react(this.$refs.plot1, this.sourceData, this.layout);
    // Scroll to far right
    this.$refs.plot1.scrollLeft += this.$refs.plot1.scrollWidth
  }
}
</script>
