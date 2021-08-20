<template>
  <div class="spinner">
    <b-spinner variant="primary" style="width: 7rem; height: 7rem;" />
  </div>
</template>

<script>
export default {
  name: "Loading",
}
</script>

<style lang="css" scoped>
.spinner {
  display: grid;
  place-items: center;
  height: 100vh;
}
</style>