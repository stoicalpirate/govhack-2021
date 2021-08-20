<template>
  <div>
    <h3>SpeakerTime</h3>
    <h5>Politicians who've spoken the most today.</h5>
    <div ref="plot1"></div>
  </div>
</template>

<script>
import  Plotly  from 'plotly.js-dist/plotly';

/*
NOTES: 
- Example here: https://forum.vuejs.org/t/using-plotly-from-within-a-vue-component/91846
- The sort bars will display with last item on top and first item on bottom.
*/ 

export default {
  name: "HorizontalBarChart",
  props: ['sourceData'],
  mounted() {
    // Plot the chart
    Plotly.react(this.$refs.plot1, this.sourceData, this.layout);
  }
}
</script>